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
from .common import onlineDesc
from .common import projectUrl
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

    cover = '---\ndescription: 作者：%s\n---\n\n' % metadata['author']
    cover += gitbookMetadata(metadata)
    for (resName, resUrls) in resourceInfo.items():
        cover += '{% hint style="success" %}\n' \
            + '### [%s](%s)（[备用地址](%s)）\n' % (resName, resUrls[1], resUrls[0]) \
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

    cover = '---\ndescription: %s\n---\n\n' % onlineDesc
    cover += gitbookMetadata(metadata) + '<hr/>\n'
    cover += '\n{% hint style="none" %}\n'
    for (resName, resUrls) in resourceInfo.items():
        cover += '##### [%s](%s)（[备用地址](%s)）\n' % (resName, resUrls[1], resUrls[0])
    cover += '{% endhint %}\n'

    bookInfo = json.dumps({
        'title': metadata['name'],
        'author': metadata['author'],
        'description': onlineDesc,
        'language': 'zh-hans',
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
    descHeader = '---\ndescription: %s\n---\n\n' % onlineDesc
    for (chapterPath, chapterContent) in gitbookChapters(content, header = descHeader).items():
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
    chapterFolder = os.path.join(workDir, './XXRS/chapter/')
    for file in os.listdir(chapterFolder):  # compress html content
        htmlCompress(os.path.join(chapterFolder, file))
    os.system('cd %s && tar cJf %s XXRS' % (workDir, releaseInfo['static']))


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
    os.system('cd %s && zip -r xxrs.zip *' % tempDir.name)
    shutil.move(os.path.join(tempDir.name, 'xxrs.zip'), releaseInfo['calibre'])
    tempDir.cleanup()


def calibreBuild(workDir: str, suffix: str, extOption: list, metadata: dict, content: dict) -> None:
    buildDir = '/xxrs/'
    calibreImage = 'linuxserver/calibre:6.14.1'
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
    calibreDepends(workDir, metadata, content)  # generate calibre input
    os.system('cd %s && zip -r xxrs.zip *' % workDir)  # compress as zip file
    shutil.copy(
        os.path.join(rootPath, './assets/cover.jpg'),
        os.path.join(workDir, './cover.jpg')  # load ebook cover
    )
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


def setPdocMark(originFile: str, targetFile: str) -> None:
    jdkImage = 'openjdk:17-alpine'
    tempDir = tempfile.TemporaryDirectory()  # access temporary directory
    suffix = os.path.splitext(originFile)[-1]
    shutil.copy(originFile, os.path.join(tempDir.name, 'xxrs%s' % suffix))
    shutil.copy(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mobi-meta.jar'),  # script folder
        os.path.join(tempDir.name, 'mobi-meta.jar')
    )
    dockerCommand = 'docker run --rm -v %(src)s:%(tmp)s --workdir %(tmp)s --entrypoint sh %(img)s -c "%(cmd)s"' % {
        'src': tempDir.name,
        'tmp': '/xxrs/',
        'img': jdkImage,
        'cmd': 'java -jar mobi-meta.jar edit xxrs%s xxrs_mod%s --pdoc' % (suffix, suffix),
    }
    subprocess.Popen(dockerCommand, shell = True).wait()  # blocking wait
    shutil.copy(os.path.join(tempDir.name, 'xxrs_mod%s' % suffix), targetFile)
    tempDir.cleanup()


def azw3Release(metadata: dict, content: dict) -> None:
    tempDir = tempfile.TemporaryDirectory()  # access temporary directory
    print('Calibre AZW3 Build -> %s' % tempDir.name)
    calibreBuild(tempDir.name, '.azw3', ['--mobi-toc-at-start'], metadata, content)
    setPdocMark(os.path.join(tempDir.name, './xxrs.azw3'), releaseInfo['azw3'])
    tempDir.cleanup()
