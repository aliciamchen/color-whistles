"""Calculate and save average dist for each participant reproduction during learning phase"""
import argparse
import numpy as np
import pandas as pd
import json
import tslearn.metrics
import params
import os


def calc_learning_scores(df_learning_signals, df_init):
    df_reproductions = df_learning_signals[df_learning_signals["block_id"] == 6]
    learn_dists = {}


    for speaker in pd.unique(df_learning_signals["speaker"]):

        # Check for all reproductions
        if df_reproductions[df_reproductions["speaker"] == speaker][
            "referent"
        ].nunique() != len(params.learning_referents):
            continue

        repro_dists = []

        for referent in params.learning_referents:
            print(referent)
            speaker_sig = df_reproductions[
                (df_reproductions["speaker"] == speaker)
                & (df_reproductions["referent"] == referent)
            ]["signalWithZeros"].to_list()

            init_sig = df_init[df_init["referent"] == referent]["signalWithZeros"].to_list()

            dist = tslearn.metrics.dtw(init_sig, speaker_sig)
            print(dist)
            repro_dists.append(dist)

        assert len(repro_dists) == df_learning_signals["referent_id"].nunique()
        learn_dist = sum(repro_dists) / len(repro_dists)
        learn_dists[speaker] = learn_dist

    return learn_dists


def main(args):

    df_learning_signals = pd.read_csv(args.learning_sigs)
    df_init_signals = pd.read_csv(args.init_sigs)

    learn_dists = calc_learning_scores(df_learning_signals, df_init_signals)

    with open(os.path.join(args.output_dir, "learn_dists.json"), "w") as f:
        json.dump(learn_dists, f)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()


    parser.add_argument("--learning_sigs", type=str, help="file for learning signals")
    parser.add_argument("--init_sigs", type=str, help="file for init signals")

    parser.add_argument(
        "--output_dir", required=True, type=str, help="place to save output"
    )

    args = parser.parse_args()

    main(args)