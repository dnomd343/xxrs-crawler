#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from enum import Enum

defaultPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../../release/'
)

simplifiedChineseReplenish = [  # missing chinese character in GB2312
    '嘚', '啰', '瘆',  # 嘚瑟 / 喽啰 / 瘆人
    '箓', '髈', '槃',  # 符箓 / 蹄髈 / 涅槃
    '鞧', '祇', '倓',  # 后鞧 / 神祇 / 倓然
    '瞭', '跶', '蹚',  # 瞭望 / 蹦跶 / 蹚浑水
    '秾', '窸', '窣',  # 夭桃秾李 / 窸窸窣窣

    '尅',  # 韩语拟音：哦都尅，即“怎么办”
    '唵', '吽',  # 藏传佛教咒语：唵嘛呢叭咪吽
    '冇', '嘢', '咁', '佢', '冚',  # 粤语词汇
    '叆', '叇',  # 叆叇：云彩很厚的样子，形容浓云蔽日
    '欻', '歘',  # 欻：忽然/迅速；歘：象声词，急促的声响

    '侘',  #《涉江》：“怀信侘傺，忽乎吾将行兮”
    '荄',  #《吁嗟篇》：“糜灭岂不痛，愿与株荄连”
    '洩',  #《郑伯克段于鄢》：“大隧之外，其乐也洩洩”
    '飖',  #《北征赋》：“风猋发以飘飖兮，谷水漼以扬波”
    '翛',  #《庄子·内篇·大宗师》：“翛然而往，翛然而来而已矣”

    '揦', '捯', '欸', '咗', '汵', '姤', '琯', '炁',  # 补充汉字
]


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
    if character in ['—', '·']:  # white list
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
