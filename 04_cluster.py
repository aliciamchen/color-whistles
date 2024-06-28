import argparse
import os
import numpy as np
import pandas as pd
from sklearn.cluster import HDBSCAN
import params


def main(args):

    pairwise_dists = np.loadtxt(args.dists_file)
    signal_labels = pd.read_json(args.labels_file)
    signal_labels.columns = ["game", "speaker", "referent", "referent_id"]

    assert pairwise_dists.shape[0] == len(signal_labels)

    speaker_ids = np.unique(signal_labels["speaker"])

    dfs_to_save = []

    for speaker in speaker_ids:
        if speaker == "init":
            continue

        indices = np.where(signal_labels["speaker"] == speaker)[0]
        n_signals = len(indices)

        signal_dists = pairwise_dists[np.ix_(indices, indices)]

        for min_cluster_size in params.cluster_params["min_cluster_size"]:
            hdbscan = HDBSCAN(
                min_cluster_size=min_cluster_size,
                metric="precomputed",
                allow_single_cluster=True
            ).fit(signal_dists)

            labels = hdbscan.labels_

            # store results
            df = signal_labels[signal_labels["speaker"] == speaker].copy()
            df["min_cluster_size"] = min_cluster_size
            df["cluster_label"] = labels

            dfs_to_save.append(df)

    results = pd.concat(dfs_to_save).reset_index()
    results.to_csv(os.path.join(args.output_dir, "cluster_output.csv"), index=False)


    # for min cluster size = 5, add cluster labels to embedding_viz
    # embedding_viz = pd.read_csv(os.path.join(args.output_dir, "embedding_viz.csv")).drop(columns=["cluster_label"])

    # results_5 = results[results["min_cluster_size"] == 3]

    # embedding_viz = embedding_viz.merge(results_5, on=["game", "speaker", "referent", "referent_id"], how="left")
    # embedding_viz.to_csv(os.path.join(args.output_dir, "embedding_viz_w_clusters.csv"), index=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--dists_file", required=True, type=str, help="`.txt` pairwise dists file")
    parser.add_argument("--labels_file", required=True, type=str, help="`.json` labels file")
    parser.add_argument("--output_dir", required=True, type=str, help="plac to save output")

    args = parser.parse_args()

    main(args)