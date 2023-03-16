#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json

MarkdownSymbols = [
    '\\', '`', '*', '_', '~',
    '{', '}', '[', ']', '(', ')',
    '#', '+', '-', '.', '!', '|',
]


def markdownTransfer(content: str) -> str:
    for symbol in MarkdownSymbols:
        content = content.replace(symbol, '\\' + symbol)  # add `\` before symbol
    return '&emsp;&emsp;' + content  # add chinese indentation


def jsonSerialize(metadata: dict, content: dict) -> str:
    return json.dumps({
        'metadata': metadata,
        'content': content,
    }, separators = (',', ':'))  # without space


def txtMetadata(metadata: dict) -> str:  # txt metadata
    return '%s\n\n作者：%s\n\n\n%s' % (
        metadata['name'],
        metadata['author'],
        '\n\n'.join(metadata['desc']),
    )


def txtSerialize(metadata: dict, content: dict) -> str:
    result = [txtMetadata(metadata)]
    for (title, chapter) in content.items():
        result.append('\n\n'.join([title] + chapter))  # combine txt content
    return '\n\n\n'.join(result) + '\n'


def htmlMetadata(metadata: dict) -> str:  # html metadata
    return '<h1>%s</h1>\n' % metadata['name'] + '\n'.join(
        ['<p>%s</p>' % x for x in metadata['desc']]
    )


def htmlSerialize(metadata: dict, content: dict) -> str:
    result = [htmlMetadata(metadata)]
    for (title, chapter) in content.items():
        result.append(
            '<h2>%s</h2>\n' % title + '\n'.join(
                ['<p>%s</p>' % x for x in chapter]
            )
        )
    return '\n\n'.join(result) + '\n'


def gitbookMetadata(metadata: dict) -> str:
    return '---\ndescription: 作者：%s\n---\n\n# %s\n\n' % (
        metadata['author'], metadata['name']
    ) + '<figure><img src="%s" alt=""><figcaption><p>%s</p></figcaption></figure>\n\n' % (
        'assets/cover.jpg', metadata['name']
    ) + '\n>\n'.join(['> %s' % x for x in metadata['desc']]) + '\n\n'


def gitbookChapterPath(caption: str) -> str:
    chapterNum = re.search(r'^第(\d+)章', caption)[1]  # match chapter number
    chapterNum = '0' * (3 - len(chapterNum)) + chapterNum  # add `0` prefix
    return os.path.join('content', 'chapter-%s.md' % chapterNum)


def gitbookSummary(chapters: dict) -> str:
    summary = '# XXRS\n\n'
    summary += '* [序言](README.md)\n\n'
    summary += '## 内容 <a href="#content" id="content"></a>\n\n'
    for caption in chapters:
        summary += '* [%s](%s)\n' % (caption, gitbookChapterPath(caption))
    return summary


def gitbookChapters(chapters: dict) -> dict:
    result = {}
    for (caption, content) in chapters.items():
        content = [markdownTransfer(x) for x in content]
        result[gitbookChapterPath(caption)] = '# %s\n\n%s\n' % (
            caption, '\n\n'.join(content)
        )
    return result
