#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from snownlp import SnowNLP

defaultPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../../release/'
)

traditionalWhiteList = [
    '其余', '残余', '有余', '多余', '之余', '梦余', '空余',
    '业余', '剩余', '余地', '余光', '余音', '余后', '余下',
    '余生', '余力', '余毒', '余出', '余晖', '余钱', '余脉',
    '余痛', '余年', '余温', '余额', '余人', '余先生',

    '上乾下坤', '一览无余', '茶余饭后', '著鞭跨马',
    '慰藉', '狼藉', '蕴藉', '碟片', '哪吒', '括弧', '瞭望',
    '覆盖', '覆舟', '覆到', '覆碗', '幺蛾子', '雪糕', '共用',
    '翻来覆去', '覆水难收', '覆手为雨', '下覆昆仑', '翻天覆地',

    '乾兑', '乾旋', '大乾', '为乾', '乾元',
    '登乾', '乾卦', '丁乾', '乾金', '战乎乾', '乾三连',
    '乾西北', '乾在上', '乾为天', '乾代表天', '乾为上卦',
    '的士兵', '吒为正义', '金吒木吒郎', '连夜学一学', '乾、',
]


def traditionalCheck(sentence: str) -> None:
    for c in traditionalWhiteList:  # skip white list
        sentence = sentence.replace(c, '')
    simplified = SnowNLP(sentence).han  # convert into simplified chinese
    if simplified == sentence:  # simplified chinese already
        return
    sentence = list(sentence)
    simplified = list(simplified)
    for i in range(0, min(len(sentence), len(simplified))):  # traverse each character
        if sentence[i] != simplified[i]:  # found different character
            sentence[i] = '\033[0;33m%s\033[0;39m' % sentence[i]  # set colorful flag
            simplified[i] = '\033[0;32m%s\033[0;39m' % simplified[i]
    print('%s\n> %s\n> %s\n%s' % (
        '-' * 128, ''.join(sentence), ''.join(simplified), '-' * 128
    ))


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


for row in loadContent(sys.argv[1]):
    traditionalCheck(row)
