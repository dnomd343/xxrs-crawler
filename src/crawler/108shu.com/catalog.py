#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch catalog and output as JSON format.

    USAGE: python3 catalog.py
"""

import re
import sys
import json
sys.path.append('..')
from utils import logger
from utils import httpRequest
from bs4 import BeautifulSoup


def extractCatalog(rawHtml: bytes) -> dict:  # extract catalog from html content
    catalog = {}
    html = BeautifulSoup(str(rawHtml, encoding = 'utf-8'), 'lxml')
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
        logger.info('Catalog page -> %d' % pageId)
        catalog.update(extractCatalog(httpRequest(pageUrl)))
    return catalog


logger.warning('Fetch catalog of `108shu.com`')
print(json.dumps(fetchCatalog(45)))
