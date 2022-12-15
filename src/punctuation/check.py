#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product

punctuationPairs = [
    ('‘', '’'),
    ('“', '”'),
    ('《', '》'),
    ('（', '）'),
]


def pairsCheck(sentence: str) -> bool:
    errorFlag = False
    punctuationStack = []
    sentence = list(sentence)

    def colorful(char: str, color: int) -> str:  # string with color
        return '\033[0;%dm%s\033[0;39m' % (color, char)

    for (i, punctuationPair) in product(range(0, len(sentence)), punctuationPairs):
        if sentence[i] == punctuationPair[0]:  # get left punctuation
            punctuationStack.append(punctuationPair)
            sentence[i] = colorful(sentence[i], 33)  # mark punctuation
        elif sentence[i] == punctuationPair[1]:  # get right punctuation
            if punctuationStack.pop()[1] != sentence[i]:
                errorFlag = True
                sentence[i] = colorful(sentence[i], 31)  # match error case
            else:
                sentence[i] = colorful(sentence[i], 33)  # mark punctuation

    if len(punctuationStack) != 0 or errorFlag:  # something error in sentence
        for punctuation in reversed(punctuationStack):  # replenish missing punctuation
            sentence.append(colorful(punctuation[1], 35))
        print(''.join(sentence))
        return False
    return True  # no error match in sentence


pairsCheck('测试“这个是OK的《2333》没错‘233’嗯嗯”')
