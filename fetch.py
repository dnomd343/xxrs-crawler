#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import requests
from logger import logger

userAgent = (  # default user-agent
    'Mozilla/5.0 (Linux; Android 10; moto g(7) play) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/100.0.4896.79 Mobile Safari/537.36'
)


def httpRequest(url: str, fileName: str) -> bool:
    try:
        logger.debug('Http request `%s` -> %s' % (url, fileName))
        request = requests.get(url, timeout = 30,
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


catalog = json.loads(open('./catalog/catalog.json').read())

for _, pageId in catalog.items():
    for subPage in [1, 2]:
        pageUrl = 'https://m.wxsy.net/novel/57104/read_%s/%d.html' % (pageId, subPage)
        pageFile = './html/%s-%d.html' % (pageId, subPage)
        if httpRequest(pageUrl, pageFile):
            logger.info('Page request success -> %s' % pageUrl)
        else:
            logger.error('Page request failed -> %s' % pageUrl)
        time.sleep(1)
