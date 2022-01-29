# %% load modules

import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

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
list(df1.columns)

scores = []

# %%

for i in range(df1.shape[0]):

    time.sleep(np.random.randint(1, 4))

    endpoint = "https://forum.psci.me/article/credible"
    params = {"url": df1.iloc[i]["Link"]}
    headers = {
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0",
        # "Accept": "application/json, text/plain, */*",
        # "Accept-Language": "en,en-US;q=0.7,en-GB;q=0.3",
        "browser_uuid": "is_credible",  # necessary!!
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "cross-site",
        # "Sec-GPC": "1",
        # "referrer": "https://www.isthiscredible.com/",
    }

    resp = requests.get(endpoint, params=params, headers=headers)
    data = resp.json()

    print(data)
    try:
        scores.append(pd.json_normalize(data).score.values[0])
    except:
        scores.append("NA")

df1["Score"] = scores

sum(df1["Score"] == "NA")
sum(df1["Score"] != "NA")


# %%

df1.to_csv("../data/clean/data_scored.csv")


# %%
