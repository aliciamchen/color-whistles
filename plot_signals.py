import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from tools.matthias_scripts import process_whistles

# %% Plot learning signals

with open("stim/learning_signals.json") as f:
    signals = json.load(f)

signals_processed = []
for signal in signals:
    signal0 = process_whistles.interpolate_signal(signal)
    signals_processed.append(signal0)

for i, signal in enumerate(signals_processed):
    f, ax = plt.subplots(figsize=(10, 5))
    process_whistles.plot_signal(signal, lw=4, ax=ax)
    plt.axis('off')
    plt.savefig(f"figs/learning_signal_{i}.svg")

# %% Plot sample communication signals

def fetch_json_signal(df, speaker, referent):
    raw_signal = json.loads(
        df.loc[(df["speakerid"] == speaker) & (df["correct"] == referent)][
            "signalproduced"
        ].item()
    )
    return raw_signal

df = pd.read_csv("outputs/comm.zip")

speaker_referent_pairs = [
    ('6053ce04a276ce713b3e7c1a', '#9a760e'),
    ('61001bf99a534440d8563358', '#8a7c00')
]

for speaker, referent in speaker_referent_pairs:
    raw_signal = fetch_json_signal(df, speaker, referent)
    signal = process_whistles.interpolate_signal(raw_signal)
    f, ax = plt.subplots(figsize=(10, 5))
    process_whistles.plot_signal(signal, lw=4, ax=ax)
    plt.axis('off')
    plt.savefig(f"figs/comm_signal_{speaker}_{referent}.svg")
