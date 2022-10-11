#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from logger import logger


def loadData(catalog: dict) -> dict:
    data = {}
    for _, pageId in catalog.items():
        data[pageId] = json.loads(
            open('./json/%s.json' % pageId).read()
        )
    return data


def listDiff(list_1: list, list_2: list) -> bool:
    diffFlag = False
    if len(list_1) != len(list_2):
        diffFlag = True
        logger.error('List with different length')
    for i in range(0, len(list_1)):
        if list_1[i] != list_2[i]:
            diffFlag = True
            logger.error('List diff: `%s` <-> `%s`' % (list_1[i], list_2[i]))
    return diffFlag


def check(catalog: dict, data: dict) -> None:
    titles = [x['title'] for _, x in data.items()]
    ids = [x['myId'] for _, x in data.items()]
    preIds = [x['preId'] for _, x in data.items()]
    nextIds = [x['nextId'] for _, x in data.items()]
    nextIds.pop(-1)
    preIds.pop(0)

    # if listDiff(ids, preIds + [ids[-1]]):
    #     logger.warning('Pre IDs mismatch')
    # if listDiff(ids, [ids[0]] + nextIds):
    #     logger.warning('Next IDs mismatch')
    if listDiff(ids, [x for _, x in catalog.items()]):
        logger.warning('IDs mismatch')
    if listDiff(titles, [x for x in catalog]):
        logger.warning('Titles mismatch')


def combine() -> dict:
    catalog = json.loads(open('./catalog/catalog.json').read())
    data = loadData(catalog)
    check(catalog, data)

    result = {}
    for _, info in data.items():
        result[info['title']] = info['contents']
    return result


print(json.dumps(combine()))
