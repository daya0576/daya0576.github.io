---
title: "iMessage x Pi Durable"
date: 2026-10-25T10:00:00+08:00
categories:
- AI
- Pi
series:
- Pi
---

> A minimal and self-managing iMessage bot — powered by pi durable

众所周知，大陆可用的 IM 有限，除了微信，最为广泛的可能就是苹果的 iMessage 了，也是与 CC 聊天沟通最多的地方。所以开发了 [pi-imessage](https://github.com/daya0576/pi-imessage) 以便在 iMessage 简单与 LLM 对话。每次我们冷战，便会在家庭群聊中让 Fable 判定谁对谁错。幸运的是，在主动沟通下，倒也总能冰释前嫌，维系这段婚姻。

最近将 pi-imessage 从 pi coding agent sdk 迁移至 pi durable，并为其打造了一个可视化的 web ui，以便观察完整内部运行情况。这篇文章将尝试通过一个例子，将 pi durable 的一次请求描述清楚：

![](/images/blog/global/file-3bb69f273ae7daaf073bedb9a1061e4a.png)

## Session

> A Session owns one mutation line, **conversations**, **entries**, **tasks**, **submissions**, and **documents**.

### 1）Conversations

> A conversation is a transcript scope. It may fork another conversation.

一条对话线，可任意 fork 一个分支。例如在 Slack 中，一条 thread 对应 fork 出的一个分支。

> In Pi Durable, a subagent is an ordinary conversation owned by the tool task that created it.

虽然在 iMessage 中没有 thread 的概念，但一个对话中，可随时创建一个子对话（==非常自然的一个 subagent tool==）。

案例群聊对应的 conversation 只保存了一个 id。它既不是从别的对话 fork 出来的（没有 parent），也不属于某个 task（没有 owner），是一个 root conversation：
```ts
{
  "id": 29759
}

// 数据结构
type ConversationRecord = {
  id: ConversationId;
  parent?: { conversationId; at: EntryId };
  owner?:  { conversationId; taskId };
};
```

P.S. 一个 Session 可以同时持有多个 root conversation。pi-imessage 中每个 iMessage chat 各占一个，群聊和私聊彼此平级，都直接挂在同一个 Session 下。

### 2）Entries

> Entry: one immutable transcript record, such as a user message (pi.user), a model response (pi.assistant), a tool result (pi.tool-result), a system prompt change (pi.system), a reset (pi.reset), or your own kind.

一轮对话创建了四类 entry：用户消息（`pi.user`），system prompt（仅在变化时写入），每轮模型回复（`pi.assistant`，包含 thinking 和 toolCall）、每次工具结果（`pi.tool-result`）。

例如我在群里发的那条消息。其中 `model` 字段是模型实际看到的内容，`kind` 标记这条记录的类型。

```ts
{
  "model": [
    {
      "role": "user",
      "content": "[Group 'pi admin' from +8617612150403] 描述我相册里的最近 1 张照片～",
      "timestamp": 1792936109669
    }
  ],
  "kind": "pi.user",
  "id": 188017,
  "conversationId": 29759
}
```

### 3）Tasks

> A task is a durable state machine attached to one conversation.

在 durable 中，模型请求（Generation），工具调用，甚至上下文压缩等，都是 task，而每个 task 维护着各自的==状态机==（进程崩溃后从 phase 继续）。

内置的 Generation 任务分为以下 phases：
1. **prepare**：准备 system prompt，如果有变化则记录写入 entry。
2. **request**：流式调用模型。
3. **tools**：所有 tool 调用结束后，触发新一轮的 generation。

内置的 Tool 任务分为以下 phases：
1. **call**：正常路径。
2. **execute**：只有崩溃恢复才会进入，根据 replay 参数决定是否重试（==safe vs unsafe==）。

案例中第一次 `immich_search` 的 tool task 记录：
```
{
  "id": 188024,
  "conversationId": 29759,
  "kind": "pi.tool",
  "version": 2,
  "input": { "kind": "model", "assistant": 188023, "callId": "toolu_01DH3ZFiCEhYnszUvNoKECCj" },
  "owner": 188019,
  "background": false,
  "abortRequested": false,
  "state": {
    "status": "terminal",
    "outcome": { "status": "completed", "result": { "kind": "model", "entryId": 188025 } }
  },
  "startedAt": 1792936120316,
  "endedAt": 1792936120395
}
```

<u>用户的一次输入 prompt 是如何触发 generation？</u>

1. pi-imessage 轮训 iMessage chat.db 提交新消息至 Conversation
2. pi durable 提交 Submission
    1. 创建 entry (pi.user)
    2. 提交 Task (Generation)
3. pi durable 通过 Scheduler 消费 Task

```ts
const message = { type: "input", content, requestId: guid, whenBusy: "steer" } as const;
return conversation.submit(message, BACKGROUND_CONTEXT);
```

<u>Tool task 是如何被触发的？</u>

模型自己决定要不要 thinking、要不要调工具（`stopReason === "toolUse"`）。

<u>Tool task 结束后，如何触发下一个 tool task？</u>

tool call 是一次 generation，模型一次性给出的，默认并行执行。

<u>每次新一轮的 generation 是如何最终停止？</u>

第一轮 generation 的 tools 执行完毕后，第二轮 generation 的结果如果 `stopReason: stop`，则不发起第三轮 generation。

```
generation#1 调 LLM
← assistant: [toolCall A, toolCall B]  stopReason: toolUse
   ├─ 跑 A
   └─ 跑 B

generation#2 调 LLM，messages 带上 A、B 的结果
← assistant: "完成了"  stopReason: stop    
```

### 4）Submissions

> Submission: something you hand to a conversation, either user input or an entry to write, which you can wait for.

Submission 是把一条输入交给 conversation 后拿到的回执。它本身也是一条持久化记录，状态只会单向推进：`queued`（会话忙，先排队）-> `placed`（已写入 user entry，generation 开始）-> `done`（最终回答落盘）。个人理解方便客户端做幂等与回复。

以案例中我发的那条群聊消息为例。pi-imessage 轮询 chat.db 发现新消息后，用 iMessage 消息的 GUID 作为 requestId 提交：
```ts
const message = { type: "input", content, requestId: guid, whenBusy: "steer" } as const;
const submission = await conversation.submit(message, BACKGROUND_CONTEXT);
// submit() 在落盘后即返回，此时回执是 placed，user entry 已写入
// {
//   "id": 188018,
//   "conversationId": 29759,
//   "requestId": "52A7D09E-3AEC-48D3-8428-63957C26EF9F",
//   "type": "input",
//   "status": "placed",
//   "entry": 188017
// }

const settled = await submission.wait();
// 四轮 generation 结束后，answer 指向最终回答的 entry
// {
//   ...,
//   "status": "done",
//   "entry": 188017,
//   "answer": 188037
// }
```

### 5）Documents

> A document is mutable JSON state represented by Chord operations and occasional complete bases.

Entry 不可变，但有些状态天然要反复修改，这类状态放在 document 里。例如维护了 iMessage chat.db 已经读到哪一行，chatGuid 对应哪个 conversationId 等全局信息。

## 总结

> A Session owns one mutation line, **conversations**, **entries**, **tasks**, **submissions**, and **documents**.

至此，对 Session 中管理的五个概念有了最基础的理解，希望你也有所收获～

```
Conversation 36522（私聊）
│
├─ Submission 184709  placed
│
├─ Entry 184708  user   "描述我相册里的最近 1 张照片～"
├─ Entry 184711  system // prompt 更新
│
├─ Task gen#1 → Entry assistant(immich_search)   → Task tool → Entry tool-result
├─ Task gen#2 → Entry assistant(immich_download) → Task tool → Entry tool-result
├─ Task gen#3 → Entry assistant(read)            → Task tool → Entry tool-result
├─ Task gen#4 → Entry 184734 assistant(text, stop)
│
├─ Submission 184709  done, answer = 184734
│
└─ Document  pi.usage（token 消耗）每轮更新
```

![](/images/blog/global/17928990251922.jpg)

## THE END

突然发现，相比于与全能的 AI 反复对话，更快理解问题的手段，竟然是直接阅读 项目的 README 文档。

## 参考：

1. https://github.com/daya0576/pi-imessage/
2. https://github.com/earendil-works/pi/tree/main/packages/durable#design-documents
