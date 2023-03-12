#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

punctuations = [
    ' ', '-', '.', '~', '·', '—',
    '‘', '’', '“', '”', '…',
    '、', '。', '《', '》', '！', '（', '）',
    '，', '：', '；', '？',
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
    return ''.join(['➕' if x == '' else x for x in result])


def sentenceType(content: list) -> list:
    result = set()
    for row in content:
        result.add(abstract(row))
    return list(sorted(result))


print('\n'.join(
    sentenceType(loadContent('rc-5'))
))
