#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import shutil
import tempfile
import subprocess

from .common import isRoot
from .common import rootPath
from .common import saveFile
from .common import projectUrl
from .common import projectDesc
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
    saveFile(releaseInfo['txt'], txtSerialize(metadata, content))


def jsonRelease(metadata: dict, content: dict) -> None:
    saveFile(releaseInfo['json'], jsonSerialize(metadata, content))


def htmlRelease(metadata: dict, content: dict) -> None:
    saveFile(releaseInfo['calibre'], htmlSerialize(metadata, content))


def gitbookRelease(metadata: dict, content: dict) -> None:
    createFolder(releaseInfo['gitbook'])
    createFolder(os.path.join(releaseInfo['gitbook'], './assets/'))
    createFolder(os.path.join(releaseInfo['gitbook'], './chapter/'))

    cover = gitbookMetadata(metadata)
    for (resName, resUrls) in resourceInfo.items():
        cover += '{% hint style="success" %}\n' \
            + '### >>> [%s](%s) <<<\n' % (resName, resUrls[0]) \
            + '{% endhint %}\n\n'
    cover += '{%% embed url="%s" %%}\n项目地址\n{%% endembed %%}\n' % projectUrl

    saveFile(os.path.join(releaseInfo['gitbook'], 'README.md'), cover)
    saveFile(os.path.join(releaseInfo['gitbook'], 'SUMMARY.md'), gitbookSummary(content))
    for (chapterPath, chapterContent) in gitbookChapters(content).items():
        saveFile(os.path.join(releaseInfo['gitbook'], chapterPath), chapterContent)
    shutil.copy(  # gitbook cover
        os.path.join(rootPath, './assets/cover.jpg'),
        os.path.join(releaseInfo['gitbook'], './assets/cover.jpg')
    )


def staticDepends(workDir: str, metadata: dict, content: dict) -> None:
    createFolder(os.path.join(workDir, './assets/'))
    createFolder(os.path.join(workDir, './chapter/'))

    cover = gitbookMetadata(metadata) + '<hr/>\n'
    for (resName, resUrls) in resourceInfo.items():
        cover += '\n{% hint style="tip" %}\n' \
            + '#### [%s](%s)（[备用地址](%s)）\n' % (resName, resUrls[0], resUrls[1]) \
            + '{% endhint %}\n'

    bookInfo = json.dumps({
        'title': metadata['name'],
        'author': metadata['author'],
        'description': projectDesc,
        "language": "zh-hans",
        'plugins': [
            '-lunr', '-search', '-sharing', 'hints', 'github',
            'hide-element', 'fontsettings', 'image-captions', 'back-to-top-button'
        ],
        'pluginsConfig': {
            'github': {'url': projectUrl},
            'hide-element': {
                'elements': ['.gitbook-link']
            }
        }
    })
    saveFile(os.path.join(workDir, 'README.md'), cover)
    saveFile(os.path.join(workDir, 'book.json'), bookInfo)
    saveFile(os.path.join(workDir, 'SUMMARY.md'), gitbookSummary(content))
    for (chapterPath, chapterContent) in gitbookChapters(content).items():
        saveFile(os.path.join(workDir, chapterPath), chapterContent)
    shutil.copy(  # gitbook cover
        os.path.join(rootPath, './assets/cover.jpg'),
        os.path.join(workDir, './assets/cover.jpg')
    )


def staticBuild(workDir: str) -> None:
    buildDir = '/xxrs/'
    nodeImage = 'node:10-alpine'
    buildCommand = 'docker run --rm -v %s:%s --entrypoint sh %s -c "%s"' % (
        workDir, buildDir, nodeImage,
        'npm install gitbook-cli -g && gitbook install %s && gitbook build %s --log=debug' % (
            buildDir, buildDir
        )
    )
    print('Gitbook Build -> %s' % workDir)
    subprocess.Popen(buildCommand, shell = True).wait()  # blocking wait
    os.chdir(os.path.join(workDir, './_book'))
    os.system('tar cJf %s *' % releaseInfo['static'])


def staticRelease(metadata: dict, content: dict) -> None:
    if not isRoot():
        print('\033[0;33mDue to the permission problems, it is recommended to run under root user.\033[0m')
        return
    tempDir = tempfile.TemporaryDirectory()  # access temporary directory
    staticDepends(tempDir.name, metadata, content)
    staticBuild(tempDir.name)
    tempDir.cleanup()
