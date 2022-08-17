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


def exclude_incomplete_games(df):
    """
    Args:
        df (DataFrame): raw communication data from experiment

    Returns:
        DataFrame: same df but with participants excluded
    """
    games = pd.unique(df['gameid'])
    speakers = pd.unique(df['speakerid'])

    print(f'Number of games: {len(games)}')
    print(f'Number of speakers: {len(speakers)}')

    # get rid of games that are fewer than 80 rounds
    for game in games:
        if len(df[df['gameid'] == game].index) < params.n_rounds:
            df.drop(df[df['gameid'] == game].index, inplace=True)

    print(
        f"Retained {df['gameid'].nunique()} complete games, with {df['speakerid'].nunique()} total speakers.")

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

    filename = "data/raw/2022-01-27_one2one/communication_game_data.zip"
    df = pd.read_csv(filename)

    df_cleaned = assign_indices(exclude_incomplete_games(df))
    game_info = fetch_game_info(df_cleaned)

    df_cleaned.to_csv("test_output/communication.zip")

    with open("test_output/game_info.json", "w") as f:
        json.dump(game_info, f)
