#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download raw html content as `.html` files.

    USAGE: python3 fetch.py [CATALOG] [OUTPUT_DIR]
"""

import os
import sys
import json
import time
sys.path.append('..')
from utils import logger
from utils import htmlFetch
from concurrent.futures import ThreadPoolExecutor


def pageFetch(info: dict, delay: float):
    logger.debug('Page fetch: `%s` -> `%s`' % (info['url'], info['file']))
    if htmlFetch(info['url'], info['file']):  # save html content
        logger.info('Page fetch success -> `%s`' % info['url'])
    else:
        logger.error('Page fetch failed -> `%s`' % info['url'])
    time.sleep(delay)


pages = []
catalog = json.loads(open(sys.argv[1]).read())  # load catalog
for _, chapterId in catalog.items():  # traverse all chapters
    pages.append({
        'url': 'https://www.wxsy.net/novel/57104/read_%s.html' % chapterId,
        'file': os.path.join(sys.argv[2], '%s.html' % chapterId),
    })


with ThreadPoolExecutor(max_workers = 2) as pool:
    for page in pages:
        pool.submit(pageFetch, page, 5)
