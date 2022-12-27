#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

rootPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../../'
)
dataPath = os.path.join(rootPath, './release/')
metadataFile = os.path.join(rootPath, './assets/metadata.json')


def loadData(jsonName: str) -> dict:  # load book data from json file
    content = json.loads(open(
        os.path.join(dataPath, '%s.json' % jsonName)
    ).read())
    metadata = json.loads(open(metadataFile).read())
    return {
        'metadata': metadata,
        'content': content,
    }


def saveFile(fileName: str, content: str) -> None:  # save into file
    with open(fileName, 'w') as fileObj:
        fileObj.write(content)


def createFolder(folderName: str) -> None:  # create folder
    if not os.path.exists(folderName):
        os.mkdir(folderName)
