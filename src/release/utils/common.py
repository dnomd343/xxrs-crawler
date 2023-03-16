#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

rootPath = os.path.join(  # project root directory
    os.path.dirname(os.path.realpath(__file__)), '../../../'
)
dataPath = os.path.join(rootPath, './release/')
releasePath = os.path.join(dataPath, './output/')
metadataFile = os.path.join(rootPath, './assets/metadata.json')

releaseInfo = {  # release file name
    'json': 'XXRS.json',
    'txt': '栩栩若生.txt',
    'epub': '栩栩若生.epub',
    'mobi': '栩栩若生.mobi',
    'static': 'XXRS.tar.xz',
    'calibre': 'xxrs.html',
    'gitbook': 'xxrs-online/',
}
releaseInfo = {  # convert to absolute path
    key: os.path.join(releasePath, file) for (key, file) in releaseInfo.items()
}


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
