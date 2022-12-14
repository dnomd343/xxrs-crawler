#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import json
from itertools import product

punctuationPairs = [
    ('‘', '’'),
    ('“', '”'),
    ('《', '》'),
    ('（', '）'),
]

endingPunctuations = [
    '。', '？', '！',
    '~', '”', '’',
    '……', '——',
    '：',  # special: letter beginning
]

warningPunctuations = [
    ' ', '-', '·', '.', '；',
]

defaultPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../../release/'
)


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


def isCaption(content: str) -> bool:
    return re.search(r'^第\d+章 \S*$', content) is not None


def pairsCheck(sentence: str) -> bool:
    errorFlag = False
    punctuationStack = []
    sentence = list(sentence)

    def colorful(char: str, color: int) -> str:  # string with color
        return '\033[0;%dm%s\033[0;39m' % (color, char)

    for (i, punctuationPair) in product(range(0, len(sentence)), punctuationPairs):
        if sentence[i] == punctuationPair[0]:  # get left punctuation
            punctuationStack.append(punctuationPair)
            sentence[i] = colorful(sentence[i], 33)  # mark it
        elif sentence[i] == punctuationPair[1]:  # get right punctuation
            if len(punctuationStack) == 0:  # missing left punctuation
                errorFlag = True
                sentence[i] = colorful(sentence[i], 31)  # mark error case
            elif punctuationStack.pop()[1] != sentence[i]:  # right punctuation not match
                errorFlag = True
                sentence[i] = colorful(sentence[i], 31)  # mark error case
            else:
                sentence[i] = colorful(sentence[i], 33)  # mark it

    if len(punctuationStack) != 0 or errorFlag:  # something error in sentence
        for punctuation in reversed(punctuationStack):  # replenish missing punctuation
            sentence.append(colorful(punctuation[1], 35))
        print('%s\n%s' % ('-' * 128, ''.join(sentence)))
        return False
    return True  # no error match in sentence


def endingCheck(sentence: str) -> bool:
    if isCaption(sentence):  # skip caption
        return True
    for endingPunctuation in endingPunctuations:
        if sentence.endswith(endingPunctuation):  # match ending punctuation
            return True
    print('%s\n%s\033[0;31m_\033[0;39m' % ('-' * 128, sentence))
    return False


def doubleCheck(sentence: str) -> bool:

    def groupCombine(content: str) -> list:  # combine same character
        group = ''
        result = []
        for c in content:
            if c in group:
                group += c
                continue
            if len(group) != 0:
                result.append(group)
            group = c
        result.append(group)
        return result

    flag = False
    sentence = groupCombine(sentence)
    for (p, i) in product(['…', '—'], range(0, len(sentence))):
        if p in sentence[i] and len(sentence[i]) != 2:
            flag = True
            sentence[i] = '\033[0;31m%s\033[0;39m' % sentence[i]
    if flag:
        print('%s\n%s' % ('-' * 128, ''.join(sentence)))
    return not flag


def existCheck(sentence: str) -> bool:
    if isCaption(sentence):  # skip caption
        return True
    flag = False
    for warningPunctuation in warningPunctuations:
        if warningPunctuation in sentence:
            flag = True
            sentence = sentence.replace(warningPunctuation, '\033[0;33m%s\033[0;39m' % warningPunctuation)
    if flag:
        print('%s\n%s' % ('-' * 128, sentence))
    return not flag


def contentCheck(content: list) -> None:

    def runCheck(checkFunc) -> None:
        flag = True
        for row in content:
            flag &= checkFunc(row)  # run check function
        if not flag:  # with output
            print('-' * 128)  # show split line

    runCheck(pairsCheck)
    runCheck(endingCheck)
    runCheck(doubleCheck)
    runCheck(existCheck)


contentCheck(loadContent(sys.argv[1]))
