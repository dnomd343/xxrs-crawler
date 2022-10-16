#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download raw html content as `.html` files.

    USAGE: python3 fetch.py [CATALOG] [OUTPUT_DIR] [PROXY] [THREAD] [DELAY]
"""

import os
import sys
import json
sys.path.append('..')
from utils import logger
from utils import htmlFetch


def loadChapter():
    catalog = json.loads(open(sys.argv[1]).read())  # load catalog
    for _, chapterId in catalog.items():  # traverse all chapters
        for subPage in [1, 2]:  # two sub pages in one chapter
            yield {
                'url': 'https://m.wxsy.net/novel/57104/read_%s/%d.html' % (chapterId, subPage),
                'file': os.path.join(sys.argv[2], '%s-%d.html' % (chapterId, subPage)),
            }


logger.warning('Fetch html of `m.wxsy.net`')
htmlFetch(
    loadChapter(),
    proxy = sys.argv[3],
    thread = int(sys.argv[4]),
    delay = float(sys.argv[5]),
)
