#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from common import loadData


def jsonRelease(metadata: dict, content: dict) -> str:
    return json.dumps(
        {
            'metadata': metadata,
            'content': content,
        }, separators = (',', ':')
    )


if __name__ == '__main__':
    data = loadData(sys.argv[1])
    print(jsonRelease(data['metadata'], data['content']))
