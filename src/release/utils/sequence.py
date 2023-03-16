#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def jsonRelease(metadata: dict, content: dict) -> str:
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


def txtRelease(metadata: dict, content: dict) -> str:
    result = [txtMetadata(metadata)]
    for (title, chapter) in content.items():
        result.append('\n\n'.join([title] + chapter))  # combine txt content
    return '\n\n\n'.join(result) + '\n'


def htmlMetadata(metadata: dict) -> str:  # html metadata
    return '<h1>%s</h1>\n' % metadata['name'] + '\n'.join(
        ['<p>%s</p>' % x for x in metadata['desc']]
    )


def htmlRelease(metadata: dict, content: dict) -> str:
    result = [htmlMetadata(metadata)]
    for (title, chapter) in content.items():
        result.append(
            '<h2>%s</h2>\n' % title + '\n'.join(
                ['<p>%s</p>' % x for x in chapter]
            )
        )
    return '\n\n'.join(result) + '\n'
