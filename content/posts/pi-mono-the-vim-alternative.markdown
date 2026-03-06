---
title: "在新时代重新学习“编程” - #6 Pi Coding Agent 初体验"
date: 2026-03-05T14:41:30+08:00
toc: true
draft: true
categories:
- AI
- 编程
series:
- ai_freshman
---

最近闲下时，便会尝试搜索 Agentic Coding 课程，尝试系统性学习新时代编程的最佳实践。但奇怪的是每次都无功而返，找不到心仪的课程。仔细一想，似乎倒也在情理之中？毕竟在没有 AI 的时候，“古法编程”也没有一成不变的模版套路。所以在 AI 新时代，应该如何重新学习“编程”呢？

> “大三，大学基本没有什么竞赛经历，想暑假通过实习积累一些经验和丰富简历，但是不知道现在应该先学点什么为实习和求职面试准备一下”

直到一天偶然看到一位大学生的发帖求助👆。作为“过来人”，个人会给出两条建议：1）向 AI 求助 2）尽早开始面试，通过面试来准备面试。

转念一想，在新时代重新学习“编程”，似乎也异曲同工：1）agent 就是开发者最好的老师 2）通过编程来学习编程 - 俗称造轮子。


## 造轮子

说干就干，准备从零开始开发一款**极简**（minimal）+ **自管理**（self-managing）的 [iMessage Bot](https://github.com/daya0576/pi-imessage) - 支持自己编写工具、插件、技能。最终成为家庭的一份子。


## 工具选择

工欲善其事，必先利其器，个人选择 Pi 作为 coding agent（关于 Pi 是什么，参考上一篇文章：[读 Pi: The Minimal Agent Within OpenClaw](/blog/20260224/openclaw_pai_the_minimal_agent/)）

短短几日的开发体验，令人有种“沉迷游戏”的罪恶感。值得一提的是，在编写项目代码的过程中，可以快速让 Pi 自己给自己开发插件，例如：
- `tmux-cursor`: 在 tmux 中失去焦点时隐藏编辑器光标，获得焦点时恢复 - 切换 panel
- `tmux-window-name`: agent 运行时在 tmux 窗口名后追加 [busy]/[done] 状态标识 - 用于并发使用 agent
- `plan-mode`: 进入只读模式，阻止所有文件修改操作，支持 /plan 命令和 Ctrl+X 快捷键切换
- `protect-markdown-files`: 拦截所有 .md 文件的修改，弹出交互式确认框（允许/拒绝/反馈/手动编辑）
- `answer`: 从上一条 assistant 消息中提取问题，弹出交互式 Q&A 界面逐一作答后发送给 agent，Ctrl+. 触发
- ...

常用的开发布局：
1. 左边使用 vim 编辑文档，review 代码，..
2. 右上角运行 Coding Agent，与他沟通并修改代码
3. 右下角运行临时的命令或脚本
4. 通过不同的 window 并行管理

![开发布局截图 - vim + coding agent + tmux](/images/blog/global/Xnip2026-03-05_15-33-33.png)

## 困惑

由于是从零开始的项目，尝试以下协作模式：
1. 人类编写维护 Markdown 文件，包含 AGENT.md、research、design 等
2. 机器新增/修改所有测试用例、代码和配置文件。

在项目的初期为了让 agent 更好的工作，甚至尝试设计了一个 `feature.jsonc`，专门用于维护 `feature -> 子 feature -> testcases` 之间的关系。

然而这种强约束反而逐渐成为了束缚，因为个人对于 iMessage 的工作机制以及 research 的不断进行，代码时刻在快速调整。

最后突然发现，有没有可能：代码从某种程度上来说，就是最好的文档？所以仅维护进度 Markdown，并**主动 review 自动生成的每一行代码**（至少将不同子模块的职责尽可能解耦，同时多了几分乐趣。。）

## 最后

作为读者，你觉得：

1. agentic coding 中，文档和代码的维护的最佳方式？
2. 你会阅读代码生成的每一行代码吗？