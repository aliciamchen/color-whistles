import json
import pandas as pd

df = pd.read_csv("test/one2many_comm.zip")

game_scores = {}

for speaker in pd.unique(df["speakerid"]):

    score = df[df["speakerid"] == speaker]["score"].mean()
    game_scores[speaker] = score


with open("test/one2many_game_scores.json", "w") as f:
    json.dump(game_scores, f)
