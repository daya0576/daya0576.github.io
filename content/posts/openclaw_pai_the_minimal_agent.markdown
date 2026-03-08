---
title: "在新时代重新学习“编程” - #5 读 Pi: The Minimal Agent Within OpenClaw"
date: 2026-02-24T13:49:18+08:00
TOC: true
categories:
- AI
- 编程
series:
- ai_freshman
---

> OpenClaw runs a single embedded agent runtime derived from pi-mono.

在翻阅 OpenClaw 文档时，无意发现其 [Agent Runtime](https://docs.openclaw.ai/concepts/agent) 是基于 [pi-mono](https://github.com/badlogic/pi-mono/) 构建。恰好又看到 Armin 写的一篇文章：[Pi: The Minimal Agent Within OpenClaw](https://lucumr.pocoo.org/2026/1/31/pi/)，于是顺着好奇心读了下去。

## 什么是 Pi

pi-mono 是一个模块化的 AI agent 工具包，涵盖 coding agent CLI、统一 LLM API、TUI & Web UI、Slack bot 等组件。本文聚焦其中的 **coding agent** —— 原作者最初将其定位为 Claude Code 的替代品。

值得一提的是，项目本身的分层设计相当清晰，下面是各子模块之间的大致依赖关系：

```
pi-mom
└── pi-coding-agent
    ├── pi-agent-core
    │   └── pi-ai
    └── pi-tui
```


## 设计理念

OpenClaw 背后与 Pi 遵循同样的设计理念：既然大模型那么擅长输出文字与代码，不如放手，全权交给它们。


## 大道至简

项目 Pi 吸引原文作者的两个原因 ♥️：minimal & extensible

### 1）极简
想起一句名言：“less is more”。举个例子，Pi 的 system prompt 是所有 agent 中最短的：

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

每个工具对应一段独立的 TypeScript 代码。以 `Write` 工具为例，逻辑非常清晰：
- 输入：path（文件路径）+ content（完整文件内容）
- 输出：`{ type: "text", text: "Successfully wrote N bytes to <path>" }`

### 2）强大的插件系统

极简内核之上，是一套强大的[插件系统](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions)：假如将内核比做阳光和光合作用，插件系统便是肥沃广阔的土壤，各种特性由此生根发芽，自由生长，无限延伸（详见下文）。


## Pi 没有什么

在理解 Pi 中有什么前，先通过 Pi 中没有什么来理解边界。

<u>Pi 为什么不支持 MCP（Model Context Protocol）？</u>   
Pi 的核心理念是**代码生代码**：当用户想扩展 agent 能力时，不是去找插件、装插件，而是如上所说直接让 agent 自己写代码来解决问题（*Agents Built for Agents Building Agents*）。所以很自然地，MCP 不在 Pi 自身的实现中。


## Pi 有什么

Pi 包含的其他若干重要特性：
1. **session 与模型解耦**：中途可切换任意模型提供商，不依赖某个模型独有的特性。
2. **session 持久化与热加载**：session 不只存储对话，还维护插件状态（持久化到磁盘） -> 支持热重载 -> 最终实现 agent 的不断自我进化：写代码、验证、热加载测试，循环迭代，直到符合预期。
3. **session 树**：Session 以树形结构组织，处理复杂主任务时，可随时开启"干净"的子 Session 处理子任务，避免主 context 爆炸。

## 实际例子

通过几个具体的例子来说明上面的特性：

### 1）Hello World（持久化与热重载）

在 Pi 中输入一句话需求：*"create a hello world extension and give me a demo of persist state"*

Pi 几乎瞬间写好了一个插件，热加载后新增 `hello` 和 `hello-stats` 两个命令。从下图可以看到，调用记录已被持久化保存在 session 中：

![Xnip2026-02-23_17-13-15](/images/blog/global/Xnip2026-02-23_17-13-15.png)

P.S. 持久化信息保存在本地文件（消息类型为 `custom`）：

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

### 2）代码 review（树形结构）

随着 agent 大量地生出代码，但人类 review 代码的速度已经远远追不上，所以何不直接让 agent 先帮忙 review 一遍代码。

举个简单例子：调用 agent 编写 Python 程序后，单独切出分支，利用一个“中立” agent 进行代码 review，然后切回主分支进行改进。

![Xnip2026-02-24_17-27-37](/images/blog/global/Xnip2026-02-24_17-27-37.png)

这种设计的好处：1）节省 token：两条线互不干扰，review 的对话不会污染主线的上下文，coding 思考的上下文也不会干扰 review 的过程 2）Review 记录永久保留：随时可以用 /tree 回去查看当时的完整 findings，或者在不同时间点对同一份代码开多个 review 分支做对比。

```
# 普通 session（线性）：
消息1 → 消息2 → 消息3 → 消息4 → ...

# Pi session（树形）：
消息1 → 消息2 → 消息3
                    ├── 分支A：写代码
                    │       ↓
                    ├── 分支B：review代码（全新视角）
                    │       ↓
                    └── 总结并回到消息3，带着修复继续
```


## 个人感受

1. **代码生代码**：上面这些例子，都是 agent 从零开始，根据用户的一句话自己写出想要的东西。当模型的能力快速变强，编程的模式也在快速发展，而 Pi 代码生代码（Software Building Software）的设计哲学，似乎更符合未来。
2. **学习模式改变**：编程之外，学习新知识的模式也发生了变化。从依赖搜索引擎、人工筛选整理、反复消化吸收，变为纯 AI 对话。
3. **AI 时代的 VIM**：Pi 于我而言，有点像是 AI 时代的 VIM 替代品，用着用着，便有了人机合一的感觉。


## 参考
1. https://lucumr.pocoo.org/2026/1/31/pi/
2. https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/extensions.md
3. https://github.com/mitsuhiko/agent-stuff/tree/main/pi-extensions
4. https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/
5. https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#philosophy

