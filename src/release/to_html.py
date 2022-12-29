#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from common import loadData


def formatMetadata(metadata: dict) -> str:
    return '<h1>栩栩若生</h1>\n' + '\n'.join(
        ['<p>%s</p>' % x for x in metadata['desc']]
    )


def formatChapter(caption: str, content: list) -> str:
    return '<h2>%s</h2>\n' % caption + '\n'.join(['<p>%s</p>' % x for x in content])


def htmlRelease(metadata: dict, content: dict) -> str:
    result = [formatMetadata(metadata)]
    for (title, chapter) in content.items():
        result.append(
            formatChapter(title, chapter)
        )
    return '\n\n'.join(result)


if __name__ == '__main__':
    data = loadData(sys.argv[1])
    print(htmlRelease(data['metadata'], data['content']))
