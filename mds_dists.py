"""Calculate pairwise distances between all signals for MDS projection"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import tools
import tools.preprocess  # delete later
import tools.cluster
from tools.matthias_scripts import process_whistles

import json
import time


# %% Load one-to-one communication signals; add game info

df_one2one = pd.read_csv("results/2022-01-30_one2one/all_participants.csv")

with open("data/one2one/one2one_game_info.json", 'r') as f:
    one2one_game_info = json.load(f)

for game, part_ids in one2one_game_info.items():
    for part_id in part_ids:
        df_one2one.loc[df_one2one["participant"] == part_id, "gameid"] = game

# %% Load five learning signals

learning_signals = tools.preprocess.load_signals_from_folder("./data")
df_learning_sigs = tools.preprocess.signals2df(learning_signals['learning_signals'])
df_learning_sigs['participant'] = 'learning'  # Indicate that these are the learning signals

# %% Combine communication and learning signals into big dataframe

df_121_full = pd.concat([df_one2one, df_learning_sigs], ignore_index=True)
games_121 = pd.unique(df_121_full['gameid'])

df_121_training = df_121_full[df_121_full['participant'] == 'learning']
df_121_25games = df_121_full[df_121_full['gameid'].isin(games_121[:25])]
df_25 = pd.concat([df_121_25games, df_121_training], ignore_index=True)

# %% Calculate pairwise distances

start_time = time.time()
dists, indices  = tools.cluster.compute_DTW_distances_all(df_25)
print("--- %s seconds ---" % (time.time() - start_time))

np.save("output/alldists_plustraining_25games", dists)
np.save("output/alldists_plustraining_indices_25games", indices)