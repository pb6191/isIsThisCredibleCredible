# %% load modules

import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import requests
import seaborn as sns

pd.set_option(
    "display.max_rows",
    8,
    "display.max_columns",
    None,
    "display.width",
    None,
    "display.expand_frame_repr",
    True,
    "display.max_colwidth",
    None,
)

np.set_printoptions(
    edgeitems=5,
    linewidth=233,
    precision=4,
    sign=" ",
    suppress=True,
    threshold=50,
    formatter=None,
)

#%%

df1 = pd.read_csv("../data/clean/data_scored.csv")
list(df1.columns)

# %%

df2 = df1.dropna()

# %%

dt = df2[["Dem", "Rep", "Combined", "Score"]].copy()

dt.corr()


sns.pairplot(dt)

# %%
