# %%
import json
import os
import numpy as np
import pandas as pd
import seaborn as sns
from tools import viz

# load in LUV files from json
#  `embedding_viz.csv` has the clusters
# for each participant, loop thru clusters
# for each cluster find the centroid (maybe use a hex2luv converter? or use luv from json)
# add the centroid color to the csv for all stuff in that cluster
# then given referent ids make a list that sorts centroid colors by referent id (make a dict of all participants to this list)
# then plot! from `tools.viz`
# probably add participant ids to this plot too

# %%

df = pd.read_csv("test_output/embedding_viz.csv")
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
    viz.plot_luv_colors(speaker_centroid_maps[speaker])
# %%
