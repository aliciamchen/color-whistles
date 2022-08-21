"""Calculate and save average dist for each participant reproduction during learning phase"""
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import tools.preprocess
from scipy import stats
import tslearn.metrics
import params
from tslearn.utils import to_time_series_dataset

df_learn = pd.read_csv("test_output/learning.zip")
df_learning_signals = pd.read_csv("test_output/learning_signals.zip")
df_init = pd.read_csv("test_output/init_signals.zip")

# %%

# Learning score
df_reproductions = df_learning_signals[df_learning_signals['block_id'] == 6]

learn_dists = {}

for speaker in pd.unique(df_learning_signals['speaker']):

    # Check for all reproductions
    if df_reproductions[df_reproductions['speaker'] == speaker]['referent'].nunique() != len(params.learning_referents):
        continue

    repro_dists = []

    for referent in params.learning_referents:
        speaker_sig = df_reproductions[(df_reproductions['speaker'] == speaker) & (
            df_reproductions['referent'] == referent)]['signalWithZeros'].to_list()

        init_sig = df_init[df_init['referent'] ==
                           referent]['signalWithZeros'].to_list()

        dist = tslearn.metrics.dtw(init_sig, speaker_sig)
        repro_dists.append(dist)

    assert len(repro_dists) == df_learning_signals['referent_id'].nunique()
    # print(repro_dists)
    learn_dist = sum(repro_dists) / len(repro_dists)

    learn_dists[speaker] = learn_dist





with open("test_output/learn_dists.json", 'w') as f:
    json.dump(learn_dists, f)
# scores
