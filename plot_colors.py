# Plot colorbar for schematic figure


# %%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# %%

# Load colors
with open("tools/wcs_row_F.json") as file:
    loaded_colors = json.load(file)

# %%
cmap = loaded_colors["rgb"]

nColors = len(cmap)

plt.figure(figsize=(2*nColors, 5))  # Increase the height of the figure

sns.heatmap(
    data=np.array([list(range(nColors))]),
    cmap=cmap,
    linewidths=0.1,
    cbar=False,
    xticklabels=False,
    yticklabels=False,
)

plt.show()

# save as pdf
plt.savefig("test_output/colorbar.pdf")

# %%
