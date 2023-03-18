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


def htmlCompress(file: str) -> None:
    rawHtml = open(file).read().split('\n')
    with open(file, 'w') as fileObj:
        fileObj.write('\n'.join([x.strip() for x in rawHtml if x.strip() != '']) + '\n')


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
    os.rename(os.path.join(workDir, '_book'), os.path.join(workDir, 'XXRS'))
    htmlCompress(os.path.join(workDir, './XXRS/index.html'))
    os.chdir(os.path.join(workDir, './XXRS/chapter/'))
    for file in os.listdir():  # compress html content
        htmlCompress(file)
    os.chdir(workDir)
    os.system('tar cJf %s XXRS' % releaseInfo['static'])


def staticRelease(metadata: dict, content: dict) -> None:
    if not isRoot():
        print('\033[0;33mDue to the permission problems, it is recommended to run under root user.\033[0m')
        return
    tempDir = tempfile.TemporaryDirectory()  # access temporary directory
    staticDepends(tempDir.name, metadata, content)
    staticBuild(tempDir.name)
    tempDir.cleanup()


def calibreDepends(workDir: str, metadata: dict, content: dict) -> None:
    metaInfo = [
        '<?xml version="1.0"?>',
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">',
        '<rootfiles>',
        '<rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>',
        '</rootfiles>',
        '</container>',
    ]
    opfInfo = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uuid_id">',
        '<opf:metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">',
        '<dc:title>%s</dc:title>' % metadata['name'],
        '<dc:language>zho</dc:language>',
        '<dc:publisher>Dnomd343</dc:publisher>',
        '<dc:creator opf:file-as="%(aut)s" opf:role="aut">%(aut)s</dc:creator>' % {'aut': metadata['author']},
        '<dc:contributor opf:file-as="calibre" opf:role="bkp">%s</dc:contributor>' % projectUrl,
        '<dc:description>%s</dc:description>' % '&lt;div&gt;%s&lt;/div&gt;' % (
            ''.join(['&lt;p&gt;%s&lt;/p&gt;' % x for x in metadata['desc']])
        ),
        '<meta name="calibre:author_link_map" content="{&quot;%s&quot;: &quot;&quot;}"/>' % metadata['author'],
        '<meta name="calibre:title_sort" content="%s"/>' % metadata['name'],
        '</opf:metadata>',
        '<manifest>',
        '<item id="html" href="xxrs.html" media-type="application/xhtml+xml"/>',
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '</manifest>',
        '<spine toc="ncx">', '<itemref idref="html"/>', '</spine>',
        '</package>',
    ]
    createFolder(os.path.join(workDir, 'META-INF'))
    saveFile(os.path.join(workDir, 'mimetype'), 'application/epub+zip')
    saveFile(os.path.join(workDir, 'content.opf'), '\n'.join(opfInfo) + '\n')
    saveFile(os.path.join(workDir, 'xxrs.html'), htmlSerialize(metadata, content))
    saveFile(os.path.join(workDir, 'META-INF', 'container.xml'), '\n'.join(metaInfo) + '\n')


def calibreRelease(metadata: dict, content: dict) -> None:
    tempDir = tempfile.TemporaryDirectory()  # access temporary directory
    calibreDepends(tempDir.name, metadata, content)
    os.chdir(tempDir.name)
    os.system('zip -qr %s *' % releaseInfo['calibre'])
    tempDir.cleanup()


def calibreBuild(workDir: str, suffix: str, extOption: list, metadata: dict, content: dict) -> None:
    buildDir = '/xxrs/'
    calibreImage = 'linuxserver/calibre'
    calibreCommand = [
        'ebook-convert',
        'xxrs.zip', 'xxrs%s' % suffix,
        '--output-profile=generic_eink',
        '--level1-toc=\'//h:h2\'',
        '--cover=cover.jpg',
        '--toc-title=目录',
        '--remove-paragraph-spacing',
        '--remove-paragraph-spacing-indent-size=2',
        '--verbose',
    ]
    buildCommand = 'docker run --rm -t -v %s:%s --workdir %s --entrypoint bash %s -c "%s"' % (
        workDir, buildDir, buildDir, calibreImage, ' '.join(calibreCommand + extOption)
    )
    shutil.copy(  # ebook cover
        os.path.join(rootPath, './assets/cover.jpg'),
        os.path.join(workDir, './cover.jpg')
    )
    os.chdir(workDir)
    calibreDepends(workDir, metadata, content)
    os.system('zip -qr xxrs.zip *')  # generate calibre input format
    subprocess.Popen(buildCommand, shell = True).wait()  # blocking wait


def epubRelease(metadata: dict, content: dict) -> None:
    tempDir = tempfile.TemporaryDirectory()  # access temporary directory
    print('Calibre EPUB Build -> %s' % tempDir.name)
    calibreBuild(tempDir.name, '.epub', [], metadata, content)
    shutil.copy(os.path.join(tempDir.name, './xxrs.epub'), releaseInfo['epub'])
    tempDir.cleanup()


# MOBI Type: KF7 = 0 (old) / KF7 + KF8 = 1 (both) / KF8 = 2 (new)
def mobiRelease(metadata: dict, content: dict, mobiType: int = 1) -> None:
    mobiOption = ['--mobi-toc-at-start']
    if mobiType == 0:
        mobiOption.append('--mobi-file-type=old')
    elif mobiType == 1:
        mobiOption.append('--mobi-file-type=both')
    elif mobiType == 2:
        mobiOption.append('--mobi-file-type=new')
    else:
        print('Unknown MOBI type')
        return
    tempDir = tempfile.TemporaryDirectory()  # access temporary directory
    print('Calibre MOBI Build -> %s' % tempDir.name)
    calibreBuild(tempDir.name, '.mobi', mobiOption, metadata, content)
    shutil.copy(os.path.join(tempDir.name, './xxrs.mobi'), releaseInfo['mobi'])
    tempDir.cleanup()


def azw3Release(metadata: dict, content: dict) -> None:
    tempDir = tempfile.TemporaryDirectory()  # access temporary directory
    print('Calibre AZW3 Build -> %s' % tempDir.name)
    calibreBuild(tempDir.name, '.azw3', ['--mobi-toc-at-start'], metadata, content)
    # TODO: change `[EBOK]` as `[PDOC]`
    shutil.copy(os.path.join(tempDir.name, './xxrs.azw3'), releaseInfo['azw3'])
    tempDir.cleanup()
