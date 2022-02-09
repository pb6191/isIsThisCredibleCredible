#%%

import requests
import urllib.parse

#%%


def get_score(url):
    endpoint = "https://forum.psci.me/article/credible"
    params = {"url": urllib.parse.quote(url)}
    headers = {"browser_uuid": "is_credible"}

    url = url.strip()
    if url.endswith("/"):
        url = url[:-1]

    data = {"url": url, "i": 0}
    resp = requests.get(endpoint, params=params, headers=headers)
    if resp:
        data = resp.json()
        data["url"] = url
    return resp, data
