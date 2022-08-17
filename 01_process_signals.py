"""
Make big dataframe with processed learning and communication signals
"""

import os
import argparse
import numpy as np
import pandas as pd
import tools
import params
import json
from tools.matthias_scripts import process_whistles
from tools import preprocess


def fetch_json_signal(df, speaker, referent):
    raw_signal = json.loads(df.loc[(df['speakerid'] == speaker) & (
        df['correctid'] == referent)]['signalproduced'].item())
    return raw_signal


def make_signal_df(raw_signal, **kwargs):
    """Make dataframe of signal, where each row is a time point
    Recommended kwargs: `game, speaker, listener, round, block, referent_id, referent`

    Args:
        raw_signal (dict): output of `fetch_json_signal` (but doesn't have to be)

    Returns:
        DataFrame: dataframe where kwargs are optional columns
    """

    processed_signal = process_whistles.interpolate_signal(
        raw_signal, sampling_frequency=params.sampling_freq)

    df_signal = preprocess.signal2df(processed_signal)

    # Some more preprocessing to make DTW easier
    df_signal['isOn'] = df_signal['isOn'].replace({0: False, 1: True})
    df_signal["signal"] = df_signal["val"].where(df_signal["isOn"], np.nan)
    df_signal["signalWithZeros"] = df_signal["signal"].where(
        ~np.isnan(df_signal["signal"]), 0
    )

    # Add kwargs to dataframe
    for k, v in kwargs.items():
        df_signal.insert(0, k, v)

    return df_signal


def make_comm_df(df):
    # go through each row / signal, mak signal df, adn then concatenate
    speakers = pd.unique(df['speakerid'])
    games = pd.unique(df['gameid'])

    all_signals = []
    for row in df.itertuples():
        raw_signal = json.loads(row.signalproduced)

        # Some signals are empty or just have one point, we want to ignore those
        if (not raw_signal) or (len(raw_signal) == 1):
            continue

        df_signal = make_signal_df(
            raw_signal,
            score=row.score,
            referent=row.correct,
            referent_id=row.correctid,
            block=row.blockid,
            round=row.round,
            listener=row.listenerid,
            speaker=row.speakerid,
            speaker_idx=row.speaker_idx,
            game=row.gameid
        )

        all_signals.append(df_signal)

    big_df = pd.concat(all_signals, ignore_index=True)

    return big_df


def make_learn_df():
    pass


def make_big_df():
    # concat learn and comm dfs
    pass


if __name__ == "__main__":

    filename = "test_output/communication.zip"
    df = pd.read_csv(filename)

    df_comm = make_comm_df(df)

    df_comm.to_csv("test_output/signals.zip")