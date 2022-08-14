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
    df_= df.set_index(idxs)
    indices = df_.index.unique()
    unique_indices = indices.unique()
    nSignals = len(unique_indices)  # there's probably a better way to do this

    # signal_indices = df["idx"].unique()
    # print(signal_indices)
    assert nSignals != 0
    # print(f"Found {nSignals} signals, making list of signals")
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


def signals2df(signals, sampling_frequency=50):
    """Make full dataframe for a single participant

    Args:
        signals (list): list of lists of dicts loaded from single `.json` file

    Returns:
        DataFrame:
            Columns:
            'idx': one index for each sound
            't': time
            'val': pitch value
            'isOn': whether sound is being produced
            'signal': pitch value that is actually produced
            'signalWithZeros': pitch val with zeros at the pauses
    """
    dfs = []

    for idx, signal in enumerate(signals):

        if not signal: # if signals is empty
            continue

        if len(signal) == 1: # if signal has only one point, treat as empty
            print("signal length 1; discarded")
            continue

        # print(signal)
        signal_processed = process_whistles.interpolate_signal(
            signal, sampling_frequency=sampling_frequency
        )

        df = signal2df(signal_processed)
        df.insert(loc=0, column="idx", value=idx)

        dfs.append(df)

    df_full = pd.concat(dfs)
    # print(df_full)
    # print(df_full["isOn"])
    # df_full["isOn"][df_full["isOn"] == 1] = True
    df_full["isOn"] = df_full["isOn"].replace({0: False, 1:True})
    # print(df_full["isOn"])
    df_full["signal"] = df_full["val"].where(df_full["isOn"], np.nan)

    df_full["signalWithZeros"] = df_full["signal"].where(
        ~np.isnan(df_full["signal"]), 0
    )

    return df_full


def load_signals_from_folder(folder_path):
    """Load signals from folder and generate list, adapted from `process_whistles.py`

    Args:
        folder_path (str): directory of folder to load the signals from

    Returns:
        list: list of json loaded signals (one element per `.json` file)
    """
    print("Looking for signals...")
    all_participant_signals = []
    participant_ids = []

    # might need to fix the way these files are loaded in and ordered

    files = sorted(glob.glob(folder_path + "/*.json"))

    for idx, path in enumerate(files):
        file_name, _ = os.path.splitext(os.path.basename(path))
        print(f"Participant {idx}: Found file {file_name} in {folder_path}")
        with open(path) as file:
            signals = json.load(file)

        all_participant_signals.append(signals)
        participant_ids.append(file_name)

    all_signals = dict(zip(participant_ids, all_participant_signals))

    return all_signals


def allsignals2df(all_participant_signals, **kwargs):
    """Make big dataframe from all signals in a folder

    Args:
        all_participant_signals (list): list of all signals loaded from their individual .json files (output from `load_signals_from_folder`)

    Returns:
        DataFrame:
            Columns:
            ‘participant': participant index
            'idx': one index for each sound
            't': time
            'val': pitch value
            'isOn': whether sound is being produced
            'signal': pitch value that is actually produced
            'signalWithZeros': pitch val with zeros at the pauses
    """

    # if type(all_participant_signals) == dict:
    #     all_participant_signals = list(all_participant_signals.values())


    dfs = []
    i = 0
    for participant_idx, signals in all_participant_signals.items():
        df = signals2df(signals, **kwargs)
        df.insert(loc=0, column="participant", value=participant_idx)
        df.insert(loc=0, column="participant_idx", value=i)
        dfs.append(df)
        i += 1

    df_full = pd.concat(dfs)

    return df_full

