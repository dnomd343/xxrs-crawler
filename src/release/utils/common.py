#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

projectUrl = 'https://github.com/dnomd343/xxrs-crawler'

rootPath = os.path.join(  # project root directory
    os.path.dirname(os.path.realpath(__file__)), '../../../'
)
dataPath = os.path.join(rootPath, './release/')
releasePath = os.path.join(dataPath, './output/')
metadataFile = os.path.join(rootPath, './assets/metadata.json')

releaseInfo = {  # release file name
    'json': 'XXRS.json',
    'txt': '栩栩若生.txt',
    'azw3': '栩栩若生.azw3',
    'epub': '栩栩若生.epub',
    'mobi': '栩栩若生.mobi',
    'calibre': 'xxrs.zip',
    'static': 'XXRS.tar.xz',
    'gitbook': 'xxrs-online/',
}
releaseInfo = {  # convert to absolute path
    key: os.path.join(releasePath, file) for (key, file) in releaseInfo.items()
}

resourceInfo = {  # resource download links
    'TXT 下载': [
        'https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.txt',
        'https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.txt',
    ],
    'EPUB 下载': [
        'https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.epub',
        'https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.epub',
    ],
    'MOBI 下载': [
        'https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.mobi',
        'https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.mobi',
    ],
    'AZW3 下载': [
        'https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.azw3',
        'https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.azw3',
    ],
}


def isRoot() -> bool:  # whether the current user is root
    return os.geteuid() == 0


def createFolder(folderName: str) -> None:  # create folder
    if not os.path.exists(folderName):
        os.mkdir(folderName)


def saveFile(fileName: str, content: str) -> None:  # save into file
    with open(fileName, 'w') as fileObj:
        fileObj.write(content)


def loadBook(jsonName: str) -> tuple[dict, dict]:  # load book data from json file
    content = json.loads(open(
        os.path.join(dataPath, '%s.json' % jsonName)  # book content
    ).read())
    metadata = json.loads(open(metadataFile).read())  # book metadata
    return metadata, content


createFolder(releasePath)  # create output folder
