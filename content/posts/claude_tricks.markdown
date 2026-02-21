---
title: "在新时代重新学习“编程” - #3 Claude Code 工作流学习"
date: 2026-02-19T11:00:31+08:00
TOC: true
categories:
- AI
- 编程
series:
- ai_freshman
---

![](/images/blog/global/17716550765797.jpg)


尽管本文的最佳实践都是针对 [Claude Code](https://code.claude.com/docs/en/best-practices)，但触类旁通，真正学习的是与 AI 打交道的沟通技巧。

# “how I use Claude Code” - [@bcherny](https://x.com/bcherny/status/2007179832300581177)

> There is no one correct way to use Claude Code: we intentionally build it in a way that you can use it, customize it, and hack it however you like. Each person on the Claude Code team uses it *very* differently.

来自 Claude 创始人 Boris Cherny 的分享日常工作流：
1. **异步**管理五个 Agent（本地 + 云端 + 移动端 无缝切换），同时利用系统通知，在需要人工输入或确认时及时提醒自己。~~orz 像极了公司中从来不用笔记本电脑，每天带个 iPad 平板到处乱晃的老板。~~
2. 永远使用最好的模型并开启 thinking：虽然每次问答相对有点慢，但长远地看，更加准确的回答反而提高了整体效率，节约了时间。
3. 多人协作维护一个 `CLAUDE.md` 文件（每个 repo 一个）。更新逻辑非常简单：只要每次 claude 做错事，就无脑加一条“永远不要xxx”，确保下次不再犯。并且在 code review 时，也可以动态 `@claude` 来不断更新该文件。
4. 每次从 plan mode 开始（双击 `shift+tab`）--- 好的计划是成功的一半。
5. 自定义命令快捷键，高效触发高频的操作，例如自定义的 `/commit-push-pr`
6. 使用 [sub-agents](https://code.claude.com/docs/en/sub-agents) 自动化工作流程，例如每次回话结束后执行代码测试等固定流程。
7. 使用 [PostToolUse hook](https://code.claude.com/docs/en/hooks#posttooluse-input) 调用脚本保证 100% 格式化代码。
8. 相比于 `--dangerously-skip-permissions`（一把梭），更加推荐使用 `/permissions` 管理命令权限，并通过 `.claude/settings.json` 在 repo 级别共享。
9. 使用 [MCP](https://code.claude.com/docs/en/mcp) 集成第三方工具，例如让 Agent 在 Slack 中查看与发送消息，调用 Sentry 检查错误日志等。同上配置在 repo 中同步共享。
10. 强调“验收”的重要性 - 构建一个良性的 feedback look 会事半功倍交付 2-3 倍质量的软件，例如让 Agent 自己打开游览器模拟验证，并不断重复改进。特别是长时间运行的复杂任务（例如超过一天），参考插件 [Ralph Loop](https://github.com/anthropics/claude-plugins-official/tree/2cd88e7947b7382e045666abee790c7f55f669f3/plugins/ralph-loop)

# “Claude Code 101 - The complete claude code tutorial” - [@eyad_khrais](https://x.com/eyad_khrais/status/2010076957938188661?s=20)

> 10 out of 10 times, the output I've gotten with plan mode did significantly better than when I just started talking and spewing everything into Claude Code. It's not even close.

1. **Think First**：类似上面 Boris 的建议，每次都从 plan mode 开始，相互问问题，最终达成一致，选出一个最合适的方案。多花在 plan 上 5 分钟的时间，可能节省了未来 1 个小时修修补补的时间。
2. **CLAUDE.md**：1）文件不要过长 2）聚焦项目而不是常识 3）在 what 之外加上 why，例如“使用 TypeScript strict mode，因为之前隐式 any 类型导致过生产故障” 4）使用 `#` 随时更新 CLAUDE.md 文件。--- 总而言之，糟糕的 CLAUDE.md 文件就像给新员工编写的 onboard 详细文档（太泛、太正式、没有真正有用的信息），好的 CLAUDE.md 文件像一份个人笔记。
3. **The Limitations of Context Windows**：虽然模型的上下文窗口达到了 1M，但达到上限前，例如 20-40%时，输出的质量就开始逐步下滑。应对策略：1）限制对话范围，例如一个 feature 只对应一个对话 2）使用持久化文件作为 external memory，例如 [SCRATCHPAD.md](https://scratchpad.md/)  与 [plan.md](https://plan.md/) 3）及时清空上下文，果断开一个新对话
4. **Prompts Are Everything**：几个提升 prompt 的技巧：1）尽可能明确 - “Explicit is better than implicit” 2）多说"不要做什么"，因为 Claude 模型热衷于过度设计... 3）如上多说“为什么”，毕竟模型可没有读心术 4）记住 AI 的目的是辅助提升效率而不是完全取代人类，我们还是需要有识别模型犯错的能力。
5. **Bad Input == Bad Output**：当人们在吐槽模型很糟糕时，大概率是自己的输入质量过低（瓶颈很多时候变为人类本身）。作者推荐的原则：“**Specific** > vague. **Constraints** > open-ended. **Examples** > descriptions.”。同时也要清晰认识不同模型的区别，并进一步**合理搭配使用**，例如用 Opus 做规划和架构，用 Sonnet 去执行，遇到棘手问题，切回 Opus 解决难题。
6. **MCP, Tools, and Configurations**：保持好奇心，多去尝试 Claude 提供的 MCP servers、Hooks、自定义命令、Skills、Plugins 等等。
7. **When Claude Gets Stuck**：当 Claude 费劲实现一半代码，但偏离本意太远时，相比于持续沟通改进，不如优化需求，从头开始（`/clear`）。想起以前在咖啡厅古法编写代码，遇到一个小时也无法解决的难题时，喜欢及时站起出去走走呼吸呼吸新鲜空气，重置一下大脑“上下文”。往往有奇效。
8. **Build Systems**：使用 `-p` 进入 “headless mode”，例如 `git diff --staged | claude -p "用中文写一个简洁的 commit message"`。进而无缝嵌入至操作系统，构建丝滑的自动化流程。


# 其他
突然想起了快十年前的一篇博客：[《PyCharm 收藏多年快捷键分享 WOW》](/blog/20170607/pycharm-shortcut/)。感叹世界在快速迭代变化，不变的是人 --- 不知为何大脑中突然循环起一首歌：“社会很单纯 坏的是人～”。

# 参考
1. https://x.com/bcherny/status/2007179832300581177
2. https://code.claude.com/docs/en/best-practices
3. https://x.com/eyad_khrais/status/2010076957938188661?s=20
