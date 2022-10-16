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


def splitHtml(rawHtml: str) -> dict:  # extract from raw html content
    html = BeautifulSoup(rawHtml, 'lxml')
    title = re.search(r'^(第\d+章)(.*)$', html.select('h1')[0].text)
    return {
        'title': '%s %s' % (title[1], title[2].strip()),
        'content': [x.text.strip() for x in html.select('div[class="content"]')[0].select('p')]
    }


def combinePage(pageId: str) -> dict:  # combine sub pages
    page_1 = splitHtml(open(os.path.join(sys.argv[2], '%s-1.html' % pageId)).read())
    page_2 = splitHtml(open(os.path.join(sys.argv[2], '%s-2.html' % pageId)).read())
    if page_1['title'] != page_2['title']:
        logger.error('Title error -> `%s`' % page_1['title'])
    return {
        'title': page_1['title'],
        'content': page_1['content'] + page_2['content'],
    }


result = {}
logger.warning('Extract info of `108shu.com`')
catalog = json.loads(open(sys.argv[1]).read())  # load catalog
for chapterName, chapterId in catalog.items():  # traverse all chapters
    logger.info('Analyse chapter `%s`' % chapterId)
    info = combinePage(chapterId)
    if chapterName != info['title']:
        logger.error('Title error -> %s' % info['title'])
    result[chapterName] = info['content']
print(json.dumps(result))
