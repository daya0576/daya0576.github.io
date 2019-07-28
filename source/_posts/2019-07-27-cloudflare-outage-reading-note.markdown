---
title: Cloudflare 全球宕机复盘读后感
date: 2019-07-27 21:45:50
tags:
- sre
- reading
---


Cloudflare 在七月二日发生了一次全球性的宕机，直接导致个人托管在上面的两个网站 502 超过半个小时，甚至上班的时候，还收到了一些业务告警（某些渠道通过 cloudflare 做路由）。可见这次故障的影响范围之大，互联网的一些基础服务已经成为了 21 世纪的水电煤..

而作为一名 SRE，明白在故障的整个生命周期中，非常关键的一环就是故障复盘(postmortem)，以防止同样愚蠢的错误不再发生(通常大故障都是由很多小错误连锁造成的)。前天在千岛湖 outing 半夜四点睡不着的时候，起床偶遇这篇文章[《Details of the Cloudflare outage on July 2, 2019》](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/), 一口气读完了，写的很精彩（很会讲故事），当然总觉得还缺了什么。

用这篇文章记录一下个人的感受和思考，**当然更加推荐阅读原文。**

<!--more-->

# 什么是 Cloudflare ?
今天刷 Twitter 的时候刚好看到一个[官方的回答](https://support.cloudflare.com/hc/en-us/articles/205177068-Step-1-How-does-Cloudflare-work-)还挺不错的。总结一下原理就是在用户与你的网站之间加了一层代理，以提升 security, performance and reliability.
![](/images/blog/190727_cloudflare_outage/15642299070568.jpg)


# 故障过程
整理了一下，习惯将故障的每一步都按 timeline 列出来(UTC)：
![](/images/blog/190727_cloudflare_outage/15642294239100.jpg)

# 故障原因
**代码变更：**更新 WAF 规则时，引入了一个很容易回溯(backtrace)的正则表达式，尝试画图去解释 backtrace 的原理... 但貌似更加抽象了。但建议直接跳过吧，因为相比故障原因，更加重要的是**故障的根因**！
![](/images/blog/190727_cloudflare_outage/15642303061327.jpg)



# 故障根因
原文中列了很多，我挑出了个人认为导致故障最重要的三点：

1. **WAF 规则变动直接自动部署到生产环境：** cloudflare 的代码变更，正常的部署模式为DOG(内部员工), PIG(部分免费用户), Canaries(灰度) 和 Global(全量部署), 但对于 WAF 规则的变更，由于常常需要极速部署以便于快速应急，所以日常也都是一把推。
2. **全球流量下降的警报没有第一时间发出**
3. **回滚预案执行超时：**权限与内部平台的问题，导致无法第一时间止血。

针对上面的两点思考：

1. 在我们公司有一个任何人都不能触碰的红线叫做变更三板斧：对于任意线上变更都需要 **可灰度，可监控，可回滚**。如果 cloudflare 在这次故障中的变更中，遵守了三板斧的任意一个，都会大大减少故障恢复的时间，甚至避免故障。变更三板斧真的是无数人血与泪传承下来的 golden rules.
2. 不管是 Netflix 的 chaosmonkey 还是蚂蚁的红蓝攻防，都是一种比较好的业内最佳实践了，只有真实频繁的去模拟故障，才能做到预案与应急能力的保鲜 & 提升。

# 其他思考
> "This generated a Change Request ticket. We use Jira to manage these tickets and a screenshot is below."
> "In the last 60 days, 476 change requests have been handled for the WAF Managed Rules (averaging one every 3 hours)."

Cloudflare 的变更管理&感知看上去做的挺不错的, 但真正发生故障的时候，也花了将近 **18 分钟**才定位到根因。公司也有很多人在做「变更感知」与「故障定位」，但个人觉得或许相对于感知，故障根因定位(关联的变更)才是最难的：比较依赖于专家经验，但真正大故障又往往是之前从来没有遇到过的场景。所以是不是换个思路，对与所有的跌零因子都做好预案，故障发生时，只需要无脑执行预案即可，第一时间止血恢复业务，之后慢慢排查原因。

> "I agree 100% transparency is best. "
> "blame free".

国外和国内文化上比较大的两个差别，但仁者见仁智者见智，并没有所谓的对错吧。


# 链接参考
1. 《Details of the Cloudflare outage on July 2, 2019》: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/
2. pageduty: https://www.pagerduty.com/

**最后的最后，这句话真的很触动我。。**
> This is the first thing I've ever done professionally that I truly, completely love. I wake up every day just thrilled at the work we're doing. [Source](https://gist.github.com/jgrahamc/6bb02a6f7c3799a1590b3cdb901f8e08)
![](/images/blog/190717_cloudflare_outage/15633465043345.jpg)



EOF

