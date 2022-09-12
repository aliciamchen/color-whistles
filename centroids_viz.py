# %%
import json
import os
import numpy as np
import pandas as pd
import seaborn as sns
from tools import viz
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.color import luv2rgb

# load in LUV files from json
#  `embedding_viz.csv` has the clusters
# for each participant, loop thru clusters
# for each cluster find the centroid (maybe use a hex2luv converter? or use luv from json)
# add the centroid color to the csv for all stuff in that cluster
# then given referent ids make a list that sorts centroid colors by referent id (make a dict of all participants to this list)
# then plot! from `tools.viz`
# probably add participant ids to this plot too

def plot_ref_colors(cmap, title=None, save=False, output_dir="./results/colors.png"):
    """View colors on a horizontal grid; every color is labeled with its index

    Args:
        cmap (list): list of RGB coords
        save (bool, optional): Whether to save the output `.png` file. Defaults to False.
        output_dir (str, optional): Place to save the plot. Defaults to "./results/colors.png".
    """
    nColors = len(cmap)

    plt.figure(figsize=(2*nColors, 2))

    sns.heatmap(
        data=np.array([list(range(nColors))]),
        cmap=cmap,
        annot=np.array([list(range(nColors))]),
        annot_kws={"size": 20},
        linewidths=0.1,
        cbar=False,
        xticklabels=False,
        yticklabels=False,
    )

    plt.title(title, fontsize=50)
    if save:
        plt.savefig(output_dir)

    if not save:
        plt.show()


def plot_luv_colors(luv, title=None, **kwargs):
    if type(luv) is not list:
        luv = np.array(luv)

    rgb_array = luv2rgb(luv)
    rgb_cmap = rgb_array.tolist()
    plot_ref_colors(cmap=rgb_cmap, title=title, **kwargs)

# %%

df = pd.read_csv("test/one2many_embedding_viz.csv")
df['centroid'] = np.nan
df['centroid'] = df['centroid'].astype(object)

with open("tools/wcs_row_F.json") as f:
    colors_coords = json.load(f)

luv_coords = colors_coords['luv']
# %%

for speaker in pd.unique(df['speaker']):
    if speaker == 'init':
        continue

    clusters = pd.unique(df[df['speaker'] == speaker]['cluster_label'])
    # print(clusters)
    for cluster in clusters:
        referent_ids = pd.unique(df[(df['speaker'] == speaker) & (df['cluster_label'] == cluster)]['referent_id'])

        colors_in_cluster = []
        for referent_id in referent_ids:
            colors_in_cluster.append(luv_coords[referent_id])

        colors_numpy = np.array(colors_in_cluster)
        # print(colors_numpy)
        centroid = np.mean(colors_numpy, axis=0)
        # print(centroid)
        df.loc[(df['speaker'] == speaker) & (df['cluster_label'] == cluster), 'centroid'] = str(list(centroid))
        # print(df)

# %%

speaker_centroid_maps = {}

for speaker in pd.unique(df['speaker']):
    if speaker == 'init':
        continue

    filtered_df = df.loc[df['speaker'] == speaker]
    filtered_df.sort_values(by=['referent_id'], inplace=True)

    centroid_map = filtered_df['centroid'].to_list()
    # print(centroid_map)
    centroid_map_fixed = list(map(lambda x: eval(x), centroid_map))
    speaker_centroid_maps[speaker] = centroid_map_fixed

# %%
for speaker in pd.unique(df['speaker']):
    if speaker == 'init':
        continue
    plot_luv_colors(speaker_centroid_maps[speaker], title=speaker)
# %%
# TODO: plot all centroid maps in one file