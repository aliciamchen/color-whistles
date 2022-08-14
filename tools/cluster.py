"""
Helper functions for clustering signals
"""

# from audioop import avg
# from turtle import color
import numpy as np
import pandas as pd
from sklearn import cluster

from tslearn.utils import to_time_series_dataset
from tslearn.metrics import cdist_dtw

from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import pairwise_distances

from tqdm import tqdm


def compute_DTW_distances(df):
    """
    Args:
        DataFrame: signal data for a single participant, output of `tools.preprocess.signals2df`

    Returns:
        ndarray: square distance matrix between all the sounds
    """
    nSignals = df["idx"].nunique()

    signal_indices = df["idx"].unique()
    # print(signal_indices)
    assert nSignals != 0
    print(f"Found {nSignals} signals, making list of signals")
    signallists = [
        df[df["idx"] == idx]["signalWithZeros"].to_list() for idx in signal_indices
    ]
    assert len(signallists) != 0

    X = to_time_series_dataset(signallists)
    dists = cdist_dtw(X)

    return dists

def compute_DTW_distances_all(df):
    """Compute DTW distances for all participants in a single experiment

    Args:
        DataFrame: signal data for a single participant, output of `tools.preprocess.signals2df`

    Returns:
        ndarray: square distance matrix between all the sounds
    """
    df_= df.set_index(['participant', 'idx'])
    indices = df_.index.unique()
    unique_indices = indices.unique()
    nSignals = len(unique_indices)  # there's probably a better way to do this

    # signal_indices = df["idx"].unique()
    # print(signal_indices)
    assert nSignals != 0
    print(f"Found {nSignals} signals, making list of signals")
    signallists = [
        df_[df_.index == idx]["signalWithZeros"].to_list() for idx in tqdm(unique_indices)
    ]
    assert len(signallists) != 0

    # TODO: put the above stuff into a new function

    print('calculating distances..')
    X = to_time_series_dataset(signallists)
    print('done converting to time series dataset')
    dists = cdist_dtw(X, n_jobs=-1)

    return dists, unique_indices


def make_clusters(dists, distance_threshold=4.5):
    # print(dists)
    clustering = AgglomerativeClustering(
        n_clusters=None,
        compute_full_tree=True,
        distance_threshold=distance_threshold,
        affinity="precomputed",
        linkage="average",
        compute_distances=True,
    ).fit(dists)

    # TODO: add other clustering methods?
    return clustering


def avg_dist_within_clusters(clustering, dists):

    nClusters = clustering.n_clusters_
    clusterLabels = clustering.labels_

    avg_dists = []
    cluster_counts = []  # number of counts of each cluster
    for i in range(nClusters):
        filtered_dist_mtx = dists[
            np.ix_(np.where(clusterLabels == i)[0], np.where(clusterLabels == i)[0])
        ]

        avg_dists.append(np.mean(filtered_dist_mtx))
        cluster_count = (clusterLabels == i).sum()
        cluster_counts.append(cluster_count)

    assert(len(cluster_counts) == len(avg_dists))  # len of both should be # clusters

    avg_dists_array = np.array(avg_dists)
    cluster_counts_array = np.array(cluster_counts)

    avg_dist = np.sum(avg_dists_array * cluster_counts_array) / np.sum(cluster_counts_array)
    return avg_dist


def optimal_thresh_gridsearch(dists, slope_thresh=.05):
    thresholds = np.linspace(5, 0, 50)
    avg_dists = []

    for threshold in thresholds:
        clustering = make_clusters(dists, threshold)
        avg_dist = avg_dist_within_clusters(clustering, dists)
        avg_dists.append(avg_dist)
    # print(avg_dists)
    dist_diffs = []
    for idx in range(len(avg_dists) - 1):
        dist_diffs.append(avg_dists[idx + 1] - avg_dists[idx])

    # print(dist_diffs)

    for idx, diff in enumerate(dist_diffs):
        if diff != 0:
            if abs(diff) < slope_thresh:
                # print(f"abs diff: {abs(diff)}; index: {idx}; slope_thresh: {slope_thresh}")
                thresh = thresholds[idx-1]
                break


    print(f"Optimal dendrogram threshold: {thresh}")
    return thresh


def distance_btwn_clusters(clustering, dists):

    # Should return matrix with dimensions (nClusters, nClusters) computing pairwise dist b/w each of the clusters
    nClusters = clustering.n_clusters_
    clusterLabels = clustering.labels_
    avg_dists = np.zeros((nClusters, nClusters))

    for i in range(nClusters):
        for j in range(nClusters):
            # find average distance between points in cluster i and cluster j
            filtered_dist_mtx = dists[
                np.ix_(np.where(clusterLabels == i)[0], np.where(clusterLabels == j)[0])
            ]  # lol there has to be a better way to do this...

            avg_dists[i, j] = np.mean(filtered_dist_mtx)

    # print(avg_dists)
    return avg_dists


def distance_btw_color_centroids(clustering, color_coords):
    # Extract color centroids
    # color coords is a list of color coords
    nClusters = clustering.n_clusters_
    clusterLabels = clustering.labels_
    colors = np.array(color_coords)

    # First, extract color centroids for each cluster
    centroids = np.zeros((nClusters, colors.shape[1]))
    for cluster in range(nClusters):
        sub_color_coords = colors[clusterLabels == cluster]
        centroid = np.mean(sub_color_coords, axis=0)
        centroids[cluster, :] = centroid

    # Then, find distance between centroids
    color_dists = pairwise_distances(centroids, centroids)

    return centroids, color_dists


def make_linkage_mtx(clustering):
    """Make linkage matrix from sklearn documentation
    For making dendrogram

    Args:
        clustering ([type]): [description]
    """
    counts = np.zeros(clustering.children_.shape[0])
    n_samples = len(clustering.labels_)
    for i, merge in enumerate(clustering.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_mtx = np.column_stack(
        [clustering.children_, clustering.distances_, counts]
    ).astype(float)

    return linkage_mtx

