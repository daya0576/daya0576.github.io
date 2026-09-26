---
title: "读 Python behind the scenes #6: how Python object system works"
date: 2026-09-06T09:37:20+08:00
draft: true
categories:
- Python behind the scenes
- Python
series:
- CPython
---

碎碎念：上周六参加了 pycon 2026，令人印象深刻的是：语言特性的分会场有两位高中生嘉宾，最火热的话题是 free threading。但相比 Agent 分会场的座无虚席，这边显得过分冷清，倒是令人嘘唏。

> https://tenthousandmeters.com/blog/python-behind-the-scenes-6-how-python-object-system-works/

从第一天学习 Python 开始，我们便知道 Python 中万物皆对象，这篇文章将介绍 Python 对象的实现原理。

## 背景

想象下面的一段代码：

```python
def f(x):
    return x + 7
```

第一眼猜测
