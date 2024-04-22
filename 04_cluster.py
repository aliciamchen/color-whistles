# Cluster signals using GMM using the `embedding.disc`

# %%

import numpy as np
import pandas as pd
import json
from sklearn.cluster import HDBSCAN
import params


# df = pd.read_csv("test_output/embedding_disc.csv")

# %% Load data

# load in matrix of all pairwise distances
pairwise_dists = np.loadtxt("test_output/pairwise_dists.txt")
signal_labels = pd.read_json("test_output/all_signal_labels.json")
signal_labels.columns = ["game", "speaker", "referent", "referent_id"]


assert pairwise_dists.shape[0] == len(signal_labels)

# %%

speaker_ids = np.unique(signal_labels["speaker"])

dfs_to_save = []

for speaker in speaker_ids:
    if speaker == "init":
        continue

    indices = np.where(signal_labels["speaker"] == speaker)[0]
    n_signals = len(indices)

    signal_dists = pairwise_dists[np.ix_(indices, indices)]
    # print(signal_dists)

    for min_cluster_size in params.cluster_params["min_cluster_size"]:
        hdbscan = HDBSCAN(
            min_cluster_size=min_cluster_size,
            metric="precomputed",
            allow_single_cluster=True
        ).fit(signal_dists)

        labels = hdbscan.labels_

        # medoids = np.zeros((n_signals, n_signals))
        # for i in range(n_signals):
        #     medoid_idx = np.argmin(np.mean(signal_dists[labels == i], axis=0))
        #     medoids[i] = signal_dists[labels == i][medoid_idx]

        # store results
        df = signal_labels[signal_labels["speaker"] == speaker].copy()
        df["min_cluster_size"] = min_cluster_size
        df["cluster_label"] = labels

        dfs_to_save.append(df)

results = pd.concat(dfs_to_save).reset_index()
results.to_csv("test_output/cluster_output.csv", index=False)

