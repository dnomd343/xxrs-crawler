#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract data from raw html content.

    USAGE: python3 extract.py [CATALOG] [HTML_DIR]
"""

import os
import re
import sys
import json
sys.path.append('..')
from utils import logger
from bs4 import BeautifulSoup


def clearContent(raw: str) -> str:  # remove popularize
    if '\n' in raw:
        raw = re.search(r'^(.+?)\n', raw)[1]
    return raw


def splitHtml(rawHtml: str) -> dict:  # extract from raw html content
    html = BeautifulSoup(rawHtml, 'lxml')
    title = re.search(r'^(第\d+章)(.*)$', html.select('h1')[0].text)
    content = [x.text.strip() for x in html.select('p[class="content_detail"]')]
    return {
        'title': '%s %s' % (title[1], title[2].strip()),
        'content': [clearContent(x) for x in content]
    }


result = {}
logger.warning('Extract info of `xswang.com`')
catalog = json.loads(open(sys.argv[1]).read())  # load catalog
for chapterName, chapterId in catalog.items():  # traverse all chapters
    logger.info('Analyse chapter `%s`' % chapterId)
    htmlFile = os.path.join(sys.argv[2], '%s.html' % chapterId)
    info = splitHtml(open(htmlFile).read())
    if chapterName != info['title']:
        logger.error('Title error -> %s' % info['title'])
    result[chapterName] = info['content']
print(json.dumps(result))
