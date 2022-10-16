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
from logger import logger
from bs4 import BeautifulSoup


def splitHtml(rawHtml: str) -> dict:  # extract from raw html content
    html = BeautifulSoup(rawHtml, 'lxml')
    title = re.search(r'^(第\d+章)(.*)$', html.select('h1')[0].text)
    div = html.select('div[class="book_content"]')[0].prettify().split('\n', 1)[1]
    content = [x.strip() for x in div.split('\n <br/>\n <br/>')]
    content.pop(-1)  # remove last item
    return {
        'title': '%s %s' % (title[1], title[2].strip()),
        'content': content
    }


result = {}
catalog = json.loads(open(sys.argv[1]).read())  # load catalog

for chapterName, chapterId in catalog.items():  # traverse all chapters
    logger.info('Analyse chapter `%s`' % chapterId)
    htmlFile = os.path.join(sys.argv[2], '%s.html' % chapterId)
    info = splitHtml(open(htmlFile).read())
    if chapterName != info['title']:
        logger.error('Title error -> %s' % info['title'])
    result[chapterName] = info['content']

print(json.dumps(result))