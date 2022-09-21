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

def fetch_json_signal(df, speaker, referent):
    raw_signal = json.loads(
        df.loc[(df["speakerid"] == speaker) & (df["correctid"] == referent)][
            "signalproduced"
        ].item()
    )
    return raw_signal


def key_by_value(my_dict, value):
    """Smol helper function"""
    keys = list(my_dict.keys())
    values = list(my_dict.values())
    return keys[values.index(value)]


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
            game=row.gameid,
        )

        all_signals.append(df_signal)

    big_df = pd.concat(all_signals, ignore_index=True)

    return big_df


def make_init_df(initialization, init_signals_dir=params.learning_sigs_dir):
    """Make dataframe of initialization signals
    This indexes the signals by referent ids, so there may be as many signals as referents
    (i.e. it may repeat signals)

    Args:
        initialization (str): either "one2one" or "one2many"
        init_signals_dir (str, optional): folder to find `.json` file of learning phase signals.
        Defaults to params.learning_sigs_dir.

    Returns:
        _type_: _description_
    """
    print("Processing initialization signals...")

    signals = preprocess.load_signals_from_folder(init_signals_dir)[
        "learning_signals"
    ]  # load from `learning_signals.json`

    all_signals = []

    for referent_id, signal_id in params.init_signal_mappings[initialization].items():

        df_signal = preprocess.make_signal_df(
            signals[signal_id],
            sampling_freq=params.sampling_freq,
            signal_id=signal_id,
            referent_id=referent_id,
            referent=params.learning_referents[initialization][
                key_by_value(params.init_color_mappings[initialization], referent_id)
            ],
            speaker="init",
        )

        all_signals.append(df_signal)

    big_df = pd.concat(all_signals, ignore_index=True)

    return big_df


def make_learn_df(initialization, df):
    """Make dataframe of learning phase signals

    Args:
        initialization (str): type of initialization, either "one2many" or "one2one"
        df (DataFrame): raw learning phase dataframe

    Returns:
        DataFrame:
    """
    print("Processing learning phase signals...")
    all_signals = []

    for row in df.itertuples():

        signal_string = row.signal

        # somehow `json.loads` doesn't work for these signals, we have to fix some stuff
        signal_string = signal_string.replace("'", '"')
        signal_string = signal_string.replace(" ", "")

        raw_signal = eval(signal_string)

        # Some signals are empty or just have one point, we want to ignore those
        if (not raw_signal) or (len(raw_signal) == 1):
            continue

        df_signal = preprocess.make_signal_df(
            raw_signal,
            sampling_freq=params.sampling_freq,
            referent=params.learning_referents[initialization][row.referent_id],
            referent_id=params.init_color_mappings[initialization][row.referent_id],
            signal_id=row.signal_id,
            block_id=row.block_id,
            n_correct_lc_guesses=row.num_correc_lc_guesses,
            lc_reached=row.learning_criterion_reached,
            trial_index=row.trial_index,
            trial_type=row.trial_type,
            speaker=row.workerid,
        )

        all_signals.append(df_signal)

    big_df = pd.concat(all_signals, ignore_index=True)

    return big_df


def main(args):
    comm_filename = args.comm_file
    learn_filename = args.learn_file
    label = args.expt_tag
    output_dir = args.output_dir

    df_learn = pd.read_csv(learn_filename)
    df_comm = pd.read_csv(comm_filename)

    df_init = make_init_df(label)
    df_learn_long = make_learn_df(label, df_learn)
    df_comm_long = make_comm_df(df_comm)

    df_init.to_csv(os.path.join(output_dir, f"{label}_init_signals.zip"), index=False)
    df_learn_long.to_csv(
        os.path.join(output_dir, f"{label}_learn_signals.zip"), index=False
    )
    df_comm_long.to_csv(
        os.path.join(output_dir, f"{label}_comm_signals.zip"), index=False
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--expt_tag",
        required=True,
        type=str,
        help="which experiment? for labeling files",
    )
    parser.add_argument(
        "--learn_file",
        required=True,
        type=str,
        help="file for (excluded) learning data",
    )
    parser.add_argument(
        "--comm_file", required=True, type=str, help="file for (excluded) comm data"
    )
    parser.add_argument(
        "--output_dir", required=True, type=str, help="place to save output"
    )

    args = parser.parse_args()

    main(args)

