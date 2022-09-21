
# quick script to csompute 3d MDS embeddings per participant, both for discreteness calculations and for viz purposes
# for later: Plot clusters (using code from before) without color centroids and with color centroids; save to file
import argparse
import json
import os

import numpy as np
import pandas as pd
from sklearn.manifold import MDS

import params


def main(args):

    pairwise_dists = np.loadtxt(args.dists_file)

    with open(args.labels_file, "r") as f:
        signal_labels = json.load(f)

    assert pairwise_dists.shape[0] == len(signal_labels)


    mds_2d = MDS(
        n_components=2,
        eps=params.mds["eps"],
        n_jobs=-1,
        verbose=1,
        dissimilarity="precomputed",
        random_state=params.seed,
        n_init=params.mds["n_init"],
        max_iter=params.mds["max_iter"],
    )

    mds_3d = MDS(
        n_components=3,
        eps=params.mds["eps"],
        n_jobs=-1,
        verbose=1,
        dissimilarity="precomputed",
        random_state=params.seed,
        n_init=params.mds["n_init"],
        max_iter=params.mds["max_iter"],
    )

    print("Calculating 2d embedding")
    embedding_2d = mds_2d.fit_transform(pairwise_dists)

    print("Calculating 3d embedding")
    embedding_3d = mds_3d.fit_transform(pairwise_dists)

    df_embedding_2d = pd.DataFrame(
        data=np.concatenate((signal_labels, embedding_2d), axis=1),
        columns=["game", "speaker", "referent", "referent_id"]
        + [f"mds_{i + 1}" for i in range(params.mds["n_components"])],
    )

    df_embedding_3d = pd.DataFrame(
        data=np.concatenate((signal_labels, embedding_3d), axis=1),
        columns=["game", "speaker", "referent", "referent_id"]
        + [f"mds_{i + 1}" for i in range(params.mds["n_components"])],
    )

    df_embedding_2d.to_csv(os.path.join(args.output_dir, f"{args.expt_tag}_embedding_2d.csv"), index=False)
    df_embedding_3d.to_csv(os.path.join(args.output_dir, f"{args.expt_tag}_embedding_3d.csv"), index=False)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--expt_tag", required=True, type=str, help="which experiment? for labeling files")
    parser.add_argument("--dists_file", required=True, type=str, help="`.txt` pairwise dists file")
    parser.add_argument("--labels_file", required=True, type=str, help="`.json` labels file")
    parser.add_argument("--output_dir", required=True, type=str, help="plac to save output")

    args = parser.parse_args()

    main(args)
