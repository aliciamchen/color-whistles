"""Calculate and save average dist for each participant reproduction during learning phase"""
# %%
import argparse
import numpy as np
import pandas as pd
import json
import tslearn.metrics
import params
from tslearn.utils import to_time_series_dataset
import os

# Filter for unique init signals


# %%

# Learning score
def calc_learning_scores(initialization, df_learning_signals, df_init):
    df_reproductions = df_learning_signals[df_learning_signals["block_id"] == 6]
    # print(df_reproductisons)
    learn_dists = {}

    # print(initialization)

    for speaker in pd.unique(df_learning_signals["speaker"]):

        # print(speaker)
        # Check for all reproductions
        if df_reproductions[df_reproductions["speaker"] == speaker][
            "referent"
        ].nunique() != len(params.learning_referents[initialization]):
            continue

        repro_dists = []
        # print(params.learning_referents[initialization])

        for referent in params.learning_referents[initialization]:
            print(referent)
            speaker_sig = df_reproductions[
                (df_reproductions["speaker"] == speaker)
                & (df_reproductions["referent"] == referent)
            ]["signalWithZeros"].to_list()

            # print(speaker_sig)
            init_sig = df_init[df_init["referent"] == referent]["signalWithZeros"].to_list()

            dist = tslearn.metrics.dtw(init_sig, speaker_sig)
            print(dist)
            repro_dists.append(dist)

        assert len(repro_dists) == df_learning_signals["referent_id"].nunique()
        # print(repro_dists)
        learn_dist = sum(repro_dists) / len(repro_dists)
        # print(learn_dist)
        learn_dists[speaker] = learn_dist

    return learn_dists


def main(args):

    # df_learn = pd.read_csv("test_output/learning.zip")
    # df_learning_signals = pd.read_csv("test_output/learning_signals.zip")
    # df_init = pd.read_csv("test_output/init_signals.zip")

    # df_learn = pd.read_csv(args.learn_file)
    df_learning_signals = pd.read_csv(args.learning_sigs)
    df_init_signals = pd.read_csv(args.init_sigs)

    learn_dists = calc_learning_scores(args.expt_tag, df_learning_signals, df_init_signals)

    with open(os.path.join(args.output_dir, f"{args.expt_tag}_learn_dists.json"), "w") as f:
        json.dump(learn_dists, f)
    # scores


if __name__ == "__main__":

    parser = argparse.ArgumentParser()


    parser.add_argument("--expt_tag", required=True, type=str, help="which experiment? for labeling files")
    parser.add_argument("--learning_sigs", type=str, help="file for learning signals")
    parser.add_argument("--init_sigs", type=str, help="file for init signals")

    parser.add_argument(
        "--output_dir", required=True, type=str, help="place to save output"
    )

    args = parser.parse_args()

    main(args)