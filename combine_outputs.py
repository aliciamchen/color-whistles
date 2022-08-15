# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import seaborn as sns
import tslearn.clustering
import tslearn.utils
import tools.preprocess
import sklearn



f1 = 'data/one2one_comm_cleaned.zip'
f2 = 'data/signalsWithGameInfo.zip'

f3 = 'data/one2one_game_info.json'
f4 = 'data/stimuli.json'
f5 = 'output/learning_scores.json'
# f6 = 'output/optimal_ks.json'
f7 = 'output/systematicity.json'
f8 = 'output/comm_scores.json'
f9 = 'output/hopkins_stat.csv'

df_comm = pd.read_csv(f1)
df_signals = pd.read_csv(f2)

with open(f3, 'r') as f:
    game_info = json.load(f)

with open(f4, 'r') as f:
    stimuli = json.load(f)

with open(f5, 'r') as f:
    learn_scores = json.load(f)

with open(f9, 'r') as f:
    discreteness = pd.read_csv(f)

with open(f7, 'r') as f:
    systematicity = json.load(f)

with open(f8, 'r') as f:
    comm_scores = json.load(f)


def populate_learn_score(participant):
    try:
        return(learn_scores[participant])
    except:
        return np.nan

df = pd.DataFrame(columns=['game', 'participant', 'colorsignal_corr', 'hopkins_stat', 'learn_dist', 'own_comm_score', 'partner_comm_score'])

for game, pair in game_info.items():
    for participant in pair:
        new_row = {
            'game': game,
            'participant': participant,
            'colorsignal_corr': systematicity[participant],
            'hopkins_stat': discreteness[discreteness['participant'] == participant].iloc[0]['hopkins_stat'],
            'learn_dist': populate_learn_score(participant),#learn_scores[participant],
            'own_comm_score': comm_scores[participant],
        }
        df = df.append(new_row, ignore_index=True)

    # Add partner communication scores
    df.loc[df['participant'] == pair[0], 'partner_comm_score'] = comm_scores[pair[1]]
    df.loc[df['participant'] == pair[1], 'partner_comm_score'] = comm_scores[pair[0]]
    # df[df['participant'] == pair[1]].loc['partner_comm_score'] = comm_scores[pair[0]]

# %% Add discreteness and systematicity outputs

discreteness_cutoff = df['hopkins_stat'].quantile(q=0.5)
df['discreteness'] = np.where(df['hopkins_stat'] > discreteness_cutoff, False, True)

systematicity_cutoff = 0.5 # df['colorsignal_corr'].quantile(q=0.5)
df['systematicity'] = np.where(df['colorsignal_corr'] > systematicity_cutoff, True, False)

scaler = sklearn.preprocessing.MinMaxScaler()
# Normalize hopkins stat
df[['hopkins_stat_norm']] = scaler.fit_transform(df[['hopkins_stat']]) # (df['hopkins_stat'] / (df['hopkins_stat'].max() - df['hopkins_stat'].min()))

# %% Add learning score
# TODO: fix this using minmax scale

df['learn_score'] = 1 - (df['learn_dist'] / (df['learn_dist'].max()))
# %% Add flags

flag_map = {
    0: [True, True],
    1: [True, False],
    2: [False, True],
    3: [False, False]
}

flag_map_1 = {
    "D+S+": [True, True],
    "D+S-": [True, False],
    "D-S+": [False, True],
    "D-S-": [False, False]
}

for flag, vals in flag_map_1.items():
    df.loc[(df['systematicity'] == vals[1]) & (df['discreteness'] == vals[0]), 'category'] = flag

# %% Save

df.to_csv('output/sys_disc_final.csv')
# %%
