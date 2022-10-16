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
    for item in [x.select('a')[0] for x in html.select('dd')]:
        title = re.search(r'^(第\d+章)(.*)', item.text.strip())
        pageId = item.attrs['href'].replace('/book/56718/', '').replace('.html', '')
        catalog['%s %s' % (title[1], title[2].strip())] = pageId
    catalog = sorted(catalog.items(), key = lambda d: int(
        re.search(r'^第(\d+)章', d[0])[1]  # sort by chapter
    ))
    return {x[0]: x[1] for x in catalog}  # formatted output


logger.warning('Fetch catalog of `xswang.com`')
print(json.dumps(
    extractCatalog(httpRequest('https://www.xswang.com/book/56718/'))
))
