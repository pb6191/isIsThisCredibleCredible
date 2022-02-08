# %% load modules

from pathlib import Path
import numpy as np
import pandas as pd
import time
import utils

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

#%% read domains

df1 = pd.read_csv("../data/clean/data_domains_cleaned.csv")
df1.columns


# %%

scores = []
for r in df1.itertuples():
    print(r)
    time.sleep(np.random.randint(1, 4))
    resp, data = utils.get_score(r.Link)
    if resp:
        data["i"] = r.index
        scores.append(pd.json_normalize(data))
    else:
        scores.append([])

# %% save scores


elements_to_delete = []
for i in range(len(scores)):
    try:
        print(i)
        scores[i].shape
    except:
        elements_to_delete.append(i)

for index in sorted(elements_to_delete, reverse=True):
    del scores[index]

df_scores = pd.concat(scores)
# replace . in column names with _
df_scores.columns = [c.replace(".", "_") for c in df_scores.columns]
df_scores = df_scores.query("score.notna()")
df_scores.to_csv("../data/clean/domains_scores.csv", index=False)

#%% score data

df_scores.columns

cols = [
    "url",
    "score",
    "quality_quality_sources_score",
    "quality_self_promotion_score",
    "quality_diversity_sources_score",
    "quality_quotes_score",
    "quality_quotes_score",
    "quality_source_credibility_score",
    "quality_author_history_score",
    "quality_opinion_score",
]

df_scores2 = df_scores[cols]
df_scored = pd.merge(df1, df_scores2, how="left", left_on="Link", right_on="url")

#%%

df_scored.to_csv("../data/clean/data_scored.csv", index=False)

# %%
