#!/bin/bash

set -e
mkdir -p outputs_color_sounds

python 00_fetch_games.py --learn_raw raw_data/learning_data.zip --comm_raw raw_data/communication_game_data.zip --output_dir outputs_color_sounds
python 01_process_signals.py --learn_file outputs_color_sounds/learn.zip --comm_file outputs_color_sounds/comm.zip --output_dir outputs_color_sounds
python 02_pairwise_dists.py --init_signals outputs_color_sounds/init_signals_tidy.zip --comm_signals outputs_color_sounds/comm_signals_tidy.zip --output_dir outputs_color_sounds
python 03_embeddings.py --dists_file outputs_color_sounds/pairwise_dists.txt --labels_file outputs_color_sounds/signal_labels.json --output_dir outputs_color_sounds

# mkdir -p outputs/metrics

# python 04_cluster.py --dists_file outputs/pairwise_dists.txt --labels_file outputs/signal_labels.json --output_dir outputs
# Rscript 05_general_syst.R outputs/pairwise_dists.txt outputs/signal_labels.json outputs/metrics
# Rscript 06_cluster_syst.R outputs/pairwise_dists.txt outputs/signal_labels.json outputs/metrics

# Rscript 07_hopkins.R outputs/embedding_3d.csv outputs/metrics

# python 08_learn_performance.py --learning_sigs outputs/learn_signals_tidy.zip --init_sigs outputs/init_signals_tidy.zip --output_dir outputs
