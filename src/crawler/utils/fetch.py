#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from .logger import logger
from concurrent import futures
from concurrent.futures import ALL_COMPLETED
from concurrent.futures import ThreadPoolExecutor

userAgent = (  # default user agent
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
)


def httpRequest(url: str) -> bytes:  # fetch raw html content
    request = requests.get(url, timeout = 30, headers = {  # timeout -> 30s
        'user-agent': userAgent,  # with fake user-agent
        'accept-encoding': 'gzip, deflate',  # allow content compress
    })
    if request.status_code not in range(200, 300):  # http status code 2xx
        raise RuntimeError('Http request failed')
    return request.content


def htmlSave(url: str, file: str) -> bool:  # save html content
    logger.debug('Html fetch `%s` -> `%s`' % (url, file))
    try:
        content = httpRequest(url)  # http request
    except:
        logger.debug('Html fetch retry -> `%s`' % url)
        try:
            content = httpRequest(url)  # retry
        except:
            logger.debug('Html fetch failed -> `%s`' % url)
            return False  # request failed
    logger.debug('Html fetch success -> `%s`' % url)
    try:
        with open(file, 'wb') as fileObj:  # save html content
            fileObj.write(content)
    except:
        logger.debug('Html save failed -> `%s`' % file)
        return False  # save failed
    logger.debug('Html save success -> `%s`' % file)
    return True


def pageFetch(info: dict, delay: float):  # fetch html content into file
    logger.debug('Page fetch: `%s` -> `%s`' % (info['url'], info['file']))
    if htmlSave(info['url'], info['file']):  # save html content
        logger.info('Page fetch success -> `%s`' % info['url'])
    else:
        logger.error('Page fetch failed -> `%s`' % info['url'])
    time.sleep(delay)


def htmlFetch(page, thread: int = 1, delay: float = 0):
    logger.info('Start html fetch process (thread = %d, delay = %f)' % (thread, delay))
    threadPool = ThreadPoolExecutor(max_workers = thread)
    threads = []
    while True:
        try:
            threads.append(threadPool.submit(pageFetch, next(page), delay))
        except StopIteration:
            break
    futures.wait(threads, return_when = ALL_COMPLETED)
    logger.info('Html fetch complete')
