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

从 OpenClaw 文档中无意读到其 Agent Runtime 是基于 [pi-mono](https://github.com/badlogic/pi-mono/) 开发的。凑巧看见大名鼎鼎 Armin 的一篇文章：[Pi: The Minimal Agent Within OpenClaw](https://lucumr.pocoo.org/2026/1/31/pi/)。以表尊重，简单记录一下。


# 原文摘要

> Despite the differences in approach, both OpenClaw and Pi follow the same idea: LLMs are really good at writing and running code, so embrace this.

OpenClaw 与 Pi 遵循同样的思路：既然大模型那么擅长输出文字与代码，不如放手全权交给它们。

## 什么是 Pi?

个人补充：Pi 是一个可扩展的 AI Agent 分为以下几层：
```
pi-mom                  # Slack bot，面向团队的自管理工作助手
└── pi-coding-agent     # 完整的终端编码 agent（pi CLI），含 session/tools/extensions/skills
    ├── pi-agent-core   # 通用 agent 引擎：状态机、tool 执行循环、事件流
    │   └── pi-ai       # 底层 LLM 统一接口：多 Provider、流式输出、工具调用
    └── pi-tui          # 终端 UI 组件库：Editor/Markdown/SelectList/差分渲染
```

> Pi is interesting to me because of two main reasons:
> First of all, it has a tiny core. It has the shortest system prompt of any agent that I’m aware of and it only has four tools: Read, Write, Edit, Bash.

项目 Pi（minimal agent）吸引原文作者的两个原因：

### 1）首先 Pi 极其轻量

code agent 的 system prompt 极其精简（作者称是所有 agent 中最短的）：

{{< github-code url="https://github.com/badlogic/pi-mono/blob/380236a003ec7f0e69f54463b0f00b3118d78f3c/packages/coding-agent/src/core/system-prompt.ts#L147-L164" >}}

```ts
let prompt = `You are an expert coding assistant operating inside pi, a coding agent harness. You help users by reading files, executing commands, editing code, and writing new files.

Available tools:
${toolsList}

In addition to the tools above, you may have access to other custom tools depending on the project.

Guidelines:
${guidelines}

Pi documentation (read only when the user asks about pi itself, its SDK, extensions, themes, skills, or TUI):
- Main documentation: ${readmePath}
- Additional docs: ${docsPath}
- Examples: ${examplesPath} (extensions, custom tools, SDK)
- When asked about: extensions (docs/extensions.md, examples/extensions/), themes (docs/themes.md), skills (docs/skills.md), prompt templates (docs/prompt-templates.md), TUI components (docs/tui.md), keybindings (docs/keybindings.md), SDK integrations (docs/sdk.md), custom providers (docs/custom-provider.md), adding models (docs/models.md), pi packages (docs/packages.md)
- When working on pi topics, read the docs and examples, and follow .md cross-references before implementing
- Always read pi .md files completely and follow links to related docs (e.g., tui.md for TUI API details)`;
```

并仅仅内置了“四大金刚”工具：`Read`, `Write`, `Edit`, `Bash`

{{< github-code url="https://github.com/badlogic/pi-mono/blob/3a3e37d39014acc4269171be2a51518f6a71be1f/packages/coding-agent/src/core/tools/index.ts#L87" >}}

```ts
// All available tools (using process.cwd())
export const allTools = {
	read: readTool,
	bash: bashTool,
	edit: editTool,
	write: writeTool,
	grep: grepTool,
	find: findTool,
	ls: lsTool,
};
```

其中工具 `Write` 的逻辑：
- 输入：path（文件路径）+ content（完整文件内容）
- 逻辑：创建新文件或完全重写（自动创建目录）
- 输出：`{ type: "text", text: "Successfully wrote N bytes to <path>" }`

> The second thing is that it makes up for its tiny core by providing an extension system that also allows extensions to persist state into sessions, which is incredibly powerful.

### 2）强大的插件系统
精简内核之上，提供了强大的[插件系统](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions)（支持状态持久化到 session 中），最终实现无限可能。

在 Pi 在，插件本质上是一个 TypeScript 模块，用于扩展


> Pi also is a collection of little components that you can build your own agent on top. That’s how OpenClaw is built, and that’s also how I built my own little Telegram bot and how Mario built his mom.

Pi 不仅是一个 agent，还提供方便用户二次开发，来构建你自己的 agent。

P.S. OpenClaw 就是这样基于 Pi 构建的



## What’s Not In Pi

> And in order to understand what’s in Pi, it’s even more important to understand what’s not in Pi, why it’s not in Pi and more importantly: why it won’t be in Pi. The most obvious omission is support for MCP. 
> And this is not a lazy omission. This is from the philosophy of how Pi works. Pi’s entire idea is that if you want the agent to do something that it doesn’t do yet, you don’t go and download an extension or a skill or something like this. You ask the agent to extend itself. It celebrates the idea of code writing and running code.

Pi 设计哲学：**代码生代码** --- 假如用户想扩展 agent，不是去人工下载扩展或安装 skill，而是让 agent 自我成长（直接生成需要的代码）。所有很自然的，MCP 并不在 Pi 自身的实现中。


## Agents Built for Agents Building Agents

> So for instance, Pi’s underlying AI SDK is written so that a session can really contain many different messages from many different model providers.

session 与 模型解耦：一个 session 可以在中途切换任意模型提供商，不依赖某个模型独有的特性。

> Because this system exists and extension state can also be persisted to disk, it has built-in hot reloading so that the agent can write code, reload, test it and go in a loop until your extension actually is functional.
> 
> Even better: sessions in Pi are trees.

除了人与 AI 对话，session 文件中还维护了自定义的**系统状态与插件状态**。由于文件被持久化，所以支持**热重载**，最终实现 agent 的不断进化：自己写扩展的代码，验证，测试 --- 不停循环这一过程，直到符合预期。

文中提到另一个巧妙设计：session 在 Pi 中的结构为树形，例如处理一个复杂主任务的过程中，支持不断开启“干净”的子 session 处理子任务，避免主任务 context 爆炸。

以使用 MCP 为例，工具的定义需要在 session 初始化时，就被塞到 context 中。如果中途需要修改，则需将之前所有对话作废，重新开启一个新的 session。

## Tools Outside The Context

下面分享作者让 pi 自己构建的几个扩展：

### [/answer](https://github.com/mitsuhiko/agent-stuff/blob/main/pi-extensions/answer.ts)

> I don’t use plan mode. I encourage the agent to ask questions and there’s a productive back and forth.

作者认为让 agent 根据上下文主动问问题，远比 Claude Code 的 think 模式更高效。下图为一个友好的 TUI 交互，自动解析 agent 的问题让用户输入回答。

![pi-answer](/images/blog/global/pi-answer.png)

### [/todos](https://github.com/mitsuhiko/agent-stuff/blob/main/pi-extensions/todos.ts)

通过本地 TODO list 管理 agent 任务。

![](/images/blog/global/17717460456678.jpg)

### [/review](https://github.com/mitsuhiko/agent-stuff/blob/main/pi-extensions/review.ts)

让 agent 相互 review 代码：

```
普通 session（线性）：
消息1 → 消息2 → 消息3 → 消息4 → ...

# Pi session（树形）：
消息1 → 消息2 → 消息3
                    ├── 分支A：写代码
                    │       ↓
                    │   分支B：review代码（全新视角）
                    │       ↓
                    └── 回到消息3，带着修复继续
```

### [/control](https://github.com/mitsuhiko/agent-stuff/blob/main/pi-extensions/control.ts)

Multi-agent 的情况下，通过该命令在 agent 中直接控制另外的 agent

P.S. 完整的插件列表：https://github.com/mitsuhiko/agent-stuff/tree/main/pi-extensions

## Software Building Software

上面几个有趣的例子，都是 agent 自己从零开始自己编写用户的想法，没有 MCP，也没有 SKILL --- 软件生软件。

而 OpenClaw 则将这理念做到极致：没有独立界面，也没有 APP，直接接入日常聊天工具。



# 个人感受





# 参考
1. https://lucumr.pocoo.org/2026/1/31/pi/
2. https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/extensions.md