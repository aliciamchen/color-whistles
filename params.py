"""Stuff to put in here:
whistles sampling frequency
input output filenames
"""

sampling_freq = 50
n_rounds = 80

seed = 88
learning_sigs_dir = "data/learning_signals"

mds_discreteness = {
    'n_components': 3,
    'eps': 1e-9,
    'n_init': 40,
    'max_iter': 5000
}

mds_viz = {
    'n_components': 2,
    'eps': 1e-9,
    'n_init': 40,
    'max_iter': 5000
}

learning_referents = ["#d9445d", "#ae6c00", "#009069", "#008b98", "#8c6db5"]

# In the raw data the init labels are labeled as
init_idx_color_mappings = {
    0: 0,
    1: 6,
    2: 18,
    3: 23,
    4: 32,
}

# gaussian mixture
bgm = {
    'n_components': 20,
    'max_iter': 1000
}