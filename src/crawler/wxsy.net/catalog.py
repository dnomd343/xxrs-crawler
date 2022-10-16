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
    div = html.select('div[class="pt-chapter-cont-detail full"]')[0]
    for item in div.select('a'):
        catalog[item.attrs['title']] = re.search(r'/novel/57104/read_(\d+).html', item.attrs['href'])[1]
    catalog = sorted(catalog.items(), key = lambda d: int(
        re.search(r'^第(\d+)章', d[0])[1]  # sort by chapter
    ))
    return {x[0]: x[1] for x in catalog}  # formatted output


logger.warning('Fetch catalog of `wxsy.net`')
print(json.dumps(
    extractCatalog(httpRequest('https://www.wxsy.net/novel/57104/'))
))
