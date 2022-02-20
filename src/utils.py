#%%

import urllib.parse

import requests

#%%


def get_credible_score(url, proxy=None):
    endpoint = "https://forum.psci.me/article/credible"
    params = {"url": urllib.parse.quote(url)}
    headers = {"browser_uuid": "is_credible"}

    url = url.strip()
    if url.endswith("/"):
        url = url[:-1]

    data = {"url": url, "i": 0}
    if proxy is None:
        resp = requests.get(endpoint, params=params, headers=headers)
    else:
        resp = requests.get(endpoint, params=params, headers=headers, proxies=proxy)
    if resp:
        data = resp.json()
        data["url"] = url
    return resp, data
