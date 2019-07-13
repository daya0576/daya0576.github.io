---
title: 《Site Reliability Engineering》读后感 - Part III
tags:
---

接上篇博客(Part I & Part II), 继续写一些零零散散的读书笔记。
![](images/blog/180403_google_sre/book.jpg)
<!--more-->


# Part III. Practices
做了一个很有趣的比喻, 将如何运营好一个服务, 比做人类需求(五层次理论 - Maslow):
更有趣的是, 作者从底向上, 解释了模型的构成, 其中提到的**各个子问题**就对应第三部分的**每一章节**.
In an ACM article [\[Kri12]\](https://dl.acm.org/citation.cfm?id=2366332), we explain how Google performs company-wide resilience testing to ensure we’re capable of weathering the unexpected should a zombie apocalypse or other disaster strike.(????)


## Chapter 10 - Practical Alerting
1. "May the queries flow, and the pager stay silent." XD
2. 说到监控不仅仅是看一个请求响应的时间, 还可以分解并获取其中各个应用各个阶段的时间花费分布(比如阿里的Tracer就能很完美的做到).
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
8. 对于报警的处理:
    1. 严重紧急的报警发送给当前oncall工程师
    2. 重要但不紧急的发给工单
    3. 其他报警显示到dashboard.


## Chapter 11 - Being On-Call
1. On-Call 对于维持系统稳定性来说, 是每个 SRE 工程师的**重要责任(critical duty)**, 但存在**几个大坑??**, 会在下文中一一道来(如何保持reliable services and sustainable workload).
2. "We cap the amount of time SREs spend on purely operational work at 50%; at minimum, 50% of an SRE’s time should be allocated to engineering projects..." - 相对于纯手工的工作，每个 SRE 至少抽出超过一半的时间做平台开发。之前的章节也反复强调过这个原则了。
3. 计算 oncall 数量和质量的两个公式："The quantity of on-call can be calculated by the percent of time spent by engineers on on-call duties. The quality of on-call can be calculated by the number of incidents that occur during an on-call shift."   每个主管都有义务去根据这两个指标，量化并平衡 oncall 的工作。
4. "multi-site team", 好处是不用上夜班了，并且保证每个人都对生产环境保持熟悉感。但于沟通和协作会存在一定的困难。
6. "Adequate compensation needs to be considered for out-of-hours support." - 会对应急的同学提供适当的补偿是非常有必要的，例如 Google 会提供调休和金钱上的奖励。
7. 应急需理性.. 因为直觉往往都是错的，所以要尽量减少应急人员的压力。文中提到了"Well-defined incident-management procedures"，蚂蚁有个专门的部门叫做 GOC(Global Operation Center)，在应急的时候统一指挥，在这点做的还是挺不错的。但我认为更重要并有一定争议的一个原则叫做: "A blameless postmortem culture" / "focusing on events rather than the people".
8. "Finally, when an incident occurs, it’s important to evaluate what went wrong, recognize what went well, and take action to prevent the same errors from recurring in the future." - 复盘很重要！
9. "Recognizing automation opportunities is one of the best ways to prevent human errors" - 人类总是会犯错的，所以无论什么事，都可以提倡自动化。
10. "Operational Overload" - 之前提到每个人的手动运维的工作不能超过 50%，但如果就是没控制过超过了呢？文中提到比如临时抽调一个有经验的 SRE 加入，但最理想的情况下，overload 的情况应该像业务系统一样可以被监控和第一时间发现。  但是 overload 的原因是什么呢？一个主要的原因就是 "Misconfigured monitoring"![](/images/blog/180403_google_sre/15625820798875.jpg)还有个思路是将同一时间多个报警，聚合为一个事件进行投递，减少对 on-call 人员的打扰。这个在蚂蚁已经有对应的工具了 XD
11. "Operational Underload" - 总是说做了过多的 toil, 但如果生产环节如果太"安静"了（故障发生的频率并不是很高），导致应急人员手生了要怎么办呢？   "Google also has a company-wide annual disaster recovery event called DiRT (Disaster Recovery Training) that..." Google 每年也会有演练，模拟故障。和蚂蚁的红蓝攻防一个意思。

## Chapter 12 - Effective Troubleshooting
1. "However, we believe that troubleshooting is both learnable and teachable." - 有个比喻好形象，传授如何排查线上问题就像如何教别人骑车一样，只可意会不可言传～ 但...
2. 文中总结了应急效率低的一些原因，感觉是一些理论挺繁琐的，但正是因为理性的分析，才能更加科学的解决一些问题吧。
2. "The system is slow → the expected behavior, the actual behavior, and, if possible, how to reproduce the behavior." - 提问的艺术中也提到的「最小重现」。
3. "Ideally, the reports should have a consistent form and be stored in a searchable location, such as a bug tracking system. Here, our teams often have customized forms or small web apps that ask for information that’s relevant to diagnosing the particular systems they support, which then automatically generate and route a bug." - 所有历史 case 沉淀为知识库
4. "Many teams discourage reporting problems directly to a person for several reasons:" - 例如出了问题，不鼓励直接找认识的 sre, 而是找对应值班的同学👍
5. "Novice pilots are taught that their first responsibility in an emergency is to fly the airplane" - 经常听人提到的，应急中业务恢复是放在第一位的，而不是查找根因。
6. "Ask "what," "where," and "why"" - 排查的时候，想清楚这几个问题，下次我也试试。
7. "What touched it last" - 系统运行的好好的，为啥会出问题，肯定是引入了某些变更。现实中，绝大部分的故障是由于变更导致的。
8. "Case Study" - 举了一个真实的故障 case, 描述的还挺引人入胜的，感兴趣的可以看一下。
9. "Application’s latency, showing 50th, 95th, and 99th percentiles" - 耗时的监控，99th percentiles 代表，假如整体样本如果有100个，排在第99的那个数值。还是挺有启发的，因为平均值很多时候会误导人。![](/images/blog/180403_google_sre/15630074932574.jpg)


