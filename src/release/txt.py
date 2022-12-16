#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

rootPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../../'
)
dataPath = os.path.join(rootPath, './release/')
metadataFile = os.path.join(rootPath, './assets/metadata.json')


def loadData(jsonName: str) -> dict:
    content = json.loads(open(
        os.path.join(dataPath, '%s.json' % jsonName)
    ).read())
    metadata = json.loads(open(metadataFile).read())
    return {
        'metadata': metadata,
        'content': content,
    }


def releaseChapter(caption: str, content: list) -> str:
    return '\n\n'.join([caption] + content)


data = loadData('rc-4')
c = data['content']
for (c, dat) in c.items():
    print(releaseChapter(c, dat))
    break
