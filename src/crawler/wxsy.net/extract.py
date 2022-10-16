#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract data from raw html content.

    USAGE: python3 extract.py [CATALOG] [HTML_DIR] [OUTPUT_DIR]
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
    script = html.select('script')[9].text  # js code with chapter info
    info = {
        'title': html.select('div[class="pt-read-title"]')[0].contents[1].contents[0].attrs['title'],
        'preId': re.search(r'window\.__PREVPAGE = "(\d*)"', script)[1],
        'nextId': re.search(r'window\.__NEXTPAGE = "(\d*)"', script)[1],
        'myId': re.search(r'window\.chapterNum = (\d+)', script)[1],
        'content': [x.text.strip() for x in html.select('p[class="content_detail"]')],
    }
    if info['title'] != re.search(r'window\.chapterName = \'(.+)\'', script)[1]:  # chapter title check
        logger.error('Title error -> %s' % info['title'])
    info['content'] = [clearContent(x) for x in info['content']]
    return info


logger.warning('Extract info of `wxsy.net`')
catalog = json.loads(open(sys.argv[1]).read())  # load catalog
for _, chapterId in catalog.items():  # traverse all chapters
    logger.info('Analyse chapter `%s`' % chapterId)
    with open(os.path.join(sys.argv[3], '%s.json' % chapterId), 'w') as fileObj:
        htmlFile = os.path.join(sys.argv[2], '%s.html' % chapterId)
        fileObj.write(json.dumps(
            splitHtml(open(htmlFile).read())
        ))
