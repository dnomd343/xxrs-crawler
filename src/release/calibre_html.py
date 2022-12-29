#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from common import loadData
from common import saveFile
from common import releaseInfo


def formatMetadata(metadata: dict) -> str:
    return '<h1>%s</h1>\n' % metadata['name'] + '\n'.join(
        ['<p>%s</p>' % x for x in metadata['desc']]
    )


def htmlRelease(metadata: dict, content: dict) -> str:
    result = [formatMetadata(metadata)]
    for (title, chapter) in content.items():
        result.append(
            '<h2>%s</h2>\n' % title + '\n'.join(['<p>%s</p>' % x for x in chapter])
        )
    return '\n\n'.join(result) + '\n'


if __name__ == '__main__':
    data = loadData(sys.argv[1])
    saveFile(
        releaseInfo['htmlFile'],
        htmlRelease(data['metadata'], data['content'])
    )
