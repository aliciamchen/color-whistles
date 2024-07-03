# Variables
PYTHON = python
RSCRIPT = Rscript
FETCH_SCRIPT = 00_fetch_games.py
PROCESS_SCRIPT = 01_process_signals.py
PAIRWISE_SCRIPT = 02_pairwise_dists.py
EMBEDDINGS_SCRIPT = 03_embeddings.py
CLUSTER_SCRIPT = 04_cluster.py
GENERAL_SYST_SCRIPT = 05_general_syst.R
CLUSTER_SYST_SCRIPT = 06_cluster_syst.R
HOPKINS_SCRIPT = 07_hopkins.R
LEARN_PERFORMANCE_SCRIPT = 08_learn_performance.py
GAME_PERFORMANCE_SCRIPT = 09_game_performance.py
ALIGNMENT_SCRIPT = 10_alignment.R
COMBINE_OUTPUTS_SCRIPT = 11_combine_outputs.py
MDS_SCRIPT = mds_dims.py
OUTPUT_DIR = outputs
METRICS_DIR = $(OUTPUT_DIR)/metrics

# Phony targets
.PHONY: all fetch process pairwise embeddings cluster metrics performance combine mds clean

# Main target
all: fetch process pairwise embeddings cluster metrics performance combine mds

# Fetching data
fetch: $(OUTPUT_DIR)/learn.zip $(OUTPUT_DIR)/comm.zip $(OUTPUT_DIR)/game_info.json

$(OUTPUT_DIR)/learn.zip $(OUTPUT_DIR)/comm.zip $(OUTPUT_DIR)/game_info.json: raw_data/learning_data.zip raw_data/communication_game_data.zip $(FETCH_SCRIPT)
	$(PYTHON) $(FETCH_SCRIPT) --learn_raw raw_data/learning_data.zip --comm_raw raw_data/communication_game_data.zip --output_dir $(OUTPUT_DIR)

# Processing signals
process: $(OUTPUT_DIR)/init_signals_tidy.zip $(OUTPUT_DIR)/learn_signals_tidy.zip $(OUTPUT_DIR)/comm_signals_tidy.zip

$(OUTPUT_DIR)/init_signals_tidy.zip $(OUTPUT_DIR)/learn_signals_tidy.zip $(OUTPUT_DIR)/comm_signals_tidy.zip: $(OUTPUT_DIR)/learn.zip $(OUTPUT_DIR)/comm.zip $(PROCESS_SCRIPT)
	$(PYTHON) $(PROCESS_SCRIPT) --learn_file $(OUTPUT_DIR)/learn.zip --comm_file $(OUTPUT_DIR)/comm.zip --output_dir $(OUTPUT_DIR)

# Calculating pairwise distances
pairwise: $(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json

$(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json: $(OUTPUT_DIR)/init_signals_tidy.zip $(OUTPUT_DIR)/comm_signals_tidy.zip $(PAIRWISE_SCRIPT)
	$(PYTHON) $(PAIRWISE_SCRIPT) --learn_file $(OUTPUT_DIR)/learn.zip --comm_file $(OUTPUT_DIR)/comm.zip --output_dir $(OUTPUT_DIR)

# Generating embeddings
embeddings: $(OUTPUT_DIR)/embedding_1d.csv $(OUTPUT_DIR)/embedding_2d.csv $(OUTPUT_DIR)/embedding_3d.csv

$(OUTPUT_DIR)/embedding_1d.csv $(OUTPUT_DIR)/embedding_2d.csv $(OUTPUT_DIR)/embedding_3d.csv: $(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json $(EMBEDDINGS_SCRIPT)
	$(PYTHON) $(EMBEDDINGS_SCRIPT) --dists_file $(OUTPUT_DIR)/pairwise_dists.txt --labels_file $(OUTPUT_DIR)/signal_labels.json --output_dir $(OUTPUT_DIR)

# Clustering
cluster: $(OUTPUT_DIR)/cluster_output.csv

$(OUTPUT_DIR)/cluster_output.csv: $(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json $(CLUSTER_SCRIPT)
	$(PYTHON) $(CLUSTER_SCRIPT) --dists_file $(OUTPUT_DIR)/pairwise_dists.txt --labels_file $(OUTPUT_DIR)/signal_labels.json --output_dir $(OUTPUT_DIR)

# Metrics calculations
metrics: $(OUTPUT_DIR)/metrics/systematicity.csv $(OUTPUT_DIR)/metrics/btwn_clust_syst.csv $(OUTPUT_DIR)/metrics/within_clust_syst.csv $(OUTPUT_DIR)/metrics/hopkins.csv $(OUTPUT_DIR)/metrics/alignments.csv

$(OUTPUT_DIR)/metrics/systematicity.csv: $(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json $(GENERAL_SYST_SCRIPT)
	$(RSCRIPT) $(GENERAL_SYST_SCRIPT) $(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json $(OUTPUT_DIR)/metrics

$(OUTPUT_DIR)/metrics/btwn_clust_syst.csv $(OUTPUT_DIR)/metrics/within_clust_syst.csv: $(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json $(CLUSTER_SYST_SCRIPT)
	$(RSCRIPT) $(CLUSTER_SYST_SCRIPT) $(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json $(OUTPUT_DIR)/metrics

$(OUTPUT_DIR)/metrics/hopkins.csv: $(OUTPUT_DIR)/embedding_3d.csv $(HOPKINS_SCRIPT)
	$(RSCRIPT) $(HOPKINS_SCRIPT) $(OUTPUT_DIR)/embedding_3d.csv $(OUTPUT_DIR)/metrics

$(OUTPUT_DIR)/metrics/alignments.csv: $(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json $(ALIGNMENT_SCRIPT)
	$(RSCRIPT) $(ALIGNMENT_SCRIPT) $(OUTPUT_DIR)/pairwise_dists.txt $(OUTPUT_DIR)/signal_labels.json $(OUTPUT_DIR)/metrics

# Performance calculations
performance: $(OUTPUT_DIR)/learn_dists.json $(OUTPUT_DIR)/game_scores.json

$(OUTPUT_DIR)/learn_dists.json: $(OUTPUT_DIR)/learn_signals_tidy.zip $(OUTPUT_DIR)/init_signals_tidy.zip $(LEARN_PERFORMANCE_SCRIPT)
	$(PYTHON) $(LEARN_PERFORMANCE_SCRIPT) --learning_sigs $(OUTPUT_DIR)/learn_signals_tidy.zip --init_sigs $(OUTPUT_DIR)/init_signals_tidy.zip --output_dir $(OUTPUT_DIR)

$(OUTPUT_DIR)/game_scores.json: $(OUTPUT_DIR)/comm.zip $(GAME_PERFORMANCE_SCRIPT)
	$(PYTHON) $(GAME_PERFORMANCE_SCRIPT) --comm_file $(OUTPUT_DIR)/comm.zip --output_dir $(OUTPUT_DIR)

# Combining outputs
combine: $(OUTPUT_DIR)/all_calculations.csv

$(OUTPUT_DIR)/all_calculations.csv: $(OUTPUT_DIR)/game_info.json $(OUTPUT_DIR)/learn_dists.json $(OUTPUT_DIR)/game_scores.json $(OUTPUT_DIR)/metrics/systematicity.csv $(OUTPUT_DIR)/metrics/btwn_clust_syst.csv $(OUTPUT_DIR)/metrics/within_clust_syst.csv $(OUTPUT_DIR)/metrics/hopkins.csv $(OUTPUT_DIR)/metrics/alignments.csv $(COMBINE_OUTPUTS_SCRIPT)
	$(PYTHON) $(COMBINE_OUTPUTS_SCRIPT) --output_dir $(OUTPUT_DIR)

# MDS calculation
mds: $(OUTPUT_DIR)/stresses.json

$(OUTPUT_DIR)/stresses.json: $(OUTPUT_DIR)/pairwise_dists.txt $(MDS_SCRIPT)
	$(PYTHON) $(MDS_SCRIPT) --dists_file $(OUTPUT_DIR)/pairwise_dists.txt --output_dir $(OUTPUT_DIR)

# Clean up
clean:
	find $(OUTPUT_DIR) -type f -not -path "$(METRICS_DIR)/*" -delete
	find $(METRICS_DIR) -type f -delete
