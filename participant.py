from random import sample
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from scipy.spatial import distance_matrix

import tools.cluster
import tools.colors
import tools.preprocess
import tools.viz
import tools.stats

from sklearn.manifold import MDS
from sklearn import cluster, preprocessing
from skimage.color import luv2rgb
# from sklearn.metrics import r2_score

from scipy.stats import pearsonr



# %load_ext autoreload
# %autoreload 2


class Participant(tools.colors.Colors):
    def __init__(self, participant_idx, speaker_id=None):
        """
        Args:
            participant_idx (int): manual participant index to feed in
        """
        tools.colors.Colors.__init__(self)
        self.speaker_id = speaker_id
        self.idx = participant_idx

    def set_game_id(self, game_id):
        self.game_id = game_id

    def load_expt_info(self, df):
        """Load experiment info from participant df"""
        pass


    def load_signals(self, signals, sampling_frequency=50, distance_threshold=4.5):
        self.signals = signals
        # print(f"Found {len(signals)} signals")
        # find empty signals, get rid of corresponding colors
        empty_signals = []
        for idx, signal in enumerate(signals):
            # print(signal)
            if len(signal) < 2:  # if signal is empty or there is only one keypress
                empty_signals.append(idx)

        # print(signals[10])
        # print(empty_signals)
        print(f"Number of empty signals: {len(empty_signals)}")
        lab = [val for i, val in enumerate(self.lab) if i not in empty_signals]
        luv = [val for i, val in enumerate(self.luv) if i not in empty_signals]
        rgb = [val for i, val in enumerate(self.rgb) if i not in empty_signals]

        self.lab = lab
        self.luv = luv
        self.rgb = rgb

        # print(self.luv)
        # luv_mtx = np.asarray(self.luv)
        self.luv_dists = distance_matrix(self.luv, self.luv)

        self.empty_signals = empty_signals

        self.sampling_freq = sampling_frequency

        self.df_signals = tools.preprocess.signals2df(
            self.signals, sampling_frequency=self.sampling_freq
        )

        self.nSounds = len(self.signals)
        self.DTWdists = tools.cluster.compute_DTW_distances(self.df_signals)

        ## find optimal distance threshold
        self.thresh = tools.cluster.optimal_thresh_gridsearch(
            self.DTWdists, slope_thresh=0.0631
        )

        self.clustering = tools.cluster.make_clusters(
            self.DTWdists, distance_threshold=self.thresh
        )
        print(f"Number of clusters: {self.clustering.n_clusters_}")
        self.linkage_mtx = tools.cluster.make_linkage_mtx(self.clustering)

        # TODO: (maybe?) Sort DTW dists to make a sorted heatmap

        # Local systematicity stuff
        self.DTWdists_scaled = preprocessing.MinMaxScaler().fit_transform(self.DTWdists)
        self.luv_dists_scaled = preprocessing.MinMaxScaler().fit_transform(
            self.luv_dists
        )

        self.DTWminusLUV_diff = self.DTWdists_scaled - self.luv_dists_scaled
        self.DTW_LUV_norm = np.linalg.norm(self.DTWminusLUV_diff)
        self.avg_permuted_norm = tools.stats.calc_avg_permuted_norm(
            self.DTWdists_scaled, self.luv_dists_scaled, nReps=500
        )

        ## Type systematicity stuff

        # Extract RGB coords of color centroids

        self.sound_cluster_dists = tools.cluster.distance_btwn_clusters(
            self.clustering, self.DTWdists
        )
        (
            self.luv_centroids,
            self.color_cluster_dists,
        ) = tools.cluster.distance_btw_color_centroids(self.clustering, self.luv)

        self.rgb_centroids = luv2rgb(self.luv_centroids)
        self.sound_cluster_dists_scaled = preprocessing.MinMaxScaler().fit_transform(
            self.sound_cluster_dists
        )
        self.color_cluster_dists_scaled = preprocessing.MinMaxScaler().fit_transform(
            self.color_cluster_dists
        )

        self.cluster_diff = (
            self.sound_cluster_dists_scaled - self.color_cluster_dists_scaled
        )
        self.avg_permuted_cluster_norm = tools.stats.calc_avg_permuted_norm(
            self.color_cluster_dists_scaled, self.sound_cluster_dists_scaled, nReps=500
        )
        self.cluster_norm = np.linalg.norm(self.cluster_diff)

    def find_all_dists(self):
        indiv_color_dists = []
        indiv_signal_dists = []
        for idx_1 in range(self.DTWdists_scaled.shape[0]):
            for idx_2 in range(idx_1+1, self.DTWdists_scaled.shape[0]):
                color_dist = self.luv_dists_scaled[idx_1, idx_2]
                signal_dist = self.DTWdists_scaled[idx_1, idx_2]
                indiv_color_dists.append(color_dist)
                indiv_signal_dists.append(signal_dist)

        clust_color_dists = []
        clust_signal_dists = []
        for idx_1 in range(self.sound_cluster_dists_scaled.shape[0]):
            for idx_2 in range(idx_1 + 1, self.sound_cluster_dists_scaled.shape[0]):
                color_dist = self.color_cluster_dists_scaled[idx_1, idx_2]
                signal_dist = self.sound_cluster_dists_scaled[idx_1, idx_2]
                clust_color_dists.append(color_dist)
                clust_signal_dists.append(signal_dist)

        return indiv_color_dists, indiv_signal_dists, clust_color_dists, clust_signal_dists



    def plot_dist_scatter(self, ax):
        # color dist on x axis, sound dist on y axis
        # sound 0; color 1-39
        # sound 1: color 2-39
        color_dists = []
        signal_dists = []
        for idx_1 in range(self.DTWdists_scaled.shape[0]):
            for idx_2 in range(idx_1+1, self.DTWdists_scaled.shape[0]):
                color_dist = self.luv_dists_scaled[idx_1, idx_2]
                signal_dist = self.DTWdists_scaled[idx_1, idx_2]
                color_dists.append(color_dist)
                signal_dists.append(signal_dist)

        r, p = pearsonr(color_dists, signal_dists)
        ax.scatter(color_dists, signal_dists)
        ax.set_title(f"indiv sounds part {self.idx}, r = {r}, p = {p}")
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

        print(f"Local systematicity r = {r}, p = {p}")

        # return color_dists, signal_dists
        # ax.set_xlabel("color distance")
        # ax.set_ylabel("signal distance")

    def plot_dist_scatter_cluster(self, ax):
        color_dists = []
        signal_dists = []
        for idx_1 in range(self.sound_cluster_dists_scaled.shape[0]):
            for idx_2 in range(idx_1 + 1, self.sound_cluster_dists_scaled.shape[0]):
                color_dist = self.color_cluster_dists_scaled[idx_1, idx_2]
                signal_dist = self.sound_cluster_dists_scaled[idx_1, idx_2]
                color_dists.append(color_dist)
                signal_dists.append(signal_dist)

        if len(color_dists) > 2:
            r, p = pearsonr(color_dists, signal_dists)
        else:
            r = np.nan
            p = np.nan

        ax.scatter(color_dists, signal_dists)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_title(f"clusters part {self.idx}, r = {r}, p = {p}")

        print(f"Type systematicity r = {r}, p = {p}")
        # ax.set_xlabel("color distance")
        # ax.set_ylabel("signal distance")
        # return color_dists, signal_dists

    def plot_cluster_dist_scatter(self, ax):
        pass

    def load_file(self, data_filename, sampling_frequency=50):
        """Load participant data from file.

        Args:
            data_filename (str): `.json` file to load participant data
            sampling_frequency (int, optional): Defaults to 50.
        """
        self.data_filename = data_filename

        with open(data_filename) as file:
            self.signals = json.load(file)

        self.load_signals(self.signals, sampling_frequency=sampling_frequency)

    def view_sound(self, sound_idx):
        """View a single sound.

        Args:
            sound_idx (int): index of sound 0-39
        """
        if sound_idx >= self.nSounds:
            raise IndexError(f"Sound {sound_idx} does't exist.")

        fig, ax = plt.subplots()
        tools.viz.plot_sound(self.df_signals, idx=sound_idx, ax=ax)
        plt.show()

    def plot_sounds(self, output_dir=None, show=True):
        """Plot all sounds in a 5x8 grid, optionally save
        TODO: get rid of optionally save part and put it in another file

        Args:
            output_dir (str, optional): Place to save file. Defaults to None.
            show (bool, optional): Whether to show plot. Defaults to True.

        Returns:
            [type]: [description]
        """
        plot_dims = (5, 8)  # row, col

        def extract_rowcol(i, plot_dims):
            col = i % plot_dims[1]
            row = i // plot_dims[1]

            assert i == plot_dims[1] * row + col

            assert col < plot_dims[1]
            assert row < plot_dims[0]

            return row, col

        # Plot
        fig, axs = plt.subplots(plot_dims[0], plot_dims[1], figsize=(50, 20))

        for sound_idx in range(self.nSounds):
            row, col = extract_rowcol(sound_idx, plot_dims)
            tools.viz.plot_sound(self.df_signals, sound_idx, ax=axs[row, col])

        for ax in axs.flat:
            ax.label_outer()

        if output_dir is not None:
            plt.savefig(output_dir)

        if show:
            plt.show()

    def plot_clusters_2d(self, ax, centroids=True):
        # TODO: change cluster_cmap to something that doesnt have to be passed in (maybe randomize colors?)
        # mds = MDS(
        #     n_components=2,
        #     max_iter=3000,
        #     eps=1e-12,
        #     random_state=111,
        #     dissimilarity="precomputed",
        #     n_jobs=1,
        # )

        # pos = mds.fit(self.DTWdists).embedding_

        # nmds = MDS(
        #     n_components=2,
        #     metric=False,
        #     max_iter=3000,
        #     eps=1e-12,
        #     dissimilarity="precomputed",
        #     random_state=111,
        #     n_jobs=1
        #     # n_init=30,
        # )

        # embedding = nmds.fit_transform(self.DTWdists, init=pos)

        mds = MDS(
            n_components=2,
            metric=True,
            max_iter=300,
            eps=1e-12,
            dissimilarity="precomputed",
            random_state=111,
            n_init=30,
        )

        embedding = mds.fit_transform(self.DTWdists)
        if centroids:
            colors = [
                self.cluster_color_map[label] for label in self.clustering.labels_
            ]
        else:
            colors = self.rgb

        # plt.figure()
        ax.scatter(embedding[:, 0], embedding[:, 1], c=colors)

        if centroids:
            for i in range(embedding.shape[0]):
                ax.annotate(i, (embedding[i, 0] + 0.05, embedding[i, 1]))

        ax.set_title(f"Participant {self.idx}")
        # plt.show()

    def plot_clusters_1d(self, ax, centroids=True, annot=False):

        mds = MDS(
            n_components=1,
            metric=True,
            max_iter=300,
            eps=1e-12,
            dissimilarity="precomputed",
            random_state=111,
            n_init=30,
        )

        embedding = mds.fit_transform(self.DTWdists)
        if centroids:
            colors = [
                self.cluster_color_map[label] for label in self.clustering.labels_
            ]
        else:
            colors = self.rgb

        # plt.figure()
        ax.scatter(embedding, [0 for i in embedding], c=colors)

        if annot:
            for i in range(embedding.shape[0]):
                ax.annotate(i, (embedding[i, 0] + 0.05, embedding[i, 1]))


        # ax.set_title(f"Participant {self.idx}")

    # def plot_colors_2d_

    def save_plots(self):
        pass

    def set_cluster_cmap(self, cluster_color_map):
        self.cluster_color_map = cluster_color_map

    # TODO: add a plot that displays sounds with their corresponding color


# Testing
if __name__ == "__main__":

    # TODO: change this so that it loops through all the participants

    sample_part = Participant(0)
    sample_part.load_file(data_filename="./test_data/signals/test_part_0.json")
    # sample_part.set_cluster_cmap(cluster_color_map={0: "red", 1: "green"})

    # test grid plot
    # sample_part.plot_sounds(output_dir="./results/gridplot_test.png", show=True)

    print(sample_part.clustering.children_)
    print(sample_part.clustering.distances_)
    print(
        tools.cluster.distance_btwn_clusters(
            sample_part.clustering, sample_part.DTWdists
        )
    )

