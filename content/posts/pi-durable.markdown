---
title: "读 Pi Durable"
date: 2026-10-03T06:47:56+08:00
categories:
- AI
- Pi
series:
- Pi
toc: true
---

> https://earendil.com/posts/pi-durable/

Pi 发布 1.0 的同时，推出了 Pi Durable。这篇文章让我们简单快速了解它的原理与正确使用姿势。

## 什么是 Pi Durable？

Pi 1.0 一般运行在你终端中，如果遇到进程挂了，只能人工介入手动恢复继续。

而 Pi Durable 提供了一种 harness 框架，可以让 agent 跑在任何地方，被多个用户各种客户端同时操作，支持无限的长对话，以及==从故障中自动恢复==（很持久）。

## 什么是 Harness？

每个人对 Harness 的定义不同，本文的定义：

- `Harness = 存储 + 运行机制`（与模型交互），它提供了供模型调用的 tools & 运行环境。
- `Agent = 模型 + 配置`，例如 thinking level，可用的 tools 等

注意 tools 可以运行在任何环境，例如你的笔记本，远程虚拟机，或一个运行在内存的沙箱，不需要 Harness 跑在同一台机器上。

p.s. Pi Durable 和 Pi 一样极简，仅包含15,000 行代码，方便 Agent 直接阅读和理解它。

## Long runs anywhere

目标：我们希望 agent 可以在任意地方持久运行。

关于存储，Pi Durable 原生支持内存、SQLite 和 JSONL。接口也非常轻量，方便接入任意实现（注意同一份存储同时只由一个进程管理，其他客户端通过连接这个进程来访问）。

```ts
export interface Storage {
    // 原子写入：会话、消息、任务、请求、文档等
    commit(writes: readonly StorageWrite[], context: Context): Promise<Seq>;

    // 分配 ID
    mintId<I extends Id<string>>(): Promise<I>;

    // 读取会话
    conversation(
        id: ConversationId,
        context: Context,
    ): Promise<ConversationRecord | undefined>;

    // 其余接口省略：
    // entry / scanEntries              消息记录
    // task / scanTasks                 任务状态
    // submission / scanSubmissions     提交的请求
    // submissionByRequest              按 requestId 查重
    // document / scanDocuments         应用状态

    close(context: Context): Promise<void>;
```

以 SQLite 为例，完整记录持久化保存在磁盘中，harness 只把当前所需的数据放在内存中，例如活跃对话、正在运行的任务、待提交的任务。一个对话天然对应一个模型的 context window，值得注意的是 Pi Durable 会在==快到窗口上限时，提前总结上下文==，然后丝滑继续，所以即使上万条消息也不会有内存问题。

下面是一个最小例子，通过 env 动态决定执行环境：

```ts
import { BACKGROUND_CONTEXT } from "@earendil-works/chord/context";
import { createModels } from "@earendil-works/pi-ai/models";
import { openaiProvider } from "@earendil-works/pi-ai/providers/openai";
import { createRegistry, Harness } from "@earendil-works/pi-durable";
import { NodeExecutionEnv } from "@earendil-works/pi-durable/env/node";
import {
    openNodeSqliteStorage,
} from "@earendil-works/pi-durable/storage/sqlite/node";
import { CodingTools } from "@earendil-works/pi-durable/tools";

const context = BACKGROUND_CONTEXT; // every call takes a context for cancellation
const models = createModels();
models.setProvider(openaiProvider());

const registry = createRegistry();
registry.install(CodingTools); // read, write, edit, bash

const env = ({ cwd }: { cwd?: string }) =>
    new NodeExecutionEnv({ cwd: cwd ?? process.cwd() });
const harness = await Harness.open(
    await openNodeSqliteStorage("./agent.sqlite"),
    { models, registry, env },
    context,
);
// The root conversation: created on first use, and the same one after every
// restart.
const root = await harness.root(context, {
    agent: {
        model: { provider: "openai", modelId: "gpt-6.1-sol" },
        cwd: "/work/repo",
    },
});
```

### 故障自动恢复

在 Pi Durable 中，一次运行被分为多个步骤，分别对应持久化的 checkpoint，所以在进程中断重启后，可以“断点续传”：

```ts
const job = {
    type: "input",
    content: "Fix the flaky login test",
    requestId: "job-42",
} as const;
await root.submit(job, context);
// The process dies here, in the middle of a tool call.

// A new process opens the same storage.
const harness = await Harness.open(
    await openNodeSqliteStorage("./agent.sqlite"),
    { models, registry, env },
    context,
);
harness.resume(); // continue the interrupted run
const root = await harness.root(context);
// the same submission, answered
const settled = await (await root.submit(job, context)).wait(context);
```

### 同时多个对话

我们希望 harness 可以并行运行多个对话，相互不阻塞。Pi Durable 支持从任意节点分叉，新对话可以访问分叉点之前的所有历史。

想象在 slack 主频道中，每个子 thread 就是一个小分叉 ✌️ ------ 同时也对应一个 agent（自定义模型，thinking level，tools，额外的指令，以及运行环境等等），例如 reviewer 可以用更便宜的模型和只读的 tools。

```ts
const channel = await harness.root(context);
const question = await channel.submit(
    { type: "input", content: "@agent why did the deploy fail?" },
    context,
);
const answered = await question.wait(context);

// Someone replies to the agent's answer in a thread. Every conversation names
// its owner, which decides what an abort reaches (more on that under Tasks).
// The thread has none.
const thread = await channel.fork(
    answered.answer!,
    { ownership: { kind: "ownerless" } },
    context,
);

// Both conversations work at the same time.
const inThread = await thread.submit(
    { type: "input", content: "@agent can we roll it back?" },
    context,
);
const inChannel = await channel.submit(
    { type: "input", content: "@agent who is on call today?" },
    context,
);
await Promise.all([inThread.wait(context), inChannel.wait(context)]);
```

### 插件

我们希望 agent 的任何能力都可以作为插件，Pi Durable 中的插件包含：

```ts
defineExtension({
    name: "project-context",
    sections: [...], // 提示词
    tools: [...],    // 工具
    hooks: [...],    // 执行钩子
    tasks: [...],    // 持久化任务
});
```

#### System prompt sections

每次请求发出前，都会动态获取最新的 system prompt（注意对应的变化也记录在历史 session 中，所以即使进程重启后，模型看到上下文的和重启前一模一样）：

```ts
import { defineExtension, section } from "@earendil-works/pi-durable";

const ProjectContext = defineExtension({
    name: "project-context",
    sections: [
        // Read from the conversation's execution environment. The files can be
        // loaded and watched in the background; every request renders the
        // latest state.
        section("agents_md", (input) => agentsMd.latest(input.env)),
        section("skills", (input) => skills.latest(input.env)),
    ],
});
```

#### Tools

从下面的代码可以看到，每个 tools 定义了是否允许在进程崩溃后重新执行。每个 thread 也可以选择各自的 tools：
- `replay: "safe"`：恢复后可以重试。
- `replay: "unsafe"`（默认）：恢复后不重试，将中断的信息交给模型处理。

```ts
import { Type } from "@earendil-works/pi-ai";
import { defineTool } from "@earendil-works/pi-durable";

const searchIssues = defineTool({
    name: "search_issues",
    description: "Search the issue tracker",
    parameters: Type.Object({ query: Type.String() }),
    replay: "safe", // only reads, so a rerun after a crash is fine
    execute: async (args, api) => {
        // streamed to every client watching
        api.output(`searching for ${args.query}\n`);
        return {
            content: [{ type: "text", text: await tracker.search(args.query) }],
        };
    },
});

const deploy = defineTool({
    name: "deploy",
    description: "Deploy a version to production",
    parameters: Type.Object({ version: Type.String() }),
    // No replay: a deploy interrupted by a crash is reported to the model,
    // never repeated.
    execute: async (args) => ({
        content: [{ type: "text", text: await ci.deploy(args.version) }],
    }),
});

registry.install(defineExtension({ name: "ops", tools: [searchIssues, deploy] }));

// The thread may search, but not deploy.
await thread.configure({ tools: { remove: [deploy] } }, context);
```

tool 在执行时，可以直接调用 harness 的接口，例如用自定义模型开始新的任务，甚至==一个新的 session==，甚至可以与其他 session 进行交互。这种灵活的设计，让 subagent 的实现变得非常简单和自然。

p.s. 由 tool 创建的 session 本质上与主 session 没有区别，都在存储中持久化，所以也可以从故障中自动恢复继续。

```ts
import type { AssistantMessage } from "@earendil-works/pi-ai";
import { AssistantEntry, configure } from "@earendil-works/pi-durable";

const triage = defineTool({
    name: "triage",
    description: "Label an incoming issue as bug, feature, or question",
    parameters: Type.Object({ issue: Type.String() }),
    // a rerun after a crash finds the same subagent and the same submission
    replay: "safe",
    execute: async (args, api, context) => {
        const child = await api.commit(async (tx) => {
            const existing = (
                await tx.scanConversations({ ownerTaskId: api.taskId }, 1)
            ).items[0];
            if (existing !== undefined) return existing.id;
            // Owned by this call, so aborting the call aborts the subagent.
            const created = await tx.createConversation({
                ownership: { kind: "task", taskId: api.taskId },
            });
            // It starts as a copy of this conversation's agent. Make it a small
            // model without tools.
            await configure(tx, created.id, {
                model: { provider: "openai", modelId: "gpt-6-luna" },
                tools: [],
                instructions: "Answer with one word: bug, feature, or question.",
            });
            return created.id;
        }, context);
        // lets a UI show the subagent under the call
        await api.details({ conversationId: child }, context);
        const subagent = await api.conversation(child, context);
        const request = {
            type: "input",
            content: args.issue,
            requestId: `triage:${api.taskId}`,
        } as const;
        const settled = await (
            await subagent!.submit(request, context)
        ).wait(context);
        // The answer is an entry in the subagent's transcript. Read it and take
        // its text.
        const entry = await api.commit(
            (tx) => tx.entry(AssistantEntry, settled.answer!),
            context,
        );
        const message = entry?.model?.[0] as AssistantMessage;
        const text = message.content
            .flatMap((content) => (content.type === "text" ? [content.text] : []))
            .join("");
        return { content: [{ type: "text", text }] };
    },
});
```

插件还可以覆盖其他插件的 tools 实现，以 `bash` 为例：

```ts
import { wrapTool } from "@earendil-works/pi-durable";
import { createBashTool } from "@earendil-works/pi-durable/tools";

// Times every bash call, whichever bash the conversation ends up with.
const Timing = defineExtension({
    name: "timing",
    wraps: [
        wrapTool(createBashTool(), (bash) => ({
            ...bash,
            execute: async (args, api, context) => {
                const start = Date.now();
                try {
                    return await bash.execute(args, api, context);
                } finally {
                    metrics.record("bash", Date.now() - start);
                }
            },
        })),
    ],
});
```

#### Hooks

例如在每次 `deploy` tool 执行前，通过 `askInSlack` 审批：

```ts
import { hook, ToolTask } from "@earendil-works/pi-durable";

const Approval = defineExtension({
    name: "approval",
    hooks: [
        hook(ToolTask, {
            beforeTool: async (call, api, context) => {
                if (call.name !== "deploy") return undefined;
                // After a restart, the hook finds the stored answer instead of
                // asking again.
                let approved = await api.memo<boolean>(
                    "approval:deploy",
                    context,
                );
                approved ??= await api.memo(
                    "approval:deploy",
                    await askInSlack(call),
                    context,
                );
                return approved
                    ? undefined
                    : { block: "Nobody approved the deploy." };
            },
        }),
    ],
});
```

多个 extension 可以对同个 hook 进行注入，最终串行执行。注意 `beforeTool` 比较特别，可以中断串行执行。

#### Tasks

harness 本身就是通过 原生的 task 执行对话交互的，例如1）模型请求 2）tool 调用 3）上下文压缩。Extension 同理，值得一提的是 ==checkpoint 机制==。

下面完整例子的调用关系：
```
- [tool] checkout
    - [task] shop.checkout
        - [phase] pay
            - [task] shop.payment
                - [phase] charge
        - [phase] decide 
```

<details>
  <summary>完整代码</summary>

```ts
import { defineTask, type TaskId } from "@earendil-works/pi-durable";

const Payment = defineTask<{ card: string }, { phase: "charge" }, string>({
    name: "shop.payment",
    version: 1,
    initial: () => ({ phase: "charge" }),
    phases: {
        charge: async (task, runtime, context) => {
            // The key makes the charge idempotent: if a crash reruns this
            // phase, the card is only charged once.
            const charge = await bank.charge(
                task.input.card,
                `payment-${task.id}`,
            );
            await runtime.commit(
                () => ({
                    status: "terminal",
                    outcome: charge.ok
                        ? { status: "completed", result: charge.receipt }
                        : { status: "failed", error: { message: charge.error } },
                }),
                context,
            );
        },
    },
    // Another payment failed, or the checkout was cancelled: undo this one.
    abort: async (task, runtime, context) => {
        await bank.refund(`payment-${task.id}`);
        await runtime.commit(
            () => ({ status: "terminal", outcome: { status: "aborted" } }),
            context,
        );
    },
});

type CheckoutState =
    | { phase: "pay" }
    | { phase: "decide"; payments: TaskId<string>[] };
const Checkout = defineTask<{ cards: string[] }, CheckoutState, string>({
    name: "shop.checkout",
    version: 1,
    initial: () => ({ phase: "pay" }),
    phases: {
        pay: async (task, runtime, context) => {
            await runtime.commit(async (tx) => {
                const payments: TaskId<string>[] = [];
                for (const card of task.input.cards) {
                    payments.push(
                        await tx.createTask(Payment, { card }, {
                            ownership: { kind: "task", taskId: task.id },
                        }),
                    );
                }
                // Run no code until every payment is done. The first failed
                // payment aborts the others.
                return {
                    status: "waiting",
                    checkpoint: { phase: "decide", payments },
                    on: payments,
                    policy: "failFast",
                };
            }, context);
        },
        decide: async (task, runtime, context) => {
            const outcomes = await runtime.outcomes(
                task.state.checkpoint.payments,
                context,
            );
            const paid = outcomes.every(
                (outcome) => outcome.status === "completed",
            );
            await runtime.commit(
                () => ({
                    status: "terminal",
                    outcome: paid
                        ? { status: "completed", result: "Order placed." }
                        : {
                            status: "failed",
                            error: { message: "A payment failed." },
                        },
                }),
                context,
            );
        },
    },
    abort: (_task, runtime, context) =>
        runtime.commit(
            () => ({ status: "terminal", outcome: { status: "aborted" } }),
            context,
        ),
});

// The agent starts a checkout with a tool.
const checkout = defineTool({
    name: "checkout",
    description: "Pay for the cart, split across several cards",
    parameters: Type.Object({ cards: Type.Array(Type.String()) }),
    execute: async (args, api, context) => {
        // Owned by this call: aborting the call aborts the checkout and refunds
        // its payments.
        const owner = {
            ownership: { kind: "task", taskId: api.taskId },
        } as const;
        const id = await api.createTask(
            Checkout,
            { cards: args.cards },
            owner,
            context,
        );
        const { outcome } = (await api.waitForTask(id, context)).state;
        const text =
            outcome.status === "completed" ? outcome.result : outcome.status;
        return { content: [{ type: "text", text }] };
    },
});

registry.install(defineExtension({
    name: "shop",
    tools: [checkout],
    tasks: [Payment, Checkout],
}));
```
</details>

假如进程在 charge 阶段崩溃（task 尚未提交完成状态），恢复后会根据当前的 checkpoint（i.e. phase）重新执行 charge，并通过 taskid 做幂等：
```ts
   phases: {
       charge: async (task, runtime, context) => {
           // 根据 checkpoint 恢复
           const charge = await bank.charge(
               task.input.card,
               `payment-${task.id}`,
           );

           // 持久化提交任务的终态
           await runtime.commit(
               () => ({
                   status: "terminal",
               // ...
```

所有的 taks 形成一个 ownership 树：假如用户取消 checkout，各个 payment 子节点会执行对应的 abort 定义，只有当子节点清理完成，任务结束后，父节点才结束。

```ts
const owner = {
    ownership: { kind: "task", taskId: api.taskId },
} as const;
```

task 默认在前台执行，可通过 `{ background: true }` 参数开启后台任务（不会影响对话的空闲状态）。


### 上下文压缩

上面提到过 `compact` 在后台提前运行（本身也是一个 task），而不打断对话。当然你也可以随时手动调用触发。

```ts
const harness = await Harness.open(storage, {
    models,
    registry,
    settings: {
        compaction: {
            // past contextWindow - reserveTokens, the next request waits for a
            // summary
            reserveTokens: 16384,
            // this far before that, a summary starts in the background
            backgroundTokens: 32768,
        },
    },
}, context);

// Manual, also while the agent is working.
await root.compact("Keep the names of the failing tests", context);
```

### 应用状态

应用状态期望也和对话一样持久化，例如 todo list，plan，sandbox 等等。这些信息保存在 typed JSON 中（称为 Documents）：

```ts
import { defineDoc } from "@earendil-works/pi-durable";

const Todos = defineDoc<{ items: string[] }>({
    kind: "app.todos",
    version: 1,
    scope: "conversation",
    history: "rewindable",
    fork: "asOf", // a fork starts with the todos its parent had at the fork entry
    initial: () => ({ items: [] }),
});

const Todo = defineExtension({
    name: "todo",
    tools: [
        defineTool({
            name: "todo",
            description: "Add an item to your todo list",
            parameters: Type.Object({ item: Type.String() }),
            execute: async (args, api, context) => {
                await api.commit(async (tx) => {
                    const todos = await tx.doc(Todos, api.conversationId);
                    todos.items.push(args.item);
                }, context);
                const text = `Added ${args.item}`;
                return { content: [{ type: "text", text }] };
            },
        }),
    ],
    // The model sees the list before every request.
    sections: [
        section("todos", async (input, context) => {
            const todos = await input.read.snapshot(
                Todos,
                input.conversationId,
                context,
            );
            return todos?.items.join("\n") || undefined;
        }),
    ],
});

// A UI subscribes to the committed value.
const todos = await harness.documentState(Todos, channel.id, context);
todos?.subscribe((value) => renderTodos(value?.items ?? []));
```

### 动态可插拔

在 agent 运行中，支持动态热加载或替换插件（在下一次 tool 调用时生效）：

```ts
// The extension's file changed on disk.
// same name "ops": replaces the installed one
registry.install(await loadExtension("./ops.ts"));
```

### 多人互动

有点类似 tmux，每个客户端可以 attach 到同一个对话，获取最新的状态（committed state）并持续同步更新（通过 `thread.watch()` 获取每一条新的 commit）。

```ts
// A second client joins the thread while the agent is working.
const view = await thread.viewState(context);
render(view.value);
view.subscribe((value) => render(value));

// And steers it. The message joins the running work after the current tool
// calls.
await thread.submit(
    { type: "input", content: "Check the staging logs first", whenBusy: "steer" },
    context,
);
```

## Try it

心动不如行动，将 agent 指向 Pi Durable 的 README，开始构建你的 harness 应用吧！

## 碎碎念

原本希望通过让 agent 学习我的写作风格，使用「说人话」skill，自动生成这篇博客。第一印象 效果颇为不错，结构合理，文字也没有太多的 AI slop 味道。

然而人成为了整个流程的瓶颈，因为我只能从总结压缩后的内容摄取 10% 的知识。故还是选择人工花费数小时，慢慢翻译文章，通过输出消化知识。就像看一本书，作者可能就一句话的观点，却通过 300 页的例子和“废话”反复让读者理解接受。

所以即使随着 AI 模型的快速进化，个人并不觉得工作会被 AI 迅速取代。人类自身的局限性，导致了极低的理解能力，沟通效率等，最终产生了无数就业岗位。