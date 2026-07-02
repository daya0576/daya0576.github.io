---
title: "读 Building Pi and Self Modifying Software"
date: 2026-05-04T15:09:41+08:00
categories:
- AI
- Pi
series:
- Pi
---

<div class="video-wrapper">
<iframe src="https://www.youtube.com/embed/n5f51gtuGHE?si=04jzhHHoCdoHk5-a" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

Mario 和 Armen 的专访，简单记录观看的几点笔记。

> "..I think like human progress comes from like building on top of each other"
> 
> "..I really didn't care that it spits out GPL code and doesn't attribute like I was like oh maybe this will just completely destroy copyrights and like for me that was like oh this is I'm fine with it."

Armin 认为所有人都应该无私的共享，因为人类的进步就来自于相互借鉴。例如在员工可以把「知识」从公司带走而不受到竞业限制（有利于整体环境的长远利益）。而 AI 的出现，虽然“偷”走了他的代码，但他一点也不生气，因为从某种角度，粉碎了版权保护制度，反而是一件好事。

最近 CC 给我取个外号，叫做“爽气哥”，反讽我的小气。读完这段话后，深受启发，我决定以后做个大气的人。

> A good engineer is an engineer that says no a lot and I dont need this a lot, because that keeps complexity down.

Armin 与 30+ 个技术团队沟通，观察他们是如何在工作中使用 agent。有趣的是，当这些人有假期时（例如圣诞🎄），反而有更多机会和时间，沉浸式地去尝试和体验最新的工具。

但更大更频繁的 PR，很快导致软件质量下降，Armin 认为背后的原因在于 1）工程师会替未来的自己负责，相反 agent 完全没有这种意识和约束，生成的代码总会有一种“坏味道”；2）非工程师也开始普遍开始参与软件开发，例如销售用在官网中新增了一个根本不存在的功能，但没有一个人注意到；3）一个好的工程师勇于说“不”，通过拒绝来维持系统的复杂度。而 agent 的便利性让用户什么都想要，反而导致了各种各样的问题；4）参考热力学第二定律，代码库如果放任不管，只会趋向于混乱。必须持续投入额外的精力，避免 AI 产生的代码增加熵。而完全使用 agent 写代码时，很容易让项目“偷偷”变得混乱，难以维护。

Mario 的补充：agent context 上下文窗口有限，无法获取到所有相关信息，导致产出“垃圾”。

> "The way I deal with ensuring high quality is I refactor mercilessly, because that pulls me into the codebase."

<u>如何提升代码质量 & 降低复杂度？</u>当手动写代码时，你能感受到代码开始不对在腐化，你会停下来去花时间**重构**，同时也是重新深入理解代码的最佳途径。而通过 coding agent 不断新增代码的方式，让用户完全失去了这种“嗅觉”，陷入了恶性循环。所以为了保持项目代码质量，还是要保持重构的习惯。

<u>但假如所有的代码都是 AI 生成的，我们要怎么去重构呢？</u> 代码分级，对于核心代码要重点关注，例如 pi 中的 agent loop 的代码会逐行阅读经常重构，而将 session 导出至 html 的代码作者从来没看过。

> "We write a big spec that hopefully will result in something crazy… The best possible spec is the software itself."

很多公司在吹嘘，组建一支全自动的 agent 大军，丢给它们 spec 后就开始自动工作。而 Mario 对于这种方式产出的代码质量存疑：1）人写的 spec 不可能是完美的，而最好最全面的 spec 或许就是软件代码本身 2）agent 不应该用于完全取代人类，而是帮助人类从重复性的工作中解放出来，去专注做只有人能做的事；3）提升效率 100x 倍，大概率只会产出 100 倍的问题，最后导致没有人可以理解。

> MCP vs Cli

agent 非常擅长编写与运行代码，与其用 MCP 绕一圈，不如直接让模型写脚本。

> "And I read recently Breakneck, which I unfortunately forgot the author of. It sort of goes a little bit into an exploration of like how China works and how maybe Europe and the US are different. And I found it at least thoughtprovoking."

最后主持人让嘉宾各自推荐一本书：
- Mario：《编码 : 隐匿在计算机软硬件背后的语言》
- Armin：《Breakneck: China's Quest to Engineer the Future》 --- 剖析中国在技术和经济领域快速崛起的原因，以及与西方的差异。






