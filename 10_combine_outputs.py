import argparse
import numpy as np
import pandas as pd
import json
import os

def main(args):

    output_dir = args.output_dir

    f1 = os.path.join(output_dir, 'game_info.json')
    f2 = os.path.join(output_dir, 'learn_dists.json')
    f3 = os.path.join(output_dir, 'game_scores.json')
    f4 = os.path.join(output_dir, 'metrics/systematicity.csv')
    f5 = os.path.join(output_dir, 'metrics/hopkins.csv')
    f6 = os.path.join(output_dir, 'metrics/btwn_clust_syst.csv')
    f7 = os.path.join(output_dir, 'metrics/within_clust_syst.csv')

    f8 = os.path.join(output_dir, 'metrics/alignments.csv')

    with open(f1, 'r') as f:
        game_info = json.load(f)

    with open(f2, 'r') as f:
        learn_dists = json.load(f)

    with open(f3, 'r') as f:
        game_scores = json.load(f)

    systematicity = pd.read_csv(f4, index_col="speaker")
    hopkins = pd.read_csv(f5, index_col="speaker")

    btwn_clust_syst = pd.read_csv(f6, index_col="speaker")
    within_clust_syst = pd.read_csv(f7, index_col="speaker")

    # Filter for min_cluster_size == 3
    btwn_clust_syst = btwn_clust_syst[btwn_clust_syst["min_cluster_size"] == 3]
    within_clust_syst = within_clust_syst[within_clust_syst["min_cluster_size"] == 3]

    # for within_clust_syst, take average of dcor for each speaker, weighted by number of signals, name it weighted_dcor
    within_clust_syst = within_clust_syst.groupby("speaker").apply(lambda x: np.average(x["dcor"], weights=x["n_signals"]))


    alignment = pd.read_csv(f8, index_col="game")

    def populate_learn_score(participant):
        """some of the learning scores are missing, so this is for fixing that"""
        try:
            return(learn_dists[participant])
        except:
            return np.nan

    df = pd.DataFrame(columns=['game', 'speaker', 'systematicity', 'discreteness', 'learn_score', 'own_score', 'comm_score', 'alignment'])

    for game, pair in game_info.items():
        for participant in pair:
            new_row = {
                'game': game,
                'speaker': participant,
                'systematicity': systematicity.at[participant, "dcor"],
                'hopkins': hopkins.at[participant, "hopkins_stat"],#discreteness[discreteness['participant'] == participant].iloc[0]['hopkins_stat'],
                'learn_score': populate_learn_score(participant),#learn_scores[participant],
                'own_score': game_scores[participant],
                "n_clusters": btwn_clust_syst.at[participant, "n_clusters"],
                "btwn_clust_sys": btwn_clust_syst.at[participant, "dcor"],
                "within_clust_sys": within_clust_syst[participant],
                "alignment": alignment.at[game, "dist"] if game in alignment.index else "NaN"
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)


        # Add partner communication scores
        df.loc[df['speaker'] == pair[0], 'comm_score'] = game_scores[pair[1]]
        df.loc[df['speaker'] == pair[1], 'comm_score'] = game_scores[pair[0]]


    df['learn_score'] = -1 * df['learn_score'] + df['learn_score'].max()
    df['alignment'] = -1 * df['alignment'] + df['alignment'].max()


    df.to_csv(os.path.join(output_dir, "all_calculations.csv"), index=False)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--output_dir", required=True, type=str, help="plac to save output")

    args = parser.parse_args()

    main(args)