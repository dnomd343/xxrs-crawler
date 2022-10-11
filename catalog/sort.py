#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

catalog = {}
for catalogPage in json.loads(open('raw.json').read()):
    for pageInfo in catalogPage:
        pageId = re.search(r'^/novel/57104/read_(\d+)\.html$', pageInfo['url'])[1]
        catalog[pageInfo['name']] = pageId

catalog = sorted(catalog.items(), key = lambda d: int(re.search(r'^第(\d+)章', d[0])[1]))
catalog = {x[0]: x[1] for x in catalog}

print(json.dumps(catalog))
