#!/usr/bin/env python3
# -*- coding: utf-8 -*-

punctuationPairs = [
    ('‘', '’'),
    ('“', '”'),
    ('《', '》'),
    ('（', '）'),
]


def isLeftPunctuation(char: str) -> bool:
    for punctuationPair in punctuationPairs:
        if char == punctuationPair[0]:
            return True
    return False


def isRightPunctuation(char: str) -> bool:
    for punctuationPair in punctuationPairs:
        if char == punctuationPair[1]:
            return True
    return False


def getLeftPunctuation(char: str) -> str:
    for punctuationPair in punctuationPairs:
        if char == punctuationPair[1]:
            return punctuationPair[0]
    return ''  # no match


def pairsCheck(sentence: str) -> bool:
    punctuationStack = []
    sentence = list(sentence)
    for i in range(0, len(sentence)):
        char = sentence[i]
        if isLeftPunctuation(char):
            punctuationStack.append(char)
        elif isRightPunctuation(char):
            if punctuationStack.pop() != getLeftPunctuation(char):
                return False
    return len(punctuationStack) == 0


print(
    pairsCheck('测试“这个是OK的《2333》没错‘’”嗯嗯')
)
