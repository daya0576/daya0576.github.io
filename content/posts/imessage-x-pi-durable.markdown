---
title: "iMessage x Pi Durable"
date: 2026-10-25T10:00:00+08:00
draft: true
categories:
- AI
- Pi
series:
- Pi
---

> A minimal and self-managing iMessage bot — powered by pi durable

众所周知，大陆可用的 IM 有限，除了微信，最为广泛的可能就是苹果的 iMessage 了，也是与 CC 聊天沟通最多的地方。所以开发了 [pi-imessage](https://github.com/daya0576/pi-imessage) 以便在 iMessage 简单与 LLM 对话。有趣的是，每次我们冷战，便会在群聊中让 Fable 判定谁对谁错。幸运的是，在主动沟通下，倒也总能冰释前嫌，维系这段婚姻。

最近将 pi-imessage 从 pi coding agent sdk 迁移至 pi durable，并为其打造了一个可视化的 web ui，以便与看到每个对话的完整内部运行情况。这篇文章将尝试通过一个例子，将 pi durable 的一次请求描述清楚。

![](/images/blog/global/file-3bb69f273ae7daaf073bedb9a1061e4a.png)

^ 图片的例子中，让 agent 去在 immich 中找一张照片。

![](/images/blog/global/17928990251922.jpg)

^ 可视化的内部调用：

## Session

> A Session owns one mutation line, **conversations**, **entries**, **tasks**, **submissions**, and **documents**.

一个 Session 由 `Harness.open()` 基于一种 storage backend 创建。

### 1）Conversations

> A conversation is a transcript scope. It may fork another conversation.

一条对话线，可任意 fork 一个分支。例如在 Slack 中，一条 thread 对应 fork 出的一个分支：

```
type ConversationRecord = {
  id: ConversationId;
  parent?: { conversationId; at: EntryId };   // fork 自哪条对话的哪个 entry
  owner?:  { conversationId; taskId };        // 由哪个 task 拥有
};
```

> In Pi Durable, a subagent is an ordinary conversation owned by the tool task that created it.

虽然在 iMessage 中没有 thread 的概念，但一个对话中，可随时创建一个子对话（==非常自然的一个 subagent tool==）。

### 2）Entries

不可变的 transcript 记录：

```ts

```

个人理解，但出现写入操作时，就会有一条不可变的 entry 记录。在我们的案例中，灰色部分都是 entry 的写入，例如用户的输入，或是 system prompt 的变化，都会插入一条：

![](/images/blog/global/17928999855446.jpg)


### 3）Tasks

> A task is a durable state machine attached to one conversation.

在 durable 中，模型请求（Generation），工具调用，甚至上下文压缩等，都是 task，而每个 task 维护着各自的状态机。

内置的 Generation task 分为以下 phases：
1. **prepare**：准备 system prompt，如果有变化则记录写入 entry
2. **request**：流式调用模型
3. **tools**：所有 tool 调用结束后，触发新一轮的 generation

内置的 Tool task 分为以下 phases：1）**call** 2）**execute**。execute 只有崩溃恢复才会进入。根据 replay 参数决定是否重试（==safe vs unsafe==）

<u>用户的一次输入 prompt 是如何触发 generation？</u>

```ts
// pi-imessage 轮训 iMessage chat.db 提交新消息至 Conversation
const message = { type: "input", content, requestId: guid, whenBusy: "steer" } as const;
...
return conversation.submit(message, BACKGROUND_CONTEXT);

// pi durable 提交 Submission -> 创建 entry (user) + 提交 Task (Generation)
// pi durable 通过 Scheduler 消费 Task
...
```

<u>Tool task 是如何被触发的？</u>

模型自己决定要不要 thinking、要不要调工具（`stopReason === "toolUse"`）。

<u>Tool task 结束后，如何触发下一个 tool task？</u>
<u>Tool task 结束后，如何触发新一轮的 generation？</u>
<u>每次新一轮的 generation 是如何最终停止？</u>

tool call 是一次 generation，模型一次性给出的，默认并行执行：

```
generation#1 调 LLM
← assistant: [toolCall A, toolCall B]  stopReason: toolUse
   ├─ 跑 A
   └─ 跑 B

generation#2 调 LLM，messages 带上 A、B 的结果
← assistant: "完成了"  stopReason: stop    
```

第一轮 generation 的 tools 执行完毕后，第二轮 generation 的结果如果 `stopReason: stop`，则不发起第三轮 generation。


### Submissions

> Submission: something you hand to a conversation, either user input or an entry to write, which you can wait for.

理解为存储中的单独一张表或文件，例如用户提交消息，理解返回回执供 await 或 abort。

```

```

### Documents

> A document is mutable JSON state represented by Chord operations and occasional complete bases.

同上，例如维护了 iMessage chat.db 已经读到哪一行，iMessage chatGuid 对应哪个 conversationId 等全局信息。

```
```

## THE END

突然发现，相比于与全能的 AI 对话，更快理解项目的手段是直接阅读项目 README 文档。
