# %% load modules

import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import urlexpander

import creds
import utils

PS = {
    "outputdir": Path("..") / "data" / "clean" / "credible_scores",
    "domains": Path("../data/clean/data_domains_cleaned.csv"),
}
PM = {"pause_s": 0, "workers": 3, "debug": False}

#%%


def main(url, paths, pause_s=0):
    tid = threading.get_ident()
    print(f"\npid: {os.getpid()} - {url} - thread id {tid}")

    # change proxy
    k = np.random.randint(0, len(proxies) - 1)
    p = proxies[k]
    print(f"{k}, {p['proxy_address']}")
    proxy_dict = {"http": f'http://{p["proxy_address"]}:{p["ports"]["http"]}'}

    # get score
    url = url.lower().strip()
    resp, data = utils.get_credible_score(url, proxy_dict)  # output data is dictionary
    domain = urlexpander.get_domain(url)
    if resp:
        dat = {
            "url": [url],
            "domain": [domain],
            "bias": [data.get("site_meta").get("bias")],
            "cred": [data.get("site_meta").get("cred")],
            "score": [data.get("score")],
            "quality": [data.get("quality")],
            "story_id": [data.get("story_id")],
            "response": [data],
        }
        if "error" in dat["quality"][0]:
            qual = dat["quality"][0]["error"].split(": ")
            qual = qual[1] if len(qual) > 1 else qual[0]
            dat["quality"] = [qual]
        else:
            dat["quality"] = ["see score"]
    else:
        print(f"error: {url}")
        dat = {
            "url": [url],
            "domain": [domain],
            "bias": [np.nan],
            "cred": [np.nan],
            "score": [np.nan],
            "quality": ["error_no_response"],
            "story_id": [np.nan],
            "response": [np.nan],
        }

    # save
    dfpath = paths["outputdir"]
    dfpath.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(dat)
    fname = dfpath.joinpath(f"{tid}.csv")
    if not fname.exists():
        df.to_csv(fname, index=False)
    else:
        df.to_csv(fname, header=False, index=False, mode="a")

    if pause_s > 3:
        time.sleep(pause_s)

    return df


#%%

if __name__ == "__main__":
    #%% load stuff

    df1 = pd.read_csv(PS["domains"])
    if PM["debug"]:
        df1 = df1.iloc[:10]
    df1 = df1.drop_duplicates()

    resp = requests.get(
        "https://proxy.webshare.io/api/proxy/list/",
        headers={"Authorization": creds.proxy_key},
    )
    proxies = resp.json()["results"]

    #%% remove already-checked urls

    to_checked = set(df1["url"])
    if list(PS["outputdir"].glob("*.csv")):  # if yes csv files
        checked = set(
            pd.concat(
                [
                    pd.read_csv(f, usecols=["url"], dtype={"url": "string"})
                    for f in PS["outputdir"].glob("*.csv")
                ]
            )["url"]
        )
        to_checked = to_checked.difference(checked)
    print(f"{len(to_checked)} urls to check")

    with ThreadPoolExecutor(max_workers=PM["workers"]) as executor:
        print(f"urls to check: {len(to_checked)}")
        futures = {
            executor.submit(main, url, PS, PM["pause_s"]): url for url in to_checked
        }
        for i, f in enumerate(as_completed(futures)):
            url = futures[f]
            output = f.result()
            # print(output)
            print(f"processed {i + 1} of {len(to_checked)}\n\n")

#%%
