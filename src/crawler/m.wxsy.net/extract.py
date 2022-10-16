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


def splitHtml(rawHtml: str) -> dict:  # extract from raw html content
    body = BeautifulSoup(rawHtml, 'lxml').body
    script = body.select('script')[5].text  # js code with chapter info
    info = {
        'title': body.select('div[class="size18 w100 text-center lh100 pt30 pb15"]')[0].text.strip(),
        'content': [x.text.strip() for x in body.select('p[class="content_detail"]')],
        'prePage': body.select('div[class="pt-prechapter"]')[0].a.attrs['href'],
        'nextPage': body.select('div[class="pt-nextchapter"]')[0].a.attrs['href'],
        'preId': re.search(r'window\.__PREVPAGE = "(\d*)"', script)[1],
        'nextId': re.search(r'window\.__NEXTPAGE = "(\d*)"', script)[1],
        'myId': re.search(r'window\.chapterNum = (\d+)', script)[1],
        'caption': re.search(r'window\.chapterName = \'(.+)\'', script)[1],
    }
    if not info['title'].startswith(info['caption']):  # chapter title should start with caption
        logger.error('Title error -> %s' % info['caption'])
    info['index'] = info['title'].replace(info['caption'], '')  # remove caption string
    info.pop('title')
    return info


def combinePage(id: str) -> dict:  # combine sub pages
    page_1 = splitHtml(open(os.path.join(sys.argv[2], '%s-1.html' % id)).read())
    page_2 = splitHtml(open(os.path.join(sys.argv[2], '%s-2.html' % id)).read())

    # page info check
    if not page_1['index'] == '[1/2页]' or not page_2['index'] == '[2/2页]':
        logger.error('Sub page error -> `%s` <-> `%s`' % (page_1['index'], page_2['index']))
    if not page_1['caption'] == page_2['caption']:
        logger.error('Caption error -> `%s` <-> `%s`' % (page_1['caption'], page_2['caption']))
    if not page_1['myId'] == page_2['myId']:
        logger.error('Page ID error -> `%s` <-> `%s`' % (page_1['myId'], page_2['myId']))
    if not page_1['preId'] == page_2['preId']:
        logger.error('Pre page ID error -> `%s` <-> `%s`' % (page_1['preId'], page_2['preId']))
    if not page_1['nextId'] == page_2['nextId']:
        logger.error('Next page ID error -> `%s` <-> `%s`' % (page_1['nextId'], page_2['nextId']))

    # check by pre-page and next-page url
    if not page_1['prePage'] == '/novel/57104/read_%s.html' % page_1['preId']:
        logger.warning('Page-1 pre url -> `%s` (ID = %s)' % (page_1['prePage'], id))
    if not page_1['nextPage'] == '/novel/57104/read_%s/2.html' % page_1['myId']:
        logger.warning('Page-1 next url -> `%s` (ID = %s)' % (page_1['nextPage'], id))
    if not page_2['prePage'] == '/novel/57104/read_%s.html' % page_2['myId']:
        logger.warning('Page-2 pre url -> `%s` (ID = %s)' % (page_2['prePage'], id))
    if not page_2['nextPage'] == '/novel/57104/read_%s.html' % page_2['nextId']:
        logger.warning('Page-2 next url -> `%s` (ID = %s)' % (page_2['nextPage'], id))
    # there are empty links in the first and last page (ignore it)

    return {  # release chapter
        'title': page_1['caption'],
        'preId': page_1['preId'],
        'myId': page_1['myId'],
        'nextId': page_1['nextId'],
        'content': page_1['content'] + page_2['content']
    }


logger.warning('Extract info of `m.wxsy.net`')
catalog = json.loads(open(sys.argv[1]).read())  # load catalog
for _, chapterId in catalog.items():  # traverse all chapters
    logger.info('Analyse chapter `%s`' % chapterId)
    with open(os.path.join(sys.argv[3], '%s.json' % chapterId), 'w') as fileObj:
        fileObj.write(json.dumps(combinePage(chapterId)))
