

# quick script to csompute 3d MDS embeddings per participant
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

import json
import time

# %%

# below dataframe is saved in `calc_MDS.ipynb`
df = pd.read_csv("data/signalsWithGameInfo.zip", index_col=0)
# TODO: load in participants, make list of participants
with open("data/one2one_game_info.json", 'r') as f:
    game_info = json.load(f)

# TODO: load in individual color data, so you can put this info in dataframe
# %% For each particupant, compute DTW distances, then compute MDS embeddings on distances
# Then save MDS embeddings to big data frame
dfs = []

for game, participants in game_info.items():
    for participant in participants:
        this_df = df[df['participant'] == participant]
        participant_idx = pd.unique(this_df['participant_idx'])[0]
        dists = tools.cluster.compute_DTW_distances(this_df)

        mds = MDS(
            n_components=3,
            eps=1e-9,
            n_jobs=-1,
            dissimilarity="precomputed",
            random_state=110,
            n_init=40,
            max_iter=10000
        )

        embedding = mds.fit_transform(dists)

        new_df = pd.DataFrame(
            data=embedding,
            columns=['MDS_1', 'MDS_2', 'MDS_3']
        )

        new_df['participant'] = participant
        new_df['game'] = game
        new_df['participant_idx'] = participant_idx

        dfs.append(new_df)
    # TODO: add color info here (given limited time ok to not to do now)

df_big = pd.concat(dfs, ignore_index=True)
# %%

df_big.to_csv('output/embeddings_3d.csv')
# %%
