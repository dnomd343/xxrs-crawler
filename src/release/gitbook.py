#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from common import loadData
from common import saveFile
from common import createFolder

workDir = './temp/'
contentDir = os.path.join(workDir, './content/')


def initFolder() -> None:
    createFolder(workDir)
    createFolder(contentDir)


def loadChapter(caption: str, content: list) -> str:
    chapterNum = re.search(r'^第(\d+)章', caption)[1]
    chapterNum = '0' * (3 - len(chapterNum)) + chapterNum  # add `0` prefix
    fileName = 'chapter-%s.md' % chapterNum
    saveFile(
        os.path.join(workDir, './content/', fileName),
        '# %s\n\n%s\n' % (caption, '\n\n'.join(content))
    )
    return fileName


def loadChapters(chapters: dict) -> dict:
    catalog = {}
    for (title, chapter) in chapters.items():
        catalog[title] = loadChapter(title, chapter)
    return catalog


def loadCover(metadata: dict) -> None:
    cover = '---\ndescription: 作者：%s\n---\n\n# %s\n\n' % (metadata['author'], metadata['name'])
    cover += '<figure><img src="assets/cover.jpg" alt=""><figcaption></figcaption></figure>\n\n'
    cover += '\n>\n'.join(['> %s' % x for x in metadata['desc']])
    saveFile(os.path.join(workDir, 'README.md'), cover)


def loadSummary(catalog: dict) -> None:
    summary = '# XXRS\n\n'
    summary += '* [栩栩若生](README.md)\n\n'
    summary += '## 内容 <a href="#content" id="content"></a>\n\n'
    for (title, mdFile) in catalog.items():
        summary += '* [%s](content/%s)\n' % (title, mdFile)
    saveFile(os.path.join(workDir, 'SUMMARY.md'), summary)


initFolder()
# c = loadChapters(loadData('rc-4')['content'])
# loadSummary(c)
loadCover(loadData('rc-4')['metadata'])
