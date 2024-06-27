"""
Helper functions for preprocessing signal data
"""

import glob
import json
import os

import numpy as np
import pandas as pd

from tools.matthias_scripts import process_whistles


def make_signal_lists(df, idxs=['gameid', 'participant', 'idx']):
    """Make list of signals from dataframe representation of signals
    For metrics (DTW, etc.)

    Args:
        df (DataFrame): time-series dataframe
        idxs (list, optional): unique indices for signals. Defaults to ['gameid', 'participant', 'idx'].

    Returns:
        _type_: _description_
    """
    df_ = df.set_index(idxs)
    indices = df_.index.unique()
    unique_indices = indices.unique()
    nSignals = len(unique_indices)  # there's probably a better way to do this

    assert nSignals != 0

    signallists = [
        df_[df_.index == idx]["signalWithZeros"].to_list() for idx in unique_indices
    ]
    assert len(signallists) != 0

    return signallists


def signal2df(signal_processed):
    """Convert single processed set of signals to DataFrame

    Args:
        signal_processed (tuple): (time, sound, on/off) tuple of arrays
        (one element of output of `process_whistles.interpolate_signal`)

    Returns:
        DataFrame
    """
    df = pd.DataFrame(
        data={
            "t": signal_processed[0],
            "val": signal_processed[1],
            "isOn": signal_processed[2],
        }
    )

    return df


def make_signal_df(raw_signal, sampling_freq, **kwargs):
    """Make dataframe of signal, where each row is a time point
    Recommended kwargs: `game, speaker, listener, round, block, referent_id, referent`

    Args:
        raw_signal (dict): output of `fetch_json_signal` (but doesn't have to be)
        sampling_freq: sampling frequency for processing signals (load in from `params.py` file)

    Returns:
        DataFrame: dataframe where kwargs are optional columns
    """

    processed_signal = process_whistles.interpolate_signal(
        raw_signal, sampling_frequency=sampling_freq)

    df_signal = signal2df(processed_signal)

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


def load_signals_from_folder(folder_path):
    """Load signals from folder and generate list, adapted from `process_whistles.py`

    Args:
        folder_path (str): directory of folder to load the signals from

    Returns:
        dict: dict of json loaded signals (one element per `.json` file), where key is the original `.json` filename (i.e. the participant id)
    """
    print("Looking for signals...")
    all_participant_signals = []
    participant_ids = []

    # might need to fix the way these files are loaded in and ordered

    files = sorted(glob.glob(folder_path + "/*.json"))

    for idx, path in enumerate(files):
        file_name, _ = os.path.splitext(os.path.basename(path))
        print(f"Found file {file_name} in {folder_path}")
        with open(path) as file:
            signals = json.load(file)

        all_participant_signals.append(signals)
        participant_ids.append(file_name)

    all_signals = dict(zip(participant_ids, all_participant_signals))

    return all_signals
