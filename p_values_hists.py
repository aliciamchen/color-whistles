# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
all_calculations = pd.read_csv("test_output/all_calculations.csv")

df_within = pd.read_csv("test_output/within_clust_syst.csv")
df_between = pd.read_csv("test_output/between_clust_syst.csv")
df_systematicity = pd.read_csv("test_output/syst_v2.csv")

# for each participant, add comm_score from all_calculations into df_within and df_between
df_within = pd.merge(df_within, all_calculations[["speaker", "game", "comm_score"]], on="speaker")
df_between = pd.merge(df_between, all_calculations[["speaker", "game", "comm_score"]], on="speaker")
df_systematicity = pd.merge(df_systematicity, all_calculations[["speaker", "game", "comm_score"]], on="speaker")
df_systematicity = pd.merge(df_systematicity, df_between[["speaker", "n_clusters"]], on="speaker")
# filter between cluster systematicity to only include participants with more than 1 cluster
df_between = df_between[df_between["n_clusters"] > 1]

# %% Visualize all variables
sns.pairplot(data=all_calculations, vars=["systematicity", "discreteness", "learn_score", "own_score", "comm_score", "alignment", "btwn_clust_sys", "n_clusters", "within_clust_sys"], hue="game")
plt.show()


# %% Are p values for global systematicity related to  communication score?
plt.figure(figsize=(8, 4))  # Set the figure size to be wider
plt.scatter(data=df_systematicity, x="dcor", y="p", c="comm_score", s=50, alpha=0.8)
plt.axhline(y=0.05, color='red', linestyle='--')
plt.xlabel("Global systematicity")
plt.ylabel("p value")
plt.title("Global systematicity - p values by communication score")
plt.colorbar(label="comm_score")

# Add gray lines connecting points based on the 'game' column
games = df_systematicity['game'].unique()
for game in games:
    df_game = df_systematicity[df_systematicity['game'] == game]
    plt.plot(df_game['dcor'], df_game['p'], marker='', linestyle='-', color='gray', alpha=0.5)

plt.show()

# %%
# plot global systematicity by communication score
# color should be the number of colors
plt.scatter(data=df_systematicity, x="dcor", y="comm_score", c="n_clusters", s=50, alpha=0.8)
plt.xlabel("Global systematicity")
plt.ylabel("Communication score")
plt.colorbar(label="n_clusters")
plt.show()

# %% Plot n_clusters by global systematicity, colored by communication score

# What does this show?
plt.scatter(data=df_systematicity, x="dcor", y="n_clusters", c="comm_score", s=50, alpha=0.8)
plt.xlabel("Global systematicity")
plt.ylabel("Number of clusters")
plt.title("Global systematicity - number of clusters by communication score")
plt.colorbar(label="comm_score")
plt.show()

# %% Plot number of clusters by communication score

plt.scatter(data=df_between, x="n_clusters", y="comm_score")
plt.xlabel("Number of clusters")
plt.ylabel("Communication score")
plt.show()

# %% Within cluster systematicity

# Plot distribution of p values across all speakers
sns.histplot(data=df_within, x="p", bins=40)
plt.axvline(x=0.05, color='red', linestyle='--')
plt.title("Within-cluster systematicity - distribution of p values across clusters, all games")
plt.show()

# %% Sanity check: Are p values related to the number of signals in the cluster?

plt.scatter(data=df_within, x="n_signals", y="p", c="comm_score")
plt.axhline(y=0.05, color='red', linestyle='--')
plt.xlabel("Number of signals in cluster")
plt.ylabel("p value")
plt.title("Within-cluster systematicity - p values by number of signals in cluster")
plt.colorbar(label="comm_score")
plt.show()

## Between cluster systematicity
# %% Are p values / communication score related to total number of clusters?

plt.scatter(data=df_between, x="n_clusters", y="p", c="comm_score")
# Add gray lines connecting points based on the 'game' column
games = df_between['game'].unique()
for game in games:
    df_game = df_between[df_between['game'] == game]
    plt.plot(df_game['n_clusters'], df_game['p'], marker='', linestyle='-', color='gray', alpha=0.5)

plt.axhline(y=0.05, color='red', linestyle='--')
plt.xlabel("Number of clusters")
plt.ylabel("p value")
plt.title("Between-cluster systematicity - p values by number of clusters")
plt.colorbar(label="comm_score")

plt.show()




# %%  Between-cluster

# Are p values for between-cluster systematicity related to  communication score?

#get rid of the ones where the value is 0
plt.scatter(data=df_between, x="dcor", y="p", c="comm_score")

games = df_between['game'].unique()
for game in games:
    df_game = df_between[df_between['game'] == game]
    plt.plot(df_game['dcor'], df_game['p'], marker='', linestyle='-', color='gray', alpha=0.5)

plt.axhline(y=0.05, color='red', linestyle='--')
plt.xlabel("Between-cluster systematicity")
plt.ylabel("p value")
plt.title("Between-cluster systematicity - p values by communication score")
plt.colorbar(label="comm_score")
plt.show()



# %% Plot average within-cluster systematicity by between-cluster systematicity

# group by speaker; for each speaker, calculate the average within-cluster systematicity by weighing the dcor by the number of signals
df_within_avg = df_within.groupby("speaker").apply(lambda x: pd.Series({"speaker": x["speaker"].iloc[0], "dcor": np.average(x["dcor"], weights=x["n_signals"])})).reset_index(drop=True)
# df_within_avg = pd.DataFrame(df_within_avg, columns=["dcor"])

# merge with between-cluster systematicity
df_between_avg = df_between[["speaker", "game", "dcor"]].copy()

# merge within and between
df_avg = pd.merge(df_within_avg, df_between_avg, on="speaker", suffixes=("_within", "_between"))

# add communication score
df_avg = pd.merge(df_avg, all_calculations[["speaker", "comm_score", "systematicity"]], on="speaker")


# plot
plt.scatter(data=df_avg, x="dcor_between", y="dcor_within", c="comm_score")
# sns.scatterplot(data=df_avg, x="dcor_between", y="dcor_within", c="comm_score")

games = df_avg['game'].unique()
for game in games:
    df_game = df_avg[df_avg['game'] == game]
    plt.plot(df_game['dcor_between'], df_game['dcor_within'], marker='', linestyle='-', color='gray', alpha=0.5)

plt.xlabel("average between-cluster systematicity")
plt.ylabel("average within-cluster systematicity")
plt.colorbar(label="comm_score")

plt.title("average Within-cluster systematicity by between-cluster systematicity")
plt.show()

# %% plot average between vs average within vs global sys
plt.scatter(data=df_avg, x="dcor_between", y="dcor_within", c="systematicity")
plt.xlabel("average between-cluster systematicity")
plt.ylabel("average within-cluster systematicity")
plt.colorbar(label="global systematicity")
plt.show()

# %% Are p values for within-cluster systematicity related to  communication score?

plt.scatter(data=pd.merge(df_within_avg, all_calculations[["speaker", "comm_score"]], on="speaker"), x="dcor", y="comm_score")
plt.xlabel("average within-cluster systematicity")
plt.ylabel("communication score")
plt.title("Within-cluster systematicity for each participant by communication score")
plt.show()
# TODO: test if this is significant?

# %% Are p values for between-cluster systematicity related to  communication score?
plt.scatter(data=df_between, x="dcor", y="comm_score")
plt.xlabel("Between-cluster systematicity")
plt.ylabel("Communication score")
plt.title("Between-cluster systematicity for each participant by communication score")
plt.show()

# %% For each speaker, plot the distribution of p values
for speaker in df_within["speaker"].unique():
    df_speaker = df_within[df_within["speaker"] == speaker]
    plt.hist(df_speaker["p"], bins=20)
    plt.title(f"Speaker {speaker}")
    plt.show()

# TODO: make scale the same for all plots, and also highlight p values less than 0.5
# %% Between cluster systematicity

sns.histplot(df_between["p"], bins=50)
plt.axvline(x=0.05, color='red', linestyle='--')
plt.title("Between-cluster systematicity - distribution of p values across participants")
plt.show()

# %%


# %%
# Plot distribution of global systematicity scores
sns.histplot(df_systematicity["dcor"], bins=20)
plt.title("Global systematicity - distribution of systematicity scores across participants")
plt.show()

# %%

# plot p values for systematicity scores
sns.histplot(df_systematicity["p"], bins=50)
plt.axvline(x=0.05, color='red', linestyle='--')
plt.title("Global systematicity - distribution of p values across participants")
# plt.xlim(-0.1, 1)
plt.show()
