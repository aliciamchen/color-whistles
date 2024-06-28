#!/bin/bash

set -e

python 00_fetch_games.py --learn_raw raw_data/learning_data.zip --comm_raw raw_data/communication_game_data.zip --output_dir outputs
python 01_process_signals.py --learn_file outputs/learn.zip --comm_file outputs/comm.zip --output_dir outputs
python 02_pairwise_dists.py --init_signals outputs/init_signals_tidy.zip --comm_signals outputs/comm_signals_tidy.zip --output_dir outputs
python 03_embeddings.py --dists_file outputs/pairwise_dists.txt --labels_file outputs/signal_labels.json --output_dir outputs
python 04_cluster.py --dists_file outputs/pairwise_dists.txt --labels_file outputs/signal_labels.json --output_dir outputs