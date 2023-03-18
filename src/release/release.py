#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import loadBook
from utils import txtRelease
from utils import jsonRelease
from utils import mobiRelease
from utils import staticRelease
from utils import calibreRelease
from utils import gitbookRelease

releaseEntry = {
    'txt': txtRelease,
    'json': jsonRelease,
    'mobi': mobiRelease,
    'static': staticRelease,
    'calibre': calibreRelease,
    'gitbook': gitbookRelease,
}


releaseSrc = 'rc-5'
metadata, content = loadBook(releaseSrc)
releaseEntry['mobi'](metadata, content)
