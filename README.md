## Setup

`pip install -e .`

## Running

`00_fetch_games.py`
`python 00_fetch_games.py --expt_tag one2one --learn_raw data/raw/one2one/learning_data.zip --comm_raw data/raw/one2one/communication_game_data.zip --output_dir test`

`python 00_fetch_games.py --expt_tag one2many --learn_raw data/raw/one2many/learning_data.zip --comm_raw data/raw/one2many/communication_game_data.zip --output_dir test`

`01_process_signals.py`
`python 01_process_signals.py --expt_tag one2one --learn_file test/one2one_learn.zip --comm_file test/one2one_comm.zip --output_dir test`

`python 01_process_signals.py --expt_tag one2many --learn_file test/one2many_learn.zip --comm_file test/one2many_comm.zip --output_dir test`

`python 03_embeddings.py --expt_tag one2many --dists_file test/one2many_pairwise_dists.txt --labels_file test/one2many_signal_labels.json --output_dir test`

`python 06_learn_performance.py --expt_tag one2many --learning_sigs test/one2many_learn_signals.zip --init_sigs test/one2many_init_signals.zip --output_dir test`
# Data

`clean.py`

- removes incomplete games from `communication_game_data.zip`, saves cleaned data
- saves `.json` game info (speaker/listener pairings)

`learn_comm_scores.py`

- takes learning data and (cleaned) communication data, saves learning and communication scores in a `.json` file
- needs `.json` game info (this can probably be optimized so it doesn't need it)

note: why not make a big `.json` file of all the signals instead of making individual `.json` files for the signals? this is probably hidden in a jupyter notebook somewhere...


- `communication_game_data.zip`
    1. get rid of incomplete games using `clean.py`
    2. --> calculate learning and communication scores using `learn_comm_scores.py`
- `learning_data.zip`
    1. calculate learning and communication scores using `learn_comm_scores.py`
    2.