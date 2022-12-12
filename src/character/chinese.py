#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum

class Chinese:
    OK = 'simplified'  # simplified chinese
    WARN = 'traditional'  # traditional chinese
    ERROR = 'unknown'  # unknown character


def is_traditional(character: str) -> bool:  # whether character is traditional chinese
    character = character[0]
    try:
        character.encode('big5hkscs')
    except:
        return False
    return True


def is_simplified(character: str) -> bool:  # whether character is simplified chinese
    character = character[0]
    try:
        character.encode('gb2312')
    except:
        return False
    return True


def chinese_check(character: str) -> Chinese:  # chinese character check
    character = character[0]
    if is_simplified(character):  # simplified chinese case
        return Chinese.OK
    if is_traditional(character):  # traditional chinese case
        return Chinese.WARN
    return Chinese.ERROR  # unknown case


def sentence_check(sentence: str) -> (bool, str):  # chinese sentence check
    flag = False
    characters = []
    for character in sentence:
        if chinese_check(character) == Chinese.OK:  # normal case
            characters.append(character)
        elif chinese_check(character) == Chinese.WARN:  # warning case
            flag = True
            characters.append('\033[0;33m%s\033[0;39m' % character)
        else:
            flag = True
            characters.append('\033[0;31m%s\033[0;39m' % character)  # error case
    return not flag, ''.join(characters)


print(sentence_check('我們今天去吃飯了►►►太好吃了'))
print(sentence_check('测试成功OK'))
