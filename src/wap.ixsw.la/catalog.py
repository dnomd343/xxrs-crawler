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
    return str(request.content, encoding = 'utf-8')


def extractCatalog(rawHtml: str) -> dict:  # extract catalog from html content
    catalog = {}
    html = BeautifulSoup(rawHtml, 'lxml')
    div = html.select('div[class="directoryArea"]')[0]
    for item in div.select('a[style=""]'):
        name = re.search(r'^(第\d+章)(.*)$', item.text)
        pageId = item.attrs['href'].replace('/ks82668/', '').replace('.html', '')
        catalog['%s %s' % (name[1], name[2].strip())] = pageId
    return catalog


print(json.dumps(
    extractCatalog(httpRequest('https://wap.ixsw.la/ks82668/all.html'))
))
