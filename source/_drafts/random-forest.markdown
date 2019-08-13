---
title: 箱线图 & 随机森林 学习记录
tags:
---

去年的工作主要在探索监控报警的智能降噪，其实反过来就是时间序列的异常检测🤔。之前分享过 [正态分布](/blog/20190305/Anomaly-Detection/) 与 [k-means 聚类](/blog/20181004/kmeans-algorithm/)，这篇文章分享一下随机森林(Random Forests) 与 箱线图(Box plot).

虽然只是个人的一个记录，但目标是尽可能的通俗易懂，并用 Python 实践一下。

<!--more-->

# 箱线图(Box plot)
网上找了一张图，还算比较清晰：
![](/images/blog/190813_box_plot/15656717480732.jpg)
(source: https://www.leansigmacorporation.com/box-plot-with-minitab/)

## 图中变量解释
给定一堆数据，分别计算：
- **Q2(median):** 中位数
- **Q1 & Q3(25th percentile / 75th percentile):** 这个在[监控中经常用到](/blog/20190811/google-sre-reading-note/#Chapter-12-Effective-Troubleshooting-20190713)，因为平均值很多时候会误导人，例如下图耗时的监控。我理解 99th percentiles 代表，假如整体样本如果有1000个，排在第990位的那个数值。![](/images/blog/180403_google_sre/15630074932574.jpg)
- **IQR(interquartile range):** 即 `Q3 - Q1`
- **minimum:** `minimum = min(min(源数据), Q1-1.5*IQR)`，1.5 应该是个可变的参数，但说实话没太理解公式的目的是什么🤔
- **maximum:** 同上

对于 python 的计算：
```python


```


## 问题
1. 和正太分布的最大不同？...

