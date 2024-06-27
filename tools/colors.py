import json
import os
from scipy.spatial import distance_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import tools.viz
from tools.config.definitions import root_dir


class Colors:
    """Class for dealing with color info
    """

    def __init__(self, filename=os.path.join(root_dir, "wcs_row_F.json")):
        """Load and store colors.

        Args:
            filename (str, optional): `.json` file to load color info. Defaults to "wcs_row_F.json".
        """
        with open(filename) as file:
            loaded_colors = json.load(file)

        self.wcs_cnums = loaded_colors["wcs_cnums"]
        self.lab = loaded_colors["lab"]
        self.luv = loaded_colors["luv"]
        self.rgb = loaded_colors["rgb"]

        self.nColors = len(self.wcs_cnums)

        assert len(self.wcs_cnums) == len(self.lab) == len(self.luv) == len(self.rgb)

        # Calculate color distances in luv space
        self.luv_dists = distance_matrix(self.luv, self.luv)


    def display_colors(self, **kwargs):
        """Display colors using seaborn heatmap function

        Optional parameters (passed into arguments of `tools.viz.plot_colors`):
            save (bool): whether to save the output .png file (default: False)
            output_dir (string): place to save the colormap (default: "./results/colors.png")
        """
        tools.viz.plot_ref_colors(cmap=self.rgb, **kwargs)

    def calc_color_dists(self):
       # calculate correlation matrix between 40 colors
       pass

# Testing
if __name__ == "__main__":
    colors = Colors()

    f, ax = plt.subplots()
    ax = sns.heatmap(colors.luv_dists, cmap="YlGn")
    plt.savefig("../results/luv_color_dists_YlGn.png")

    f, ax = plt.subplots()
    ax = sns.heatmap(colors.luv_dists, cmap="BuPu")
    plt.savefig("../results/luv_color_dists_BuPu.png")

    f, ax = plt.subplots()
    ax = sns.heatmap(colors.luv_dists, cmap="Oranges")
    plt.savefig("../results/luv_color_dists_BuPu.png")
