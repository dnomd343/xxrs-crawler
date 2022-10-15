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
import requests
from logger import logger

userAgent = (  # default user agent
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
)


def httpRequest(fileUrl: str, fileName: str) -> bool:  # save html content
    try:
        logger.debug('Http request `%s` -> `%s`' % (fileUrl, fileName))
        request = requests.get(fileUrl, timeout = 30,  # timeout -> 30s
            headers = {
                'user-agent': userAgent,  # with fake user-agent
            }
        )
        if request.status_code not in range(200, 300):  # http status code 2xx
            logger.warning('Http request failed -> `%s`' % fileUrl)
            return False
        logger.debug('Http request success -> `%s`' % fileUrl)
        with open(fileName, 'w') as fileObj:  # save html content
            fileObj.write(request.text)
        logger.debug('File save success -> `%s`' % fileName)
    except:
        return False
    return True


catalog = json.loads(open(sys.argv[1]).read())  # load catalog

for _, chapterId in catalog.items():  # traverse all chapters
    pageUrl = 'https://www.wxsy.net/novel/57104/read_%s.html' % chapterId
    pageFile = os.path.join(sys.argv[2], '%s.html' % chapterId)
    if httpRequest(pageUrl, pageFile):  # save html content
        logger.info('Page request success -> %s' % pageUrl)
    else:
        logger.error('Page request failed -> %s' % pageUrl)
    time.sleep(1)  # avoid being blocked by the server
