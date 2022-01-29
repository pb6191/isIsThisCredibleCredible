# %% load modules

import time
import numpy as np
import pandas as pd
import requests
import urllib.parse

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

df1 = pd.read_csv("../data/clean/data_cleaned.csv")
df1.columns

# %%

endpoint = "https://forum.psci.me/article/credible"
scores = []

for r in df1.itertuples():
    print(r)
    time.sleep(np.random.randint(1, 4))
    params = {"url": urllib.parse.quote(r.Link)}
    headers = {"browser_uuid": "is_credible"}
    resp = requests.get(endpoint, params=params, headers=headers)

    if resp:
        data = resp.json()
        data["i"] = r.index
        data["url"] = r.Link
        scores.append(pd.json_normalize(data))
    else:
        scores.append([])

# %% save scores

df_scores = pd.concat(scores)
# replace . in column names with _
df_scores.columns = [c.replace(".", "_") for c in df_scores.columns]
df_scores = df_scores.query("score.notna()")
df_scores.to_csv("../data/clean/scores.csv", index=False)

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
