import os
import argparse
import json
import pandas as pd

def main(args):

    df = pd.read_csv(args.comm_file)

    game_scores = {}

    for speaker in pd.unique(df["speakerid"]):

        score = df[df["speakerid"] == speaker]["score"].mean()
        game_scores[speaker] = score

    with open(os.path.join(args.output_dir, "game_scores.json"), "w") as f:
        json.dump(game_scores, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--comm_file", type=str, help=".zip file of communication data")
    parser.add_argument(
        "--output_dir", required=True, type=str, help="place to save output"
    )

    args = parser.parse_args()
