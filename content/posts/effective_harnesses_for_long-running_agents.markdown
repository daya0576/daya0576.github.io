---
title: "Effective_harnesses_for_long Running_agents"
date: 2026-02-15T21:03:36+08:00
draft: true
---

> Agents still face challenges working across many context windows. We looked to human engineers for inspiration in creating a more effective harness for long-running agents.

从 VIM 里通过 Copilot 自动补全，到 VSCode 中对话式的 vibe coding，最近在想 --- 有没有可能更进一步：只提供需求背景和明确的期望结果，剩下的让 agent 长时间运行直到搞定呢？（while loop 运行若干小时，甚至几天）

尝试了 Spec Driven Development ([spec-kit](https://github.com/github/spec-kit))，一言难尽，有种在 2026 年开**手动挡**汽车的别扭感。。想要人工掌控细节，却反而导致了频繁的熄火。// 可能因为人是最大的瓶颈。

阅读了一篇文章：[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)，来了解背后的问题、和解决办法。

# 名词解释 - Glossary

- 员工：claude agent
- 新员工：
- feature：用户需求

# 问题分析

> The core challenge of long-running agents is that they must work in discrete sessions, and each new session begins with no memory of what came before.

为了实现 agent **自主地**超长时间运行，最大的问题在于：**每次开启新的 session 后，之前的上下文完全丢失**。想象你每隔一天都招聘一个新员工来帮你编程干活： 1） 模型喜欢一口吃成胖子，倾向于一次性做很多，却往往干到一半留了个烂摊子，下个人只能靠“猜”来继续完成工作。2）假如在已有项目上开发新需求：虽然代码没有 bug 并且注释清晰明确，但理解已有代码的成本也特别高。

应对策略相对应地分为两个部分：
1. **Initializer agent**：帮助模型初始化环境，包含 `init.sh` 脚本，`claude-progress.txt` 文件，以及一个初始化的 git commit。
2. **Coding agent**：每次增量改动完成后，记录新完成的工作与进度，提交代码并关闭 session --- 保持一个“干净”的状态（确保下个全新的 session 开启时，可以通过持久化的文件中，快速理解当前状态与进度）。

// TODO：例子

# 环境管理

## 需求拆解
将用户最初的需求，拆解为一系列小需求。例如用户想构建一个一模一样的 claude.ai，自动分解为 200+ 需求。

为什么 json 而不是 markdown？
因为 json 文件不容易被模型 乱改或 overwrite 

## Incremental progress

为了避免上文提到的“一口气吃成胖子”的问题，限制 agent 一次只做一个小需求。并且每次完成后，需要保持一个 clean state：提交代码，并在 process 文件中进行总结 -》 同时方便 revert code 与“新员工”快速接收。

## Testing

为了避免 agent 没有测试就偷偷将 feature 标识为完成，通过明确的指令让 agent 通过自动化游览器工具，模拟人完成端到端的测试。

## Getting up to speed

新员工接手时，简单却提升效率的小技巧（节省了大量 token，因为不需要从头重新理解整个 codebase）：
1. 查看当前目录文件
2. 阅读 git log 历史记录
3. 选择未完成的并优先级最高的需求

```
1. Run pwd to see the directory you’re working in. You’ll only be able to edit files in this directory.
2. Read the git logs and progress files to get up to speed on what was recently worked on.
3. Read the features list file and choose the highest-priority feature that’s not yet done to work on.
```

# 挑战

1. 假如将单个专职 agent 拆解为专职的多个 agent 协同作业，例如测试 agent，质量保证 agent。会不会做的更好。
2. 这篇文章的实践仅限于前后端 web 项目的开发，其他领域？


# References
1. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
2. https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding





