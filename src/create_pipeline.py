# %% load modules

from dbm import dumb
from pathlib import Path
from idna import ulabel
import numpy as np
import pandas as pd
import time
import utils
import urllib.request
from utils import get_score
import os
import requests
import random
import threading
import csv

from concurrent.futures import ThreadPoolExecutor, as_completed

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

#%% read domains

df1 = pd.read_csv("../data/clean/data_domains_cleaned.csv")
df1.columns

#%% get proxy key

file = open("proxy_key.txt")
for line in file:
    PROXY_KEY = line


#%%
resp = requests.get(
    "https://proxy.webshare.io/api/proxy/list/",
    headers={"Authorization": PROXY_KEY},
)
proxies = resp.json()["results"]


#%%


def write_csv(header, data, path, mode):
    with open(path, mode, encoding="utf-8") as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow(header)
        writer.writerows(data)


#%%


def main(url, paths):
    k = random.randint(0, len(proxies) - 1)
    p = proxies[k]
    print(f"{k}, {p['proxy_address']}")
    # prox = f"http://{p['username']}:{p['password']}@{p['proxy_address']}:{p['ports']['http']}"
    proxyDict = {"http": "http://" + p["proxy_address"] + ":" + str(p["ports"]["http"])}
    resp, data = utils.get_score(url, proxyDict)
    tid = threading.get_ident()
    print(f"\n\npid: {os.getpid()} - {url} - thread id {tid}")

    dfpath = paths["outputdir"]
    dfpath.mkdir(parents=True, exist_ok=True)

    if resp:
        dat = {"url": [url], "score": [np.nan], "response": [(data)]}
    else:
        dat = {"url": [url], "score": [np.nan], "response": [np.nan]}

    try:
        dat["score"] = data["score"]
    except:
        dat["score"] = [np.nan]

    df = pd.DataFrame(dat)

    fname = dfpath.joinpath(f"{tid}.csv")
    # if not fname.exists():
    #    mode = "w"
    # else:
    #    mode = "a"
    # write_csv(
    #    header=["url", "score", "response"],
    #    data=zip([dat["url"]], [dat["score"]], [dat["response"]]),
    #    path=fname,
    #    mode=mode,
    # )

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
            # print(f)
            # print(i)
            # print(url)
            # print(output)

#%%


#%%
