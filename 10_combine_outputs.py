# %%
import numpy as np
import pandas as pd
import json
import os
from sklearn.preprocessing import MinMaxScaler

output_dir = 'test_output'

f1 = os.path.join(output_dir, 'game_info.json')
f2 = os.path.join(output_dir, 'learn_dists.json')
f3 = os.path.join(output_dir, 'game_scores.json')
f4 = os.path.join(output_dir, 'systematicity.csv')
f5 = os.path.join(output_dir, 'discreteness.csv')

f6 = "test/one2one_betwn_clust_syst.csv"
f7 = "test/one2one_within_clust_syst.csv"

with open(f1, 'r') as f:
    game_info = json.load(f)

with open(f2, 'r') as f:
    learn_dists = json.load(f)

with open(f3, 'r') as f:
    game_scores = json.load(f)

systematicity = pd.read_csv(f4, index_col="speaker")
discreteness = pd.read_csv(f5, index_col="speaker")

within_clust_syst = pd.read_csv(f6, index_col="speaker")
btwn_clust_syst = pd.read_csv(f7, index_col="speaker")

def populate_learn_score(participant):
    """some of the learning scores are missing, so this is for fixing that"""
    try:
        return(learn_dists[participant])
    except:
        return np.nan

df = pd.DataFrame(columns=['game', 'speaker', 'systematicity', 'discreteness', 'learn_score', 'own_score', 'comm_score'])

for game, pair in game_info.items():
    for participant in pair:
        new_row = {
            'game': game,
            # 'participant_idx': #int(discreteness[discreteness['participant'] == participant].iloc[0]['participant_idx']), # this is jank, change later
            'speaker': participant,
            'systematicity': systematicity.at[participant, "dcor"],
            'discreteness': discreteness.at[participant, "hopkins_stat"],#discreteness[discreteness['participant'] == participant].iloc[0]['hopkins_stat'],
            'learn_score': populate_learn_score(participant),#learn_scores[participant],
            'own_score': game_scores[participant],
            "btwn_clust_sys": btwn_clust_syst.at[participant, "dcor"],
            "within_clust_sys": within_clust_syst.at[participant, "dcor"],
        }
        df = df.append(new_row, ignore_index=True)

    # Add partner communication scores
    df.loc[df['speaker'] == pair[0], 'comm_score'] = game_scores[pair[1]]
    df.loc[df['speaker'] == pair[1], 'comm_score'] = game_scores[pair[0]]

# %% Normalize

# scaler = MinMaxScaler()

# df['discreteness'] = scaler.fit_transform(df[['discreteness']].to_numpy())
# df['systematicity'] = scaler.fit_transform(df[['systematicity']].to_numpy())
# df['learn_score'] = 1 - scaler.fit_transform(df[['learn_score']].to_numpy())
# df['own_score'] = scaler.fit_transform(df[['own_score']].to_numpy())
# df['comm_score'] = scaler.fit_transform(df[['comm_score']].to_numpy())
df['learn_score'] = -1 * df['learn_score'] + df['learn_score'].max()
df.to_csv(os.path.join("test", "one2one_sys_disc_agg.csv"), index=False)

# %%
