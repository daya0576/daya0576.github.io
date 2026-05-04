---
title: "Flask, OpenClaw & Pi - 时光交错的宿命"
date: 2026-04-10T07:35:49+08:00
categories:
- AI
- 编程
- Pi
series:
- Pi
---

![](/images/blog/global/17757783359245.jpg)

> https://mariozechner.at/posts/2026-04-08-ive-sold-out/

Pi 作者选择加入 [Earendil](https://earendil.com/) 后分享的文章，其中包含 **开源项目商业化** 的经历和思考，令人感触颇深，忍不住分享给大家。

## 名词解释

1. Pi：一个模块化的 AI agent 工具包，近期爆火的龙虾 Openclaw 就是基于 Pi 构建。详情参考另一篇文章 [读 Pi: The Minimal Agent Within OpenClaw](/blog/20260224/openclaw_pai_the_minimal_agent/)
2. Maria：Pi 项目的作者
3. Earendil：Armin 创建的一家公共利益公司（Public Benefit Corporation），除了追求利益，还要履行社会的公共利益承诺。
4. Armin：Flask/Jinja 的作者，之前在 Sentry 工作。与 Maria 是多年的好友，也是 Pi 的大力推崇者。
5. Colin：Earendil 公司中的另一位成员
6. Peter：openclaw 项目的作者
7. OSS：开源软件 (Open Source Software)
8. Sentry：sentry.io 是一款有名的错误日志（error stack）实时监控平台，Armin 在这家公司工作了 10 年，于 2025 年 4 月左右离职。

## 历史教训

原文作者第一个成功的项目：[libGDX](https://libgdx.com/)。这是一个基于 Java 的跨平台游戏框架，例如被我们熟知的「杀戮尖塔」就是基于该项目开发。

由于项目的成功，作者加入了 RoboVM 公司 ------ libGDX 的 iOS 跨平台解决方案（将 Java 字节码翻译为 iOS 设备的原生机器码）。RoboVM 的核心技术是开源的，但附加的调试器等是收费的，也是 Maria 的主要工作之一。

RoboVM 公司逐步发展为 5 人的团队后，被 Xamarin 收购，随之开源项目被闭源。很快 Xamarin 又被卖给了微软，然后微软立即关闭了 RoboVM。

作者表示，虽然赚了一点钱，但一切都 TM 的太闹心了。。作为一个开源的“代言人”，却不得不被迫向全世界宣布：对不起，RoboVM 要闭源了。通过这次经历，作者发现当开源与商业化相遇时，大概率会导致一地鸡毛。


## 我真正想要什么？

> "I tell you what I want, what I really, really want" - Spice Girls

几乎每个人都听过 OpenClaw，而作者的 Pi 是火遍全球的 OpenClaw 的幕后英雄。作者打趣地说，当那些联系不上 Peter 的人都会来联系他，包含 VC 和所有你听过的知名科技公司。最近两个月中，作者每天都要接 3-5 个电话。

作者原先以为 Pi 只是一个“美丽的废物”，个人的开源项目，没有任何商业价值。但同行，VC 和 科技公司认为 Pi 有独特的商业价值。

看到越来越多的人基于 Pi 构建应用，作者也出现了动摇，是否应该需要更近一步，例如组建团队，通过商业化自给自足。

但是作者不想创建自己的公司，==只是因为他有一个四岁的孩子，他真正想要的是自己看着他长大，尽自己所能地守护他、帮助他成长==。他不想孩子因为爸爸不在而哭泣，除此之外所有事情都是次要的。 并且创建自己的公司，可预见性的会重蹈 RoboVM 的覆辙，在商业化的压力下作出糟糕的决定，并成为曾经的“混蛋”... 

总结一下，作者真正想要的：
- 和孩子待在一起，不打乱现有的生活节奏，永远不要让孩子因自己的“工作”哭泣。
- 通过团队，让 pi 这个 OSS，可持续发展。
- 不再重蹈商业化的覆辙

## 时光交错

### Armin
作者 Maria 与 Armin 在 14 年前就在 reddit 社区上相识（在 `/austria` 奥地利子版块）。作者表示他们在很多政治上的观点都未达成一致，有趣的是，作者说只要在 Reddit 上看到 Armin 的发言，还没看到内容，就忍不住想要去纠正他😂。但作者也欣赏的说 Armin 和那些无脑网络喷子的最大区别在于，他从不情绪化或攻击他人。最终都以分歧或新的共识友好结束对话。

在 2016 年，作者第一次与 Armin 线下见面。一杯咖啡下肚后，两者一见如故，发现有很多相似的地方 ------ 特别是在软件开发和开源上。从那天开始，两人开始欣赏彼此，并成为了真正的朋友。

### Peter
同一天作者还拜访了 Peter（🤔竟然也是奥地利人），他随意的烤了一块作者这辈子都没见过的大牛排，并和作者聊了未来的商业计划。

时间转眼来到了 2025 年 4 月，Peter 在推特上发疯一样的逢人就安利 agent。作者和 Armin 一开始表示怀疑，但订阅 Claude Code 后，便好久没认真睡觉了。。。

### Colin
5 月，三个人受 Peter 邀请，一起聚在的公寓里进行 vibe coding。在那此线下聚会中，作者第一次认识了 Colin，第一次见面让人觉得是金融精英，穿着看上去非常昂贵的袜子，但相谈十分钟后便畅开心扉。BTW，Colin 也是 Earendil 公司的一员。

### Earendil
因为线下越来越多的接触，作者还成为了 Earendil 公司早期小规模的投资者。作者风趣的说：为什么不给那帮在车库里创业的小伙纸丢点钱呢？这样我去拜访他们的时候，也能坐上二手的 Herman Miller 人体工学椅 :p

### 时光交错的宿命
随后的故事大家都知道了，Peter 的龙虾大火，Armin 写了文章告诉世界 Pi 和 龙虾的关系，作者 Maria 也如开头所说被大量风投和科技巨头联系。作者向 Armin 和 Colin 说明了情况，并寻求建议，没想到对方发来了一份 offer（作者开玩笑说被套路了，因为对方通过自己提供的信息，设计了一份难以拒绝的 offer）。

## 为什么最终选择 Earendil？

Armin 在开源项目和商业化上，有很深的理解和成功经验。Colin 作为前金融从业者，有很强的产品直觉，可以处理创业公司中的所有琐事。与公司其他人接触的过程中，发现每个人都都是通才并各有特点和各自的背景，但都能和自己产生共鸣。

没有一个投资人在自己的黑名单上，所以不必担心有人会干预 pi 后续的开发。

而吸引作者的还包括 Earendil 这家公司的初心：AI 或软件不应该取代人类，而是为人类服务。

最后也是最重要的，公司中几乎每个人都有孩子，公司充分尊重这一点并写入[价值观](https://earendil.com/values/)中：

> Family First
> * Our family could be our closest friends, our parents, siblings, our spouse and kids, or our dogs. These are the relationships that will define our lives. They come first
> * We pursue our work with intensity and high standards, but we refuse to sacrifice one for the other. In conflicts, family takes precedence.

## 对于 pi 来说意味着什么？

### 1）技术部分：
- github repo: `badlogic/pi-mono` -> `earendil-works/pi`
- npm package: `@mariozechner/pi-coding-agent` -> `@earendil/pi`
- pi.dev 首页保持不变，但会加上 Earendil 的 logo
- Discord 维持现状，因为这是社区共同努力的结果，而非 Earendil 公司的私有财产。

### 2）管理方式
pi 属于 Earendil 公司的一部分，作者作为股东掌控所有的决定。

外部贡献的流程不变，提交 PR 作者审核，然后合并。

关于 OSS weekends and vacations 的机制也不会变化。解释一下：在 pi 项目中，在维护者的周末或假期期间，提交的 issue 会自动关闭（没有提交 issue 审核通过的 pr 也会被自动关闭）。个人道觉得是个不错的简易过滤机制，太多的人脑子一热，乱丢垃圾（当然也包括我自己）。

### 3）商业化策略

分为三层：

1. 核心代码依旧保持 MIT 协议 ------ 任何人可以使用，fork，甚至基于它构建产品并销售，这一点永不改变。
2. 部分商业代码也会开源，但采取延迟发布的策略（2~4 年后转化为真正的开源协议例如 MIT）。以保证公平性，即使公司“跑路”倒闭了，代码最终也一定会完全开放。
3. 部分企业级代码会采取闭源，收取的费用反哺上两层。

P.S. 如果有一天，你觉得我们偏离轨道了，请按下 GitHub 上的 fork 按钮。

## 结语

> And not having to go this alone feels great.

“很高兴给 pi 找了一个新家，不再一个人的感觉真棒。”







