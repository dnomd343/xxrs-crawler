# 栩栩若生

```mermaid
  graph LR
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

      s1a_raw -- replenish --> s1_combine
      s1b_raw --> s1_combine
      s2a_raw -- replenish --> s2_combine
      s2b_raw -- replenish --> s2_combine
      s3_raw -- clean up --> s3_combine

      s1_combine -- fix --> s1_fixed
      s2_combine -- fix --> s2_fixed
      s3_combine -- fix --> s3_fixed
    end

    subgraph crawler
      source_1([108shu.com]) --> s1a_raw
      source_2([aidusk.com]) --> s1b_raw
      source_3([ixsw.la]) --> s1b_raw
      source_4([m.wxsy.net]) --> s2a_raw
      source_5([wxsy.net]) --> s2a_raw
      source_6([xswang.com]) --> s2b_raw
      source_7([zhihu.com]) --> s3_raw
    end
```


## 数据爬虫来源

+ [`108shu.com`](./src/crawler/108shu.com) ：[`http://www.108shu.com/book/54247/`](http://www.108shu.com/book/54247/)

+ [`aidusk.com`](./src/crawler/aidusk.com) ：[`http://www.aidusk.com/t/134659/`](http://www.aidusk.com/t/134659/)

+ [`ixsw.la`](./src/crawler/ixsw.la) ：[`https://www.ixsw.la/ks82668/`](https://www.ixsw.la/ks82668/)

+ [`m.wxsy.net`](./src/crawler/m.wxsy.net) ：[`https://m.wxsy.net/novel/57104/`](https://m.wxsy.net/novel/57104/)

+ [`wxsy.net`](./src/crawler/wxsy.net) ：[`https://www.wxsy.net/novel/57104/`](https://www.wxsy.net/novel/57104/)

+ [`xswang.com`](./src/crawler/xswang.com) ：[`https://www.xswang.com/book/56718/`](https://www.xswang.com/book/56718/)

+ [`zhihu.com`](./src/crawler/zhihu.com) ：[`https://www.zhihu.com/column/c_1553471910075449344`](https://www.zhihu.com/column/c_1553471910075449344)
