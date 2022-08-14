"""Calculate and save learning + communication scores"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import tools.preprocess
from scipy import stats
import tslearn.metrics
from tslearn.utils import to_time_series_dataset

fname1 = "data/raw/2022-01-27_one2one/learning_data.zip"
fname2 = "data/one2one/one2one_comm_cleaned.zip"

df_one2one_learn = pd.read_csv(fname1)
df_one2one_comm = pd.read_csv(fname2)

with open("data/one2one/one2one_game_info.json") as f:
    one2one_game_info = json.load(f)

speakers_one2one = pd.unique(df_one2one_comm['speakerid']).tolist()
# %% Calculate communication score

communication_scores = {}

for game, pair in one2one_game_info.items():
    for participant in pair:
        participantScore = df_one2one_comm[df_one2one_comm['speakerid'] == participant]['score'].mean()
        communication_scores[participant] = participantScore

# %% Calculate learning score

# Load learning signals
learning_signals = tools.preprocess.load_signals_from_folder("data/learning_signals")  # load from `learning_signals.json`
df_learning_sigs = tools.preprocess.signals2df(learning_signals['learning_signals'])
df_learning_sigs['participant'] = 'learning'

def make_signal_lists(df, idxs=['gameid', 'participant', 'idx']):
    df_= df.set_index(idxs)
    indices = df_.index.unique()
    unique_indices = indices.unique()
    nSignals = len(unique_indices)  # there's probably a better way to do this

    assert nSignals != 0
    print(f"Found {nSignals} signals, making list of signals")
    signallists = [
        df_[df_.index == idx]["signalWithZeros"].to_list() for idx in unique_indices
    ]
    assert len(signallists) != 0

    return signallists



new_learn_scores = {}
nReferents = 5

for speaker_idx, speaker in enumerate(speakers_one2one):

    # Check for 5 reproductions
    nReproductions = len(df_one2one_learn[(df_one2one_learn['workerid'] == speaker) & (df_one2one_learn['block_id'] == 6)].index)
    if nReproductions == 0:
        continue
    assert nReproductions == nReferents

    df_ = df_one2one_learn[(df_one2one_learn['workerid'] == speaker) & (df_one2one_learn['block_id'] == 6)]

    speaker_signals = []
    for referent in range(nReferents):

        if not len(df_.loc[(df_['referent_id'] == referent)]['signal']):
            speaker_signals.append([])
            continue

        signal_string = df_[df_['referent_id'] == referent]['signal'].item()

        signal_string = signal_string.replace("\'", "\"")
        signal_string = signal_string.replace(" ", "")

        signal_ = eval(signal_string)
        speaker_signals.append(signal_)

    print(f"len speaker signals: {len(speaker_signals)}")

    df_speaker_signals = tools.preprocess.signals2df(speaker_signals)
    speaker_signal_indices = pd.unique(df_speaker_signals['idx'])  # the signals that exist

    df_learning_signals = df_learning_sigs


    speaker_sigs_list = make_signal_lists(df_speaker_signals, idxs=['idx'])
    learning_sigs_list = make_signal_lists(df_learning_signals, idxs=['idx', 'participant'])

    # Now, let's find the distances, average all of them
    assert speaker_sigs_list != learning_sigs_list
    print(len(speaker_sigs_list))
    distances = []

    for i, referent in enumerate(speaker_signal_indices):
        distance = tslearn.metrics.dtw(speaker_sigs_list[i], learning_sigs_list[referent])
        distances.append(distance)

    avg_distance = sum(distances) / len(distances)

    new_learn_scores[speaker] = avg_distance


# %% Save learning and communication scores

with open("output/one2one_comm_scores.json", 'w') as f:
    json.dump(communication_scores, f)

with open("output/one2one_learning_scores_new.json", 'w') as f:
    json.dump(new_learn_scores, f)
# scores