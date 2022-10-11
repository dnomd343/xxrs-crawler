#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

strData = ''
data = json.loads(open('xxrs.json').read())
for title, content in data.items():
    strData += '%s\n\n' % title
    strData += '%s\n\n\n' % '\n\n'.join(content)
print(strData.strip())
