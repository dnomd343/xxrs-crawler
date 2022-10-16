#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch catalog and output as JSON format.

    USAGE: python3 catalog.py [PROXY]
"""

import re
import sys
import json
sys.path.append('..')
from utils import logger
from utils import httpRequest
from bs4 import BeautifulSoup


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
        logger.info('Catalog page -> %d' % pageIndex)
        catalog.append(analysePage(
            httpRequest(
                'https://m.wxsy.net/novel/57104/all.html?sort=1&page=%d' % pageIndex,
                proxy = sys.argv[1]
            )
        ))
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


logger.warning('Fetch catalog of `m.wxsy.net`')
release = formatCatalog(fetchCatalog(18))  # 18 pages in total
print(json.dumps(release))  # output as JSON format
