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


def characterSet(content: list) -> list:  # split into character set
    characters = set()
    for row in content:
        characters.update({x for x in row})
    return sorted(characters)


def toUnicode(character: str) -> int:  # get unicode number
    character = character[0]  # only first character
    unicode = 0
    for i in range(0, 4):
        unicode += character.encode('utf-32le')[i] * 256 ** i
    return unicode


def showCharacters(characters: list) -> None:  # show character stat
    letter = []
    chinese = []
    punctuation = []

    def asciiRange(start: str, end: str) -> list:
        return list(range(ord(start), ord(end) + 1))

    for c in characters:
        if int('4E00', 16) <= toUnicode(c) <= int('9FA5', 16):  # chinese unicode range
            chinese.append(c)
        elif toUnicode(c) in (  # numbers and letters
            asciiRange('0', '9') + asciiRange('a', 'z') + asciiRange('A', 'Z')
        ):
            letter.append(c)
        else:
            punctuation.append(c)

    print('\n\033[0;32mPunctuations\033[0;39m\033[0;35m(%d)\033[0;39m\n%s\n' % (
        len(punctuation), '|'.join(['[\033[0;33m%s\033[0;39m]' % p for p in punctuation])
    ))

    print('\033[0;32mLetters\033[0;39m\033[0;35m(%d)\033[0;39m' % len(letter))
    print(' '.join(['\033[0;31m%s\033[0;39m' % c for c in letter]) + '\n')

    print('\033[0;32mChinese\033[0;39m\033[0;35m(%d)\033[0;39m' % len(chinese))
    for i in range(0, len(chinese)):
        print('\033[0;36m%s\033[0;39m%s' % (
            chinese[i], '\n' if i % 60 == 59 else ''
        ), end = '')
    print('\n')


showCharacters(
    characterSet(loadContent(sys.argv[1]))
)
