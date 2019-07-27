---
title: Cloudflare 全球宕机报告读后感
tags:
---

Cloudflare 在七月二日发生了一次全球的宕机，自己托管在上边的两个网站自然是挂了，甚至上班的时候还收到了业务的告警，因为某些支付渠道使用了 Cloudflare 做路由。

在故障的整个生命周期中，很重要的一环就是故障复盘(postmortem)，防止同样愚蠢的错误不再发生。前天半夜四点睡不着的时候，起床偶遇这篇文章[《Details of the Cloudflare outage on July 2, 2019》](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)，一口气读完了，写的很精彩（很会讲故事），当然总觉得还缺了什么。用这篇文章记录一下个人的感受，**但更加推荐阅读原文。**    

<!--more-->

# 故障过程
习惯将一个故障的每一步都列为，
![](/images/blog/190717_cloudflare_outage/15641615441857.jpg)

# 

# 链接参考
1. 《Details of the Cloudflare outage on July 2, 2019》: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/
2. pageduty: https://www.pagerduty.com/



> This generated a Change Request ticket. We use Jira to manage these tickets and a screenshot is below.
> In the last 60 days, 476 change requests have been handled for the WAF Managed Rules (averaging one every 3 hours).
> Cloudflare 的变更管理做的挺不错的。

> Three minutes later the first PagerDuty page went out indicating a fault with the WAF.
> 告警系统用 PagerDuty, 感觉 cloudflare 还是挺开放的，

> Once approved deployment to what we call the “animal PoPs” occurs: DOG, PIG, and the Canaries.

> But, by design, the WAF doesn’t use this process because of the need to respond rapidly to threats.


> Manually inspecting all 3,868 rules in the WAF Managed Rules to find and correct any other instances of possible excessive backtracking. (Inspection complete)


> But getting to the global WAF kill was another story. Things stood in our way. We use our own products and with our Access service down we couldn’t authenticate to our internal control panel (and once we were back we’d discover that some members of the team had lost access because of a security feature that disables their credentials **if they don’t use the internal control panel frequently**).
> 应急的时候没有权限。。

> In the last 60 days, 476 change requests have been handled for the WAF Managed Rules (averaging one every 3 hours).



**评论也很精彩 ;)**

> This is the first thing I've ever done professionally that I truly, completely love. I wake up every day just thrilled at the work we're doing. [Source](https://gist.github.com/jgrahamc/6bb02a6f7c3799a1590b3cdb901f8e08)
![](/images/blog/190717_cloudflare_outage/15633465043345.jpg)





