#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snownlp import SnowNLP


def traditionalCheck(sentence: str) -> None:
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


traditionalCheck('繁體中文的叫法在臺灣亦很常見')

