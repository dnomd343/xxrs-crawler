#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

defaultPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../../release/'
)


def load_content(filename: str) -> list:  # load json content
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


def load_word(filename: str) -> list:  # load banned words list
    banned_list = []
    for word in open(filename).read().split('\n'):
        word = word.strip()
        if word != '':
            banned_list.append(word)
    return banned_list


def search_word(content: list, word: str) -> list:  # search target word
    result = []
    for row in content:
        if word in row:
            result.append(row.replace(word, '\033[0;33m%s\033[0;39m' % word))
    return result


def search_list(content: list, words: list) -> None:  # search target banned list
    for word in words:
        result = search_word(content, word)
        if len(result) == 0:  # banned word not found
            continue
        print('Found \033[0;36m%d\033[0;39m banned word: \033[0;32m%s\033[0;39m' % (len(result), word))
        print('-' * 128)
        for i in range(0, len(result)):
            print('%d: %s' % (
                i, result[i] + ('' if i + 1 == len(result) else '\n')
            ))
        print('-' * 128 + '\n')


search_list(load_content(sys.argv[1]), load_word(sys.argv[2]))
