---
title: "在新时代重新学习“编程” - #6 造轮子"
date: 2026-03-09T09:00:30+08:00
categories:
- AI
- 编程
series:
- ai_freshman
---

最近闲下时，便会尝试搜索 Vibe Coding 的课程，尝试“系统性”学习新时代编程的最佳实践。但奇怪的是每次都无功而返，找不到心仪的课程。仔细一想，似乎倒也在情理之中？毕竟在没有 AI 的旧时代，“古法编程”也没有一成不变的模版套路。

另一个原因，或许是表面写代码的「工具」改变了，但底下软件开发的基本原则与最佳实践从未改变。所以问题可以转化为：<u>应该如何学习这个新工具呢？？</u>

> “大三，想暑假通过实习积累一些经验和丰富简历，但是不知道现在应该先学点什么为实习和求职面试准备一下”

苦苦不得其解，直至一天偶然看到一条帖子👆。作为“过来人”，个人可能会给出两条建议：1）向 AI 求助 2）尽早开始面试，通过面试来准备面试。

转念一想，在新时代重新学习“编程”，似乎也异曲同工：1）agent 本身除了写代码也是开发者最好的指导老师 2）通过编程来学习编程 - 俗称造轮子


## 造轮子

> Pi also is a collection of little components that you can build your own agent on top. That's how OpenClaw is built, and that's also how I built my own little Telegram bot and how Mario built his mom. If you want to build your own agent, connected to something, Pi when pointed to itself and mom, will conjure one up for you.

说干就干，由于 OpenClaw 黑盒调试的痛苦，准备基于 Pi 从零开始开发一款极简 + 自管理的 iMessage Agent --- 支持自己编写工具、插件、技能，最终成为家庭的一份子。

功能拆解（优先级排序）：
1. 消息收发：私聊/群聊/短信消息（图片、输入提示、表情..）。
2. 消息历史：消息持久化，支持网页端查看甚至回复
3. 插件系统：支持用户编写自定义插件（typescript 脚本）
4. 定时任务：定时唤醒（heartbeat）
5. 沙箱环境：隔离执行代码（sandbox）
6. 记忆系统：跨对话记东西
7. 技能管理：可扩展能力模块（skills）

在 agent 的帮助下，花费一周开发出了 POC：

![](/images/blog/global/17730189476545.jpg)


## 开发工具选择

工欲善其事，必先利其器，个人选择 Pi 作为 coding agent（关于 Pi 是什么，参考上一篇文章：[读 Pi: The Minimal Agent Within OpenClaw](/blog/20260224/openclaw_pai_the_minimal_agent/)）

短短几日的开发体验，令人有种“沉迷游戏”的罪恶感。值得一提的是，在编写项目代码的过程中，可以快速让 Pi 自己给自己开发插件与技能，例如：
- `tmux-cursor`: 在 tmux 中失去焦点时隐藏编辑器光标，获得焦点时恢复 - 切换 panel
- `tmux-window-name`: agent 运行时在 tmux 窗口名后追加 [busy]/[done] 状态标识 - 用于并发使用 agent
- `plan-mode`: 进入只读模式，仅是阻止所有文件修改操作。
- `protect-markdown-files`: 拦截所有 .md 文件的修改，弹出交互式确认框（允许/拒绝/反馈/手动编辑）
- ...

常用的开发布局：
1. 左边使用 vim 编辑文档，review 代码，..
2. 右上角运行 Coding Agent，与他沟通并修改代码
3. 右下角运行临时的命令或脚本
4. 通过不同的 window 并行管理子模块的开发

![开发布局截图 - vim + coding agent + tmux](/images/blog/global/Xnip2026-03-05_15-33-33.png)


## 困惑

由于是从零开始的项目，尝试以下协作模式：
1. 人类编写维护 Markdown 文件，包含 AGENT.md、research、design 等
2. 机器新增/修改所有测试用例、代码和配置文件。

在项目的初期为了让 agent 更好的工作，甚至尝试设计了一个 `feature.jsonc`，专门用于维护 `feature -> 子 feature -> testcases` 之间的关系。

然而这种结构化的强约束反而逐渐成为了束缚，因为个人对于 iMessage 的工作机制以及调研的不断进行，代码时刻在快速调整。

最后突然发现，有没有可能：代码从某种程度上来说，就是最好的文档？所以仅维护进度 Markdown，并**主动 review 自动生成的每一行代码**（至少将不同子模块的职责尽可能解耦，同时多了几分乐趣。。）


## 最后

作为读者，你觉得：

1. 你最喜欢的 Claude Code/OpenCode 的功能是？
2. Agentic coding 中，文档和代码的维护的最佳方式？
3. 2026 年了，你还会阅读代码生成的代码吗？
4. 为什么感觉静态前端代码生成后不需要过多介入，但后端的代码如果不 review 很容易“腐化”？