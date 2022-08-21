"""
Make big dataframe with processed learning and communication signals
"""

import argparse
import json
import os

import numpy as np
import pandas as pd

import params
from tools import preprocess
from tools.matthias_scripts import process_whistles


def fetch_json_signal(df, speaker, referent):
    raw_signal = json.loads(df.loc[(df['speakerid'] == speaker) & (
        df['correctid'] == referent)]['signalproduced'].item())
    return raw_signal


def make_comm_df(df):
    """Make dataframe of communication phase signals

    Args:
        df (DataFrame): raw signal dataframe

    Returns:
        DataFrame: long-form time-series dataframe
    """
    print("Processing communication phase signals...")

    all_signals = []

    for row in df.itertuples():
        raw_signal = json.loads(row.signalproduced)

        # Some signals are empty or just have one point, we want to ignore those
        if (not raw_signal) or (len(raw_signal) == 1):
            continue

        df_signal = preprocess.make_signal_df(
            raw_signal,
            sampling_freq=params.sampling_freq,
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


def make_init_df(init_signals_dir=params.learning_sigs_dir):
    """Make dataframe of initialization signals

    Args:
        init_signals_dir (str, optional): folder to find `.json` file of learning phase signals.
        Defaults to params.learning_sigs_dir.

    Returns:
        _type_: _description_
    """
    print("Processing initialization signals...")

    signals = preprocess.load_signals_from_folder(
        init_signals_dir)  # load from `learning_signals.json`

    all_signals = []

    # because all the signals start in one `.json` file, index using filename
    for idx, raw_signal in enumerate(signals['learning_signals']):

        df_signal = preprocess.make_signal_df(
            raw_signal,
            sampling_freq=params.sampling_freq,
            referent_id=params.init_idx_color_mappings[idx],
            referent=params.learning_referents[idx],
            speaker='init'
        )

        all_signals.append(df_signal)

    big_df = pd.concat(all_signals, ignore_index=True)

    return big_df


def make_learn_df(df):
    """Make dataframe of learning phase signals
    """
    print("Processing learning phase signals...")
    all_signals = []

    for row in df.itertuples():

        signal_string = row.signal

        # somehow `json.loads` doesn't work for these signals, we have to fix some stuff
        signal_string = signal_string.replace("\'", "\"")
        signal_string = signal_string.replace(" ", "")

        raw_signal = eval(signal_string)
        # raw_signal = json.loads(row.signal)

        # Some signals are empty or just have one point, we want to ignore those
        if (not raw_signal) or (len(raw_signal) == 1):
            continue

        df_signal = preprocess.make_signal_df(
            raw_signal,
            sampling_freq=params.sampling_freq,
            referent=params.learning_referents[row.referent_id],
            referent_id=row.referent_id,
            signal_id=row.signal_id,
            block_id=row.block_id,
            n_correct_lc_guesses=row.num_correc_lc_guesses,
            lc_reached=row.learning_criterion_reached,
            trial_index=row.trial_index,
            trial_type=row.trial_type,
            speaker=row.workerid
        )

        all_signals.append(df_signal)

    big_df = pd.concat(all_signals, ignore_index=True)

    return big_df


if __name__ == "__main__":

    comm_filename = "test_output/communication.zip"
    learn_filename = "test_output/learning.zip"

    df_learn = pd.read_csv(learn_filename)
    df_comm = pd.read_csv(comm_filename)

    df_init = make_init_df()
    df_learn_long = make_learn_df(df_learn)
    df_comm_long = make_comm_df(df_comm)

    df_init.to_csv("test_output/init_signals.zip", index=False)
    df_learn_long.to_csv("test_output/learning_signals.zip", index=False)
    df_comm_long.to_csv("test_output/comm_signals.zip", index=False)
