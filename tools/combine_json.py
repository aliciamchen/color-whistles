"""
helper script to combine separate signals in separate `.json` files in one `.json` file that is a list of list of signals
Each output `.json` file should be a list of all the signals for a single participant
"""
import json
import glob
import os

in_dir = "../test_data/more_test_signals_uncombined"
out_dir = "../test_data/signals"
files = sorted(glob.glob(in_dir + "/*.json"))
nParticipants = 10
nSigPerPart = 40

participant_count = 0
signal_count = 0
current_signals = []

for idx, path in enumerate(files):

    with open(path) as file:
        signals = json.load(file)

    current_signals.append(signals)

    signal_count += 1

    if signal_count == nSigPerPart:

        # once we reach the number of signals per participant (40 in this case), save the big list
        out_path = os.path.join(out_dir, f"test_part_{participant_count}.json")
        with open(out_path, "w") as file:
            json.dump(current_signals, file)

        # Reset
        signal_count = 0
        current_signals = []
        participant_count += 1

        if participant_count == nParticipants:
            break

