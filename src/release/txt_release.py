#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from common import loadData
from common import saveFile
from common import releaseInfo


def formatMetadata(metadata: dict) -> str:
    return '%s\n\n作者：%s\n\n\n%s' % (
        metadata['name'],
        metadata['author'],
        '\n\n'.join(metadata['desc']),
    )


def txtRelease(metadata: dict, content: dict) -> str:
    result = [formatMetadata(metadata)]
    for (title, chapter) in content.items():
        result.append('\n\n'.join([title] + chapter))
    return '\n\n\n'.join(result) + '\n'


if __name__ == '__main__':
    data = loadData(sys.argv[1])
    saveFile(
        releaseInfo['txtFile'],
        txtRelease(data['metadata'], data['content'])
    )
