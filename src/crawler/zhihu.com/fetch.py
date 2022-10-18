#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download raw JSON content.

    USAGE: python3 fetch.py [OUTPUT_JSON]
"""

import sys
sys.path.append('..')
from utils import logger
from utils import httpRequest

logger.warning('Fetch json of `zhihu.com`')
jsonRaw = httpRequest('https://www.zhihu.com/api/v4/columns/c_1553471910075449344/items?limit=%d&offset=0' % 23)
with open(sys.argv[1], 'wb') as fileObj:
    fileObj.write(jsonRaw)
