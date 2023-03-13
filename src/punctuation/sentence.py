#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

delimiter = '➕'

punctuations = [
    ' ', '-', '.', '~', '·', '—',
    '‘', '’', '“', '”', '…',
    '、', '。', '《', '》', '！', '（', '）',
    '，', '：', '；', '？',
]

duplicates = [
    '~', '！', '？',
    delimiter + '，',
    delimiter + '！',
    delimiter + '？',
    delimiter + '、',
    delimiter + '~',
    delimiter + '……',
    delimiter + '——',
    delimiter + '~！',
    delimiter + '！~',
    delimiter + '，' + delimiter + '！',
    delimiter + '，' + delimiter + '？',
    delimiter + '，' + delimiter + '、',
    delimiter + '，' + delimiter + '~',
    delimiter + '，' + delimiter + '……',
    delimiter + '，' + delimiter + '。',
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
        combine += content
    return combine


def abstract(raw: str) -> str:  # keep only punctuation in sentence
    sentence = list(raw)
    for i in range(0, len(sentence)):
        if sentence[i] not in punctuations:
            sentence[i] = ''
    result = [sentence[0]]
    for c in sentence[1:]:
        if c == '' and result[-1] == '':
            continue
        result.append(c)
    return ''.join([delimiter if x == '' else x for x in result])


def removeDuplicate(sentence: str) -> str:
    for duplicate in duplicates:
        while True:
            tmp = sentence.replace(duplicate + duplicate, duplicate)
            if tmp == sentence:
                break
            sentence = tmp
    return sentence


def symbolConvert(sentence: str) -> str:
    sentence = sentence.replace('➕？！', '➕。')
    sentence = sentence.replace('➕！？', '➕。')
    sentence = sentence.replace('➕？', '➕。')
    sentence = sentence.replace('➕！~', '➕。')
    sentence = sentence.replace('➕~！', '➕。')
    if '➕！……' not in sentence:
        sentence = sentence.replace('➕！', '➕。')
    sentence = sentence.replace('➕、', '➕，')
    return removeDuplicate(sentence)


def sentenceType(content: list) -> tuple[list, list]:
    resultSingle = set()
    resultSequence = set()
    for row in content:
        sType = symbolConvert(removeDuplicate(abstract(row)))
        if delimiter in sType:
            resultSequence.add(sType)
        else:
            resultSingle.add(sType)
    return list(sorted(resultSingle)), list(sorted(resultSequence))


def sentenceCheck(content: list) -> None:
    single, sequence = sentenceType(content)
    print('\n'.join(single))
    print('-' * 64)
    print('\n'.join(sequence))


sentenceCheck(loadContent(sys.argv[1]))
