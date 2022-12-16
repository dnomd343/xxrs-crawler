#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
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


if __name__ == '__main__':
    print(loadData(sys.argv[1]))
