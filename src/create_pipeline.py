# %% load modules

import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
import requests

import utils

PATHS = {"outputdir": Path("..") / "data" / "clean" / "credible_scores"}
PARAMS = {"pause_s": 0}

#%%


def main(url, paths, pause_s=0):
    tid = threading.get_ident()
    print(f"\n\npid: {os.getpid()} - {url} - thread id {tid}")

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
            dat["score"] = [data["score"]]
            dat["story_id"] = [data["story_id"]]
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

    if pause_s > 0:
        time.sleep(pause_s)

    return df


#%%

if __name__ == "__main__":
    #%% load stuff

    df1 = pd.read_csv("../data/clean/data_domains_cleaned.csv")
    df1 = df1.drop_duplicates()

    file = open("proxy_key.txt")
    for line in file:
        PROXY_KEY = line.strip()

    resp = requests.get(
        "https://proxy.webshare.io/api/proxy/list/",
        headers={"Authorization": PROXY_KEY},
    )
    proxies = resp.json()["results"]

    #%% remove already-checked urls

    to_checked = set(df1["Link"])
    if list(PATHS["outputdir"].glob("*.csv")):  # if yes csv files
        checked = set(
            pd.concat(
                [
                    pd.read_csv(f, usecols=["url"], dtype={"url": "string"})
                    for f in PATHS["outputdir"].glob("*.csv")
                ]
            )["url"]
        )
        to_checked = to_checked.difference(checked)

    with ThreadPoolExecutor(max_workers=2) as executor:
        print(f"urls to check: {len(to_checked)}")
        futures = {
            executor.submit(main, url, PATHS, PARAMS["pause_s"]): url
            for url in to_checked
        }
        for f in as_completed(futures):
            url = futures[f]
            output = f.result()
            print(output)

#%%
