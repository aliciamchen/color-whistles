"""
Get rid of incomplete games, extract `.json` signals
Assign participant indices
"""

import argparse
import json
import os

import numpy as np
import pandas as pd

import tools
import params


def exclude_incomplete_comm(df):
    """
    Args:
        df (DataFrame): raw communication data from experiment

    Returns:
        DataFrame: same df but with participants excluded
    """
    games = pd.unique(df['gameid'])
    speakers = pd.unique(df['speakerid'])

    print(f'Detected {len(games)} games and {len(speakers)} speakers')

    # get rid of games that are fewer than 80 rounds
    for game in games:
        if len(df[df['gameid'] == game].index) < params.n_rounds:
            df.drop(df[df['gameid'] == game].index, inplace=True)

    print(
        f"Retained {df['gameid'].nunique()} complete games, with {df['speakerid'].nunique()} total speakers")

    return df


def exclude_incomplete_learn(learn_df, game_info):
    player_ids_nested = list(game_info.values())
    player_ids = [player for game in player_ids_nested for player in game]

    df = learn_df[learn_df['workerid'].isin(player_ids)]
    return df


def assign_indices(df):
    """Assign a unique index for each game and speaker (for ease of access)

    Args:
        df (DataFrame): raw communication data (with exclusions)

    Returns:
        df (DataFrame): data with indices
    """
    df['game_idx'] = df.groupby('gameid').ngroup()
    df['speaker_idx'] = df.groupby('speakerid').ngroup()

    return df


def fetch_game_info(df):
    """
    Args:
        df (DataFrame): raw communication data (with exclusions)

    Returns:
        dict: keys are games, values are lists of speakers belonging to each game
    """
    games = pd.unique(df['gameid'])

    game_info = {}

    for game in games:
        speakers = list(df[df['gameid'] == game]['speakerid'].unique())
        game_info[game] = speakers

    return game_info


if __name__ == "__main__":

    f_learn = "data/raw/2022-01-27_one2one/learning_data.zip"
    f_comm = "data/raw/2022-01-27_one2one/communication_game_data.zip"

    df_learn = pd.read_csv(f_learn)
    df_comm = pd.read_csv(f_comm)


    df_comm_cleaned = assign_indices(exclude_incomplete_comm(df_comm))

    game_info = fetch_game_info(df_comm_cleaned)
    df_learn_cleaned = exclude_incomplete_learn(df_learn, game_info)

    df_comm_cleaned.to_csv("test_output/communication.zip", index=False)
    df_learn_cleaned.to_csv("test_output/learning.zip", index=False)

    with open("test_output/game_info.json", "w") as f:
        json.dump(game_info, f)
