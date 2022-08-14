import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.color import luv2rgb

def plot_sound(df, idx, ax=None):
    """Plot a single sound.

    Args:
        df (DataFrame): dataframe for a specific participant
        idx (int): index of sound (0-39) to plot
    """
    # plt.figure()
    if ax is None:
        fig, ax = plt.subplots()

    ax.scatter(df[(df["idx"] == idx)]["t"], df[df["idx"] == idx]["signal"], s=130)
    ax.plot(
        df[(df["idx"] == idx)]["t"],
        df[(df["idx"] == idx)]["val"],
        color="r",
        linestyle="--",
    )

    ax.set_title(f"Sound {idx}")
    # plt.show()


def plot_all_sounds(df):
    nSignals = df["idx"].nunique()

    for idx in range(nSignals):
        plot_sound(df, idx)



def plot_ref_colors(cmap, save=False, output_dir="./results/colors.png"):
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

    if save:
        plt.savefig(output_dir)

    if not save:
        plt.show()


def plot_luv_colors(luv, **kwargs):
    if type(luv) is not list:
        luv = np.array(luv)

    rgb_array = luv2rgb(luv)
    rgb_cmap = rgb_array.tolist()
    plot_ref_colors(cmap=rgb_cmap, **kwargs)
