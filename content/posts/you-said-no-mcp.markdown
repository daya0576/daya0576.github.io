---
title: "读 You Said No MCP"
toc: true
date: 2026-10-01T05:00:00+08:00
categories:
- AI
- Pi
series:
- Pi
---

> https://earendil.com/posts/you-said-no-mcp/

在过去的一年，Pi 是坚决的 MCP 抵制者（[What if you don't need MCP at all?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)），原因一是由于大量的冗余描述信息占用了珍贵的上下文，二是难以扩展，三是无法自由组合。所以 Pi 的作者出于极简的原则，选择直接让 agent 直接使用 cli 通过编写代码与 server 交互。而在近日发布的 [v0.99.0](https://github.com/earendil-works/pi/releases#release-v0.99.0) 版本中，Pi 竟然新增了对 MCP 的支持。

这篇文章将快速一探究竟这个变化的前因后果。

## 时代在变化

首先作者提醒大家，时代一直在变化，今天的 MCP 早已不是一年前的 MCP。但仅仅凭这一点，还不足以将 MCP 集成到 Pi 中。众所周知，Pi 拥有非常优秀的插件生态，为什么不将 MCP 做成一个插件呢？过去确实是的，例如官方认可的 pi-mcp-adapter。但今天的 MCP 进入了 Pi core，是开发团队一起深思熟虑后的结果。

## 什么变了

将 MCP 引入 core 不仅仅是因为 MCP 变好了，而是引入 MCP 对应的重构优化本身就很通用，例如可以帮助 Pi 更好地使用 Jev（文末会有一个小例子）。换句话说，Pi 当前所缺失的能力与集成 MCP 所需的能力非常相似：一个以解释器形式存在的沙盒（Code Mode）。

虽然 MCP 一直在改进，但它最大的问题还是在与**无法组合**，即使在 Code Mode 中也没有彻底解决。但根结并不在于 MCP 协议本身，而是各家 harness 使用方式的问题。例如许多 harness 会把 tools 无脑全部塞入上下文，导致接入一个 MCP 后，模型每轮都会看到它全部 20+ 个 tools 的定义。更糟糕的是 server 为了迎合这种做法，节省 token，会直接返回了直接阅读的文本，而不是结构化数据。作者认为更好的做法是类似 OpenAPI + [intelligent tool discovery](https://github.com/earendil-works/pi/blob/v0.99.2/packages/coding-agent/docs/mcp.md#control-tool-exposure)（tools 工具返回结构化数据，并通过文档和描述按需使用）。

而 CLIs 非常实用，没有上述缺点的原因在于：agent 可以使用 pipeline 等 bash 小工具，将不同命令串起来。所以 MCP 也应该这样使用，将对应的 tools 直接暴露给 JavaScript 沙盒，让模型自己自由写代码串起来。

## MCP in a Modern LLM

最近几个月，Pi 做了大量工作来适配现代最新模型的三个能力：1）tool 延迟按需加载 2）在对话中途插入 system message 3）在对话中途调整 thinking level。然而当前的 tool 配置还没来得及重构升级，很难适配这些新能力。

所以为了用好 Code Mode，每个 tool 需要支持定义 metadata ------ 是否可以直接暴露给 LLM，还是只能在 Code Mode 中使用（参考 [Tool exposure](https://github.com/earendil-works/pi/blob/v0.99.2/packages/coding-agent/docs/extensions.md#tool-exposure)）。当前的 MCP 插件，从现有的 tool 里拿不到这些 metadata，自然无法做到最优体验。

但这带来了一个新的问题：为什么不提供一个不包含 MCP 的 Code Mode 呢？

> So we want to be part of that conversation and help shape it to work well in small harnesses instead of standing on the sidelines and just watching.

新增 Tool exposure 后，插件确实同样可以做到一样的效果。但作者表示相比于袖手旁观，更希望直接拥抱 MCP 来影响它，让它在不断变好的路上持续前行。

P.S. 改变世界的一个例子（联动 MCP 的作者）

<blockquote class="twitter-tweet" data-lang="en" data-theme="dark"><p lang="en" dir="ltr"><a href="https://x.com/figma?ref_src=twsrc%5Etfw">@figma</a> please fix this <a href="https://t.co/8F4ZJSiLoM">https://t.co/8F4ZJSiLoM</a></p>&mdash; David Soria Parra (@dsp_) <a href="https://x.com/dsp_/status/2105241259887444440?ref_src=twsrc%5Etfw">September 30, 2026</a></blockquote> <script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>


## 什么是 Code Mode

当 harness 执行 tools 时，一般分为两类：
1. bash 执行，例如 bash 执行命令，或 read、write、edit 文件
2. agent loop，例如调用 LLM API、管理 session等

Code Mode 跑在 agent loop 上，可以将它理解为一个 编排 tools call 的小沙箱：使用 javascript 灵活决定执行顺序并自由组合执行结果。带来的另一个直接好处：所有运行的中间结果都会记录在 session 中，而不像 bash 脚本保存本地的临时文件（方便恢复 session 或切换分支）。

如文章开头提到的，Code Mode 的用途远不止于 MCP，例如：

> “使用 typesafe/jev 通过 codemode 找出最可能是垃圾的 10 封邮件”

Pi 就会聪明地自动组合 MCP 与 Jev 来完成分析，整个过程几乎不浪费占用上下文。

{{< figure src="/images/blog/global/17908427031933.jpg" alt="Pi 自动搜索隐藏的 MCP 工具" caption="自动发现隐藏的 MCP 工具" >}}

{{< figure src="/images/blog/global/17908424193724.png" alt="Pi 通过 Code Mode 调用 Jev" caption="通过 Code Mode 调用 Jev" >}}

