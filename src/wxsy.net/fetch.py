#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download raw html content as `.html` files.

    USAGE: python3 fetch.py [CATALOG] [OUTPUT_DIR]
"""

import sys
import json
import time
import requests
from logger import logger

basicUrl = 'https://m.wxsy.net/novel/57104'

userAgent = (  # default user-agent
    'Mozilla/5.0 (Linux; Android 10; moto g(7) play) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/100.0.4896.79 Mobile Safari/537.36'
)


def httpRequest(url: str, fileName: str) -> bool:  # save html content
    try:
        logger.debug('Http request `%s` -> %s' % (url, fileName))
        request = requests.get(url, timeout = 30,  # timeout -> 30s
            headers = {
                'user-agent': userAgent,  # with fake user-agent
            }
        )
        if request.status_code not in range(200, 300):  # http status code 2xx
            logger.warning('Http request failed -> %s' % url)
            return False
        logger.debug('Http request success -> %s' % url)
        with open(fileName, 'w') as fileObj:  # save html content
            fileObj.write(request.text)
        logger.debug('File save success -> %s' % fileName)
    except:
        return False
    return True


catalog = json.loads(open(sys.argv[1]).read())  # load catalog

for _, chapterId in catalog.items():  # traverse all chapters
    for subPage in [1, 2]:  # two sub pages in one chapter
        pageUrl = '%s/read_%s/%d.html' % (basicUrl, chapterId, subPage)
        pageFile = '%s/%s-%d.html' % (sys.argv[2], chapterId, subPage)
        if httpRequest(pageUrl, pageFile):  # save html content
            logger.info('Page request success -> %s' % pageUrl)
        else:
            logger.error('Page request failed -> %s' % pageUrl)
        time.sleep(1)  # avoid being blocked by the server
