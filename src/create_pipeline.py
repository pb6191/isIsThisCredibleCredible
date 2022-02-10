# %% load modules

import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
import requests

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

PATHS = {"outputdir": Path("..") / "data" / "clean" / "credible_scores"}

#%% load stuff

# TODO move all this into main later (below)

df1 = pd.read_csv("../data/clean/data_domains_cleaned.csv")
df1.columns

file = open("proxy_key.txt")
for line in file:
    PROXY_KEY = line.strip()

resp = requests.get(
    "https://proxy.webshare.io/api/proxy/list/",
    headers={"Authorization": PROXY_KEY},
)
proxies = resp.json()["results"]

#%%


def main(url, paths):
    tid = threading.get_ident()
    print(f"\n\npid: {os.getpid()} - {url} - thread id {tid}")

    # TODO: save list of urls checked and skip if already checked (in case we have to restart the processes)

    # change proxy
    k = np.random.randint(0, len(proxies) - 1)
    p = proxies[k]
    print(f"{k}, {p['proxy_address']}")
    proxy_dict = {"http": f'http://{p["proxy_address"]}:{p["ports"]["http"]}'}

    # get score
    resp, data = utils.get_score(url, proxy_dict)  # data is dictionary
    dat = {
        "url": [url],
        "story_id": [np.nan],
        "score": [np.nan],
        "response": [np.nan],
    }
    if resp:
        try:
            dat["score"] = data["score"]
            dat["story_id"] = data["story_id"]
            dat["response"] = [data]
        except:
            pass

    # save
    dfpath = paths["outputdir"]
    dfpath.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(dat)
    fname = dfpath.joinpath(f"{tid}.csv")
    if not fname.exists():
        df.to_csv(fname, index=False)
    else:
        df.to_csv(fname, header=False, index=False, mode="a")

    return df


#%%

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(main, r.Link, PATHS): r.Link for r in df1.itertuples()
        }
        for f in as_completed(futures):
            url = futures[f]
            output = f.result()
            print(output)

#%%
