#!/bin/bash

set -e

# python 00_fetch_games.py --learn_raw raw_data/learning_data.zip --comm_raw raw_data/communication_game_data.zip --output_dir outputs
# python 01_process_signals.py --learn_file outputs/learn.zip --comm_file outputs/comm.zip --output_dir outputs
# python 02_pairwise_dists.py --init_signals outputs/init_signals_tidy.zip --comm_signals outputs/comm_signals_tidy.zip --output_dir outputs
# python 03_embeddings.py --dists_file outputs/pairwise_dists.txt --labels_file outputs/signal_labels.json --output_dir outputs

# mkdir -p outputs/metrics

python 04_cluster.py --dists_file outputs/pairwise_dists.txt --labels_file outputs/signal_labels.json --output_dir outputs
Rscript 05_general_syst.R outputs/pairwise_dists.txt outputs/signal_labels.json outputs/metrics
Rscript 06_cluster_syst.R outputs/pairwise_dists.txt outputs/signal_labels.json outputs/metrics

Rscript 07_hopkins.R outputs/embedding_3d.csv outputs/metrics

python 08_learn_performance.py --learning_sigs outputs/learn_signals_tidy.zip --init_sigs outputs/init_signals_tidy.zip --output_dir outputs
python 09_game_performance.py --comm_file outputs/comm.zip --output_dir outputs

Rscript 10_alignment.R outputs/pairwise_dists.txt outputs/signal_labels.json outputs/metrics
# python 10_combine_outputs.py --game_info outputs/game_info.json --learn_dists outputs/learn_dists.json --game_scores outputs/game_scores.json --syst outputs/metrics/systematicity.csv --hopkins outputs/metrics/hopkins.csv --btwn_clust_syst outputs/metrics/btwn_clust_syst.csv --within_clust_syst outputs/metrics/within_clust_syst.csv --alignments outputs/metrics/alignments.csv --output_dir outputs
python 11_combine_outputs.py --output_dir outputs

