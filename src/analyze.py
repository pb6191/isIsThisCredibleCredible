# %% load modules

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
df1.columns

# %%

df1["veracity"] = 0
mask = df1["Headline"].str.startswith("t")
df1.loc[mask, "veracity"] = 1

mask = df1["veracity"] == 0 & df1["Score"].isna()
df1.loc[mask, "Score"] = 0

# %%

dt = df1[["Dem", "Rep", "Combined", "Score", "veracity"]].copy()
dt.corr()
ax = sns.pairplot(dt, hue="veracity")
ax.savefig("../figures/cor.png", facecolor="w")

# %%
