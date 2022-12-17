#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from common import loadData


def formatMetadata(metadata: dict) -> str:
    return '# %s\n\n+ 作者：%s\n\n> %s' % (
        metadata['name'],
        metadata['author'],
        '\n> '.join(metadata['desc']),
    )


def formatChapter(caption: str, content: list) -> str:
    return '## %s\n\n%s' % (caption, '\n\n'.join(content))


def markdownRelease(metadata: dict, content: dict) -> str:
    result = [formatMetadata(metadata)]
    for (title, chapter) in content.items():
        result.append(
            formatChapter(title, chapter)
        )
    return '\n\n'.join(result)


if __name__ == '__main__':
    data = loadData(sys.argv[1])
    print(markdownRelease(data['metadata'], data['content']))
