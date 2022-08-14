"""Clean experiment data and output cleaned .csv file"""

import numpy as np
import pandas as pd
import os
import json


def clean_df(df):

    games = pd.unique(df['gameid'])
    speakers = pd.unique(df['speakerid'])

    # get rid of games that are fewer than 80 rounds

    for game in games:
        if len(df[df['gameid'] == game].index) < 80:
            df.drop(df[df['gameid'] == game].index, inplace = True)

    return df
    # games_cleaned = pd.unique(df['gameid'])


def make_game_info(df):
    # For each game, make a dict of which speakers participate in the game
    games = pd.unique(df['gameid'])
    speaker_game_info = {}
    for game in games:
        speakers_ = df[df['gameid'] == game]['speakerid'].unique()
        speakers_ = list(speakers_)
        speaker_game_info[game] = speakers_

    return speaker_game_info

def make_json_signals(df):

    speakers = pd.unique(df['speakerid'])
    for idx, speaker in enumerate(speakers):

    # print(f"speaker{speaker}")
        speaker_signals = []
        for color in range(max(df['correctid'] + 1)):
            # print(df.loc[(df['speakerid'] == speaker) & (df['correctid'] == color)]['signalproduced'])
            if not len(df.loc[(df['speakerid'] == speaker) & (df['correctid'] == color)]['signalproduced']):
                speaker_signals.append([])
                continue
            # print(df.loc[(df['speakerid'] == speaker) & (df['correctid'] == color)]['signalproduced'])
            try:
                signal = df.loc[(df['speakerid'] == speaker) & (df['correctid'] == color)]['signalproduced'].item()
            except ValueError:
                print(color)
                print(df.loc[(df['speakerid'] == speaker) & (df['correctid'] == color)]['signalproduced'])
            # print(type(signal))
            # print(signal)
            signal_ = json.loads(signal)
            # signal_ = ast.literal_eval(signal)
            speaker_signals.append(signal_)

    return speaker_signals


if __name__ == "__main__":

    ## Clean and save one to many csvs

    filename1 = "../data/2022-01-25_one2many/communication_game_data.zip"
    filename2 = "../data/2022-01-26_one2many/communication_game_data.zip"
    df1 = pd.read_csv(filename1)
    df2 = pd.read_csv(filename2)

    df = pd.concat([df1, df2], ignore_index=True)
    df_edited = clean_df(df)

    df_edited.to_csv("../data/one2many/one2many_expt_cleaned.zip")


    ## Clean and save one to one csv

    filename1 = "../data/2022-01-27_one2one/communication_game_data.zip"
    df1 = pd.read_csv(filename1)
    df_edited = clean_df(df1)
    df_edited.to_csv("../data/one2one/one2one_expt_cleaned.zip")








