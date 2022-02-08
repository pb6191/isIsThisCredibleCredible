# %% load modules

from pathlib import Path
import numpy as np
import pandas as pd
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

#%%

resp, data = utils.get_score(
    "https://www.newsmax.com/newsfront/arkansas-governor-asa-hutchinson-cdc/2022/01/31/id/1054853/"
)
