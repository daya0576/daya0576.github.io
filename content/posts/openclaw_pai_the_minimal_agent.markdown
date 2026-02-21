---
title: "在新时代重新学习“编程” - #5 读 Pi: The Minimal Agent Within OpenClaw"
date: 2026-02-21T13:49:18+08:00
draft: true
TOC: true
categories:
- AI
- 编程
series:
- ai_freshman
---

> OpenClaw runs a single embedded agent runtime derived from pi-mono.

从 [OpenClaw 文档](https://docs.openclaw.ai/concepts/agent)中无意读到 Agent Runtime 是基于 [pi-mono](https://github.com/badlogic/pi-mono/) 开发的。凑巧又读到大名鼎鼎 Armin 的一篇文章：[Pi: The Minimal Agent Within OpenClaw](https://lucumr.pocoo.org/2026/1/31/pi/)。以表尊重，简单记录一下。


# 原文摘要

> Despite the differences in approach, both OpenClaw and Pi follow the same idea: LLMs are really good at writing and running code, so embrace this.

OpenClaw 与 Pi 遵循同样的思路：既然大模型那么擅长输出文字与代码，不如放手全权交给它们。

## What is Pi?

> Pi is interesting to me because of two main reasons:
> - First of all, it has a tiny core. It has the shortest system prompt of any agent that I’m aware of and it only has four tools: Read, Write, Edit, Bash.
> - The second thing is that it makes up for its tiny core by providing an extension system that also allows extensions to persist state into sessions, which is incredibly powerful.

Pi 吸引原文作者的两个原因：
- 首先 Pi 非常轻量，它的 prompt 比任何 agent 都要短，仅仅内置了四大金刚工具：`Read`, `Write`, `Edit`, `Bash`.
- 在精简内核之上，提供了强大的插件系统（支持状态持久化到 session 中），最终实现无限可能。

> Pi also is a collection of little components that you can build your own agent on top. That’s how OpenClaw is built, and that’s also how I built my own little Telegram bot and how Mario built his mom.

Pi 不仅是一个 agent，还提供组件方便用户二次开发，来构建你自己的 agent。

P.S. OpenClaw 就是这样基于 Pi 构建的

## What’s Not In Pi

> And in order to understand what’s in Pi, it’s even more important to understand what’s not in Pi, why it’s not in Pi and more importantly: why it won’t be in Pi. The most obvious omission is support for MCP. 
> And this is not a lazy omission. This is from the philosophy of how Pi works. Pi’s entire idea is that if you want the agent to do something that it doesn’t do yet, you don’t go and download an extension or a skill or something like this. You ask the agent to extend itself. It celebrates the idea of code writing and running code.

Pi 设计哲学：**代码生代码** --- 假如用户想扩展 agent，不是去人工下载扩展或安装 skill，而是让 agent 自我成长（自己扩展自己）。所有很自然的， MCP 并不在 Pi 的实现中。

## Agents Built for Agents Building Agents



# 源码阅读



# 参考
1. https://lucumr.pocoo.org/2026/1/31/pi/