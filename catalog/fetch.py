#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import time
import requests
from bs4 import BeautifulSoup

basicUrl = 'https://m.wxsy.net/novel/57104/all.html'

userAgent = (  # default user-agent
    'Mozilla/5.0 (Linux; Android 10; moto g(7) play) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/100.0.4896.79 Mobile Safari/537.36'
)


def httpRequest(url: str) -> str:
    request = requests.get(url, headers = {
        'user-agent': userAgent,  # with fake user-agent
        'accept-encoding': 'gzip, deflate',  # allow content compress
    })
    if request.status_code not in range(200, 300):  # http status code 2xx
        raise RuntimeError('Http request failed')
    return request.text


def analysePage(rawHtml: str) -> list:
    analyseRet = []
    soup = BeautifulSoup(rawHtml, 'lxml')
    div = soup.select('div[class="border-b"]')[0]
    for row in div.select('a[class="w100 flex-wrp flex-align-center flex-between pt10 pb10"]'):
        analyseRet.append({
            'name': row.attrs['title'],
            'url': row.attrs['href'],
        })
    return analyseRet


def fetchCatalog(pageNum: int) -> list:
    catalog = []
    for pageIndex in range(1, pageNum + 1):
        print('Page: %d' % pageIndex, file = sys.stderr)
        pageUrl = '%s?sort=1&page=%d' % (basicUrl, pageIndex)
        catalog.append(analysePage(httpRequest(pageUrl)))
        time.sleep(3)
    return catalog


print(json.dumps(fetchCatalog(18)))
