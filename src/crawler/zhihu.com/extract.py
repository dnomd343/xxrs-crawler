#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract data from raw json content.

    USAGE: python3 extract.py [JSON_FILE]
"""

import re
import sys
import json
sys.path.append('..')
from utils import logger
from bs4 import BeautifulSoup


def loadData() -> list:
    rawData = json.loads(open(sys.argv[1]).read())
    data = [{
        'id': x['id'],
        'title': x['title'],
        'content': x['content'],
    } for x in rawData['data']]

    def sortFunc(x: dict) -> int:
        suffix = x['title'].replace('栩栩若生', '')
        suffix = '1' if suffix == '' else suffix  # `栩栩若生` -> `栩栩若生1`
        suffix = '22' if suffix == '（全文完）' else suffix  # `栩栩若生（全文完）` -> `栩栩若生22`
        return int(suffix)
    return sorted(data, key = sortFunc)


def splitHtml(rawHtml: str) -> list:
    html = BeautifulSoup(rawHtml, 'lxml')

    def isCaption(obj: BeautifulSoup) -> bool:
        if obj.name in ['h2', 'h3']:
            if obj.text not in [
                '人生第一次如此无语。',
                '第三棒是伍哥。',
                '东风初送第一船。',
            ]: return True
        if obj.text == "正文第870章对手":
            return True
        return False

    def formatCaption(raw: str) -> str:
        if raw.startswith('正文'):
            raw = raw.replace('正文', '')
        match = re.search(r'^第(\d+)章(.*)', raw)
        if match is not None:
            return '第%s章 %s' % (match[1], match[2].strip())
        match = re.search(r'^第(\S+)章 (.*)', raw)
        zhStr = match[1]
        zhStr = '三十零' if zhStr == '三十' else zhStr
        zhStr = '二十零' if zhStr == '二十' else zhStr
        zhStr = '十零' if zhStr == '十' else zhStr
        zhStr = zhStr.replace('三十', '3').replace('二十', '2').replace('十', '1')
        numStr = zhStr.replace('零', '0').replace('一', '1').replace('二', '2').replace('三', '3').replace('四', '4')\
            .replace('五', '5').replace('六', '6').replace('七', '7').replace('八', '8').replace('九', '9')
        return '第%s章 %s' % (numStr, match[2].strip())

    result = []
    caption = ''
    content = []
    for item in html.body.contents:
        if not isCaption(item):
            content.append(item.text)
            continue
        result.append({
            'caption': caption,
            'content': content,
        })
        content = []
        caption = formatCaption(item.text)
    result.append({
        'caption': caption,
        'content': content,
    })
    result.pop(0)
    return result


ret = {}
logger.warning('Extract info of `zhihu.com`')
for dat in loadData():
    for chapter in splitHtml(dat['content']):
        ret[chapter['caption']] = chapter['content']
print(json.dumps(ret))
