"""Stuff to put in here:
whistles sampling frequency
input output filenames
"""

sampling_freq = 50
n_rounds = 80

seed = 88
learning_sigs_dir = "data/learning_signals"

mds_discreteness = {"n_components": 3, "eps": 1e-9, "n_init": 40, "max_iter": 5000}

mds_viz = {"n_components": 2, "eps": 1e-9, "n_init": 40, "max_iter": 5000}

learning_referents = {
    "one2one": ["#d9445d", "#ae6c00", "#009069", "#008b98", "#8c6db5"],
    "one2many": [
        "#ca5a00",
        "#a67100",
        "#9a760e",
        "#009246",
        "#0089a0",
        "#0081cd",
        "#6976be",
        "#7e71ba",
        "#bd5697",
    ],
}
# learning_referents = ["#d9445d", "#ae6c00", "#009069", "#008b98", "#8c6db5"]

# referent ids in raw learning df mapped onto 0-39 referent ids
init_color_mappings = {
    "one2one": {0: 0, 1: 6, 2: 18, 3: 23, 4: 32},
    "one2many": {0: 4, 1: 7, 2: 8, 3: 16, 4: 24, 5: 28, 6: 30, 7: 31, 8: 36}
}

# init signal mappings with {referent_id: signal_id}
init_signal_mappings = {
    "one2one": {0: 0, 6: 1, 18: 2, 23: 3, 32: 4},
    "one2many": {4: 1, 7: 2, 8: 2, 16: 1, 24: 0, 28: 0, 30: 2, 31: 1, 36: 0}
}


# gaussian mixture
bgm = {"n_components": 20, "max_iter": 1000}

stimuli = {
    "one2one": ["#d9445d", "#ae6c00", "#009069", "#008b98", "#8c6db5"],
    "one2many": [
        "#ca5a00",
        "#a67100",
        "#9a760e",
        "#009246",
        "#0089a0",
        "#0081cd",
        "#6976be",
        "#7e71ba",
        "#bd5697",
    ],
}
