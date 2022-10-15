#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch catalog and output as JSON format.

    USAGE: python3 catalog.py
"""

import re
import json
import requests
from bs4 import BeautifulSoup

userAgent = (  # default user agent
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
)


def httpRequest(url: str) -> str:  # fetch raw html content
    request = requests.get(url, headers = {
        'user-agent': userAgent,  # with fake user-agent
        'accept-encoding': 'gzip, deflate',  # allow content compress
    })
    if request.status_code not in range(200, 300):  # http status code 2xx
        raise RuntimeError('Http request failed')
    return request.text


def extractCatalog(rawHtml: str) -> dict:  # extract catalog from html content
    catalog = {}
    html = BeautifulSoup(rawHtml, 'lxml')
    for item in [x.select('a')[0] for x in html.select('dd')]:
        pageId = item.attrs['href'].replace('/book/56718/', '').replace('.html', '')
        catalog[item.text.strip()] = pageId
    catalog = sorted(catalog.items(), key = lambda d: int(
        re.search(r'^第(\d+)章', d[0])[1]  # sort by chapter
    ))
    return {x[0]: x[1] for x in catalog}  # formatted output


print(json.dumps(
    extractCatalog(httpRequest('https://www.xswang.com/book/56718/'))
))
