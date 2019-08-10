---
title: "《Site Reliability Engineering》读后感 - Part III"
tags: [sre, reading]
---

下一份工作要开始做SRE了，准备看下[Google 出的《Site Reliability Engineering》](http://landing.google.com/sre/book.html)稍微准备一下。感觉写的还是挺不错的, 顺便这篇博客记录读后感。期望更多的是个人的一些思考和感悟，也算是做个纪念吧。

一不小心读了整整一年多了(从 18 年四月份开始读，但现在已经2019年七月份了)。。。希望可以今年读完吧：

**分为三个部分：**

1. [Part I - Introduction & Part II - Practices](/blog/20180403/impressions-of-google-sre/)
2. [**Part III - Practices**](/blog/20190810/google-sre-reading-note/)
3. Part IV - Management


<!--more-->

![book](/images/blog/190727_cloudflare_outage/book.jpg)



# Part III. Practices
做了一个很有趣的比喻, 将如何运营好一个服务, 比做人类需求(五层次理论 - Maslow):
更有趣的是, 作者从底向上, 解释了模型的构成, 其中提到的**各个子问题**就对应第三部分的**每一章节**.
In an ACM article [\[Kri12]\](https://dl.acm.org/citation.cfm?id=2366332), we explain how Google performs company-wide resilience testing to ensure we’re capable of weathering the unexpected should a zombie apocalypse or other disaster strike.(????)


## Chapter 10 - Practical Alerting
1. "May the queries flow, and the pager stay silent." XD
2. 说到监控不仅仅是看一个请求响应的时间, 还可以分解并获取其中各个应用各个阶段的时间花费分布(比如公司内的的 Tracer 就能很完美的对每笔请求做阶段的分析).
3. 黑箱和白箱监控:
    - White-box monitoring: 从内部获取数据, 比如日志等.
    - Black-box monitoring: 简单的说就是通过用户的角度去监控(比如应用宝)
4. 日志系统Brog获取数据的基本用法:
`{var=http_requests,job=webserver,instance=host0:80,service=web,zone=us-west} 10`
添加时间范围(最近十分钟):
`{var=http_requests,job=webserver,service=web,zone=us-west}[10m] 0 1 2 3 4 5 6 7 8 9 10`
就会出现十个值.
还可以做aggregate:
`{var=task:http_requests:**rate10m**,job=webserver,instance=host1:80, ...} 0.9`
5. 监控系统Bornmon, 报警触发规则(配置), 慢慢形成了一门语言..
6. 报警触发规则(语言)模版化的好处(提供很多现成的通用format的模版): 在一个新应用上线的时候, 会自带一些相联的基础配置, 添加新监控变得很简单. **最终使得维护难度不随系统规模线性增长.**(之前也多次提到, 感觉是一个做SRE非常重要的原则, 感触颇深)
7. 报警触发规则是语言就容易出现bug, 所以甚至提供了单元测试.
8. 对于报警的处理（过去做了一段时间告警降噪，主要 focus 在对流量的算法分析，但其实如下合理的告警策略或事件告警聚合，也是另一维度，很有效的告警降噪）:
    1. 严重紧急的报警发送给当前oncall工程师
    2. 重要但不紧急的发给工单
    3. 其他报警显示到dashboard.


## Chapter 11 - Being On-Call
1. On-Call 对于维持系统稳定性来说, 是每个 SRE 工程师的**重要责任(critical duty)**, 但存在**几个大坑??**, 会在下文中一一道来(如何保持reliable services and sustainable workload).
2. "We cap the amount of time SREs spend on purely operational work at 50%; at minimum, 50% of an SRE’s time should be allocated to engineering projects..." - 相对于纯手工的工作，每个 SRE 至少抽出超过一半的时间做平台开发。之前的章节也反复强调过这个原则了。
3. 计算 oncall 数量和质量的两个公式："The quantity of on-call can be calculated by the percent of time spent by engineers on on-call duties. The quality of on-call can be calculated by the number of incidents that occur during an on-call shift."   每个主管都有义务去根据这两个指标，量化并平衡 oncall 的工作。
4. "multi-site team", 好处是不用上夜班了，并且保证每个人都对生产环境保持熟悉感。但于**沟通和协作**会存在一定的困难（有业务团队在美国，确实会有这个问题，上班时间完美的错过了）。
6. "Adequate compensation needs to be considered for out-of-hours support." - 会对应急的同学提供适当的补偿是非常有必要的，例如 Google 会提供调休和金钱上的奖励。
7. 应急需理性.. 因为直觉往往都是错的😂，所以要尽量减少应急人员的压力。文中提到了"Well-defined incident-management procedures"，蚂蚁有个专门的部门叫做 GOC(Global Operation Center)，在应急的时候统一指挥，在这点做的还是挺不错的。但我认为更重要并有一定争议的一个原则叫做: "A blameless postmortem culture" / "focusing on events rather than the people".
8. "Finally, when an incident occurs, it’s important to evaluate what went wrong, recognize what went well, and take action to prevent the same errors from recurring in the future." - 复盘很重要！
9. "Recognizing automation opportunities is one of the best ways to prevent human errors" - 人类总是会犯错的，所以无论什么事，都可以提倡自动化。
10. "Operational Overload" - 之前提到每个人的手动运维的工作不能超过 50%，但如果就是没控制过超过了呢？文中提到比如临时抽调一个有经验的 SRE 加入，但最理想的情况下，overload 的情况应该像业务系统一样可以被监控和第一时间发现。但是 overload 的原因是什么呢？一个主要的原因就是 "Misconfigured monitoring"![](/images/blog/180403_google_sre/15625820798875.jpg)
11. "Operational Underload" - 总是说做了过多的 toil, 但如果生产环节如果太"安静"了（故障发生的频率并不是很高），导致应急人员手生了要怎么办呢？   "Google also has a company-wide annual disaster recovery event called DiRT (Disaster Recovery Training) that..." Google 每年也会有演练，模拟故障。和蚂蚁的红蓝攻防一个意思。

## Chapter 12 - Effective Troubleshooting(20190713)
1. "However, we believe that troubleshooting is both learnable and teachable." - 有个比喻好形象，传授如何排查线上问题就像如何教别人骑车一样，只可意会不可言传～ 但...
2. 文中总结了应急效率低的一些原因，感觉是一些理论挺繁琐的，但正是因为理性的分析，才能更加科学的解决一些问题吧。
2. "The system is slow → the expected behavior, the actual behavior, and, if possible, how to reproduce the behavior." - 提问的艺术中也提到的「最小重现」。
3. "Ideally, the reports should have a consistent form and be stored in a searchable location, such as a bug tracking system. Here, our teams often have customized forms or small web apps that ask for information that’s relevant to diagnosing the particular systems they support, which then automatically generate and route a bug." - 所有历史 case 沉淀为知识库（减少重复的工作）。
4. "Many teams discourage reporting problems directly to a person for several reasons:" - 例如出了问题，不鼓励直接找认识的 sre, 而是找对应本周值班的同学👍
5. "Novice pilots are taught that their first responsibility in an emergency is to fly the airplane" - 经常听人提到的，应急中业务恢复是放在第一位的，而不是查找根因。
6. "Ask "what," "where," and "why"" - 排查的时候，想清楚这几个问题，下次我也试试。
7. "What touched it last" - 系统运行的好好的，为啥会出问题，肯定是引入了某些变更。现实中，绝大部分的故障是由于变更导致的。
8. "Case Study" - 举了一个真实的故障 case, 描述的还挺引人入胜的，感兴趣的可以看一下。
9. "Application’s latency, showing 50th, 95th, and 99th percentiles" - 耗时的监控，99th percentiles 代表，假如整体样本如果有100个，排在第99的那个数值。还是挺有启发的，因为平均值很多时候会误导人。![](/images/blog/180403_google_sre/15630074932574.jpg)


## Chapter 13 - Emergency Response(20190718)
这一章举了很多实际的例子, 来说明如何应急。
1. "However, it should be noted that in this case, our monitoring was less than ideal: alerts fired repeatedly and constantly, overwhelming the on-calls and spamming regular and emergency communication channels." - 故障发生时告警爆炸的情况，每个公司都会碰到，如果能比较好的解决也会带来很大的价值。 


## Chapter 14 - Managing Incidents(20190728)
公司有一个专门的组织叫做 GOC(Global Operation Center), 专门负责应急的调度和故障生命周期管理，不知道 Google 是怎么做的 🤔
1. 举了一个故障应急的反例，然后列出了不足与应该遵守的一些原则：
    - Recursive Separation of Responsibilities: 应及时分工分层需明确，又可以细分为一下几个角色：
        - Incident Commander: 让我想到了公司的「值班长」
        - Operational Work
        - Communication: 这个角色有点像公司的 GOC
        - Planning
    - A Recognized Command Post: google 发现在处理故障的过程中，及时通讯软件很有用？？不太理解。
    - Live Incident State Document: 多人事实统一编辑故障的最新进展
    - Clear, Live Handoff: 我理解更多是故障处理的交接吧。。但在国内的公司估计很难有这种情况。。
2. "In many situations, locating the incident task force members into a central designated 'War Room' is appropriate.": "War Room".. 哈哈，不就是我们的闭关室嘛
3. 针对文章开头的反例，又根据上面的几个原则，重新改造成了一个正确的例子。这个文章结构还是挺新奇的。但好多理论的东西，感觉有点虚。 


## Chapter 15 - Postmortem Culture: Learning from Failure(20190806)
Postmortem 这个单词很有意思，中文里叫做「验尸」，而在公司我们通常把 Postmortem 称为复盘。"The cost of failure is education." - 复盘很重要，就像文章开头说的，可以让我们在失败中不断学习，很多公司都有这样的文化，可以参考我最近写的一篇文章：[《Cloudflare 全球宕机复盘读后感》](https://changchen.me/blog/20190727/cloudflare-outage-reading-note/)
1. 复盘的三个主要⚠️目的：
    - 所有故障都有可以被文字的形式归档。
    - 根因被理解并调查清楚。
    - 设定对应 action, 防止犯相同或类似的错误。
2. **写复盘不应该是一种负担或者惩罚，而是应该被当作一次珍贵的学习机会。** 即使 tradeoff 是会消耗一些工作时间。
3. 写复盘还有一个重要的原则是之前提到好多次的 blame free. 在公司参加过几次复盘，真的会变成甩锅大会（每个故障需要定责）... 简单说是浪费时间，但真正可怕的问题是有些被事实隐瞒了："people will not bring issues to light for fear of punishment."
4. Google 的复盘模版：[链接](https://landing.google.com/sre/sre-book/chapters/postmortem/)，从模版排版上可以看到，最重要的是 Root Cause & Actions，接着是 Lessons learned，最后是 整体的 Timeline.   
文档是维护在 Google docs 上的，好处是可以支持多人实时编辑(上学的时间经常用，体验真的很棒.貌似yuque也在做这方面的努力，希望可以早日像 Google docs 一样顺滑)。但更加重要的是**分享**，尽可能越大范围的传播，每个读者都可以在上面评论与注释（这点公司因为权限的关系，感觉有点差异："Our goal is to share postmortems to the widest possible audience that would benefit from the knowledge or lessons imparted."）。    
5. "Introducing a Postmortem Culture"：复盘应该是深入 SRE 血液的一种文化，而其中很重要的一点是**协作**和**分享**，例如可以尝试：
    - 每月复盘集锦
    - 线上复盘讨论小组
    - 线下复盘学习俱乐部(reading club)
    - 故障重演/演练(Wheel of Misfortune)：真实重现故障，并让新人扮演当时对应的各个角色。
6. 介绍了两个最佳实践：
    - 大力奖励在应急中，有魄力做出正确决策的人
    - 对于复盘的有效性，持续寻求反馈
7. 总结：
    - 感谢复盘的文化，让 Google 不断减少故障，并带来更好的用户体验。
    - 但有个虚拟复盘小组发挥了很大的作用，例如统一了各个产品(YouTube, Google Fiber, Gmail, Google Cloud, AdWords, and Google Maps)的复盘文档模版，并支持应急中使用的工具，实现模版生成自动化，并可以抓取复盘的数据做趋势分析，等等。
    - 积累这么多复盘文档后，如何挖掘这个宝库也是个很有价值的课题。目前可以做到自动的聚类文档，并且在未来会使用机器学习去根据复盘的知识库预测可能的缺陷和风险点，并实时分析事件，聚类相同的故障并防止重复处理。

## Chapter 16 - Tracking Outages
...


