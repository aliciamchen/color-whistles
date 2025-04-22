# %%
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
    process_whistles.plot_signal(signal, lw=10, ax=ax)
    plt.axis('off')
    plt.savefig(f"figs/comm_signal_{speaker}_{referent}.svg")



# %% Plot game-level signals with player/color grid

def plot_game_signals(df):
    """Create a grid of signals for each game, with rows as colors and columns as players."""
    # Load game scores
    with open("outputs/game_scores.json") as f:
        game_scores = json.load(f)
    
    # Group by game id to process one game at a time
    games = df['gameid'].unique()
    
    for game in games:
        print(f"Processing game {game}...")
        game_df = df[df['gameid'] == game]
        
        players = game_df['speakerid'].unique()
        color_data = game_df[['correct', 'correctid']].drop_duplicates()
        
        # Sort colors by correctid
        color_data = color_data.sort_values('correctid')
        colors = color_data['correct'].tolist()

        fig, axes = plt.subplots(
            nrows=len(colors), 
            ncols=len(players), 
            figsize=(len(players) * 4, len(colors) * 1.5),
            constrained_layout=True,
            sharex='col', 
            sharey='row'  
        )
        
        # Get average game score
        player1_score = game_scores.get(players[0], "N/A")
        player2_score = game_scores.get(players[1], "N/A")
        if isinstance(player1_score, (int, float)) and isinstance(player2_score, (int, float)):
            game_score = (player1_score + player2_score) / 2
        else:
            game_score = "N/A"
        
        score_str = f"Score: {game_score:.3f}" if isinstance(game_score, (int, float)) else f"Score: {game_score}"
        
        # Set title for the entire figure with game score
        fig.suptitle(f"Game: {game} {score_str}", fontsize=16)
        
        # If there's only one color or player, make sure axes is 2D
        if len(colors) == 1:
            axes = axes.reshape(1, -1)
        if len(players) == 1:
            axes = axes.reshape(-1, 1)
            
        # Add column headers (player IDs)
        for j, player in enumerate(players):
            axes[0, j].set_title(f"Player: {player[:6]}...", fontsize=10)
        
        # Create a separate axis for color boxes
        box_width = 0.5  
        box_height = 0.8
        
        # Add colored boxes for row labels
        for i, color in enumerate(colors):
            # Add small colored rectangle to the left of each row
            color_box = plt.Rectangle(
                (-box_width*1.2, 0), 
                box_width, 
                box_height, 
                facecolor=color, 
                transform=axes[i, 0].transAxes,
                clip_on=False
            )
            axes[i, 0].add_patch(color_box)
            
            
        # Fill in each subplot with the corresponding signal
        for i, color in enumerate(colors):
            for j, player in enumerate(players):
                ax = axes[i, j]
                try:
                    # Get signal for this player and color
                    raw_signal = fetch_json_signal(game_df, player, color)
                    signal = process_whistles.interpolate_signal(raw_signal)
                    
                    # Plot signal
                    process_whistles.plot_signal(signal, lw=4, ax=ax)
                    
                    ax.set_xticks([])
                    ax.set_yticks([])
                except Exception as e:
                    # Handle case where player didn't produce a signal for this color
                    ax.text(0.5, 0.5, "No signal", ha='center', va='center')
                    ax.set_xticks([])
                    ax.set_yticks([])
        
        # Save the figure
        plt.savefig(f"figs/game_signals_{game}.svg", bbox_inches='tight')
        plt.close()

# %% 
# Create game-level charts
plot_game_signals(df)

