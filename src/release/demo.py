#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import loadBook
from utils import txtRelease
from utils import jsonRelease
from utils import htmlRelease
from utils import gitbookRelease


metadata, content = loadBook('rc-5')

txtRelease(metadata, content)
jsonRelease(metadata, content)
htmlRelease(metadata, content)
gitbookRelease(metadata, content)
