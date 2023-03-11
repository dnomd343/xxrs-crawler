#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from common import loadData
from common import saveFile
from common import releaseInfo


def jsonRelease(metadata: dict, content: dict) -> str:
    return json.dumps({
        'metadata': metadata,
        'content': content,
    }, separators = (',', ':'))  # without space


if __name__ == '__main__':
    data = loadData(sys.argv[1])
    saveFile(
        releaseInfo['jsonFile'],
        jsonRelease(data['metadata'], data['content'])
    )
