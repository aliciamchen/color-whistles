"""Visualize stress vs. number of MDS dimensions"""
import json
import os
import argparse

import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import MDS


import params

def mds_stresses(pairwise_dists, max_components):
    components = []
    stresses = []
    for n_components in range(1, max_components + 1):

        print(f"Calculating MDS projection for {n_components} components")
        mds = MDS(
            n_components=n_components,
            eps=params.mds_discreteness["eps"],
            n_jobs=-1,
            dissimilarity="precomputed",
            random_state=params.seed,
            n_init=params.mds_discreteness["n_init"],
            max_iter=params.mds_discreteness["max_iter"],
        )

        mds.fit(pairwise_dists)
        stresses.append(mds.stress_)
        components.append(n_components)
        print(f"{n_components} components, stress: {mds.stress_}")

    return components, stresses

def scree_plot(components, stresses, ax):
    ax.plot(components, stresses, 'o-', linewidth=2, color="blue")
    ax.set(xlabel="components", ylabel="stress", title="scree plot")

def main(args):

    pairwise_dists = np.loadtxt(args.dists_file)
    components, stresses = mds_stresses(pairwise_dists, max_components=7)

    with open(os.path.join(args.output_dir, "stresses.json"), "w") as f:
        json.dump(dict(zip(components, stresses)), f)

    # Generate scree plot
    fig, ax = plt.subplots()
    scree_plot(components, stresses, ax)
    plt.savefig(os.path.join(args.output_dir, "scree_plot.png"))
    plt.show()



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--dists_file", required=True, type=str, help="`.txt` pairwise dists file")
    parser.add_argument("--output_dir", required=True, type=str, help="place to save output")

    args = parser.parse_args()

    main(args)


