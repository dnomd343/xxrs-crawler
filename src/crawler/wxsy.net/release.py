#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Combine all chapters from json files.

    USAGE: python3 release.py [CATALOG] [JSON_DIR]
"""

import os
import sys
import json
sys.path.append('..')
from utils import logger


def loadData(catalog: dict) -> dict:  # load data from json files
    data = {}
    for _, chapterId in catalog.items():
        data[chapterId] = json.loads(
            open(os.path.join(sys.argv[2], '%s.json' % chapterId)).read()  # read json content
        )
    return data


def listDiff(list_1: list, list_2: list) -> bool:  # compare two lists
    diffFlag = False
    if len(list_1) != len(list_2):  # with different length
        diffFlag = True
        logger.error('List with different length')
    for i in range(0, len(list_1)):  # check every items
        if list_1[i] == list_2[i]:
            continue
        diffFlag = True  # found different item
        logger.error('List diff: `%s` <-> `%s`' % (list_1[i], list_2[i]))
    return diffFlag


def check(catalog: dict, data: dict) -> None:  # check crawler data
    titles = [x['title'] for _, x in data.items()]
    ids = [x['myId'] for _, x in data.items()]
    preIds = [x['preId'] for _, x in data.items()]
    nextIds = [x['nextId'] for _, x in data.items()]
    nextIds.pop(-1)  # remove last item
    preIds.pop(0)  # remove first item

    # if listDiff(ids, preIds + [ids[-1]]):
    #     logger.warning('Pre IDs mismatch')
    # if listDiff(ids, [ids[0]] + nextIds):
    #     logger.warning('Next IDs mismatch')
    if listDiff(ids, [x for _, x in catalog.items()]):
        logger.warning('IDs mismatch')
    if listDiff(titles, [x for x in catalog]):
        logger.warning('Titles mismatch')


def combine() -> dict:  # combine all chapters
    catalog = json.loads(open(sys.argv[1]).read())  # load catalog
    data = loadData(catalog)  # load crawler data
    check(catalog, data)  # check data

    result = {}
    for _, info in data.items():  # combine contents
        result[info['title']] = info['content']
    return result


print(json.dumps(combine()))
