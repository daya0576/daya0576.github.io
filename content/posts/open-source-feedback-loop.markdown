---
title: 为什么个人开源项目让我感到兴奋
date: 2024-11-16 11:02:16
tags:
categories:
- 个人相关
---

Hi 好久不见～ 最近几个月沉迷于与游戏《Against The Storm》，与开发一款 web app，叫做：[Beaver Habit Tracker](https://github.com/daya0576/beaverhabits)

开发个人开源项目的过程，就如同我新购入的 Mac Mini 在导出 4K 视频时，跑满了 GPU 并忍不住开始兴奋的吼叫！

<!--more-->

# Globalization
项目从一开始，便通过全英文与开源的方式，尝试面向全球用户群体。

Demo 页面部署在 fly.io 中，从下图中 edge 边缘节点流量监控，不难看出，确实成功触达了全球用户。
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
而更加难得可贵的是，开发过程中，通过社区用户反馈的需求与问题，持续打磨优化产品。

包含但不限于：[daya0576/beaverhabits/issues](https://github.com/daya0576/beaverhabits/issues?q=is%253Aissue+)

- Import from existing setup, e.g. uhabit:
- Everyone can sign up
- Cannot order them
- To add standalone mode for iOS 
- Add docker images for `arm`, `arm/v7`, `amd`, `amd64/v3`, ...
- ...

以最后一点 docker image 为例，一开始简单本地构建镜像并 push 至 docker hub。

但后续用户反馈在 amd 甚至 amd/v3 的机器中不适配，所以通过 github action 自动构建了对应架构镜像并发布。

再后来甚至有用户直接贡献了 raspberry pi 对应的构建代码：[Add Dockerfile for arm32 build (raspberry pi3 and below) #12](https://github.com/daya0576/beaverhabits/pull/12)

# Challenges
当然在开发的过程中，也遇到了大大小小的挑战。

例如项目通过 pure python 实现，底层使用的框架叫做 [nicegui](https://nicegui.io/)。

该框架对应的设计哲学为 `backend-first`，也就是说所有的代码实现以及交互逻辑，都是通过后端实现。举个例子，点击下拉菜单，也需要通过 websocket 与后端交互后，再在前端渲染内容..

这种方式如同 GIL 一样简化了复杂度，但同时牺牲了性能。对于 nicegui 来说，较高的网络延迟将会严重影响用户的体验 🤔

小小的脑袋转念一想，将 beaver habit tracker 定位为 **selfhosted app**，既保护个人数据隐私，又解决了性能的问题。瞬间化腐朽为神奇。

同时通过 selfh.st newsletter，收获了一波流量。

# Future
开源项目通过互帮互助带来持久的成就感，如果进而一步通过提供价值来创造物质收入，将是未来进一步探索的方向。

---

Here is the streak of my table tennis training records :)
![](../images/blog/2021-09-04-jvm-note/17317247576292.jpg)
