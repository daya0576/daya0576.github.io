---
title: "[开源] 为什么个人开源项目让我感到兴奋"
date: 2024-11-16 11:02:16
tags:
categories:
- 独立开发
- 编程
- PYTHON
---

Hi 好久不见～ 最近几个月沉迷于与游戏《Against The Storm》，与开发一款 web app，叫做：[Beaver Habit Tracker](https://github.com/daya0576/beaverhabits)

开发个人开源项目的过程，就如同我新购入的 Mac Mini 在导出 4K 视频时，跑满了 GPU 并忍不住开始兴奋的吼叫！

<!--more-->

![](/images/blog/2021-09-04-jvm-note/17353550144918.jpg)

# Globalization
项目从一开始，便通过全英文与开源的方式，尝试面向全球用户群体。

Demo 页面目前部署在 [fly.io](https://fly.io/) 中。在过去一个月中，通过 [umami](https://umami.is/) 统计可以看到，已有超过 90 个国家的用户访问：
- France: 28%
- United States: 20%
- Germany: 8%
- Canada: 5%
- Japan: 4%
- India: 3%
- ...

同时从下图中 edge 节点流量监控，不难看出，确实成功触达了全球用户。

![](/images/blog/2021-09-04-jvm-note/17317273177416.jpg)

# Feedback Loop

## Positive
起初开发的目的或许只是用于个人记录，但孵化的这个美丽的废物，竟意外收获了很多人类的认可 <3
```shell
# Reddit - /r/Python/
Love seeing more NiceGUI in the wild!

And great job i like that is simple and aesthetic and not overwhelmed with soo much options.

I love this idea. I like the simplicity and the lack of ‘Goals’, which always trigger me.


# Reddit - /r/selfhosted/
Cool app !

Saving and will try later. Thanks for sharing!

Would be cool to see the streaks. Good job btw!

kind of looks like uhabits on android. It was great app but it was only limited to single platform. There was no option for sync. So you always need to have your phone around you. It was a bummer for me.
Your app has a Webapp which is great !!

Very cool, thanks for sharing

Both this and Loop Habit Tracker are exactly what I was looking for. Well done. Oh, and dope choice of name. I also put a ton of time into that game, haha.


# Github Discussion
Loving your application so far! There is no satisfactory self hosted habit app until yours! 
```

## Issues
而更加难得可贵的是，开发过程中，通过社区用户反馈的需求与问题，持续对产品进行打磨和优化。

包含但不限于：[daya0576/beaverhabits/issues](https://github.com/daya0576/beaverhabits/issues?q=is%253Aissue+)

- Import from existing setup, e.g. uhabit:
- Everyone can sign up
- Cannot order them
- To add standalone mode for iOS 
- Center the page so it works on desktop web as well
- Add a total number of a habit completed to the right of today?
- API documentation
- Add docker images for `arm`, `arm/v7`, `amd`, `amd64/v3`, ...
- ...

以最后一点 docker image 为例，一开始简单本地构建镜像并 push 至 docker hub。

但后续用户反馈在 amd 甚至 amd/v3 的机器中不适配，所以通过 github action 自动构建了对应架构镜像并发布：[.github/workflows/publish.yml#L14](https://github.com/daya0576/beaverhabits/blob/c012577267047527362cfc0c9cfc17003b9212af/.github/workflows/publish.yml#L14)

再后来甚至有用户直接贡献了 raspberry pi 对应的构建代码：[Add Dockerfile for arm32 build (raspberry pi3 and below) #12](https://github.com/daya0576/beaverhabits/pull/12)

# Challenges
当然在开发的过程中，也遇到了大大小小的挑战。

例如项目通过 pure python 实现，底层使用的框架为 [nicegui](https://nicegui.io/)。

该框架对应的设计哲学为 `backend-first`，也就是说所有的代码实现以及交互逻辑，都是通过后端实现。举个例子，点击下拉菜单，也需要通过 websocket 与后端交互后，再在前端渲染内容..

这种方式如同 GIL 一样简化了复杂度，但同时牺牲了性能。所以较高的网络延迟可能会严重影响用户的体验 🤔

小小的脑袋转念一想，将 beaver habit tracker 定位为 **selfhosted app**，既保护个人数据隐私，又解决了性能的问题。瞬间化腐朽为神奇。

同时通过 selfh.st newsletter，收获了一波流量：

![](/images/blog/2021-09-04-jvm-note/17335353503792.jpg)

# Lessons Learned

## Elevator Pitch
相比于开发代码，如何运营开源项目毫不简单，例如取个好名字，拥有一个朗朗上口的域名，实际就成功了一半。

> An elevator pitch, elevator speech, lift speech, or elevator statement is a short description of an idea, product, or company that explains the concept in a way such that any listener can understand it in a short period of time.

而在论坛中宣传自己的产品时，千万提醒自己用户像一张白纸一无所知，关键在于在第一句话中让受众立即了解你的产品。

# Future

## Open API
Beaver Habits 作为一款 minimalist 的 web app，未来除了用户提出的 issue，暂时不会新增过于复杂的功能。但会提供一套开放的 Open API，供第三方集成。

有趣的是，就在这个想法提出的当天，用户也提出了类似需求 issue [#25](https://github.com/daya0576/beaverhabits/issues/25) :)

## Make Money in Your Sleep
开源项目通过互帮互助带来持久的成就感，如果进而一步通过提供价值来创造物质收入，将是未来进一步探索的方向。

---

Here is the streak of my table tennis training records :)

![](/images/blog/2021-09-04-jvm-note/17317247576292.jpg)
