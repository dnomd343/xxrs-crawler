#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import loadBook
from utils import saveFile
from utils import txtRelease
from utils import jsonRelease
from utils import htmlRelease
from utils import releaseInfo

metadata, content = loadBook('rc-5')

saveFile(
    releaseInfo['txt'], txtRelease(metadata, content)
)

saveFile(
    releaseInfo['json'], jsonRelease(metadata, content)
)

saveFile(
    releaseInfo['calibre'], htmlRelease(metadata, content)
)
