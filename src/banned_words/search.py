#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

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


def loadWord(filename: str) -> list:  # load banned words list
    bannedList = []
    for word in open(filename).read().split('\n'):
        word = word.strip()
        if word != '':
            bannedList.append(word)
    return bannedList


def searchWord(content: list, word: str) -> list:  # search target word
    result = []
    for row in content:
        if word in row:
            result.append(row.replace(word, '\033[0;33m%s\033[0;39m' % word))
    return result


def searchList(content: list, words: list) -> None:  # search target banned list
    for word in words:
        result = searchWord(content, word)
        if len(result) == 0:  # banned word not found
            continue
        print('Found \033[0;36m%d\033[0;39m banned word: \033[0;32m%s\033[0;39m' % (len(result), word))
        print('-' * 128)
        for i in range(0, len(result)):
            print('%d: %s' % (
                i, result[i] + ('' if i + 1 == len(result) else '\n')
            ))
        print('-' * 128 + '\n')


searchList(loadContent(sys.argv[1]), loadWord(sys.argv[2]))
