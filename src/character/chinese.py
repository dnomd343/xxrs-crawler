#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def is_traditional(character: str) -> bool:  # whether character is traditional chinese
    character = character[0]
    try:
        character.encode('big5hkscs')
    except:
        return False
    return True


def is_simplified(character: str) -> bool:  # whether character is simplified chinese
    character = character[0]
    try:
        character.encode('gb2312')
    except:
        return False
    return True


def chinese_check(character: str) -> None:
    character = character[0]
    print(character)
    print('is_simplified ->', is_simplified(character))
    print('is_traditional ->', is_traditional(character))
    print()


chinese_check('我')
chinese_check('飯')
chinese_check('们')
