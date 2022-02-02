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
df1["score"].isna().sum()

#%% create veracity column

df1["veracity"] = 0
mask = df1["Headline"].str.startswith("t")
df1.loc[mask, "veracity"] = 1

df1.groupby("veracity").agg({"mean", "count"}).reset_index()

#%%

fig, ax = plt.subplots(figsize=(8, 5))
sns.violinplot(data=df1, x="veracity", y="score", inner="points", ax=ax)
ax.set_xlabel("pre-test veracity")
fig.savefig("../figures/scores-raw_dist.png", facecolor="w", dpi=300)

#%%

df1.query("score.isna()").groupby("veracity").size()

#%% recode false headlines with na scores to 0

df1["score2"] = df1["score"]
df1.describe()
mask = df1["veracity"] == 0 & df1["score"].isna()
df1.loc[mask, "score2"] = 0
df1.describe()

# %%

df1.corr()
df1.rcorr()
df1.rcorr().to_csv("../results/corr.csv")
cols = ["veracity", "score", "score2", "Combined", "Dem", "Rep"]
df1[cols].corr()
df1[cols].rcorr()
ax = sns.pairplot(df1[cols], hue="veracity")
ax.savefig("../figures/cor.png", facecolor="w", dpi=300)

# %%
