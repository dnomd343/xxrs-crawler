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


def htmlSerialize(metadata: dict, content: dict) -> str:
    htmlContent = [
        '<?xml version=\'1.0\' encoding=\'utf-8\'?>',
        '<html xmlns="http://www.w3.org/1999/xhtml">',
        '<head>', '<title>%s</title>' % metadata['name'],
        '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>',
        '</head>', '<body>', '<h1>%s</h1>' % metadata['name'],
    ]
    htmlContent += ['<p>%s</p>' % x for x in metadata['desc']]
    for (caption, chapter) in content.items():
        htmlContent.append('<h2>%s</h2>' % caption)
        htmlContent.append('\n'.join(['<p>%s</p>' % x for x in chapter]))
    htmlContent += ['</body>', '</html>']
    return '\n'.join(htmlContent) + '\n'


def gitbookMetadata(metadata: dict) -> str:
    return ''.join([
        '# %s\n\n' % metadata['name'],
        '<figure style="text-align:center">',
        '<img src="%s" alt=""><figcaption>' % 'assets/cover.jpg',
        '<p>%s</p></figcaption></figure>\n\n' % metadata['name'],
        '\n>\n'.join(['> %s' % x for x in metadata['desc']]) + '\n\n',
    ])


def gitbookChapterPath(caption: str) -> str:
    chapterNum = re.search(r'^第(\d+)章', caption)[1]  # match chapter number
    chapterNum = '0' * (3 - len(chapterNum)) + chapterNum  # add `0` prefix
    return os.path.join('chapter', '%s.md' % chapterNum)


def gitbookSummary(chapters: dict) -> str:
    summary = '# XXRS\n\n'
    summary += '* [序言](README.md)\n\n'
    summary += '## 内容 <a href="#content" id="content"></a>\n\n'
    for caption in chapters:
        summary += '* [%s](%s)\n' % (caption, gitbookChapterPath(caption))
    return summary


def gitbookChapters(chapters: dict, header: str = '') -> dict:
    result = {}
    for (caption, content) in chapters.items():
        content = [markdownTransfer(x) for x in content]
        result[gitbookChapterPath(caption)] = header + '# %s\n\n%s\n' % (
            caption, '\n\n'.join(content)
        )
    return result
