---
layout: post
title: "【读后感】《Site Reliability Engineering》by Google"
date: 2018-04-03 12:04:19
comments: true
tags: [读后感]
---

下一份工作要开始做SRE了，准备看下[Google 出的《Site Reliability Engineering》](http://landing.google.com/sre/book.html)稍微准备一下。感觉写的还是挺不错的, 顺便这篇博客记录读后感(期望更多的是个人的一些思考和感悟)。

一不小心读了整整一年多了(从入职前一个月，18 年四月份开始读，但现在已经2019年七月份了)。。。希望可以今年读完吧：
![book](/images/blog/190727_cloudflare_outage/book.jpg)
<!--more-->

# Part I - Introduction
## Chapter 1 - Introduction
1. **dev/ops分离的历史：** 最早时，在公司维护复杂系统的人叫做sysadmin(systems administrator)，但后来因为 sysadmin 和 developer 需要的技术完全不一样, 所以逐渐分为了两个完全不同的岗位：developer & operations(ops), 应该就是我们所谓的开发与运维吧。
2. 这种模型(开发与运维的完全分离)，好处和坏处
    - **1) 最大的好处就是:**业内有成熟的解决方案, 不用重复的造轮子, 所以用人与开发成本也比较低.
    - **2) 但最大的坏处:**
        - **Direct costs:** 发布和变更需要人工干预 → 系统的规模和需要的人手成线性关系(例如总不能项目多部署一套奔驰环境, 就增加一个人手).
        - **Indirect costs:** (个人理解是)开发与运维的矛盾: 开发需要尽快的上最炫最酷的新功能, 而运维则想保持服务100%的稳定性, 再加上完全不同的技术栈, 很容易造成矛盾. 所以一定要在两者之间找一个平衡点.
2. **google对于sre的目标:** 以软件开发的方式打造一个系统, 将运维的工作变得全自动(automatic). (Site Reliability Engineering teams focus on hiring software engineers to run our products and to create systems to accomplish the work that would otherwise be performed, often manually, by sysadmins.), 终极目标就是: 减少第一条中的Direct costs(人为干预), 使得系统规模与运维人员的人数不成线性增长.
3. 有一句话挺有意思的, 说的是要去**评估SRE的消耗的时间分布**, 才能保证开发人员在ops和development上花费时间的平衡. 因为sre与传统运维最大的不同就是加入了开发, 而不是一味的做operation. 但相对的develop不能超过50%, 以防止承担了过多原本属于development team的事情, 或一直投入运维人员, 而忘了利用原有的员工去做operation的工作.但打动我的是 "measure how SRE time is spent", 感觉对人对团队对整个sre的measurement, 是所有事情能顺畅实现的基础.
4. **DevOps?**
(这个词近几年很火吧, 但惭愧的是一直没搞懂到底是什么. 书中说可以把sre当作一种devops的具体实现, 并包含一些独特的扩展?) - "One could equivalently view SRE as a specific implementation of DevOps with some idiosyncratic extensions."
5. Service’s SLO?: (**第四章**会详细解释一些含义)
6. **不必过分追求100%?:** 文中强调的一个观点挺有意思的: 对于sre来说, 100%并不是一个正确的指标? 作者说因为用户其实完全感受不到99.999%与100%的区别, 而且现实中用户家中的笔记本, 路由器, ISP等等远达不到99.99%的可用性 但还是需要定目标: 如果可用性达到99.99%, 0.01%就可以作为error budget, 然后利用这个error budget去冒风险发布一些新特性, 并吸引新用户. (感觉感觉作者认为这样就很好解决了第一条中所谓的indirect cost, 使得生产事故变成一种预期之内的事情?? 解决了开发追求急切的上新功能, 而运维想要保持100%可用性的矛盾. )
7. **blame-free postmortem culture**: 强调出了事故, 不要过分的去指责而是仔细剖解问题, 防止下一次的发生? 在国内领导负责的国情感觉不是很现实 :P


## Chapter 2 - The Production Environment at Google, from the Viewpoint of an SRE
1. **Machine:** A piece of hardware (or perhaps a VM)，**Server:** A piece of software that implements a service
2. **硬件故障:** 我们平时可能认为, 硬盘内存几乎是不可能坏的, 但文中说到, 对于一个超大规模的data center来说, 硬件出故障是个很常见的问题, 所以目标就是要让用户完全无法感知到硬件的故障.
3. 因为不同的(几千个)任务动态的分布在不同的机器上, 所以不能单纯的用ip和端口去启动任务, 文中给出的一个解决方案: `/bns/<cluster>/<user>/<job name>/<task number>`, 然而并不是特明白.
4. **对于任务的分布**(例如一个任务需要3个cpu, 2g内存), 有趣的是文中说到要尽可能优化的放置(二次装箱问题). !!!但又不能把鸡蛋都放在一个篮子(同个Rack或Pod)里(很有可能一个路由坏了, 那就全gg了).
5. Remote Procedure Call (RPC), 了解一下?
6. **Life of a Request**: 在过去工作的一年, 我一直在思考一个问题: 一个request的lifecycle, 于是去读了web框架(Django)的源码, 自己去实现一个uwsgi, 看http, tcp协议... 看到书中的request lifecycle, 感觉今年的目标是更多的了解大型项目的request lifecycle, 例如高并发的负载均衡问题, 等等.
(This request ultimately ends up at Google’s DNS server, which talks to GSLB. As GSLB keeps track of traffic load among frontend servers across regions, it picks which server IP address to send to this user.) 原来在dns server这就可以根据地区和负载情况, 分配对应的服务器ip, 但是为什么走到GFE反向代理找frontend server的时候, 又要去根据GSLB进行一次负载均衡的处理呢?
<img style="max-height:300px" class="lazy" data-original="/images/blog/180403_google_sre/1-lbs.png">
7. QPS: queries per second
8. **N+2原则**: 如果说预期3,470 QPS, 而一个backend server最多能处理100QPS, 则至少需要35个server. 但是一般采用N+2的策略(37个server), 因为:
    - 1) 如果在升级中, 会有一个server不可用
    - 2) 如果一个机器挂了, 会重新放置task到别的server.
但是有时候也可以用`N+1`的原则. 因为如果需要的server很少, 比如只需要3个server的情况, 就可以利用牺牲高延迟的风险, 去节省20%的硬件资源(`+1`相对于`+2`节省了一台虚拟机).


# Part II. Principles
## Chapter 3 - Embracing Risk (拥抱风险?)
1. **100%的可用性是个错误的目标?**(100% is probably never the right reliability target?) 文中的解释:
    - 一是因为cost和reliability并不是线性关系, 99%→100%会带来极大的开销, 并对服务更新升级的速度造成负面影响.
    - 二是像第一章里提到的那样, 用户其实很难感知到99.99%和99.999%的区别.
    - 三是和 rapid innovation and efficient service operations的平衡, 即保持服务的高可用 VS 用最快的速度把新功能新特性传递给用户.
2. **如何评估服务的高可用:**
"Unplanned downtime is captured by the desired level of service availability, usually expressed in terms of the number of "nines" we would like to provide: 99.9%, 99.99%, or 99.999% availability." 想起面试的时候, 问的面试官如何去评估一个系统的高可用, 他笑了笑, 说到了四个9和五个9.
1) **Time-based availability: availability** = uptime / (uptime + downtime), 所以99.99%就意味着服务down的时间不能超过52.56分钟.
**但是!** 文中提到google的server是分布在全球的, 就很难用这种方式去测量availability, 所以引出了一个新的概念: request success rate.
2) **Aggregate availability:** availability = successful requests / total requests。
**但是!!** 不同的request失败对用户的影响其实是不同的, 例如支付失败和获取好友信息request失败.
3. **(个人认为)measurement的重要性:** 因为measurement是提升的基础, 没有量化, 如何比较提升还是破坏呢. 最简单的例子: 我们在优化一段代码速度的时候, 一定要先做profile, 再针对某几行代码做优化, 最后比较总的运行时间, 看运行速度提升了多少. 比如文中提到的: "By setting a target, we can **assess our current performance and track improvements or degradations** over time."
4. **"Hope is not a strategy."** → The more data-based the decision can be, the better.
5. **文中提到对error budget的使用**(定义: 如果可用性定的目标是99.99%, error budget就是0.01%, 然后如果这个季度测量结果为99.992%, 那么error budget就可以认为使用了20%).
所以可以用error budget很好的制约SRE团队与product development团队. 例如, 提前订好了reliability的目标, 如果在开发中, error budget消耗(使用)的太快了, 就放缓迭代发布的速率, 并增强测试.



## Chapter 4 - Service Level Objectives
1. 一开始就引出了**三个概念**:
    - service level indicators (**SLIs**): service的指标, 比如请求的响应速度, 出错的概率, system throughput(requests per second)等等.
    - service level objectives (**SLOs**): 目标, 例如latency在100ms内 or QPS(Query per Second)达到1万.
    但一般QPS很难去制定目标, 因为它是未知的(比如某个明星出轨, weibo流量爆了).
    - service level agreements (**SLAs**): 区分SLO和SLA的区别, SLA更侧重于如果没有达到之前定的目标应该怎么办. 比如Google search就没有SLA, 因为没有和用户达成协议, 就算某一天不能用了, 虽然会造成一系列的后果, 但不用对用户负责.
2. 有一句话挺有道理的: 对于SLI并不是越多越好, 而是要去监测那些**用户真正在乎的指标**.
3. **选择SLOs的准则!:**
    - Don’t pick a target based on current performance: ???
    - **Keep it simpl**e: 和单元测试一个道理..太复杂的话, 功能一变动会很难维护.
    - **Avoid absolutes**: 没有必要要求不管QPS多高, latency都保持很低.
    - Have as few SLOs as possible: 和第二条类似.
    - **Perfection can wait**: SLOs刚开始的时候不必太苛刻, 否则很容易造成开发时间的浪费. (想起我看[Django性能优化官方文档](/blog/20170503/django-performance-and-optimisation/)的一句话: "Your own time is a valuable resource, more precious than CPU time. Some improvements might be too difficult to be worth implementing, or might affect the portability or maintainability of the code. Not all performance improvements are worth the effort.")



## Chapter 5 - Eliminating Toil
1. "If a human operator needs to touch your system during normal operations, you have a bug. The definition of normal changes as your systems grow."  有点意思, 以前人们一提起运维, 就想到苦逼. 但真的是这样吗?
**看到面试官微信的简介是`Never repeat yourself.`, 心里又多了一丝的希望的小蜡烛, 因为个人觉得这就是sre和传统运维不同的地方.**
2. Operation work → **Toil** → 脏活累活, 定义如下:
    - Manual
    - Repetitive
    - Automatable
    - Tactical(没看懂): Toil is interrupt-driven and reactive, rather than strategy-driven and proactive. Handling pager alerts is toil.We may never be able to eliminate this type of work completely, but we have to continually work toward minimizing it.
    - No enduring value: 无用功?
    - O(n) with service growth!!!
3. "The work of reducing toil and scaling up services is the "Engineering" in Site Reliability Engineering." 有意思, 而且上文提到toil如果不及时处理, 就会很快的占据所有人100%的时间.
4. **Calculating Toil:** 挺无脑暴力的一个计算, 如果说一个团队有6个人, 在一个周期(**六周**)中, 每个人on-call的时间总共是两周(一周primary on-call+一周secondary on-call), 那么他toil的占比至少为33%(1/6+1/6)
5. 理论上每个SRE在toil上花费的时间不应该超过50%.
6. **Is Toil Always Bad?** tiol并不是永远是不好的, 重复无脑的工作其实能让人变得无比平静(calming)?? 并且完成少量的toil还有一丝丝成就感呢.
但多了就要gg了, 因为:
    - 过多的toil会抑制你在实际项目中做贡献, 并令你职业生涯停滞不前.
    - 每个人都会有忍耐的上限, 无限的toil只会让人精疲力尽并感到厌烦.
7. **结论:** 只要每个人都能消灭一点toil, 最终就能把精力都放在开发下一代更大规模的架构! 我们的口号是: "Let’s invent more, and toil less!!!"



## Chapter 6 - Monitoring Distributed Systems
1. **为什么需要监控:**
    - 了解整体的趋势: 比如数据库硬盘占用提升的速率, 日活跃用户增长的**趋势**. (可以提前做处理?)
    - 量化提升: 与历史数据做对比, 很方便直观的比较性能变化.
    - 及时报警: 在第一时间修复.
    - 打造dashboard?
2. **监控报警不能太频繁:** "When pages occur too frequently, employees second-guess, skim, or even ignore incoming alerts, sometimes even ignoring a "real" page that’s masked by the noise." 不能稍微有点不对劲就报警, 不然就变成狼来了.
3. **The Four Golden! Signals**:
    - latency: 注意一定要将成功请求与失败请求的延迟数据区分开(我们都知道比如一个request失败并返回了500或502, 它的延迟一般都会特别的低) 所以不能将它用作计算到到平均的延迟, i.e.要将它们过滤出来.
    - traffic: 对于web服务来说, 通常为HTTP requests per second.
    - errors: 注意对error的定义. 还有要注意的一点, 如果502了, 例如Django的Sentry就捕捉不到了. 只能通过查看返回的信息是否正确来监控.
    - saturation: 比如再来20%的流量, 系统是否能扛住. 或者预测到还有4小时, 数据库的硬盘就要满了.
4. 讲到**监测采集数据的频率其实不用太高**. 虽然会发现一些隐藏的细节, 但分析和存储的成本都太高了.
5. **监测不能搞的太复杂**, 不然监测系统会变得很fragile, 而且难以维护. 说了三个原则, 其实就是开始时就让 incidents 保持简单, 并定期去清除很少用到的巴拉巴拉.
6. "Every page should be actionable."   还提到一点: 监测系统发起的**报警的问题必须是可以被解决的**. 不难理解, 因为如果报警了解决不了, 那就是完全无效的 → 每次都要忽略掉, 久而久之很可能会忽略掉一些严重的问题的报警.



## Chapter 7 - The Evolution of Automation at Google
1. 自动化(Automation)的好处:
    - Consistency: 人总是会犯错误的, 相对于机器是个最大的缺点, 也是个最大的优势吧, 嘿嘿.
    - A Platform: 可以扩展给多个服务??  第二段没看懂.
    - Faster Repairs: 可以自动的去修复一些常见的错误, 特别是在生产环境人工修复bug的成本是巨大的..
    -  Faster Action: 人的手速再快也比不上机器
    - Time Saving: 写一个脚本花费的时间 vs 这个脚本未来能节省的时间. 在犹豫的时候, 亲身感受也会强烈自己去写自动化脚本.
    - "If we are engineering processes and solutions that are not automatable, we continue having to staff humans to maintain the system. If we have to staff humans to do the work, we are **feeding the machines with the blood, sweat, and tears of human beings**. Think The Matrix with less special effects and more pissed off System Administrators."
2. Google偏爱automation的原因:
    - google的规模很大, 服务于全球的用户, 所以对于consistency, quickness, and reliability有极高的需求.
    - 复杂但是统一的生产环境: 相比直接购买成熟的软件, Google选择自己造轮子, 所以当无APIs可用时, 就方便快捷地去自己实现一个. 从而去搭建完善的自动化系统(用机器去管理机器).
3. automate ourselves out of a job:
文中举了**一个实际例子**: Ads的SRE团队, 当初计划将mysql迁移到Google的cluster scheduling system上. 这么做的两个好处: 一是减轻维护的工作量, 因为这个平台(cluster scheduling system)会去自动的重启失败的任务. 二是可以将mysql instance做装箱放置. 也就是说在一个physical machine上, 尽可能多地放置mysql instance. 但遇到一个问题: failover需要消耗一个人30-90分钟去处理(有点没看懂failover是什么, 个人理解为机器或各种原因出了问题, 快速的将服务部署在新的硬件上.)
然后sre团队就做了一个自动化解决failover的东西叫做"Decider"(95%的情况下在30s内完成failover). 因为大家意识到"failure is inevitable, and therefore optimizing to recover quickly through automation.".
最终自动化带来的好处: 节省了无数(95%)的人力和物力, 节省了高达60%的硬件资源.
这句话写的挺好的: "the more time we saved, the more time we were able to spend on optimizing and automating other tedious work"
4. 文中提到十年前的时候, Cluster Infrastructure SRE team每隔几个月就要去大量招人, 因为员工的速率和服务的规模成正比(turning up a service in a new cluster gives new hires exposure to a service’s internals). 想到原来的公司(Hypers)给新客户部署一套环境的时候(五六个不同的产品), 需要几周的时间, 和这种情况好类似. 然而手动的配置和shell脚本都各自的缺点. 好奇Google是如何解决这个问题的.
5. (接上一条)有意思, 解决方案竟然是Prodtest (Production Test): extended Python unit test framework, 但是一个有很多依赖的单元测试(如下图):   <img style="max-height:300px" class="lazy" data-original="/images/blog/180403_google_sre/7-producttest.png">
**好处:** 方便的校验配置是否正确, 如果出错了, 快速的定位出错的步骤和详细的错误信息. 而且每次出现配置出错造成延期的时候, 就将它加入到单元测试中, 保证相同的错误在未来不会重现.
**具体疗效:** 有史以来第一次, product manager可以预测服务上线的具体时间, 并遇到延期时, 可以了解到详细原因.
**惊不惊喜(out of the blue)**: 新的挑战 → senior management让他们在一周内让五个新集群同时上线.
6. **进化!!!:** 从利用Python单元测试去找到错误的配置, 变为利用Python单元测试去自动修复.     如下图所示, 如果`TestDnsMonitoringConfigExists`没有通过, 就运行`FixDnsMonitoringCreateConfig`, 然后再尝试之前的测试. 这过程重试多次后如果还是失败的话, 就报错并通知用户.
**缺点**: "Not all fixes were naturally idempotent, so a flaky test that was followed by a fix might render the system in an inconsistent state." 说实话没有看明白, 好像是说同一个fix很可能有的时候可以成功修复一个问题, 但有的时候又失败了, 造成系统的inconsistency.
7. 用RPC代替SSH: 因为用SSH去执行命令经常需要那台机器的root权限.
8. Google自动化的进程:
    - Operator-triggered manual action (no automation)
    - Operator-written, system-specific automation
    - Externally maintained generic automation
    - Internally maintained, system-specific automation
    - Autonomous systems that need no human intervention
9. **Borg(集群管理系统):**   诞生的原因: due to the fact that abstractions of the system were relentlessly tied to physical machines. 就是说server更多的要从物理机抽象出来, e.g.原来利用host/port/job分配任务的方式就要被废除了, 而是将集群看作一个整体的资源. 也就是说, 在集群中添加一个服务, 就像给一台计算机新加一块硬盘或RAM.
10. **高度自动化的坏处:** 会越来越依赖自动化程序, 如果有一天自动化出错了, 反而不知道该怎么办了.


## Chapter 8 - Release Engineering
1. 在Google有个专门的职位叫做release engineer, 要对很多东西都有深刻的理解, 甚至还包括customer support.
2. 文中说google是数据驱动的, 所以有专门的tool(平台)记录每次发布的时间, 各个配置文件都是对应哪个feature. 这些平台都是由release engineer搞出来的.
3. release engineering的四个准则:
    - Self-Service Model:   就是说release engineer要提供足够多的automated build system and our deployment tools, 使得发布变成一件全自动的事情. 只有出意外时, 才需要人为的介入.
    - High Velocity:   一些暴露给用户的服务, 比如说Google搜索, 需要快速的迭代和发布, 这样每个版本之间的差别也越小. 最终使得 testing and troubleshooting easier(为什么呢?).   甚至还会有一种 "Push on Green"的模式, 只要有改动并且通过了所有测试, 就直接部署了.
    - Hermetic Builds:
        - 一致性: 如果有两个人, 在两台发布一个版本的代码, 结果应该是完全相同的.
        - 密封的(hermetic): 就像docker的容器一样, 完全不依赖外部的库.
        - 回滚: 通过重新发布(老的版本号)来便捷的实现. 而且连发布工具的版本也是之前发布时的旧版本.
    - Enforcement of Policies and Procedures
    发布的时候, 所有的代码改动都需要code review的流程, 并且集成到开发流程之中. 自动发布的平台会把代码变更输出一份报告, 让SREs更好的理解改动, 并在出问题的时候迅速定位. (其实这一小节并没有太看懂, 根据标题个人理解大意是说在发布时, 要严格执行一些规范流程.)
4. **cherry picking:** ...
5. Rapid: Google的自动发布系统, 然后有一门语言叫做**blueprints**, 专门用来给Rapid写配置.
6. Configuration Management: 配置管理应该是开发和sre合作最紧密的一块区域.. 而且**配置更改是instability的潜在根源**. 所以在google配置管理不断的进化, 发生了很大的变化:
    - Use the mainline for configuration:
    在head of the main branch修改配置文件, 更改review之后再apply到生产上(这里的head就是git里的HEAD吗? 没太看懂). 配置与发布版本解偶也导致不一致的问题.
    - Include configuration files and binaries in the same MPM package:
    和上条刚刚相反. 如果配置少的话, 可以直接把配置文件和执行文件一起打包发布(MPM package是什么东西). 但相对的配置的灵活性就差了很多.
    - Package configuration files into MPM "configuration packages.":
    哎, 看了三遍还是没有看懂, 还有上边的cherry picking, 看了十遍也没看懂.
    - Read configuration files from an external store:如果配置变更很平凡, 可以放到第三方平台管理.
7. 总结:
    - 开发和SRE不应该为发布头疼. 只要有正确的工具, 合适的自动化, 规范的policy, etc. 发布只不过是按个按钮的事.
    - 提早重视Release Engineering, 反而会降低成本.
    - developers, SREs, and release engineers的合作非常重要, 而且release engineer也要去深入了解代码是如何编译和部署的.


## Chapter 9 - Simplicity
1. `The price of reliability is the pursuit of the utmost simplicity.`: 有种代码越短, bug越少的意味...
2. 无聊是一种美德? "Unlike a detective story, the lack of excitement, suspense, and puzzles is actually a desirable property of source code." → **sre的克星: 惊喜**😂
3. 不应该对没用的代码产生感情... 在生产环境, 每一行代码都应该是有意义的, 要是留很多没有的不会触发的代码(比如注释). 要Version Control System要何用呢?
4. "software bloat": 臃肿的项目.
5. "perfection is finally attained not when there is no longer more to add, but when there is no longer anything to take away" - 和上一条有点类似, 如果暴露的API和参数越少, 就更容易理解. 除了问题也能更专注核心问题. less is more!
6. 设计模块的时候一定要注意**低耦合**(大二软件工程学的, 虽然当时竟然觉得都是一些概念毫无用处). 一个好处就是: 当出了问题的时候, 可以在一个子系统中快速的解决并独立发布.
7. "... it is also poor practice to create and put into production a **"util" or "misc" binary**. A well-designed distributed system consists of collaborators, each of which has a clear and well-scoped purpose." - 真的吗?
8. "Simple releases are generally better than complicated releases." - simple is better than complicated, less is better than more. 文中的例子挺有道理的, 发布的时候, 发布时, 只有一个改动肯定比发布一百个没有关联的改动来的好. 因为出了问题, 一百个改动的就很难定位问题. 而且每次发布的东西少, 发布的时候也越自信, 最后达到**小步快跑的效果**😊.
9. 总结:  只有保持**simplicity**, 才能保证reliability.


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
    - 但有个虚拟复盘小组发挥了很大的作用，例如统一了各个产品(YouTube, Google Fiber, Gmail, Google Cloud, AdWords, and Google Maps)的复盘文档模版，并支持应急中使用的工具，实现模版生成自动化，并可以抓取复盘的数据做趋势分析，等等。这不就是 GOC 嘛
    - 积累这么多复盘文档后，如何挖掘这个宝库也是个很有价值的课题。目前可以做到自动聚类相似的文档，并且在未来会使用机器学习去根据复盘的知识库预测可能的缺陷和风险点，并实时分析事件，识别相同的故障并防止重复处理。

## Chapter 16 - Tracking Outages
如果量化都做不到，何谈改进呢？稳定性也是一个道理。记得去年面试的时候，问了面试官，如何量化稳定性呢？对方笑了一下，说你听说过四个9或者5个9嘛？

"'Outalator', our outage tracker, is one of the tools we use to do just that. Outalator is a system that passively receives all alerts sent by our monitoring systems and allows us to annotate, group, and analyze this data." - 和公司的故障管理系统的区别点在于，对于数据的接受和处理🤔。

1. 复盘的局限性：对于很多小范围不严重的问题，无法覆盖。
2. 有很多有价值的信息：例如每次 oncall 期间一共收到了多少告警？其中多少是噪音(nonactionable)？哪个服务创造的最多的 toil? 过去一年在公司搞的平台貌似也涉及到这部分 0.0
3. 有个系统叫做 Escalator, 如果有些告警长时间没人阅读或处理，将会被降级，例如告警等级从 primary 变为 secondary(**很不错的想法**). 
4. "it is worthwhile to attempt to minimize the number of alerts triggered by a single event," - 告警的横向聚合，也是一种关键的降噪方式。
6. "Historical data is useful" - 文中更多的指的是数据的统计，例如每个月的故障数，各个故障的告警数，或是哪个服务或基础设施贡献了最多的故障，需要持续关注和改进。我们之前也有类似的想法，把所有故障和事件沉淀为知识库，抽象出一些特征值出来，例如监控（告警），订阅人，等等。相当于一个故障“切片”，当一个新的故障来的时候就可以快速匹配并给出最可疑的根因。
7. "the Outalator also supports a "report mode," in which the important annotations are expanded inline with the main list in order to provide a quick overview of lowlights." - 这个和业务同学也聊过。。。尝试将对应告警聚合和事件关联起来，使用 tag 管理，最终调用在线文档 api, 自动生成对应业务的**每周高可用报告**。
8. ...

## Chapter 17 - Testing for Reliability
1. MTTR: Mean Time to Repair。MTTR 为零意味着上生产前，bug 就都被测出来了🤔。
MTTD: 对应的发现时长： mean time to detect.
2. smoking test: 冒烟测试，来源原来是电路测试中，如果通电后没有冒烟，表示一切正常可以继续。
3. Stress test: 大促压测
3. Canary test: 灰度环境测试，原来来源把一只🐦放到煤矿中做测试，防止人直接吸入有毒气体。但值得注意的是灰度环境并不完美，无法检测出所有的潜在风险。
4. （...看的头晕，不是很感兴趣，先跳过了）

## Chapter 18 - Software Engineering in SRE
1. "Overall, these SRE-developed tools are full-fledged software engineering projects, distinct from one-off solutions and quick hacks" - 自己也亲身经历过一个很大的矛盾点：SRE 的职责是负责整个公司线上的稳定性，但可笑或者无奈的是，往往对于自己开发的小工具或产品，无法保证高可用率。这时突然想起《进化》中的一句话：“运维能力是整体技术架构能力的体现，运维层面爆发的问题或故障一定是整体技术架构中存在问题，割裂两者，单纯地看技术架构或运维都是毫无意义的”。
2. "the vast scale of Google production has necessitated internal software development" - 和蚂蚁一样，google 大部分面向内部的产品都是自研的，因为外部开源项目的 scalability 等方面无法满足。而 SREs 则是开发这些产品的不二人选。
3. "Google always strives to staff its SRE teams with a mix of engineers with traditional software development experience and engineers with systems engineering experience." - SRE 需要不同背景的人才，而通过软件工程实践项目，减少 sre 工作量的同时，也是吸引和保留他们的重要手段。
4. 花了大篇章幅描述了一个关于「容量评估」的 case study, 感兴趣的可以看看。
5. "Because Google SRE teams are currently organized around the services they run, SRE-developed projects are particularly at risk of being overly specific work that only benefits a small percentage of the organization." - 过去一年我一直在探索如何快速创造业务价值，但确实存在文中说到的陷阱：产品的 scope 过小，例如一个 sre 负责一条业务线，最后设计的方案只适用该业务线，假设每条业务线都搞个类似的方案，不可避免的导致 duplicated efforts and wasted time。所以最近也常常思考，方案如何跨团队复用，在整个公司成为标准，甚至产品化对外输出。
6. "Dedicated, noninterrupted, project work time is essential to any software development effort." - 挺新奇的一个论点，SRE 务必强行保留一些专注于写代码的时间，才可以开始思考如何在不停的打断和 on-call 中去寻求平衡。
7. "Therefore, the ability to work on a software project without interrupts is often an attractive reason for engineers to begin working on a development project." - 哈哈，想起之前的玩笑：“希望每天来到公司，戴上降噪耳机，不用和一个人说一句话专心写代码，直到下班”。玩笑归玩笑，同时一定要提防 sre 不能变成一个纯开发！因为需要对生产环境的深刻理解和独特视角，才能创造出一个为 sre 自身服务的优秀产品，去解决真正的痛点："The unique hands-on production experience that SREs bring to developing tools can lead to innovative approaches to age-old problems"
8. "Therefore, you’re working against the natural instinct of an SRE to quickly write some code to meet their immediate needs." - 哈哈，完善的研发流程可能是必不可少的，但可能会违背 sre 的天性：因为 sre 都是快枪手，需要在第一时间止血解决问题，所以很多时候写代码也是一把梭，而这种不遵从软件开发规律偷懒的行为，最后反而会导致人力和资源更大的浪费。
9. "SREs often develop software to streamline inefficient processes or automate common tasks, these projects mean that the SRE team doesn’t have to scale linearly with the size of the services they support." - 回到 Software Engineering 必要性的问题，因为只有这样才能保证最核心的那个原则：业务的指数扩张与人员的增加不会成线性增长。最终每个 sre 员工，sre 团队，甚至整个公司都会因此收益。

## Chapter 19 - Load Balancing at the Frontend
how we balance user traffic between datacenters: 本章主要讲 google 如何在 idc 外部之间做负载均衡。而下一章会阐述如何在 idc 内部做负载均衡。

1. "when you’re dealing with large-scale systems, putting all your eggs in one basket is a recipe for disaster." - 很简单的道理，不能把鸡蛋放到一个篮子里，即不可以存在单点问题（去中心化）。
2. "The differing needs of the two requests play a role in how we determine the optimal distribution for each request at the **global** level" - 针对一个请求很难有最优的“策略”，因为会存在各种各样的变量。例如两个用户请求，分别是搜索和上传视频，前者追求的是更低的 RTT 以达到最快的响应，而后者则需要尽可能大的带宽。
3. 负载均衡策略的又分为以下两种：
    1. "Load Balancing Using DNS" - 但 DNS 有各种限制，想到了阿里的 GSLB
    2. "Load Balancing at the Virtual IP Address" - LVS, 转发的策略为`id(packet) mod N`, 这样所有属于一个连接的包都被转发到对应的机器上，并且是无状态的方案：不用在内存中记录每个连接与机器的对应关系。看上去很完美？但想象 backends 中有一台机器挂了被移除或者新机器上线的场景，那不就全部错位了，需要从头开始 hashing (mod 就是一种最基本的 hashing)，最后导致缓存命中率下降 db 负担增加。1997 年的时候，提出了一种新的方案叫做 [consistent hashing](https://dl.acm.org/citation.cfm?id=258660)：看了一下简单说就是将输入的 id 分为 n 个区间(假设 id 是 32 位的，那它肯定有一个取值的范围，头尾相接刚好形成一个环)，不同区间对应后台不同的机器，当上线或下线机器时，可以简单的分割或者合并区间。好美妙的算法，但如何保证不会出现热点问题呢？是不是在 consistent hashing 前要做一次预处理，以保证输入足够均匀。![](/images/blog/191006_adsense/15757909665620.jpg)


## Chapter 20 - Load Balancing in the Datacenter
"This chapter focuses on load balancing within the datacenter." - 紧接上一章，描述 idc 内部如何实现负载均衡，达到资源最优利用的目标。

1. "Before we can decide which backend task should receive a client request, we need to identify and avoid unhealthy tasks in our pool of backends." - 在做负载均衡之前，需要先找出不健康的任务并干掉。有分如下几种方法：
    - Flow Control: 设定活跃连接数上限的阈值，但缺点也很明显，会导致机器的资源无法被完全榨干（静态阈值的局限性）。
    - Lame Duck State: 为机器自身定义状态，分为 Healthy, Refusing connections & Lame duck(端口还可以继续接受请求，但明确告诉客户端不要再发送请求过来了)。但如何判断机器进入 `lame duck state` 呢🤔？貌似是有一定的健康检查机制。这样的好处是提升用户体验，不会直接得到一个错误的响应。
2. "A Subset Selection Algorithm" - 这部分有点复杂没太看懂，个人理解就是不同 Subset size 情况下(客户端)，后端机器资源整体利用率与每台机器负载平衡的 tradeoff. 
3. 负载均衡的常见策略：
    - ..



## Chapter 29 - Dealing with Interrupts
最近小明的公司故障频发，而遏制故障最佳的手段就是严控变更，对每一个线上变更做人肉审批。虽然风险确实被控制住了，但 trade off 在于 sre 值班人员会被无穷无尽的“骚扰”。这一章讲的是 sre 如何处理 interrupts，还是挺期待的。

1. "Any complex system is as imperfect as its creators. In managing the operational load created by these systems, remember that its creators are also imperfect machines." - 人无完人，所以由人设计出的系统也永远不会是完美的，就像保养车一样，人工的介入是无可避免的。
2. "flow time" - 程序员的贤者时间 XD 
2. "In order to limit your distractibility, you should try to minimize context switches." - 描述的好形象，为了使程序员减少上下文切换（被打断去处理别的事情），要让 working period 尽可能的长。理想是一个星期，但一般实践是一天或半天。换句话说，就是在某个时间段，只专注于计划好的事情，例如安排下周负责 on-call, 那他只需要把这一件事情做好，不再关注别的项目："A person should never be expected to be on-call and also make progress on projects (or anything else with a high context switching cost)."
3. "handover process" - 不管是告警处理，日常的单子等等，都需要有完善的转派机制。
4. "At some point, if you can’t get the attention you need to fix the root cause of the problems causing interrupts" - 有时候需要找到根因并彻底解决掉 interrupts 的源头。例如变更就是应该由系统保障的强制三板斧，去掉人工审批的环节，达到无人值守的目标。
5. "A caveat to the preceding solutions is that you need to find a balance between respect for the customer and for yourself. " - 这里并不是说不尊重客户，而是像很多开源项目的 issue 管理一样，用户首选要对自己负责，尽可能提供足够多的信息甚至最小重现的 case，开发者才能产出高质量的回答并帮助解决。


## Chapter 30 - Embedding an SRE to Recover from Operational Overload
之前文中提到一个词叫做 toil, 而 sre 很容易陷入不停做 toil 的自我麻痹中，看看这章是如何通过加入一个新的 sre 帮助团队从繁重的运维工作中解放出来的。

1. "One way to relieve this burden is to temporarily transfer an SRE into the overloaded team." - 抽调一个新的战力，加入到被运维重压下的 sre 团队。但不仅仅只是贡献人力，而是带来新的理念和更好的实践，来把 ticket queue 清空。
2. "SRE teams sometimes fall into ops mode because they focus on how to quickly address emergencies instead of how to reduce the number of emergencies. " - 很有道理的样子，因为任何表面现象都需要去深挖根因。🤔 " in a permanent way""encourages people to think about the basic principles" - 任何表面现象都需要去深挖根因。
3. "Releases need to be rollback-safe because our SLO is tight. Meeting that SLO requires that the mean time to recovery is small, so in-depth diagnosis before a rollback is not realistic." - 每个决策或者要求的背后都应该有强有力的逻辑支撑，这样才能让团队的每个人都心服口服的去执行。这样就算你离开这个团队了，你种下的一些理念才会根深蒂固的继续执行。



# 疑惑:
1. 四个9和五个9用户真的感知不到吗? 目标是极限的追求100%的reliability吗? 如何消除那些负面影响.
2. 如何衡量大家时间都花在哪了, 如何做到 toil 的限制
3. ..






















