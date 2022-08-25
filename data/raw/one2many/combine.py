# Combine data from the two days

# %%
import numpy as np
import pandas as pd

df_comm_1 = pd.read_csv("2022-01-25/communication_game_data.zip")
df_learn_1 = pd.read_csv("2022-01-25/learning_data.zip")

df_comm_2 = pd.read_csv("2022-01-26/communication_game_data.zip")
df_learn_2 = pd.read_csv("2022-01-26/learning_data.zip")

# %%

df_comm = pd.concat([df_comm_1, df_comm_2], ignore_index=True)
df_learn = pd.concat([df_learn_1, df_learn_2], ignore_index=True)

# %%

df_comm.to_csv("communication_game_data.zip", index=False)
df_learn.to_csv("learning_data.zip", index=False)

# %%
