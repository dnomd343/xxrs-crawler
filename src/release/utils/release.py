#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

from .common import rootPath
from .common import saveFile
from .common import projectUrl
from .common import releaseInfo
from .common import createFolder
from .common import resourceInfo

from .sequence import txtSerialize
from .sequence import jsonSerialize
from .sequence import htmlSerialize

from .sequence import gitbookSummary
from .sequence import gitbookChapters
from .sequence import gitbookMetadata


def txtRelease(metadata: dict, content: dict) -> None:
    saveFile(
        releaseInfo['txt'], txtSerialize(metadata, content)
    )


def jsonRelease(metadata: dict, content: dict) -> None:
    saveFile(
        releaseInfo['json'], jsonSerialize(metadata, content)
    )


def htmlRelease(metadata: dict, content: dict) -> None:
    saveFile(
        releaseInfo['calibre'], htmlSerialize(metadata, content)
    )


def gitbookRelease(metadata: dict, content: dict) -> None:
    createFolder(releaseInfo['gitbook'])
    createFolder(os.path.join(releaseInfo['gitbook'], './assets/'))
    createFolder(os.path.join(releaseInfo['gitbook'], './content/'))

    cover = gitbookMetadata(metadata)
    for (resName, resUrls) in resourceInfo.items():
        cover += '{% hint style="success" %}\n' \
            + '### >>> [%s](%s) <<<\n' % (resName, resUrls[0]) \
            + '{% endhint %}\n\n'
    cover += '{%% embed url="%s" %%}\n项目地址\n{%% endembed %%}\n' % projectUrl

    saveFile(
        os.path.join(releaseInfo['gitbook'], 'README.md'), cover
    )
    saveFile(
        os.path.join(releaseInfo['gitbook'], 'SUMMARY.md'), gitbookSummary(content)
    )
    for (chapterPath, chapterContent) in gitbookChapters(content).items():
        saveFile(
            os.path.join(releaseInfo['gitbook'], chapterPath), chapterContent
        )
    shutil.copy(  # gitbook cover
        os.path.join(rootPath, './assets/cover.jpg'),
        os.path.join(releaseInfo['gitbook'], './assets/cover.jpg')
    )
