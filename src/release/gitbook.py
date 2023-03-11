#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import shutil
from common import loadData
from common import rootPath
from common import saveFile
from common import releaseInfo
from common import createFolder


def initFolder() -> None:
    createFolder(releaseInfo['gitbookDir'])
    createFolder(os.path.join(releaseInfo['gitbookDir'], './assets/'))
    createFolder(os.path.join(releaseInfo['gitbookDir'], './content/'))


def markdownTransfer(content: str) -> str:
    symbols = [
        '\\', '`', '*', '_', '~',
        '{', '}', '[', ']', '(', ')',
        '#', '+', '-', '.', '!', '|',
    ]
    for symbol in symbols:
        content = content.replace(symbol, '\\' + symbol)  # add `\` before symbol
    return content


def loadChapter(caption: str, content: list) -> str:
    chapterNum = re.search(r'^第(\d+)章', caption)[1]
    chapterNum = '0' * (3 - len(chapterNum)) + chapterNum  # add `0` prefix
    fileName = 'chapter-%s.md' % chapterNum
    content = [markdownTransfer(x) for x in content]
    saveFile(
        os.path.join(releaseInfo['gitbookDir'], './content/', fileName),
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
    cover += '<figure><img src="assets/cover.jpg" alt=""><figcaption><p>栩栩若生</p></figcaption></figure>\n\n'
    cover += '\n>\n'.join(['> %s' % x for x in metadata['desc']]) + '\n\n'
    cover += '## [>>> TXT下载 <<<](https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.txt)\n\n'
    cover += '## [>>> MOBI下载 <<<](https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.mobi)\n\n'
    cover += '{% embed url="https://github.com/dnomd343/xxrs-crawler" %}\n项目地址\n{% endembed %}\n'
    saveFile(os.path.join(releaseInfo['gitbookDir'], 'README.md'), cover)


def loadSummary(catalog: dict) -> None:
    summary = '# XXRS\n\n'
    summary += '* [序言](README.md)\n\n'
    summary += '## 内容 <a href="#content" id="content"></a>\n\n'
    for (title, mdFile) in catalog.items():
        summary += '* [%s](content/%s)\n' % (title, mdFile)
    saveFile(os.path.join(releaseInfo['gitbookDir'], 'SUMMARY.md'), summary)


def loadGitbook(jsonName: str) -> None:
    data = loadData(jsonName)
    loadCover(data['metadata'])
    catalog = loadChapters(data['content'])
    loadSummary(catalog)
    shutil.copy(
        os.path.join(rootPath, './assets/cover.jpg'),
        os.path.join(releaseInfo['gitbookDir'], './assets/cover.jpg')
    )


if __name__ == '__main__':
    initFolder()
    loadGitbook(sys.argv[1])
