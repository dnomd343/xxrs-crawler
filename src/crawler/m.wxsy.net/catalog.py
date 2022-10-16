#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch catalog and output as JSON format.

    USAGE: python3 catalog.py
"""

import sys
sys.path.append('..')

import re
import json
import time
import requests
from logger import logger
from bs4 import BeautifulSoup

basicUrl = 'https://m.wxsy.net/novel/57104/all.html'

userAgent = (  # default user-agent
    'Mozilla/5.0 (Linux; Android 10; moto g(7) play) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/100.0.4896.79 Mobile Safari/537.36'
)


def httpRequest(url: str) -> str:  # fetch raw html content
    request = requests.get(url, headers = {
        'user-agent': userAgent,  # with fake user-agent
        'accept-encoding': 'gzip, deflate',  # allow content compress
    })
    if request.status_code not in range(200, 300):  # http status code 2xx
        raise RuntimeError('Http request failed')
    return request.text


def analysePage(rawHtml: str) -> list:  # extract catalog from html content
    analyseRet = []
    soup = BeautifulSoup(rawHtml, 'lxml')
    div = soup.select('div[class="border-b"]')[0]
    for row in div.select('a[class="w100 flex-wrp flex-align-center flex-between pt10 pb10"]'):
        analyseRet.append({
            'name': row.attrs['title'],
            'url': row.attrs['href'],
        })
    return analyseRet


def fetchCatalog(pageNum: int) -> list:  # fetch raw catalog
    catalog = []
    for pageIndex in range(1, pageNum + 1):  # traverse all pages (1 ~ pageNum)
        logger.info('Page: %d' % pageIndex)
        pageUrl = '%s?sort=1&page=%d' % (basicUrl, pageIndex)
        catalog.append(analysePage(httpRequest(pageUrl)))
        time.sleep(1)  # avoid being blocked by the server
    return catalog


def formatCatalog(rawCatalog: list) -> dict:
    catalog = {}
    for catalogPage in rawCatalog:  # traverse pages
        for catalogItem in catalogPage:  # traverse catalog items
            pageId = re.search(r'^/novel/57104/read_(\d+)\.html$', catalogItem['url'])[1]
            catalog[catalogItem['name']] = pageId  # save page id
    catalog = sorted(catalog.items(), key = lambda d: int(
        re.search(r'^第(\d+)章', d[0])[1]  # sort by chapter
    ))
    return {x[0]: x[1] for x in catalog}  # formatted output


release = formatCatalog(fetchCatalog(18))  # 18 pages in total
print(json.dumps(release))  # output as JSON format
