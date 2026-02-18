---
title: "Claude_tricks"
date: 2026-02-17T11:00:31+08:00
draft: true
---

# how I use Claude Code - [@bcherny](https://x.com/bcherny/status/2007179832300581177)

> There is no one correct way to use Claude Code: we intentionally build it in a way that you can use it, customize it, and hack it however you like. Each person on the Claude Code team uses it *very* differently.

来自 Claude 创始人 Boris Cherny 的分享日常工作流：
1. **异步**管理五个 Agent（本地 + 云端 + 移动端 无缝切换），利用系统通知，在需要人工输入或确认时及时提醒自己。~~orz 像极了公司中从来不用笔记本电脑，每天带个 iPad 平板到处乱晃的老板。~~
2. 永远使用最好的模型并开启 thinking：虽然每次问答相对有点慢，但长远地看，更加准确的回答反而提高了整体效率，节约了时间。
3. 多人协作维护一个 `CLAUDE.md` 文件（每个 repo 一个）。更新逻辑非常简单：只要每次 claude 做错事，就无脑加一条“永远不要xxx”，确保下次不再犯。并且在 code review 时，也可以动态 `@claude` 来不断更新该文件。
4. 使用 plan mode（双击 `shift+tab`）--- 好的计划是成功的一半。
5. 使用命令快捷键，高效触发高频的操作，例如自定义的 `/commit-push-pr`
6. 使用 [sub-agents](https://code.claude.com/docs/en/sub-agents) 自动化工作流程，例如每次 session 结束后的代码简化，代码测试等。类似上一条的快捷键。
7. 使用 [PostToolUse hook](https://code.claude.com/docs/en/hooks#posttooluse-input) 调用脚本保证 100% 格式化代码。
8. 相比于 `--dangerously-skip-permissions`，更加推荐使用 `/permissions` 管理命令权限，并通过 `.claude/settings.json` 在 repo 级别共享。
9. 使用 MCP 集成第三方工具，例如在 Slack 中查看与发送消息，调用 Sentry 检查错误日志等。同上配置在 repo 中同步共享。
10. 重点关注“验收”，构建一个良性的 feedback look 会事半功倍交付 2-3 倍质量的软件，例如让 Agent 自己打开游览器模拟验证，并不断重复改进。特别是长时间运行的复杂任务（例如超过一天），参考插件 [Ralph Loop](https://github.com/anthropics/claude-plugins-official/tree/2cd88e7947b7382e045666abee790c7f55f669f3/plugins/ralph-loop)



参考：
1. https://x.com/bcherny/status/2007179832300581177
2. https://code.claude.com/docs/en/best-practices
