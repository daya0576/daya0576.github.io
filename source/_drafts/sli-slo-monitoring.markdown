---
title: 浅谈 SRE 之监控最佳实践
tags:
---

还记得三年之前，面试 SRE 结束，面试官问我还有什么想问的。我问：如何度量一个系统的高可用能力呢？ 面试官笑了一下，说你有没有听过三个九 or 四个九.. 

这篇文章将简单分享 DevOps 与 SRE 的关系，个人与监控的故事，以及如何使用 SLI/SLO 进行监控的最佳实践

<!--more-->

# 我心中的 SRE 

🤔 首先什么是 SRE(Site Reliability Engineering)？   
- 实施路径：从字面不难理解，即通过软件工程(E)来解决传统的稳定性(SR)问题。   
- 结果目标：生产系统复杂度增长与运维人数不成线性增长

感兴趣可以阅读[《Site Reliability Engineering》by Google](https://sre.google/books/) or [我的读书笔记](/blog/20180403/impressions-of-google-sre/)


# DevOps 和 SRE 的关系

说来惭愧，身为一名 SRE 快三年，一直对 DevOps 这个概念充满困惑，今天终于得到了解答～   

**先从传统的协作模式说起：**    
回顾工作的第一家创业公司，开发编写业务代码，运维负责生产环节的稳定运行。   
但问题在于开发不知道他们的代码如何被施展魔法，在生产环境中运行；而代码中业务逻辑对运维来说也完全是一个黑盒。   而这两边的隔阂与信息不对称，很容易将双方的矛盾点不断放大：faster feature VS  production reliability
1. 运维人员（Dev）关注线上的稳定性：如果出现生产可用性故障，需要半夜凌晨起来处理告警，甚至可能自己都被优化
2. 开发同学（Ops）关心如何快速在生产环境交付代码：如果新的特性没有及时发布，他们也会被作为人才向社会输送。。 

在这个背景下 `DevOps` 应运而生，期望通过以下五个方面，解决以上紧张的矛盾。而 SRE 则可以简单理解为该指导思想的**最佳实践**：

> class SRE implements DevOps

而 SRE 这是这些指导思想的最佳实践（如上）：

|  | interface DevOps | class SRE |
| --- | --- | --- |
| reduce org silos | 最简单的一个例子，就是将 dev 与 ops 放在一个同个物理空间中，更好的了解彼此 | 双方共用一套线上自动化工具，以促成更加紧密的协作  |
| accept failure as normal | 人类构建的系统总是会出错的，plan in advance，例如建设容灾能力，以及每个变更都是可回滚的  | error budget & blameless culture  |
| gradual change | 小步快跑，the smaller the change，更加轻松定位与回滚（相比于 1M code） | canary things |
| tooling & automation | leverage computer to do things over and over again, but human are easier to be boring | eliminate manual work as possible |
| measure | 可量化 | measure toil and reliability |


# 我和监控的故事

在蚂蚁，针对所有核心业务，我们有一套完善的故障等级定义机制：例如当苹果代扣**成功量** 当前分钟与上一分钟环比下跌超过 30%，即会触发一条 P1 告警；当持续 10 分钟未恢复，将开启电话外呼（无情的女声）：“集团监控告警，故障等级...”

用户的交易支付数据确实存在惊人的周期性，但也包含很强的业务属性：例如活动秒杀之冲高回落，以及小流量业务的频繁抖动等，成功量下跌的告警静态阈值确实有效，但也导致了大量误报告警。

为了解决以上问题，我参与了以下三个项目的开发建设：

1. [业务报警智能降噪](/blog/20190113/anomaly-detection/)：通过机器学习的拟合与异常监测算法，代替人的经验自动判断时序数据是否异常，最终对告警进行降噪抑制。
2. 单笔全风险：将多个应用的运行态数据，通过 trace 进行关联后，编写代码对每一笔流量的「可用性」与「正确性」进行判断：例如 
    1. 可用性：某个业务的支付请求，在入口返回给用户未知异常，同时在收单出现预期外的系统异常；巧的是异常对应机器在五分钟前进行了发布代码部署，则立即阻断变更并进行预警
    2. 正确性：商户发起一笔代扣，由于访问渠道超时，返回未知。需要新增时效性规则：商户对同笔订单是否在一个小时内发起查询并成功获取终态
3. 多维指标联合告警：结合多个时序监控的指标，快速得出结论。例如
    1. 当入口成功量下跌超过 30%，自动检查出口依赖的渠道是否异常

> 当前分钟与上一分钟的成功量，环比下跌超过 30%

## 如何做好监控

名词解释 - SLIs & SLOs & SLAs：

1. SLIs(Service Level Indicator):
2. SLOs()：
3. SLAs

> SLIs drive SLOs, which inform SLAs  



## 总结






