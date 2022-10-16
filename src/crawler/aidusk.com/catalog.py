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
    div = html.select('div[class="book_con_list"]')[1]
    for item in div.select('a'):
        name = re.search(r'^(第\d+章)(.*)$', item.text)
        catalog['%s %s' % (name[1], name[2].strip())] = item.attrs['href'].replace('.html', '')
    return catalog


logger.warning('Fetch catalog of `aidusk.com`')
print(json.dumps(
    extractCatalog(httpRequest('http://www.aidusk.com/t/134659/'))
))
