---
title: 《深入剖析Tomcat》之如何实现套娃🪆
categories:
  - JAVA
date: 2022-04-16 15:09:35
tags:
---

同事近期安利的一本葵花宝典，尝试阅读几章后，确实寻得一些避免面条式代码的良药。

为什么要写这篇博客？最近在读另外一本书：[《置身事内》](https://book.douban.com/subject/35546622/)，浅浅读过收获不大，但神奇的是在豆瓣编写书评的过程中，不断翻阅与总结催化了新的收获。所以尝试编写《深入剖析Tomcat》的读书小记，通过输出的方式加深理解。

<!--more-->


# 源码指南
这本书籍年代久远（2004），书籍附带源码为 jdk1.4 版本... 

强烈推荐以下宝藏仓库（支持 jdk8）：https://github.com/tengfeipu/How-Tomcat-Works 


# 读书小记
本篇主要分享“第五章 servlet 容器”的读书小记～

### org.apache.catalina.Container 
Tomcat 中的四种容器（p.s. 接口可以 extend），本章介绍如何只使用 1 个 Wrapper 实例，或 1 个 Context 实例（带多个 Wrapper 实例）的应用。
1. **Engine**：表示整个 Catalina servlet 引擎
2. **Host**：虚拟主机（一个或多个 Context 容器）
3. **Context**：一个 Web 应用程序，一个 Context 可以有多个 wrapper
4. **Wrapper**：表示一个独立的 servlet

一开始可能毫无头绪，但耐心完整阅读章节后会豁然开朗，理解为什么将亲切的将“容器”比喻为套娃 XD
![](../images/blog/2021-09-04-jvm-note/16503302866162.jpg)


### org.apache.catalina.Wrapper
首先以最底层的 Wrapper 容器为例（通常与 servlet 容器一一对应）

#### 1）类图结构
类图如下，从左往右：
1. `Loader` 负责 servlet 实例的加载（输入类名，输出实例）
2. `Wraper` 容器包含一个 `Pipeline` 用于 `Valve` 的调度执行
3. `Valve` 负责一个具体待执行的任务，同时它实现了 `Contained` 接口，支持获取对应的容器（包含 valve）

![](../images/blog/2021-09-04-jvm-note/16495549173898.jpg)

#### 2）时序调用
顺便结合上一章 `HttpConnector` 的讲解，为了处理一笔 http 调用，各个组件的交互如下：
![](../images/blog/2021-09-04-jvm-note/16495625199690.jpg)

值得一提 `PipelineValveContext#invokeNext` 的实现非常有趣，配合 `XxxValve` 递归调用，依次执行自定义与默认的 `Valve`
![](../images/blog/2021-09-04-jvm-note/16495634084412.jpg)

递归执行效果如下，例如 `ClientIPLoggerValve` 在 `invokeNext` 之前与之后，都可以执行自定义操作。 🤔 有没有觉得这个调用似曾相识？
![](../images/blog/2021-09-04-jvm-note/16495647257469.jpg)

不禁让人想起 python Django 框架的 middleware 实现，有种异曲同工的感觉。
![](../images/blog/2021-09-04-jvm-note/16495648804556.jpg)

但 Django 的实现可是更加“简单”一些 ：）
```python
# 定义 middleware 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

class SessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ...
    def process_response(self, request, response):
        ...

# 框架加载 middleware
self._view_middleware = []
self._template_response_middleware = []
self._exception_middleware = []

if hasattr(mw_instance, "process_view"):
    self._view_middleware.insert(
        0,
        self.adapt_method_mode(is_async, mw_instance.process_view),
    )
if hasattr(mw_instance, "process_template_response"):
    self._template_response_middleware.append(
        self.adapt_method_mode(
            is_async, mw_instance.process_template_response
        ),
    )
```


### org.apache.catalina.Context

#### 类图结构
一个 Context 包含多个 Wrapper 容器
![](../images/blog/2021-09-04-jvm-note/16495652434613.jpg)

#### 时序调用
建议理清类图后阅读源码，debug 一笔 http 请求的交互，盗一张较清晰的图：
![](../images/blog/2021-09-04-jvm-note/16495812116720.jpg)

### 总结
阅读本章后，感悟 tomcat 的核心在于各个「容器」并非独立的存在，而如名字一般，好比“套娃”各司其职。

最终通过分层，实现各司其职+单向依赖，降低了整体应用的复杂度。

### 参考
1. https://my.oschina.net/luozhou/blog/3103710