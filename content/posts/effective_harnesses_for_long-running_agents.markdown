---
title: "读 Effective harnesses for long-running agents - Anthropic"
date: 2026-02-15T21:03:36+08:00
draft: true
---


在家带娃快十个月，孩子叫出了第一声“mama”，世界似乎也发生了天翻地覆的变化。为了在新时代重新学习“编程”，尝试漫无目的地阅读感兴趣的文章并记录。

相比于一问一答的 vibe coding，最近在想 --- 有没有可能更进一步：只提供需求背景和明确的期望结果，剩下的让 agent 长时间运行直到搞定？尝试了 Spec Driven Development (参考 [spec-kit](https://github.com/github/spec-kit))，一言难尽，有种在 2026 年开手动挡汽车的别扭感。。越想要人工介入获得掌控感，反而越容易熄火。// 除非你就是特别喜欢手动挡的操作乐趣。

最近阅读了一篇来自 Anthropic 的文章：[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)，解释了背后的问题与一些看上去可行的尝试。

# 问题分析

> The core challenge of long-running agents is that they must work in discrete sessions, and each new session begins with no memory of what came before.

文中指出，为了实现 agent 自主地超长时间运行，最大的问题在于：
1. **项目初始化**：模型天生倾向于一口吃成胖子 --- 一次性实现所有功能。但干到一半留了个烂摊子时，下个“人”只能靠“猜”来继续完成工作。
2. **项目迭代**：每次开启新 session 后，之前的上下文会完全丢失。想象你每隔一天都招聘一个新员工来帮你编程干活。

# 解决办法

基于上面两个问题，文章分别提出了 `Initializer agent` & `Coding agent`。尝试使用一段小代码进行解释对应的职责与逻辑：

```python
# Glossary:
# 功能列表 - 本地文件 `feature_list.json` 管理每个需求的优先级、是否已完成等信息
# 进度 - 本地文件 `claude-progress.txt` 管理每次 session 的总结

---

# Initializer agent：
# 1. 人工定义需求：阅读基于用户定义的 `app_spec.txt` 自动生成子功能 `feature_list.json`（优先级、是否已完成等..）
# 2. 创建 `init.sh` 用于快速初始化开发环境
# 3. 实现需求 -> 测试验证 -> 提交代码 -> 更新需求状态/总结进度 -> 关闭 session

while True:
    # Coding agent：
    # 1. 恢复上下文：
    #   - 查看当前目录文件
    #   - 阅读提交记录 & 需求 & 进度
    #   - 执行 `init.sh` 初始化环境
    #   - ...
    # 2. 运行测试验证标识为「已完成」的需求，确保没有 regression
    # 3. 实现需求 -> 测试验证 -> 提交代码 -> 更新需求状态/总结进度 -> 关闭 session
```

有趣的是：
1. 需求文件使用的 json 而不是 markdown：因为结构化的 json 文件更不不容易被模型改乱。 
2. 为了避免 agent 没有测试就偷偷将 feature 标识为完成，通过明确的指令让 agent 通过自动化游览器工具，模拟人完成端到端的测试。


# 个人感受

通过官方的 demo 运行一个小时，烧掉大几十刀 token 后，个人的感受和问题：

- 
- 假如将单个专职 agent 拆解为专职的多个 agent 协同作业，例如测试 agent，质量保证 agent。会不会做的更好？
- 关于测试验收：Claude 提供了模拟游览器的端到端测试，和 unittest 相比，它有可能是多余的吗？ 

# References
1. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
2. https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding





