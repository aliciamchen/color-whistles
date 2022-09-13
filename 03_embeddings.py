
# quick script to csompute 3d MDS embeddings per participant, both for discreteness calculations and for viz purposes
# for later: Plot clusters (using code from before) without color centroids and with color centroids; save to file
import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.manifold import MDS

import params
import tools.cluster
import tools.preprocess  # delete later


def main(args):

    pairwise_dists = np.loadtxt(args.dists_file)

    with open(args.labels_file, "r") as f:
        signal_labels = json.load(f)

    assert pairwise_dists.shape[0] == len(signal_labels)


    print("Calculating 3D embedding")

    # multiple dimensions, for calculating discreteness (and clustering)
    mds_discreteness = MDS(
        n_components=params.mds_discreteness["n_components"],
        eps=params.mds_discreteness["eps"],
        n_jobs=-1,
        verbose=1,
        dissimilarity="precomputed",
        random_state=params.seed,
        n_init=params.mds_discreteness["n_init"],
        max_iter=params.mds_discreteness["max_iter"],
    )

    print("Calculating 2D embedding")
    # 2d for visualization
    mds_viz = MDS(
        n_components=params.mds_viz["n_components"],
        eps=params.mds_viz["eps"],
        n_jobs=-1,
        verbose=1,
        dissimilarity="precomputed",
        random_state=params.seed,
        n_init=params.mds_viz["n_init"],
        max_iter=params.mds_viz["max_iter"],
    )


    embedding_disc = mds_discreteness.fit_transform(pairwise_dists)
    embedding_viz = mds_viz.fit_transform(pairwise_dists)


    df_embedding_disc = pd.DataFrame(
        data=np.concatenate((signal_labels, embedding_disc), axis=1),
        columns=["game", "speaker", "referent", "referent_id"]
        + [f"mds_{i + 1}" for i in range(params.mds_discreteness["n_components"])],
    )

    df_embedding_viz = pd.DataFrame(
        data=np.concatenate((signal_labels, embedding_viz), axis=1),
        columns=["game", "speaker", "referent", "referent_id"]
        + [f"mds_{i + 1}" for i in range(params.mds_viz["n_components"])],
    )

    df_embedding_disc.to_csv(os.path.join(args.output_dir, f"{args.expt_tag}_embedding_disc.csv"), index=False)
    df_embedding_viz.to_csv(os.path.join(args.output_dir, f"{args.expt_tag}_embedding_viz.csv"), index=False)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--expt_tag", required=True, type=str, help="which experiment? for labeling files")
    parser.add_argument("--dists_file", required=True, type=str, help="`.txt` pairwise dists file")
    parser.add_argument("--labels_file", required=True, type=str, help="`.json` labels file")
    parser.add_argument("--output_dir", required=True, type=str, help="plac to save output")

    args = parser.parse_args()

    main(args)
