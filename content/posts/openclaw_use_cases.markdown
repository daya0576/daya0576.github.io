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

短短使用 [OpenClaw](https://openclaw.ai/) 几天，已逐渐加速改变生活的工作流，甚至已经成为家庭中的一员。

本文简单分享若几个简单有趣的小例子。

# 1. Stand-up Meeting

在刚开始使用 [multi-agent](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) 的过程中，时常出现上下文错乱，甚至添加新成员导致老成员全部下线的情况。排查后严格设置了 [per-channel-peer](https://docs.openclaw.ai/concepts/session#session-management) 模式，但为了避免后续的混乱或失效，设立了每日的“早会” ------ 管理员依次请求每个 agent 在群中发言，简单描述各自的状态：

<img src="/images/blog/global/17715948380017.jpg" width="650px" />


# 2. 集成 iMessage 

方便家人使用，将龙虾集成至 iMessage 作为我的个人助手自动回复消息。

除此之外，出乎意料的是，无意中连“古老”的短信也支持了自动回复🤔。

![](/images/blog/global/17716591201467.jpg)

除了略显刻意的 emoji（故意 prompt 添加），你真的可以区分屏幕背后是真人还是数字人吗？
![](/images/blog/global/17716599832929.jpg)



# 3. GitHub 工作流

抱着尝试的态度，一句话让 agent 帮忙回复 github issue 并关闭。结果完美完成任务🫡

# 4. SKILLS

将 Trello 与 openclaw 打通后，模仿着创建了第一个 skill 并发布在 clawhub 中：[beaverhabits](https://clawhub.ai/daya0576/beaverhabits)

![](/images/blog/global/17716584033191.jpg)


# 总结

## 强大的 AI
在数字世界，Agent 的能力已完全超越人，关于自动化只有想不到没有做不到任务。

伴随算力成本的不断降低，不难想象在未来的一年，不仅是个性化开箱即用的个人助手如春笋般涌出，还将不断渗透并重新洗牌每个行业。

其他个人感受：目前 AI 唯一还未真正成熟的领域，或许是人的五感（视觉、触觉、味觉、听觉、...），正是这些感官体验，让人相比于机器多了一丝“**人情味**”。但如果有一天，机器也能轻松感知这一切，碳基生物或许真的可以“下线”了。

## AI Native

> 完全发挥 AI 的主观能动性，不需要用户操作任何的 UI 控件，只通过聊天让 AI 完成所有的操作
> 
> --- @yetone

在使用 OpenClaw 的过程中，更加理解了这句话，当模型足够强大超越人类后。用户不再需要查看日志，debug 配置，你需要的是提高短板（学会提问），从而尽可能最大发挥 AI 的主观能动性与能力。
