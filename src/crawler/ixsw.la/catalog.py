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
    html = BeautifulSoup(str(rawHtml, encoding='utf-8'), 'lxml')
    for item in html.select('dd'):
        item = item.select('a')[0]
        name = re.search(r'^(第\d+章)(.*)$', item.text)
        pageId = item.attrs['href'].replace('/ks82668/', '').replace('.html', '')
        catalog['%s %s' % (name[1], name[2].strip())] = pageId
    catalog = sorted(catalog.items(), key = lambda d: int(
        re.search(r'^第(\d+)章', d[0])[1]  # sort by chapter
    ))
    return {x[0]: x[1] for x in catalog}  # formatted output


logger.warning('Fetch catalog of `ixsw.la`')
print(json.dumps(
    extractCatalog(httpRequest('https://www.ixsw.la/ks82668/'))
))
