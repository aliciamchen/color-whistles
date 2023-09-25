# %%
import numpy as np
import pandas as pd
from tools import viz
import matplotlib.pyplot as plt

# %%

df = pd.read_csv("test_output/comm_signals.zip")

# %%
speaker, referent = "610068e5f60debf1dafc444d", 10

viz.plot_sound(df[df['speaker'] == speaker], referent_id=referent)
plt.savefig(f"test_output/signal_{speaker}_{referent}.pdf")
plt.show()

# %%

speaker, referent = "61001bf99a534440d8563358", 10

viz.plot_sound(df[df['speaker'] == speaker], referent_id=referent)
plt.savefig(f"test_output/signal_{speaker}_{referent}.pdf")
plt.show()
# %%

speaker, referent = "61118a566bf579b7d69aa202", 8

viz.plot_sound(df[df['speaker'] == speaker], referent_id=referent)
plt.savefig(f"test_output/signal_{speaker}_{referent}.pdf")
plt.show()
# %%

speaker, referent = "60fcfce988af0e9f331ec84a", 7

viz.plot_sound(df[df['speaker'] == speaker], referent_id=referent)
plt.savefig(f"test_output/signal_{speaker}_{referent}.pdf")
plt.show()
# %%

speaker, referent = "6053ce04a276ce713b3e7c1a", 8

viz.plot_sound(df[df['speaker'] == speaker], referent_id=referent)
plt.savefig(f"test_output/signal_{speaker}_{referent}.pdf")
plt.show()
# %%
