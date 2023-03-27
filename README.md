# 《栩栩若生》电子书

### >>> [在线阅读](https://cdn.dnomd343.top/xxrs/online/) <<<（[备用地址](https://xxrs.343.re/)）

### >>> [TXT下载](https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.txt) <<<（[备用地址](https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.txt)）

### >>> [EPUB下载](https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.epub) <<<（[备用地址](https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.epub)）

### >>> [MOBI下载](https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.mobi) <<<（[备用地址](https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.mobi)）

### >>> [AZW3下载](https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.azw3) <<<（[备用地址](https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.azw3)）

---

> MP3/MP4 等设备请选择 TXT 格式，使用 USB 导入的 Kindle 用户请选择 AZW3 格式，其他电子阅读器及使用 Kindle 邮箱推送的用户请选择 EPUB 格式。

## 编者序

初读《栩栩若生》时，我曾给自己许诺过，若是结局皆大欢喜，就将这本小说整理发布出来，于是就有了这个项目。

小说在各个网文平台上参差不齐，章节内容均有缺失错误。项目从七个不同网站上爬取数据，相互对照，修复合并，得到了初始样本；修复逻辑可以参照自述文件的流程图，具体细节可以查阅 Commit 树记录。

再者，借助代码进行自然语言检查，对原文中大量的防屏蔽词，例如警察、政审、刀枪之类的词语，还有错误的标点符号、词法语法、繁体字以及错别字等进行修正，前前后后共有千余处。

整合后的内容也由代码格式化发布，基于 GitBook 实现在线阅读，同时提供了多种格式的电子书，适配各类电子阅读器。此外，资源文件中也提供了原始的 JSON 数据，可供下游项目二次发布。

最后，Just enjoy it！

## 整合流程

```mermaid
  graph LR

  subgraph crawler
    source_1([108shu.com])
    source_2([aidusk.com])
    source_3([ixsw.la])
    source_4([m.wxsy.net])
    source_5([wxsy.net])
    source_6([xswang.com])
    source_7([zhihu.com])
  end

  subgraph sample
    subgraph raw
      s1a_raw{{sample_1-a}}
      s1b_raw{{sample_1-b}}
      s2a_raw{{sample_2-a}}
      s2b_raw{{sample_2-b}}
      s3_raw{{sample_3}}
    end

    subgraph combine
      s1_combine[sample_1]
      s2_combine[sample_2]
      s3_combine[sample_3]
    end

    subgraph fixed
      s1_fixed(sample_1)
      s2_fixed(sample_2)
      s3_fixed(sample_3)
    end

    subgraph replenish
      sa{{sample_a}}
      sb{{sample_b}}
    end

    source_1 ==> s1a_raw
    source_2 ==> s1b_raw
    source_3 ==> s1b_raw
    source_4 ==> s2a_raw
    source_5 ==> s2a_raw
    source_6 ==> s2b_raw
    source_7 ==> s3_raw

    s1a_raw -- replenish --> s1_combine
    s1b_raw --> s1_combine
    s2a_raw -- replenish --> s2_combine
    s2b_raw -- replenish --> s2_combine
    s3_raw -- clean up --> s3_combine

    s1_combine -- fix --> s1_fixed
    s2_combine -- fix --> s2_fixed
    s3_combine -- fix --> s3_fixed

    s1_fixed --> sa
    s2_fixed -- replenish --> sa
    s2_fixed -. restore .-> sb
    s3_fixed -- replenish --> sb
  end

  subgraph release
    rc([RC version])
    sa --> rc
    sb -- fix --> rc
  end

```

<details>

<summary>展开</summary>

### 数据来源

+ [`108shu.com`](./src/crawler/108shu.com) ：[http://www.108shu.com/book/54247/](http://www.108shu.com/book/54247/)

+ [`aidusk.com`](./src/crawler/aidusk.com) ：[http://www.aidusk.com/t/134659/](http://www.aidusk.com/t/134659/)

+ [`ixsw.la`](./src/crawler/ixsw.la) ：[https://www.ixsw.la/ks82668/](https://www.ixsw.la/ks82668/)

+ [`m.wxsy.net`](./src/crawler/m.wxsy.net) ：[https://m.wxsy.net/novel/57104/](https://m.wxsy.net/novel/57104/)

+ [`wxsy.net`](./src/crawler/wxsy.net) ：[https://www.wxsy.net/novel/57104/](https://www.wxsy.net/novel/57104/)

+ [`xswang.com`](./src/crawler/xswang.com) ：[https://www.xswang.com/book/56718/](https://www.xswang.com/book/56718/)

+ [`zhihu.com`](./src/crawler/zhihu.com) ：[https://www.zhihu.com/column/c_1553471910075449344](https://www.zhihu.com/column/c_1553471910075449344)

### 样本处理

+ 爬虫获得五份 [`raw`](./sample/raw/) 样本：

  + `sample_1-a`
  + `sample_1-b`
  + `sample_2-a`
  + `sample_2-b`
  + `sample_3`

+ 简单合并后获得三份 [`combine`](./sample/combine/) 样本：

  + `sample_1`
  + `sample_2`
  + `sample_3`

+ 对照修复错误，获得三组 [`fixed`](./sample/fixed/) 样本。

+ 合并样本，获得两组 [`replenish`](./sample/replenish/) 样本：

  + `sample_a`
  + `sample_b`

+ 修复合并，得到 [`RC`](./release/) 样本。

### 内容发布

+ `RC-1` ：初始合并版本

+ `RC-2` ：修复部分屏蔽词与语法错误

+ `RC-3` ：修复繁体中文错误

+ `RC-4` ：修复标点符号错误

+ `RC-5` ：错误修复及发布样式增强

</details>

## 资源说明

### 在线阅读

项目提供了在线阅读支持，有[主地址](https://cdn.dnomd343.top/xxrs/online/)和[备地址](https://xxrs.343.re/)两个入口，前者部署在个人服务器上，使用 CDN 加速访问，后者托管在 Gitbook 服务器上。由于 Gitbook 在国内没有网络服务支持，访问流量将绕行多个地区，因此国内直接访问时加载缓慢；同时，为了更精美的 UI 风格，官方加入了相当多的加载项，在部分设备上阅读可能出现卡顿。相比之下，主地址轻量化且有 CDN 加速支持，国内用户体验更佳。

发布的资源文件中，`XXRS.tar.xz` 为静态网页数据，您可以将其部署在自己服务器上，可以达成与主地址相同的访问效果。

### 本地阅读

项目共导出四种电子书格式，分别为 `TXT` 、`EPUB` 、`MOBI` 和 `AZW3`。前者适用于 MP3/MP4 等简易设备，后三者为常见的电子书格式。EPUB 是通用电子书格式，适用于绝大多数设备，非 Kindle 用户选择它即可。MOBI 和 AZW3 是 Kindle 设备使用的格式：MOBI 分为 KF7 和 KF8 两种编码，前者兼容性好，后者支持更多新功能；AZW3 本质上为添加了 DRM 支持的 KF8 编码 MOBI，是目前 Kindle 的主流格式。

为了保证兼容性，本项目发布的 MOBI 文件同时包含了 KF7 和 KF8 编码，兼容旧版本的 Kindle 设备（未升级固件的 KPW3 以前版本）。新版本 Kindle 建议使用 AZW3 格式，其文件体积更小，支持自定义字体，且发布时已经将 CDE 元数据标记为 PDOC，可以保证封面正常显示。此外，亚马逊的邮箱推送服务在 2022 年 8 月以后停止了对 MOBI 的支持，转向了 EPUB 格式，因此 Kindle 用户使用邮箱推送时请选择后者。

### 其他资源

为了方便代码处理，项目将原始数据序列化导出为 JSON 格式，即 `XXRS.json` 文件，包含了书籍元数据和内容，您可以自行编程导出其他电子书格式。

您可以在文首链接或 Release 页面下载资源，链接中主地址通过 CDN 网络访问，备用地址直连 FTP 服务器下载。在线阅读和资源下载主地址均配置在 `cdn.dnomd343.top` 域名下，其在 DNS 解析上分流为国内和境外两套服务，国内使用阿里云 CDN 加速，境外使用 Cloudflare 加速。

### 下载链接

+ 栩栩若生 在线阅读：[`https://cdn.dnomd343.top/xxrs/`](https://cdn.dnomd343.top/xxrs/online/)

+ 栩栩若生 TXT下载：[`https://cdn.dnomd343.top/xxrs/栩栩若生.txt`](https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.txt)

+ 栩栩若生 EPUB下载：[`https://cdn.dnomd343.top/xxrs/栩栩若生.epub`](https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.epub)

+ 栩栩若生 MOBI下载：[`https://cdn.dnomd343.top/xxrs/栩栩若生.mobi`](https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.mobi)

+ 栩栩若生 AZW3下载：[`https://cdn.dnomd343.top/xxrs/栩栩若生.azw3`](https://cdn.dnomd343.top/xxrs/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.azw3)

## 许可证

MIT ©2022 [@dnomd343](https://github.com/dnomd343)
