---
title: "在新时代重新学习“编程” - #4 分享我的 OpenClaw 使用场景"
date: 2026-02-20T21:20:21+08:00
TOC: true
categories:
- AI
- 编程
series:
- ai_freshman
---

短短使用 [OpenClaw](https://openclaw.ai/) 几天，工作流已被悄悄改变，甚至慢慢成了家里的一员。

记录几个有趣的使用场景。

# 1. Stand-up Meeting

刚上手 [multi-agent](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) 时，时常遇到上下文错乱，甚至加入新成员后老成员会集体「失忆」。排查后改成了严格的 [per-channel-peer](https://docs.openclaw.ai/concepts/session#session-management) 模式，但为了防止状态悄悄失效，又顺手设立了每日「早会」——管理员依次请求每个 agent，让它们在群里简单报个到：

<img src="/images/blog/global/17715948380017.jpg" width="500px" />


# 2. 集成 iMessage 

方便家人使用，将龙虾集成至 iMessage 作为我的个人助手自动回复消息。除此之外，出乎意料的是，无意中连“古老”的短信也支持了自动回复🤔。

除了略显刻意的 emoji（故意 prompt 添加），你真的可以区分屏幕背后是真人还是数字人吗？

<img src="/images/blog/global/Xnip2026-02-24_11-57-18.png" width="500px" />


# 3. GitHub 工作流

抱着尝试的态度，一句话让 agent 帮忙回复 github issue 并关闭。结果完美完成任务🫡

# 4. SKILLS

将 Trello 与 openclaw 打通后，模仿着创建了第一个 skill 并发布在 clawhub 中：[beaverhabits](https://clawhub.ai/daya0576/beaverhabits)

![](/images/blog/global/Xnip2026-02-24_12-01-48.png)


# 总结

## 强大的 AI
在数字世界，Agent 的能力已完全超越人（特别是 Opus 4.6 指哪打哪），关于自动化只有想不到没有做不到任务。

伴随算力成本的不断降低，不难想象在未来的一年，不仅是个性化开箱即用的个人助手如春笋般涌出，还将不断渗透并重新洗牌每个行业。

另一个感受：目前 AI 还没真正触达的，或许只剩人的五感（视觉、触觉、味觉、听觉……）——正是这些具身体验，让人比机器多了一点"**人情味**"。但哪天机器也能感知这些，碳基生物大概真的可以"下线"了。

## AI Native

> 完全发挥 AI 的主观能动性，不需要用户操作任何的 UI 控件，只通过聊天让 AI 完成所有的操作
> 
> --- @yetone

在使用 OpenClaw 的过程中，对这句话理解更深了。模型足够强大之后，用户不再需要去看日志、debug 配置，只需要学会提问（人类成为了木桶的短板），把问题描述清楚，剩下的交给 AI 就好。
