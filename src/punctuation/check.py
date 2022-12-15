#!/usr/bin/env python3
# -*- coding: utf-8 -*-

punctuationPairs = [
    ('‘', '’'),
    ('“', '”'),
    ('《', '》'),
    ('（', '）'),
]


def pairsCheck(sentence: str) -> (bool, str):
    punctuationStack = []
    sentence = list(sentence)

    def colorful(char: str, color: int) -> str:  # string with color
        return '\033[0;%dm%s\033[0;39m' % (color, char)

    errorFlag = False
    for i in range(0, len(sentence)):
        for punctuationPair in punctuationPairs:
            if sentence[i] == punctuationPair[0]:  # get left punctuation
                punctuationStack.append(punctuationPair)
                sentence[i] = colorful(sentence[i], 33)  # mark punctuation
                break
            elif sentence[i] == punctuationPair[1]:  # get right punctuation
                if punctuationStack.pop()[1] != sentence[i]:
                    errorFlag = True
                    sentence[i] = colorful(sentence[i], 31)  # match error case
                else:
                    sentence[i] = colorful(sentence[i], 33)  # mark punctuation
                break
    if len(punctuationStack) == 0 and not errorFlag:
        return True, ''.join(sentence)  # no error in sentence

    for punctuation in reversed(punctuationStack):
        sentence.append(colorful(punctuation[1], 35))
        # print(punctuation)
    return False, ''.join(sentence)


status, ret = pairsCheck('测试“这个是OK的《2333》没错‘233’’《嗯嗯')
print('ok' if status else 'error')
print(ret)
