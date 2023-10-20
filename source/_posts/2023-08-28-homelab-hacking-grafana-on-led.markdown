---
title: "Homelab hacking: Grafana on an LED matrix display"
categories:
  - 智能家居
date: 2023-08-28 00:21:01
tags:
---

周末翻看 GrafanaCON 2023 的视频消磨时间，偶遇一个有趣的“节目”：[《Homelab hacking: Grafana on an LED matrix display》](https://grafana.com/about/events/grafanacon/2023/session/time-series-visualization-on-led-display/?src=ggl-s&mdm=cpc&cnt=99878325494&camp=b-grafana-exac-amer&trm=grafana&plcmt=learn-nav)（将智能家居的 Grafana metric 数据展示到 32x8 的 LED 矩阵显示屏上）。

这种事只是想想就很兴奋！趁着周末实践玩一下～

<!--more-->

![overview](../images/blog/2021-09-04-jvm-note/overview.jpg)

## TOC
- [TOC](#toc)
- [硬件准备](#硬件准备)
- [软件入门](#软件入门)
- [实现原理](#实现原理)
  - [第一步：metric 指标准备](#第一步：metric指标准备)
  - [第二步：单片机初始化](#第二步：单片机初始化)
  - [第三步：用户更新配置](#第三步：用户更新配置)
  - [第四步：指标查询&展示](#第四步：指标查询展示)
- [总结](#总结)
- [最终效果](#最终效果)

## 硬件准备

1. [必选] ESP32 开发板一枚，本文使用 `Espressif ESP32-C3-DevKitM-1`
2. [必须] 32x8 LED 面板（WS2812B）
3. [必选] 杜邦线（公对母），用于连接开发板排针和 LED 面板
4. [可选] 天线
5. [可选] 开发板盒子

开发板非常小巧，像一件精美的艺术品，竟然是上海一家公司研发的（乐鑫科技）

## 软件入门

直接使用 vscode PlatformIO 插件进行开发。

推荐食用下面的 hello world 视频快速入门：

<iframe width="560" height="315" src="https://www.youtube.com/embed/tc3Qnf79Ny8?si=WpN7iNJA51FAhTjm" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## 实现原理

项目地址：https://github.com/grafana/esp32-metrics-matrix

将代码 flash 至 ESP32 硬件后，整体时序交互如下：
![](../images/blog/2021-09-04-jvm-note/16931507619271.jpg)

### 第一步：metric 指标准备

将智能家居的温度/湿度等指标，用 Grafana agent 上传至 Grafana Cloud，供后续每分钟抓取展示。

参考之前的分享：[《如何构建家庭监控大盘》](/blog/20220327/smart-home-dashboard/)

### 第二步：单片机初始化

Arduino（硬件开发框架）提供了两个 spi 供实现：

- `setup` 在硬件 boot 时执行一次
- `loop` 顾名思义循环执行

这一步 `setup` 除了初始化 `PromClient`，还创建了一个 http server。

### 第三步：用户更新配置

接上一步 http server，作者用 gpt 编写了一个前端页面，方便用户动态控制部分配置：
![](../images/blog/2021-09-04-jvm-note/16931506456594.jpg)

### 第四步：指标查询&展示

每分钟抓取最新的 metric 指标，并在 led 面板上展示：
![](../images/blog/2021-09-04-jvm-note/16931521726946.jpg)

整体链路：小米温度计 -> Home Assistant -> Grafana Agent -> Grafana Cloud -> ESP32 -> LED
![overview](../images/blog/2021-09-04-jvm-note/overview.jpg)

## 总结

第一次接触 ESP32 硬件，玩的也很过瘾。

特别是设备通电的一瞬间，看见屏幕跳出的网络通知，突然有种奇妙的感觉：仿佛家庭中多了一个亲切的新成员 :)
<image src="/images/blog/2021-09-04-jvm-note/16931514491369.jpg" width="300">

期望未来有时间继续折腾，给大家分享更多有趣的实践~

## 最终效果

书房一开门，一股粉红的迷人气息扑面而来，太酷啦！
![1 -6-](../images/blog/2021-09-04-jvm-note/1%20-6-.png)

![](../images/blog/2021-09-04-jvm-note/16931395653162.jpg)
