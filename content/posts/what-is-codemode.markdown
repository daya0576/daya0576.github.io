---
title: "读 What is Codemode"
date: 2026-10-18T10:21:54+08:00
categories:
- AI
- Pi
series:
- Pi
---

> https://lucumr.pocoo.org/2026/10/6/codemode/

Armin 在过去写过一些文章中（例如 [Code Is All You Need](https://lucumr.pocoo.org/2025/7/3/tools/)），推荐 Coding Agent 直接调用「代码」，而不是将大量 MCP tools 常驻在上下文中。博主在工作中也有类似的实践，例如直接使用 Atlassian CLI 编辑 WIKI 页面，而不是公司提供的统一 MCP。最终获得了更丰富的功能，以及更好的性能。

然而，在 Pi 1.0 中，Armin 却在 core 中通过 Codemode 集成了 MCP。所以 ==什么是 Codemode 呢？为什么要引入 Codemode？==

## What Are Tools

参考之前的文章：[Better Models, Worse Tools](https://lucumr.pocoo.org/2026/7/4/better-models-worse-tools/)，Pi 的 tool 调用并没有什么魔法，它将 system prompt + 可用的 tool 列表调用 API 后，服务端将这些内容组装为一个大的 prompt 文本。

LLM 大口吃下 prompt 后，顺利吐还给 Pi 进行执行：
```
{
  "path": "some/file.py",
  "edits": [
    {
      "oldText": "text to replace",
      "newText": "replacement text"
    }
  ]
}
```

作者强烈推荐 bash & CLI 的原因：一是利用管道方便自由组合，二是 LLM 在训练时学会了文件系统怎么运作，例如运行 `echo foo > /tmp/test.txt` 后，模型知道应该会有一个 `test.txt` 文件在 `/tmp` 目录中。

然而，也有一些局限性：bash 无法组合多模态模型原生的能力（例如要使用原生的 `read` 而不是 `cat` 来读图片）；开 subagent 处理 tool 调用时，也变得束手束脚。

## Brains vs Hands

为了更好的理解和解决这个问题，作者做了一个非常形象的比喻：1）将 harness 比作大脑 2）将 tool 比作动手执行。两者之间应该有一个清晰的边界，支持分别运行在不同的机器上，对应不同的安全等级，例如你使用 [Gondolin](https://earendil-works.github.io/gondolin/) 类似的沙箱机制，bash 可以完全运行在 sandbox 中，但你的 harness 大脑不应该放进去。

## Orchestrating The Harness

### 什么是 Codemode
Codemode 这个名字出自 [Cloudflare](https://blog.cloudflare.com/code-mode/)，用于在 harness 侧编排复杂的操作后，在沙箱中执行，从而不用每一步都和 LLM 交互。

在 Pi 中，Codemode 通过 QuickJS 跑在 WASM runtime，并特意禁止网络访问，没有文件系统，限制内存大小：

```
// ❌ Codemode 不能直接访问文件系统
const content = fs.readFileSync("config.json");

// ✅ 必须调用 Harness 提供的工具
const content = await tools.read_file({
  path: "config.json"
});
```

### Codemode 的好处

第一个好处：节约上下文。例如如果直接由 LLM 调用 `bash` 工具，输出会直接放到 context 上下文中；而 Codemode 可以在沙箱处理完整的 bash 输出后，只把处理后的结果返还给 LLM。

第二个好处：并发处理。由于 Codemode 使用 JavaScript，Agent 可以通过代码编写并发的工作流。例如 agent 目前的一种常见行为：首先并发 probe 探测数据格式，再编写 Codemode 全量处理。

第三个好处：持久化状态。不同的 Codemode 调用之间共享数据（维护在 Harness 侧的 [transcript](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/codemode.md?utm_source=chatgpt.com#store-values) key/value 存储）。

第四个好处：调用内部接口。Pi 内部的接口会直接暴露给 Codemode，例如通过 image model 生成图片，或调用 Jev 做文本分类（不占用 tool 定义，不浪费上下文）。

## 案例分析

注意：下面的案例都是日常 session 中，agent 自发产生的真实操作：

### 1）图片生成

图片生成作为 Pi AI SDK core 中的一个 API，在过去只能创建一个定制的插件来使用它（或者笨重地运行 node 然后调用接口）。而将这些 API 暴露给 Codemode 后，可以让 agent 非常方便并自然地直接使用：

```js
const [painter] = await models.getAvailableOfType("image");
const result = await models.generateImages(painter, {
  input: [{ type: "text", text: "A cute little puppy sitting on a grassy " +
    "lawn, soft natural light, photorealistic" }],
});
if (result.stopReason !== "stop") return result.errorMessage;

for (const block of result.output) {
  // image 将图片发给 LLM，但在 harness 侧，图片
  // 也会作为临时文件，方便在 bash 中传下去
  if (block.type === "image") image(block);
  else text(block.text);
}
```

### 2）分类

在过去，调用 Jev 只能编写蹩脚的 tool，而在 Codemode 中可以通过 AI SDK 非常自然地调用分类模型：

注意：下面的例子中，使用了 `store("sentiment_results", results)` 保存了分类结果，供未来直接使用。

```js
const jev = await models.getModelOfType("classifier", "typesafe", "jev-latest");
const r = await tools.bash({
  command: "gh issue list --state open --limit 100 " +
    "--json number,title,body,comments",
});
const issues = JSON.parse(r.output);

const results = await Promise.all(issues.map(async (issue) => {
  const res = await models.classify(jev, {
    state: {
      title: issue.title,
      body: (issue.body || "").slice(0, 4000),
      comments: issue.comments.slice(-5).map(c => c.body.slice(0, 800)),
    },
    questions: {
      sentiment: {
        type: "choice",
        instructions: "What is the overall sentiment of the author towards pi?",
        criteria: {
          positive: "Appreciative, happy, constructive praise",
          neutral: "Matter-of-fact report or request without emotion",
          negative: "Frustrated, annoyed, upset, or angry",
        },
      },
      frustration: {
        type: "score",
        instructions: "How frustrated is the reporter?",
        criteria: ["not at all", "mildly", "clearly frustrated", "very angry"],
      },
      kind: {
        type: "choice",
        instructions: "What kind of issue is this?",
        criteria: {
          bug: "Bug report or regression",
          feature: "Feature request or enhancement",
          question: "Question or support request",
          other: "Docs, discussion, meta, spam",
        },
      },
    },
  });
  if (res.stopReason !== "stop") {
    return { n: issue.number, title: issue.title, error: res.errorMessage };
  }
  return { n: issue.number, title: issue.title, ...res.answers };
}));

store("sentiment_results", results);
return results
  .filter(r => !r.error)
  .sort((a, b) => b.frustration.score - a.frustration.score)
  .slice(0, 12)
  .map(r => `#${r.n} ${r.frustration.score.toFixed(2)} [${r.kind.choice}] ${r.title}`);
```

### 3）调用 MCP Servers

由于 MCP tools 没有在 prompt 中显性的定义，所以 agent 会先搜索可用的 tool，再发起调用。这种渐进式的模式，让 MCP 变得日益合理（progressive discovery）。

下面的例子中，作者猜测 LLM 在训练的过程中，提前知道了 Sentry MCP 有哪些 tool，所以省去了 discovery 这一步。

```js
const orgs = await tools.mcp__sentry__find_organizations({});
const { organizations } = orgs.structuredContent;
const results = await Promise.allSettled(organizations.map(org =>
  tools.mcp__sentry__find_projects({
    organizationSlug: org.slug,
    regionUrl: org.regionUrl,
  })
));
return organizations.map((org, i) => {
  const r = results[i];
  if (r.status !== "fulfilled") return { org: org.slug, error: String(r.reason) };
  if (r.value.isError) return { org: org.slug, error: r.value.content };
  return {
    org: org.slug,
    projects: r.value.structuredContent.projects.map(p => p.slug),
  };
});
```

## MCP Desires

作者对 MCP server 的一些建议：

1. 结构化的输出，例如返回 Json 而不是文本
2. 返回结果的一致性，否则会导致“progressive discovery”失败
3. 超大的二进制文件支持
4. 多个 MCP server 结果的合并（fan out）

## 关于未来

作者认为 引入 MCP，并不与以前鼓励使用 Code/CLI 的观点矛盾。因为在 Codemode 中使用 MCP 本质上也是调用 Code 的一种形式。

关于 Codemode，未来还有一些值得探索和完善的方向：

1. Durable Execution：复杂工作流能够在中断后恢复，而不只通过 Transcript 保存和恢复状态。
2. 其他脚本语言：探索使用 Starlark、Scheme 等语言替代 JavaScript。
3. 二进制数据处理：完善图片、音频、视频等二进制数据的传递机制。
4. 小模型兼容性：降低 Codemode 对模型代码生成、工具编排和错误处理能力的要求，让较小的模型也能可靠地使用。
