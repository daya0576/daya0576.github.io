---
title: Java BlockingQueue 学习小记
tags:
---

最近一周作息发生了一些微妙的变化，晚上 11 点睡觉清晨 7 点自然醒，身体状况明显好转的同时，也明白了什么叫做一天之际在于晨：起床后去门口吃麦当劳早餐的同时，看一会书，感觉一天多活了一个多小时。

这篇文章简单记录今早 java BlockingQueue 学习小记～

<!--more-->

# Intro
BlockingQueue 是 `java.util.concurrent` 中的一个接口。顾名思义 Queue 代表先进先出的队列，多个线程同时放入对象而其他线程获取对象，Blocking 则代表队列满了或者为空时，尝试放入或获取元素的线程会进入 `BLOCKED` 阻塞状态。 

该数据结构的好处在于完全解耦输入与输出，

![](media/16407822029714.jpg)

# 接口方法
![](media/16407823699079.jpg)

官方文档解释的很清楚，以获取队列第一个元素为例（如果队列为空）：

- `remove()`: 立即抛出异常 java.util.NoSuchElementException
- `poll()`: 立即返回 null
- `take()`: waiting if necessary
- `pull(timeout, unit)`: waiting + timeout

p.s. Special value 特殊值指的 false/null 等.. 

# 接口实现


