#%%

import requests
import urllib.parse

#%%


def get_score(url):
    endpoint = "https://forum.psci.me/article/credible"
    params = {"url": urllib.parse.quote(url)}
    headers = {"browser_uuid": "is_credible"}
    data = {"key": "value", "i": 0, "url": "none"}
    resp = requests.get(endpoint, params=params, headers=headers)
    if resp:
        data = resp.json()
        data["url"] = url
    return resp, data
