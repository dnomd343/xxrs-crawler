#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch catalog and output as JSON format.

    USAGE: python3 catalog.py
"""

import re
import json
import requests
from logger import logger
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
    items = html.select('div[class="section-box"]')[1]
    for item in items.select('a'):
        name = re.search(r'^(第\d+章)(.*)$', item.text)
        pageId = item.attrs['href'].replace('/book/54247/', '').replace('.html', '')
        catalog['%s %s' % (name[1], name[2].strip())] = pageId
    return catalog


def fetchCatalog(pageNum: int) -> dict:  # fetch all catalog
    catalog = {}
    for pageId in range(1, pageNum + 1):  # traverse all pages
        pageUrl = 'http://www.108shu.com/book/54247/index_%d.html' % pageId
        logger.info('Page: %d -> `%s`' % (pageId, pageUrl))
        catalog.update(extractCatalog(httpRequest(pageUrl)))
    return catalog


print(json.dumps(fetchCatalog(45)))
