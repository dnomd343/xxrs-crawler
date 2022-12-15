#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from itertools import product

punctuationPairs = [
    ('‘', '’'),
    ('“', '”'),
    ('《', '》'),
    ('（', '）'),
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


def contentCheck(content: list) -> None:
    for row in content:  # pairs check
        pairsCheck(row)
    print('-' * 128)
    # other check process


contentCheck(loadContent(sys.argv[1]))
