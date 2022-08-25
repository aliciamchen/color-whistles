"""
Get rid of incomplete games, extract `.json` signals
Assign participant indices
"""

import argparse
import json
import os

import numpy as np
import pandas as pd

import params


def exclude_incomplete_comm(df):
    """
    Args:
        df (DataFrame): raw communication data from experiment

    Returns:
        DataFrame: same df but with participants excluded
    """
    games = pd.unique(df["gameid"])
    speakers = pd.unique(df["speakerid"])

    print(f"Detected {len(games)} games and {len(speakers)} speakers")

    # get rid of games that are fewer than 80 rounds
    for game in games:
        if len(df[df["gameid"] == game].index) < params.n_rounds:
            df.drop(df[df["gameid"] == game].index, inplace=True)

    print(
        f"Retained {df['gameid'].nunique()} complete games, with {df['speakerid'].nunique()} total speakers"
    )

    return df


def exclude_incomplete_learn(learn_df, game_info):
    player_ids_nested = list(game_info.values())
    player_ids = [player for game in player_ids_nested for player in game]

    df = learn_df[learn_df["workerid"].isin(player_ids)]
    return df


def assign_indices(df):
    """Assign a unique index for each game and speaker (for ease of access)

    Args:
        df (DataFrame): raw communication data (with exclusions)

    Returns:
        df (DataFrame): data with indices
    """
    df["game_idx"] = df.groupby("gameid").ngroup()
    df["speaker_idx"] = df.groupby("speakerid").ngroup()

    return df


def fetch_game_info(df):
    """
    Args:
        df (DataFrame): raw communication data (with exclusions)

    Returns:
        dict: keys are games, values are lists of speakers belonging to each game
    """
    games = pd.unique(df["gameid"])

    game_info = {}

    for game in games:
        speakers = list(df[df["gameid"] == game]["speakerid"].unique())
        game_info[game] = speakers

    return game_info


def main(args):

    f_learn = args.learn_raw
    f_comm = args.comm_raw
    label = args.expt_tag
    output_dir = args.output_dir

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    df_learn = pd.read_csv(f_learn)
    df_comm = pd.read_csv(f_comm)

    df_comm_cleaned = assign_indices(exclude_incomplete_comm(df_comm))

    game_info = fetch_game_info(df_comm_cleaned)
    df_learn_cleaned = exclude_incomplete_learn(df_learn, game_info)

    df_comm_cleaned.to_csv(os.path.join(output_dir, f"{label}_comm.zip"), index=False)
    df_learn_cleaned.to_csv(os.path.join(output_dir, f"{label}_learn.zip"), index=False)

    with open(os.path.join(output_dir, f"{label}_game_info.json"), "w") as f:
        json.dump(game_info, f)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--expt_tag", required=True, type=str, help="which experiment? for labeling files")
    parser.add_argument(
        "--learn_raw", required=True, type=str, help="file for raw learning data"
    )
    parser.add_argument(
        "--comm_raw", required=True, type=str, help="file for raw comm data"
    )
    parser.add_argument(
        "--output_dir", required=True, type=str, help="place to save output"
    )

    args = parser.parse_args()

    main(args)

