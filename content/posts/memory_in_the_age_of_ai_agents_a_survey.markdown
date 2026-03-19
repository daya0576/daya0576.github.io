---
title: " 读 Memory in the Age of AI Agents: A Survey"
date: 2026-03-16T15:00:51+08:00
draft: true
---

> https://arxiv.org/abs/2512.13564   
> https://github.com/Shichun-Liu/Agent-Memory-Paper-List

自从将基于 pi 构建的 iMessage 机器人加入家庭群聊后，最近每天晚上都会一起闲聊数小时，有时甚至将 copilot 聊到限流...

![Pasted Graphic 4](/images/blog/global/Pasted%20Graphic%204.png)

![Pasted Graphic](/images/blog/global/Pasted%20Graphic.png)

由于记忆系统设计较为简陋，逐渐遇到一些新的问题：例如 1）开启新 session 后，历史聊天记录虽然持久化保存，如何让 agent 高校主动检索 2）可解释性：尝试让 agent 阅读我的博客认识家庭成员，成功总结写入`MEMORY.md`，但忘记了出处 3）记忆冲突：不同时间点的记忆导致了冲突 ...

```
# system prompt
Write to MEMORY.md files to persist context across conversations.
- Global (${workingDir}/MEMORY.md): preferences, project info, shared knowledge
- Chat-specific (<chatDir>/MEMORY.md): user details, ongoing topics, decisions
Update when you learn something important or when asked to remember something.

# workspace 保存/读取
${workingDir}/
├── settings.json                # Bot configuration (see below)
├── MEMORY.md                    # Global memory (all chats)              <- 全局记忆
├── SYSTEM.md                    # System configuration log
├── skills/                      # Global CLI tools you create
└── <chatId>/                    # Each iMessage chat gets a directory
    ├── MEMORY.md                # Chat-specific memory                   <- 对话记忆
    ├── context.jsonl            # LLM context (session persistence)
    ├── log.jsonl                # Message history
    ├── attachments/             # User-shared files
    ├── scratch/                 # Your working directory
    └── skills/                  # Chat-specific tools

```


# 名词解释

文章分三部分：
1. **forms**：记忆的具体表现形式，包含：token 纬度，模型参数权重，以及模型隐含的“直觉潜意识”。
2. **functions**：记忆的功能分类，例如客观事实，主观经验，与工作记忆（临时）等。
3. **dynamics**：记忆的生命周期：记忆形成 -> 记忆演化（例如冲突管理，遗忘机制）-> 记忆检索。

不同「记忆系统」概念的边界：
1. **Agent memory vs LLM memory**：后者简单想象为大模型自身的“缓存”，而前者是**跨任务持久化**的长期经验。
2. **Agent memory vs RAG**：后者 RAG 依赖的是静态知识“百科”，而前者是随着对话**动态持续演化**的“个人笔记”。
3. **Agent memory vs 上下文工程**：从技术目标上看，两者都尝试在有限的上下文窗口内，放入足够多有用的信息。但后者的重点在于当前已有资源的修建与压缩（短期），前者更聚焦于认知模型的建立（长期）。

p.s. 关于记忆生命周期，文中提到一个有趣观点：**短期记忆和长期记忆的分类不合理**。它们完全可以使用相同的架构存储，区别在于生命周期的调用频率。例如长期在回话开始或结束时，一次性读取或写入，而短期的记忆，在对话过程中不断高频读取与覆盖。


# Forms - 如何表示记忆？

文中将记忆的具体表现形式分为三类：外部 token，模型参数权重，以及模型的潜在向量。

## 原始 token

例如文本（text token），音频，图片等信息。

### 一维记忆架构
点状相互独立的一维信息，例如文件夹内平铺的一堆 markdown 文件，聊天对话等。点状模式最大的优势在于简单性和可扩展性 -- 新增信息或裁剪信息的维护成本低。

相对的，由于**记忆缺乏关联性**，存在一定局限性（组合推理、长期规划、抽象的形成）。并且随着知识库膨胀，冗余和噪音增长，检索的相关性逐步下降。


<details>
  <summary>可细分为：对话、偏好、画像、经验、多模态..</summary>

#### 对话
发展历程：
1. 早期将对话原封不动保存下来，塞入对话上下文。如果存不下了就持续总结压缩。
2. 为解决信息丢失的问题，借鉴操作系统分层的概念，将历史信息存在“硬盘”，只把最重要的信息放在“内存”（[MemGPT](https://research.memgpt.ai/)）。
3. 为进一步提高检索准确率：将信息压缩为方便检索的问答对（[COMEDY](https://github.com/nuochenpku/COMEDY)）；使用模糊匹配的向量表+按功能分类（[MIRIX](https://arxiv.org/abs/2507.07957)）；基于认知心理学的研究，尝试像人类大脑更加智能地“切分”与“组织”信息（例如一堆对话分为多个主题或事件场景）。
4. 最新的趋势：记忆系统逐步从静态存储，转化为自主管理。例如通过提供标准化的接口，持续动态更新（[Mem0](https://mem0.ai/)）。

#### 偏好
类似推荐系统，持续更新用户偏好，例如喜欢的颜色，电影等。

#### 画像
用户静态信息，例如名字、职业、长期习惯等。不像偏好经常动态变化。

这里主要指的 agent 自身的 profile -> 保证 agent 在长期对话与任务中的一致性。所以当然可以让 agent 读小说，然后模仿书中的角色具备自己的个性。

#### 经验
发展轨迹：
1. 记录原始的任务执行过程，i.e. 成功&失败案例（2025）
2. 抽象为可重用的工作流、模版、思维链、...
3. 转化为代码、脚本或工具指令 -> 甚至修改自身底层逻辑，实现自我迭代进化

==p.s. 使用 coding agent 修改代码，本质也是一种「经验」的积累。==

#### 多模态
例如将视频/图片，转化为轻量的描述摘要。将声音转化为文字，嵌入基于 embedding 的记忆系统。

P.S. 视频的挑战：需区分出转瞬即逝的局部信息（背景掠过的汽车） vs 整体的逻辑链条（整体剧情）。
</details>

### 二维记忆架构

类似平面维护的**二维信息**，例如图、树、或表等。树形结构的优势在于支持“从粗到细”的递归搜索（想象信息被一层一层向上抽象总结）。图形结构的优势在于捕捉关联性与因果关系。

虽然相对复杂的存储结构在长上下文回答的表现优于简单向量搜索，然而这张“大网”的复杂度是 O(N)，搜索成本与构建成本随着规模变大而加大，导致难以维护。


### 三维记忆架构

模仿人类神经科学，构建分层的**三维信息**，例如。“金字塔”型，每一层都是下一层的抽象，查询则是从上到下，从粗到细。然而，越来越复杂的结构，给信息检索带来了不小挑战。以及层与层之间的映射，每层的信息排放，业界也还没有形成统一的标准。

## 模型参数权重

分为两类：1）修改模型本身的参数：在训练时将个性化知识直接烧进权重，分为预训练、中间训练、后训练（微调），缺点在于无法更新。 2）外挂 LoRA 模块进行自定义，灵活但增加了复杂度。

## 模型潜在向量（Latent Memory）

在 token 与模型权重之外，存在模型内部中间状态里的记忆，例如 KV cache，激活值（activations），隐藏状态（hidden states），潜在向量（latent embeddings）。

通过三种方式持久化：
1. Generate - 总结后保存为向量，缺点为信息偏差。
2. Reuse - 保存模型内部原始向量，缺点为内存消耗。
3. Transform - 压缩蒸馏后保存，同上可能丢信息。

相比于原始 token，潜在向量的不可解释性反而有助于隐私的保护，处理效率更高，并在文字语言难以描述的信息具备一定优势。

# Functions - 为什么 agent 需要记忆？

从无状态的大模型，演变为自主的 agent，除了上下文窗口，记忆也是至关重要的一部分。文中强调记忆并不是一个单一大而全的系统，而是针对 agent 智能化的不同独特需求，分别提供对应的功能。

记忆最重要的三种功能（相互关联，形成动态的认知循环）：
1. 事实库（agent 知道什么？）：通过一系列客观事实，保证 agent 在交互中的**一致性、连贯性、适应性**。又可分为：
    1. 用户事实：例如偏好和个性，任务隐含的默认约束。
    2. 外部事实：例如文档，资源情况，并通过信息共享方便不通 agent 之间的协作。
2. 经验库（agent 需要如何改进？）：从过去的失败/成功经验抽象后，不断自我进化。
3. 工作库（agent 现在正在想什么？）：由于上下文的限制，仅保存和当前任务/对话相关的上下文信息。

# 总结

突然想起工作中的一位资深同事，通过一个 word 文件维护了自己所有的“笔记”。看上去杂乱无章，但每次向他请教问题，看到他通过关键字却快速找到内容。

--- 

无论是单个还是团队协作 agent，以及不同领域的使用场景，都可以被建模为：
- 最终动作（输出文本，调用工具等） = 大模型策略 + 瞬时信息 + 记忆信息 

Agent 需要从当前任务，或成功完成的任务中获取 additional 信息来 decision making。



最后是一些前瞻性的展望，例如全自动化的记忆系统，多模态记忆，共享记忆，以及诚信问题等。
