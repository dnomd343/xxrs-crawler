# 栩栩若生

## [>>> 在线阅读 <<<](https://xxrs.343.re/)

## [>>> TXT下载 <<<](https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.txt)

## [>>> MOBI下载 <<<](https://res.343.re/Share/XXRS/%E6%A0%A9%E6%A0%A9%E8%8B%A5%E7%94%9F.mobi)

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
    rc-1([RC-1])
    rc-2([RC-2])
    rc-3([RC-3])
    rc-4([RC-4])
    sa --> rc-1
    sb -- fix --> rc-1
    rc-1 ==> rc-2
    rc-2 ==> rc-3
    rc-3 ==> rc-4
  end

```

### 数据来源

+ [`108shu.com`](./src/crawler/108shu.com) ：[http://www.108shu.com/book/54247/](http://www.108shu.com/book/54247/)

+ [`aidusk.com`](./src/crawler/aidusk.com) ：[http://www.aidusk.com/t/134659/](http://www.aidusk.com/t/134659/)

+ [`ixsw.la`](./src/crawler/ixsw.la) ：[https://www.ixsw.la/ks82668/](https://www.ixsw.la/ks82668/)

+ [`m.wxsy.net`](./src/crawler/m.wxsy.net) ：[https://m.wxsy.net/novel/57104/](https://m.wxsy.net/novel/57104/)

+ [`wxsy.net`](./src/crawler/wxsy.net) ：[https://www.wxsy.net/novel/57104/](https://www.wxsy.net/novel/57104/)

+ [`xswang.com`](./src/crawler/xswang.com) ：[https://www.xswang.com/book/56718/](https://www.xswang.com/book/56718/)

+ [`zhihu.com`](./src/crawler/zhihu.com) ：[https://www.zhihu.com/column/c_1553471910075449344](https://www.zhihu.com/column/c_1553471910075449344)


### 样本分析

1. 爬虫七个网站的数据，获得五份三组不同的 `raw` 样本：

+ `sample_1-a`
+ `sample_1-b`
+ `sample_2-a`
+ `sample_2-b`
+ `sample_3`

2. 经过简单合并后可得到三份初始 `combine` 样本：

+ `sample_1`
+ `sample_2`
+ `sample_3`

3. 进行对照合并，修复各类语法词汇错误、违禁屏蔽词等，得到三组 `fixed` 样本。

4. 再次合并，获得两份 `release` 样本：

+ `sample_a`
+ `sample_b`

5. 修复合并，得到 `RC` 样本。

### 内容发布

+ `RC-1` ：初始合并版本

+ `RC-2` ：修复部分屏蔽词与语法错误

+ `RC-3` ：修复繁体中文错误

+ `RC-4` ：修复标点符号错误

## 许可证

MIT ©2022 [@dnomd343](https://github.com/dnomd343)
