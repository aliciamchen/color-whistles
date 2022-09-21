# Cluster signals using GMM using the `embedding.disc`

# %%

import numpy as np
import pandas as pd
from sklearn.mixture import BayesianGaussianMixture
import params


df = pd.read_csv("test/one2many_embedding_viz.csv")
# %%

bgm = BayesianGaussianMixture(
    n_components=params.bgm["n_components"],
    max_iter=params.bgm["max_iter"],
    random_state=params.seed,
)

for speaker in pd.unique(df["speaker"]):
    if speaker == "init":
        continue
    cluster_labels = bgm.fit_predict(df[df["speaker"] == speaker][["mds_1", "mds_2"]])
    df.loc[df["speaker"] == speaker, "cluster_label"] = cluster_labels

df.to_csv("test/one2many_embedding_viz.csv", index=False)

# If discreteness threshold is below a certain value, don't cluster
# %%
