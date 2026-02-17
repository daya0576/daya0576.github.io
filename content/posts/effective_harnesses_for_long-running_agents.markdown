---
title: "在新时代重新学习“编程” - #1 Long-running agents"
date: 2026-02-15T21:03:36+08:00
categories:
- AI
- 编程
draft: true
series:
- 在新时代重新学习“编程”
---


![](/images/blog/global/17712932866150.jpg)


在家带娃快十个月，孩子叫出了第一声“mama”，世界似乎也发生了天翻地覆的变化。为了在新时代重新学习“编程”，尝试漫无目的地阅读感兴趣的文章并记录“编程小白”学习的过程。


# 1. Spec-Driven Development（SDD）

相比于一问一答的 vibe coding，最近在想 --- 有没有可能更进一步：只提供需求背景和明确的期望结果，剩下的让 agent 长时间运行直到搞定？尝试了 Spec Driven Development (spec-kit)，一言难尽，有种在 2026 年驾驶“手动挡”汽车的别扭感。。越想要人工介入获得掌控感，反而越容易熄火。// 除非你就是特别喜欢手动挡的操作乐趣。


# 2. Effective harnesses for long-running agents

> The core challenge of long-running agents is that they must work in discrete sessions, and each new session begins with no memory of what came before.   

另一篇来自 Anthropic 的文章，文中指出，为了实现 agent 自主地超长时间运行，最大的问题在于：
1. **项目初始化**：模型天生倾向于一口吃成胖子 ------ 一次性实现所有功能。但假如干到一半留了个烂摊子，下个“人”只能靠“猜”来继续完成工作。
2. **项目迭代**：每次开启新 session 后，之前的上下文会完全丢失。想象你每隔一天都招聘一个新员工来帮你编程干活。同时 agent 喜欢“偷偷”将半成品标记为完成，所以需要利用 prompt 严格制定验收条件。

解决办法：基于上面两个问题，文章分别提出了 `Initializer agent` & `Coding agent`。下面尝试用一小段“代码”进行说明：

```
# 名词说明:
# 1. 用户需求 - 本地文件 `app_spec.txt` 人工输入项目目标、技术栈、页面布局、验收标准等细节要求
# 2. 环境管理 - 本地文件 `init.sh` 用于快速初始化开发环境，例如创建并激活 python 虚拟环境
# 3. 功能列表 - 本地文件 `feature_list.json` 包含上百个子功能的优先级、是否已完成等信息
# p.s. 使用的 json 而不是 markdown：因为结构化的 json 文件更不不容易被模型改乱
# 4. 项目进度 - 本地文件 `claude-progress.txt` 管理每次 session 的总结
# 5. 提交记录 - 利用 git 一个 commit 对应一个子功能，方便快速回滚。

---

# Initializer agent：
# 1. 阅读「用户需求」，生成「功能列表」、「环境管理」脚本、
# 2. 实现功能：
#   - 阅读「功能列表」后，挑选优先级最高的的一个功能进行实现
#   - 编写代码 -> 测试验证 -> 提交代码 -> 更新「功能列表」状态 &「项目进度」
# 3. 关闭 session

while True:
    # Coding agent：
    # 1. 恢复上下文：
    #   - 查看当前目录文件
    #   - 阅读提交记录 & 需求 & 进度
    #   - 执行 `init.sh` 初始化环境
    #   - ...
    # 2. 通过全量测试，验证标识为已完成的「功能」，确保没有 regression
    # 3. 重复 Initializer agent 中的 第二步
    # 4. 关闭 session - 保持 clean state
```

通过官方的 demo 运行一个小时，烧掉大几十刀 token 后，个人的感受和问题：
- 项目进展非常低效，例如 agent 在 git init 时，因为本身处在一个大仓库中的问题卡了很久。但神奇的是，每次“卡住”，磕磕绊绊许久，问题都最终被解决了。。
- 针对需求特别清晰明确的项目，文章提出的实践似乎是可行的。但普通用户的需求存在大量模糊地带（人反而成为了最大的瓶颈），agent 有没有可能在适当时机主动找主人确认需求？
- 假如将单个专职 agent 拆解为专职的多个 agent 协同作业，例如测试 agent，质量保证 agent。会不会做的更好？效率会更高吗？
- 关于测试验收：Claude 提供了模拟游览器的端到端测试（Puppeteer MCP），和 unittest 的互补关系？ 



# References
1. https://github.com/github/spec-kit
2. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
3. https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding





