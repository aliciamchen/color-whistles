# %%

# quick script to csompute 3d MDS embeddings per participant, both for discreteness calculations and for viz purposes
# TODO: compute both 3d and 2d embeddings here
# for later: Plot clusters (using code from before) without color centroids and with color centroids; save to file

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import tools
import tools.preprocess  # delete later
import tools.cluster
from tools.matthias_scripts import process_whistles
from sklearn.manifold import MDS

import params
import json
import time
# %%

pairwise_dists = np.loadtxt("test_output/pairwise_dists.txt")

with open("test_output/all_signal_labels.json", 'r') as f:
    signal_labels = json.load(f)

assert pairwise_dists.shape[0] == len(signal_labels)


# %% Calculate embedding


mds_discreteness = MDS(
    n_components=params.mds_discreteness['n_components'],
    eps=params.mds_discreteness['eps'],
    n_jobs=-1,
    verbose=7,
    dissimilarity="precomputed",
    random_state=params.seed,
    n_init=params.mds_discreteness['n_init'],
    max_iter=params.mds_discreteness['max_iter']
)

mds_viz = MDS(
    n_components=params.mds_viz['n_components'],
    eps=params.mds_viz['eps'],
    n_jobs=-1,
    verbose=7,
    dissimilarity="precomputed",
    random_state=params.seed,
    n_init=params.mds_viz['n_init'],
    max_iter=params.mds_viz['max_iter']
)


# %%

embedding_disc = mds_discreteness.fit_transform(pairwise_dists)
embedding_viz = mds_viz.fit_transform(pairwise_dists)

# %%

df_embedding_disc = pd.DataFrame(
    data=np.concatenate((signal_labels, embedding_disc), axis=1),
    columns=['speaker', 'referent'] + [f"mds_{i + 1}" for i in range(params.mds_discreteness['n_components'])]
)

# %%

df_embedding_viz = pd.DataFrame(
    data=np.concatenate((signal_labels, embedding_viz), axis=1),
    columns=['speaker', 'referent'] + [f"mds_{i + 1}" for i in range(params.mds_viz['n_components'])]
)

# %%

df_embedding_disc.to_csv('test_output/embedding_disc.csv', index=False)
df_embedding_viz.to_csv('test_output/embedding_viz.csv', index=False)
