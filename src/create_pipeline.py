# %% load modules

from dbm import dumb
from pathlib import Path
import numpy as np
import pandas as pd
import time
import utils
import urllib.request
from utils import get_score
import os
import threading

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

#%%


def main(url, paths):
    # TODO change proxy (don't push id publicly!)

    tid = threading.get_ident()
    print(f"\n\npid: {os.getpid()} - {url} - thread id {tid}")

    dfpath = paths["outputdir"]
    dfpath.mkdir(parents=True, exist_ok=True)

    # TODO get_score()

    # TODO save data
    scores = [{"col3": [url], "col2": {"abc": url, "cde": url}}]
    dat = {"url": [url], "score": [np.nan], "response": scores}
    df = pd.DataFrame(dat)

    fname = dfpath.joinpath(f"{tid}.csv")
    if not fname.exists():
        df.to_csv(fname, index=False)
    else:
        df.to_csv(fname, header=False, index=False, mode="a")

    return df


# main(10, PATHS)

#%%

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
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
