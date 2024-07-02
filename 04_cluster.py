import argparse
import os
import numpy as np
import pandas as pd
from hdbscan import HDBSCAN
import params


def main(args):

    pairwise_dists = np.loadtxt(args.dists_file)
    signal_labels = pd.read_json(args.labels_file)
    signal_labels.columns = ["game", "speaker", "referent", "referent_id"]

    assert pairwise_dists.shape[0] == len(signal_labels)

    speaker_ids = np.unique(signal_labels["speaker"])

    dfs_to_save = []

    for speaker in speaker_ids:
        print(f"Clustering signals for speaker {speaker}")
        if speaker == "init":
            continue

        indices = np.where(signal_labels["speaker"] == speaker)[0]

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


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--dists_file", required=True, type=str, help="`.txt` pairwise dists file")
    parser.add_argument("--labels_file", required=True, type=str, help="`.json` labels file")
    parser.add_argument("--output_dir", required=True, type=str, help="plac to save output")

    args = parser.parse_args()

    main(args)