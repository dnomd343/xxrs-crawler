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


def loadChapter():
    catalog = json.loads(open(sys.argv[1]).read())  # load catalog
    for _, chapterId in catalog.items():  # traverse all chapters
        yield {
            'url': 'https://www.wxsy.net/novel/57104/read_%s.html' % chapterId,
            'file': os.path.join(sys.argv[2], '%s.html' % chapterId),
        }


htmlFetch(loadChapter(), 2)
