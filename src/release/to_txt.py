#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from common import loadData


def formatMetadata(metadata: dict) -> str:
    return '%s\n\n作者：%s\n\n\n%s' % (
        metadata['name'],
        metadata['author'],
        '\n\n'.join(metadata['desc']),
    )


def formatChapter(caption: str, content: list) -> str:
    return '\n\n'.join([caption] + content)


def txtRelease(metadata: dict, content: dict) -> str:
    result = [formatMetadata(metadata)]
    for (title, chapter) in content.items():
        result.append(
            formatChapter(title, chapter)
        )
    return '\n\n\n'.join(result)


if __name__ == '__main__':
    data = loadData(sys.argv[1])
    print(txtRelease(data['metadata'], data['content']))
