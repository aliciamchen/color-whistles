outputs/learn.zip: raw_data/learning_data.zip 00_fetch_games.py
	python 00_fetch_games.py --learn_raw raw_data/learning_data.zip --comm_raw raw_data/communication_game_data.zip --output_dir outputs

outputs/comm.zip: raw_data/communication_game_data.zip 00_fetch_games.py
	python 00_fetch_games.py --learn_raw raw_data/learning_data.zip --comm_raw raw_data/communication_game_data.zip --output_dir outputs

outputs/game_info.json: raw_data/communication_game_data.zip 00_fetch_games.py
	python 00_fetch_games.py --learn_raw raw_data/learning_data.zip --comm_raw raw_data/communication_game_data.zip --output_dir outputs


outputs/init_signals_tidy.zip: stim/learning_signals.json 01_process_signals.py
	python 01_process_signals.py --learn_file outputs/learn.zip --comm_file outputs/comm.zip --output_dir outputs

outputs/learn_signals_tidy.zip: outputs/learn.zip 01_process_signals.py
	python 01_process_signals.py --learn_file outputs/learn.zip --comm_file outputs/comm.zip --output_dir outputs

outputs/comm_signals_tidy.zip: outputs/comm.zip 01_process_signals.py
	python 01_process_signals.py --learn_file outputs/learn.zip --comm_file outputs/comm.zip --output_dir outputs


outputs/pairwise_dists.txt: outputs/init_signals_tidy.zip outputs/comm_signals_tidy.zip 02_pairwise_dists.py
	python 02_pairwise_dists.py --learn_file outputs/learn.zip --comm_file outputs/comm.zip --output_dir outputs

outputs/signal_labels.json: outputs/init_signals_tidy.zip outputs/comm_signals_tidy.zip 02_pairwise_dists.py
	python 02_pairwise_dists.py --learn_file outputs/learn.zip --comm_file outputs/comm.zip --output_dir outputs


outputs/embedding_1d.csv: outputs/pairwise_dists.txt outputs/signal_labels.json 03_embeddings.py
	python 03_embeddings.py --dists_file outputs/pairwise_dists.txt --labels_file outputs/signal_labels.json --output_dir outputs

outputs/embedding_2d.csv: outputs/pairwise_dists.txt outputs/signal_labels.json 03_embeddings.py
	python 03_embeddings.py --dists_file outputs/pairwise_dists.txt --labels_file outputs/signal_labels.json --output_dir outputs

outputs/embedding_3d.csv: outputs/pairwise_dists.txt outputs/signal_labels.json 03_embeddings.py
	python 03_embeddings.py --dists_file outputs/pairwise_dists.txt --labels_file outputs/signal_labels.json --output_dir outputs


outputs/cluster_output.csv: outputs/pairwise_dists.txt outputs/signal_labels.json 04_cluster.py
	python 04_cluster.py --dists_file outputs/pairwise_dists.txt --labels_file outputs/signal_labels.json --output_dir outputs


outputs/metrics/systematicity.csv: outputs/pairwise_dists.txt outputs/signal_labels.json 05_general_syst.R
	Rscript 05_general_syst.R outputs/pairwise_dists.txt outputs/signal_labels.json outputs/metrics

outputs/metrics/btwn_clust_syst.csv: outputs/pairwise_dists.txt outputs/signal_labels.json 06_cluster_syst.R
	Rscript 06_cluster_syst.R outputs/pairwise_dists.txt outputs/signal_labels.json outputs/metrics

outputs/metrics/within_clust_syst.csv:outputs/pairwise_dists.txt outputs/signal_labels.json 06_cluster_syst.R
	Rscript 06_cluster_syst.R outputs/pairwise_dists.txt outputs/signal_labels.json outputs/metrics

outputs/metrics/hopkins.csv: outputs/embedding_3d.csv 07_hopkins.R
	Rscript 07_hopkins.R outputs/embedding_3d.csv outputs/metrics

outputs/learn_dists.json: outputs/learn_signals_tidy.zip outputs/init_signals_tidy.zip 08_learn_performance.py
	python 08_learn_performance.py --learning_sigs outputs/learn_signals_tidy.zip --init_sigs outputs/init_signals_tidy.zip --output_dir outputs

outputs/game_scores.json: outputs/comm.zip 09_game_performance.py
	python 09_game_performance.py --comm_file outputs/comm.zip --output_dir outputs

outputs/metrics/alignments.csv: outputs/pairwise_dists.txt outputs/signal_labels.json 10_alignment.R
	Rscript 10_alignment.R outputs/pairwise_dists.txt outputs/signal_labels.json outputs/metrics

outputs/all_calculations.csv: outputs/game_info.json outputs/learn_dists.json outputs/game_scores.json outputs/metrics/systematicity.csv outputs/metrics/btwn_clust_syst.csv outputs/metrics/within_clust_syst.csv outputs/metrics/hopkins.csv outputs/metrics/alignments.csv 11_combine_outputs.py
	python 11_combine_outputs.py --output_dir outputs

outputs/stresses.json: outputs/pairwise_dists.txt mds_dims.py
	python mds_dims.py --dists_file outputs/pairwise_dists.txt --output_dir outputs