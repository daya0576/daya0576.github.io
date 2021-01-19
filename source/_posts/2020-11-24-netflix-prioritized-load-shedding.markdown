---
title: 【读后感】限流还能这么玩 - Netflix 权重限流新思路
tags:
  - sre
date: 2020-11-24 15:23:10
---


上上周在 [sre weekly](https://sreweekly.com/) 上读了一篇文章：[《Keeping Netflix Reliable Using Prioritized Load Shedding》](https://netflixtechblog.com/keeping-netflix-reliable-using-prioritized-load-shedding-6cc827b02f94)（Netflix 出品，必数精品XD），有种耳目一新的感觉，特此在清理草稿的时候记录一下读后感。

<!--more-->


# 目标：
> reduce members’ pain by shedding requests that are not expected to affect the user’s streaming experience. 

通过优先对用户**视频观看**影响较小的请求进行限流，保护后端系统负载的同时，尽可能避免用户体验受损。


# 解法：对流量不再一视同仁
## 整体部署架构：
下图中 `Zuul` 即网关，将客户端的所有 http 请求转发给下游 api：
![-w404](/images/blog/200104_japan_travel/16062006731318.jpg)

## 解法：
```
网关(Zuul)收到请求后，通过三个维度：
throughput / functionality / criticality 
                ↓
          将流量分为三组：
          1. NON_CRITICAL
          2. DEGRADED_EXPERIENCE
          3. CRITICAL
          同时依次打分(1 to 100)
                ↓             
          后端或网关出现容量问题 -> Y -> 分数越高的请求越先响应(类似 priority queue)
                ↓ N
          无视权重，正常处理所有请求   
            
```


# 新的问题：
Q. 如何保鲜以上的打分策略，i.e. 对 NON_CRITICAL 限流后，不会对用户体验造成严重影响？
A. 解法：Chaos Automation Platform
抽样极小人群做 A/B 测试：A 组在网关注入限流（参考上文架构图），观察对应的 *playback experience.*（最核心的指标还是视频是否可以流畅播放），与 B 组是否存在偏移。

如果出现播放问题则需要人工介入修复，并且定期做 regression 以达到保鲜的目的。


# 个人思考
1. 关于 Chaos：混沌工程最近特别火，最早也是 Netflix 的工程师落地了 Chaos Monkey：通过故障注入来验证线上分布式系统整体的健壮性。其实我理解蚂蚁的红蓝攻防也是它的实践之一，只不过很可惜一直停留在灰度压测环境[doge]
2. 关于限流：个人所知蚂蚁国际的限流主要分为网关http和内部系统rpc调用的限流，可以精细到接口与请求参数等维度，底层都是使用的令牌桶算法，目前没有动态限流与权重限流等能力。但本质上因为国际业务量不大，没有这类需求与痛点，所以感叹技术与业务都是相生相伴的，缺一不可。




