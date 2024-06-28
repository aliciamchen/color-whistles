"""
Calculate pairwise distances between all signals (including input)
"""
import argparse
import json
import os

import numpy as np
import pandas as pd
import tqdm
from tslearn.metrics import cdist_dtw
from tslearn.utils import to_time_series_dataset


def main(args):

    print(f"Calculating pairwise distances")

    df_init = pd.read_csv(args.init_signals)
    df_comm = pd.read_csv(args.comm_signals)

    df = pd.concat([df_init, df_comm], ignore_index=True)
    df.set_index(["game", "speaker", "referent", "referent_id"], inplace=True)

    signal_labels = df.index.unique()

    print(f"{len(signal_labels)} total signals")
    print("Transferring signals into a big list")

    list_of_signals = [
        df[df.index == idx]["signalWithZeros"].to_list()
        for idx in tqdm.tqdm(signal_labels)
    ]

    assert len(list_of_signals) != 0

    print("Converting signals to time series dataset")
    X = to_time_series_dataset(list_of_signals)

    print("Finding pairwise distances")
    pairwise_dists = cdist_dtw(X, n_jobs=-1, verbose=1)

    with open(
        os.path.join(args.output_dir, "signal_labels.json"), "w"
    ) as f:
        json.dump(list(signal_labels), f)

    np.savetxt(
        os.path.join(args.output_dir, "pairwise_dists.txt"),
        pairwise_dists,
        comments="Pairwise signal similarities, including learning signals (see `all_signal_labels.json` for labels)",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--init_signals", required=True, type=str, help="csv of init signals"
    )
    parser.add_argument(
        "--comm_signals", required=True, type=str, help="csv of comm signals"
    )
    parser.add_argument(
        "--output_dir", required=True, type=str, help="place to save output"
    )

    args = parser.parse_args()

    main(args)

