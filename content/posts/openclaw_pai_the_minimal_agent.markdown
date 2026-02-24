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

从 OpenClaw 文档中无意读到其 [Agent Runtime](https://docs.openclaw.ai/concepts/agent) 基于 Pi 开发的（[badlogic/pi-mono](https://github.com/badlogic/pi-mono/) ）。

凑巧又阅读到 Armin 的一篇文章：[Pi: The Minimal Agent Within OpenClaw](https://lucumr.pocoo.org/2026/1/31/pi/)。

本文好奇学习一下 pi-mono 到底是什么？与 OpenClaw 的关系是？


## 什么是 Pi?

Pi 是一个 coding agent（简单理解为一个 claude code 替代品）：

项目本身具备优秀的分层设计，下图为多个子模块之间的依赖关系：
```
pi-mom                  # Slack bot，
└── pi-coding-agent     # 完整的终端编码 agent（pi CLI），含 session/tools/extensions/skills
    ├── pi-agent-core   # 通用 agent 引擎：状态机、tool 执行循环、事件流
    │   └── pi-ai       # 底层 LLM 统一接口：多 Provider、流式输出、工具调用
    └── pi-tui          # 终端 UI 组件库：Editor/Markdown/SelectList/差分渲染
```


## 设计理念

> Despite the differences in approach, both OpenClaw and Pi follow the same idea: LLMs are really good at writing and running code, so embrace this.

OpenClaw 与 Pi 遵循同样的设计理念：既然大模型那么擅长输出文字与代码，不如放手全权交给它们。


## 大道至简

> Pi is interesting to me because of two main reasons:
> First of all, it has a tiny core. It has the shortest system prompt of any agent that I’m aware of and it only has four tools: Read, Write, Edit, Bash.

项目 Pi 吸引原文作者的两个原因 ♥️：

### 1）极简 - minimal agent
Pi 的 system prompt 是所有 agent 中最短的：

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

以及仅仅内置了“四大金刚”工具：`Read`, `Write`, `Edit`, `Bash`

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
- 输出：`{ type: "text", text: "Successfully wrote N bytes to <path>" }`

### 2）强大的插件系统

> The second thing is that it makes up for its tiny core by providing an extension system that also allows extensions to persist state into sessions, which is incredibly powerful.

精简内核之上，提供了强大的[插件系统](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions) --- 自由生长，实现无限可能 ∞（待下文将详细介绍）


## Pi 没有什么

在理解 Pi 中有什么前，先通过 Pi 中没有什么来理解边界。

<u>Pi 为什么不支持 MCP（Model Context Protocol）？</u>   
Pi 的核心理念是 **代码生代码** --- 假如用户想扩展 agent 的能力时，不是去人工下载安装 skill，而是让 agent 自我生长（直接生成需要的代码）。所有很自然的，MCP 并不在 Pi 自身的实现中。

换句话说：
- 传统思路 → 人类去找插件、装插件
- Pi 的思路 → 让 agent 自己写代码解决问题（*Agents Built for Agents Building Agents*）


## Pi 有什么

Pi 中的几个重要特性：
1. **session 与模型解耦**：中途可切换任意模型提供商，不依赖某个模型独有的特性。
2. **session 持久化与热加载**：session 不只存储对话，还维护插件状态（持久化到磁盘） -> 支持热重载 -> 最终实现 agent 的不断自我进化：写代码、验证、热加载测试，循环迭代，直到符合预期。
3. **session 树**：Session 以树形结构组织，处理复杂主任务时，可随时开启"干净"的子 Session 处理子任务，避免主 context 爆炸。

## 实际例子

通过两个例子说明上面的特性：

### 1）Hello World（持久化与热重载）

在 Pi 中输入一句话需求：*"create a hello world extension and give me a demo of persist state"*

Pi “瞬间”完成一个插件的编写，热加载后新增 `hello` & `hello-stats` 两个命令。从下图中可以看到调用记录被持久化保存在 session 中：

![Xnip2026-02-23_17-13-15](/images/blog/global/Xnip2026-02-23_17-13-15.png)

说明：「持久化」信息保存于每个回话对应的 session 文件中，类型为 `custom`：

```
# ~/.pi/agent/sessions/xxx/<timestamp>_<uuid>.jsonl
{"type":"session","version":3,"id":"44836a7f-47f1-4047-867b-233d495add06","timestamp":"2026-02-23T07:35:17.546Z","cwd":"/Users/henry/repo/study/pi-mono-demo"}
{"type":"model_change","id":"627a6ce7","parentId":null,"timestamp":"2026-02-23T07:35:17.547Z","provider":"github-copilot","modelId":"claude-sonnet-4.6"}
{"type":"thinking_level_change","id":"83b9bc8f","parentId":"627a6ce7","timestamp":"2026-02-23T07:35:17.547Z","thinkingLevel":"low"}
{"type":"custom","customType":"hello-world:visit","data":{"name":"henry","timestamp":1771832189578},"id":"9e85fcde","parentId":"83b9bc8f","timestamp":"2026-02-23T07:36:29.578Z"}
{"type":"custom","customType":"hello-world:visit","data":{"name":"harry","timestamp":1771832197090},"id":"60df2c2a","parentId":"9e85fcde","timestamp":"2026-02-23T07:36:37.090Z"}
{"type":"custom","customType":"hello-world:visit","data":{"name":"lisa","timestamp":1771832325862},"id":"6cfd7dea","parentId":"60df2c2a","timestamp":"2026-02-23T07:38:45.862Z"}
{"type":"message","id":"dbeaec50","parentId":"6cfd7dea","timestamp":"2026-02-23T07:39:18.764Z","message":{"role":"user","content":[{"type":"text","text":"> Hello, lisa! 👋  This is visit #3 across ALL sessions.\n\nwhere do you save this stats? --- which file"}],"timestamp":1771832358749}}
```

### 2）代码 review

人类 review 代码的速度已远远赶不上 agent 生成代码的速度，这个例子中，通过一个中立 agent review agent 生成的代码。

```
# 普通 session（线性）：
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


## Software Building Software

上面几个有趣的例子，都是 agent 自己从零开始自己编写用户的想法，没有 MCP，也没有 SKILL --- 软件生软件。

而 OpenClaw 则将这一理念做到极致：没有独立界面，也没有 APP，直接接入日常聊天工具。


# 参考
1. https://lucumr.pocoo.org/2026/1/31/pi/
2. https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/extensions.md
3. https://github.com/mitsuhiko/agent-stuff/tree/main/pi-extensions