#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from enum import Enum

defaultPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../../release/'
)

simplifiedChineseReplenish = ['嘚', '跶', '啰', '粤', '瘆']


class Chinese:
    OK = 'simplified'  # simplified chinese
    WARN = 'traditional'  # traditional chinese
    ERROR = 'unknown'  # unknown character


def isTraditional(character: str) -> bool:  # whether character is traditional chinese
    character = character[0]
    try:
        character.encode('big5hkscs')
    except:
        return False
    return True


def isSimplified(character: str) -> bool:  # whether character is simplified chinese
    character = character[0]
    if character in simplifiedChineseReplenish:
        return True
    try:
        character.encode('gb2312')
    except:
        return False
    return True


def characterCheck(character: str) -> Chinese:  # chinese character check
    character = character[0]
    if character in ['—']:  # white list
        return Chinese.OK
    if isSimplified(character):  # simplified chinese case
        return Chinese.OK
    if isTraditional(character):  # traditional chinese case
        return Chinese.WARN
    return Chinese.ERROR  # unknown case


def sentenceCheck(sentence: str) -> (bool, str):  # chinese sentence check
    flag = False
    characters = []
    for character in sentence:
        if characterCheck(character) == Chinese.OK:  # normal case
            characters.append(character)
        elif characterCheck(character) == Chinese.WARN:  # warning case
            flag = True
            characters.append('\033[0;33m%s\033[0;39m' % character)
        else:
            flag = True
            characters.append('\033[0;31m%s\033[0;39m' % character)  # error case
    return not flag, ''.join(characters)


def chineseCheck(content: list) -> None:
    for row in content:
        status, result = sentenceCheck(row)
        if status:  # normal sentence
            continue
        print(result)


def loadContent(filename: str) -> list:  # load json content
    if not filename.endswith('.json'):
        filename += '.json'  # add file suffix
    raw = json.loads(open(
        os.path.join(defaultPath, filename)
    ).read())
    combine = []
    for (title, content) in raw.items():
        combine.append(title)
        combine += content
    return combine


chineseCheck(loadContent(sys.argv[1]))
