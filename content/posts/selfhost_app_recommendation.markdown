---
title: "自托管服务推荐（持续更新）"
date: 2025-06-07T13:52:51+08:00
categories:
- 硬件
toc: true
---

自从失业后，博主逐步取消了所有的付费订阅服务，尽可能改用开源自托管服务（Self-Hosted）。

# 2025年6月
## 个人相册：Apple Photos -> Immich
虽然对苹果公司可靠性保持信心，但无法避免由于个人误操作导致的数据丢失，以及 iCloud 容量限制令人如坐针毡 :( 

Immich 作为炙手可热的相册管理服务，不论是易用性以及更新速度都无可挑剔。几个细节：支持通过手机备份共享相册，丝滑地开启显卡硬件加速，以及自定义模型供人脸识别与元信息提取。

![](/images/blog/global/17492776677961.jpg)

更有趣的是它的收费模式：不设置任何的 Paywall。但是，极佳的用户体验以及快速的迭代更新，反而让博主义无反顾付费支持🤑：

![5401A5FB-903F-471D-9836-C5B9F3F37187_1_105_c](/images/blog/global/5401A5FB-903F-471D-9836-C5B9F3F37187_1_105_c.jpeg)

## 音乐库：Apple Music -> Navidrome (substreamer)
Navidrome 作为一个 go 编写的服务端通过 web 访问，但它兼容所有的 [Subsonic/Airsonic 客户端](https://www.navidrome.org/docs/overview/#apps)！个人目前选择 substreamer 作为苹果客户端。

虽然盗版不光彩，但相信周杰伦不会责怪一个失业的可怜虫吧 ^^

![](/images/blog/global/17492774629210.jpg)

## 摄像头监控：Shinobi
近期家中多了一位新成员👶，需要在次卧中设置摄像头，相比于人民币 300+ 原生支持 HomeKit 的 Aqara 摄像头，这次我选择了更为平民的 TP-LINK 摄像头。

两条链路如下：
- TP-LINK -> (ONVIF协议) -> Home Assistant -> HomeKit 家人共享
- TP-LINK -> (ONVIF协议) -> Shinobi（异常检测/保存录像）

![](/images/blog/global/17492781324835.jpg)

## 习惯跟踪：Beaver Habit Tracker
这是一款基于 Python 开发的自部署习惯追踪 web 应用，帮助用户轻松记录和管理日常习惯。它提供适配移动端的直观界面，专注于习惯的持续养成，而非单纯追求目标达成，让养成好习惯变得更自然。

项目主页：[daya0576/beaverhabits](https://github.com/daya0576/beaverhabits)

![](/images/blog/global/17492807249546.jpg)


## 硬件服务监控：Beszel
一款轻量级开箱即用，却又五脏俱全的监控服务（令人佩服的五体投地是，这款软件的 image 镜像仅有 2.9MB 大小）。

![](/images/blog/global/17492786307676.jpg)

## 密码管理：Vaultwarden
丝滑的管理密码，支持 passkey，TOTP，银行卡。

![](/images/blog/global/17492806190054.jpg)


## 可用性监控：Uptime Kuma
P.S. 不要忘记对监控系统自身进行监控哦。

![](/images/blog/global/17492804500014.jpg)

## 电子书阅读：Kavita
轻量的阅读管理工具，随时随地在苹果手机或安卓平板中无缝继续阅读。

![](/images/blog/global/17492803618548.jpg)

# 基础服务
```shell
# 硬件
CPU：CC150
主板：Z370M-PLUS II

# 操作系统
Unraid (Starter License)

# 网络（内网穿透）
Surge (Ponte) - Mac Mini M4
```