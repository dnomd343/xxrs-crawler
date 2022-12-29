#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import shutil
from common import loadData
from common import rootPath
from common import saveFile
from common import createFolder

workDir = './xxrs-online/'


def initFolder() -> None:
    createFolder(workDir)
    createFolder(os.path.join(workDir, './assets/'))
    createFolder(os.path.join(workDir, './content/'))


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
    cover = '---\ndescription: 作者：%s\n---\n\n# 栩栩若生\n\n' % metadata['author']
    cover += '<figure><img src="assets/cover.jpg" alt=""><figcaption><p>栩栩若生</p></figcaption></figure>\n\n'
    cover += '\n>\n'.join(['> %s' % x for x in metadata['desc']]) + '\n\n'
    cover += '{% embed url="https://github.com/dnomd343/xxrs-crawler.git" %}\n项目地址\n{% endembed %}\n'
    saveFile(os.path.join(workDir, 'README.md'), cover + '\n')


def loadSummary(catalog: dict) -> None:
    summary = '# XXRS\n\n'
    summary += '* [序言](README.md)\n\n'
    summary += '## 内容 <a href="#content" id="content"></a>\n\n'
    for (title, mdFile) in catalog.items():
        summary += '* [%s](content/%s)\n' % (title, mdFile)
    saveFile(os.path.join(workDir, 'SUMMARY.md'), summary)


def loadGitbook(jsonName: str) -> None:
    data = loadData(jsonName)
    loadCover(data['metadata'])
    catalog = loadChapters(data['content'])
    loadSummary(catalog)
    shutil.copy(
        os.path.join(rootPath, './assets/cover.jpg'),
        os.path.join(workDir, './assets/cover.jpg')
    )


if __name__ == '__main__':
    initFolder()
    loadGitbook(sys.argv[1])
