#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from common import loadData
from common import saveFile

htmlFile = 'xxrs.html'


def formatMetadata(metadata: dict) -> str:
    return '<h1>栩栩若生</h1>\n' + '\n'.join(
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
    saveFile(htmlFile, htmlRelease(data['metadata'], data['content']))
