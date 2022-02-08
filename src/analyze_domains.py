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

df1 = pd.read_csv("../data/clean/domains_scores.csv")
df1.columns
df1["score"].isna().sum()

#%% create veracity column

df1.groupby("binary_quality").agg({"mean", "count"}).reset_index()

#%%

fig, ax = plt.subplots(figsize=(8, 5))
sns.violinplot(data=df1, x="binary_quality", y="score", inner="points", ax=ax)
ax.set_xlabel("pre-test binary_quality")
fig.savefig("../figures/domains_scores-raw_dist.png", facecolor="w", dpi=300)

#%%

df1.query("score.isna()").groupby("binary_quality").size()

# %%

df1.corr()
df1.rcorr()
df1.rcorr().to_csv("../results/domains_corr.csv")
cols = ["binary_quality", "score"]
df1[cols].corr()
df1[cols].rcorr()
ax = sns.pairplot(df1[cols], hue="binary_quality")
ax.savefig("../figures/domains_cor.png", facecolor="w", dpi=300)

# %%

df1["mean_domain_score"] = df1["score"].groupby(df1["domain"]).transform("mean")

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df1, x="score", y="mean_domain_score", hue="domain", style="binary_quality"
)
plt.xlabel("score")
plt.ylabel("mean domain sore")
# place the legend outside the figure/plot
plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
plt.title("Seaborn Plot with Legend Outside")
plt.tight_layout()
plt.savefig(
    "../figures/place_legend_outside_plot_Seaborn_scatterplot.png",
    format="png",
    dpi=300,
)

# %%
