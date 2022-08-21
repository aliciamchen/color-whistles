"""
Calculate pairwise distances between all signals (including input) for MDS projection
Note: this takes >2hrs to run
"""
# %%
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tqdm
from tslearn.metrics import cdist_dtw
from tslearn.utils import to_time_series_dataset

# %%
df_init = pd.read_csv("test_output/init_signals.zip")
df_comm = pd.read_csv("test_output/comm_signals.zip")

df = pd.concat([df_init, df_comm], ignore_index=True)


# %%

# DTW distances

df.set_index(['game', 'speaker', 'referent', 'referent_id'], inplace=True)
signal_labels = df.index.unique()

# %%
print(f"{len(signal_labels)} total signals")

print("Transferring signals into a big list")
list_of_signals = [
    df[df.index == idx]["signalWithZeros"].to_list() for idx in tqdm.tqdm(signal_labels)
]

assert len(list_of_signals) != 0

# %%
print("Converting signals to time series dataset")

X = to_time_series_dataset(list_of_signals)

print("Finding pairwise distances")

pairwise_dists = cdist_dtw(
    X,
    n_jobs=-1,
    verbose=1
)
# TODO: find a good way to save unique indices
# maybe for this it's good to save it as a list of lists
# can you do that with json?

# %% Save
# np.save("test_output/all_pairwise_dists.npy", pairwise_dists)
# np.save("test_output/all_signal_labels.npy", signal_labels)
with open("test_output/all_signal_labels.json", "w") as f:
    json.dump(list(signal_labels), f)

np.savetxt(
    "test_output/pairwise_dists.txt",
    pairwise_dists,
    comments="Pairwise signal similarities, including learning signals (see `all_signal_labels.json` for labels)"
)



# %%
