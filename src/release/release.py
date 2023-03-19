#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import multiprocessing
from copy import deepcopy
from concurrent import futures

from utils import loadBook
from utils import txtRelease
from utils import jsonRelease
from utils import azw3Release
from utils import epubRelease
from utils import mobiRelease
from utils import staticRelease
from utils import calibreRelease
from utils import gitbookRelease


'''
In order to avoid unintentional modification of the content,
    using deepcopy function here.
'''
def allRelease(metadata: dict, content: dict) -> None:
    cpuCount = multiprocessing.cpu_count()
    txtRelease(deepcopy(metadata), deepcopy(content))
    jsonRelease(deepcopy(metadata), deepcopy(content))
    gitbookRelease(deepcopy(metadata), deepcopy(content))
    threadPool = futures.ThreadPoolExecutor(max_workers = cpuCount)
    azw3Task = threadPool.submit(azw3Release, deepcopy(metadata), deepcopy(content))
    epubTask = threadPool.submit(epubRelease, deepcopy(metadata), deepcopy(content))
    mobiTask = threadPool.submit(mobiRelease, deepcopy(metadata), deepcopy(content))
    staticTask = threadPool.submit(staticRelease, deepcopy(metadata), deepcopy(content))
    futures.wait([azw3Task, epubTask, mobiTask, staticTask], return_when = futures.ALL_COMPLETED)
    print('All build complete')


releaseEntry = {  # release functions
    'all': allRelease,
    'txt': txtRelease,
    'json': jsonRelease,
    'azw3': azw3Release,
    'epub': epubRelease,
    'mobi': mobiRelease,
    'static': staticRelease,
    'calibre': calibreRelease,
    'gitbook': gitbookRelease,
}


if sys.argv[1] not in releaseEntry:
    print('Unknown target `%s` in %s' % (sys.argv[1], [x for x in releaseEntry]))
bookMetadata, bookContent = loadBook(sys.argv[2])
releaseEntry[sys.argv[1]](bookMetadata, bookContent)
