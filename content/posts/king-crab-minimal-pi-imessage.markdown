---
title: "Introducing a Minimal and Self-managing iMessage Bot"
date: 2026-03-13T15:41:08+08:00
categories:
- AI
- 编程
---

Hi folks, I'd like to share a tiny project I’ve been working on over the past few weeks: [https://github.com/daya0576/pi-imessage](https://github.com/daya0576/pi-imessage)

![Xnip2026-03-13_16-13-22](/images/blog/global/Xnip2026-03-13_16-13-22.png)

# Background

While using OpenClaw, the complexity of the software makes me overwhelmed and the debugging process is painful.. 

I want something simple, so I decided to build a minimal and self-managing iMessage bot — powered by [pi](https://github.com/badlogic/pi-mono).


# Features

- **Minimal**: No BlueBubble, no webhooks, no extra dependencies
- **Self-managing**: Turn the agent into whatever you need. He builds his own tools without pre-built assumptions
- **Transparent**: tool calls and reasoning are sent to your iMessage chat, so you can see exactly what it's doing and why
- **iMessage Integration**: Responds to DMs, SMS, and group chats; identifies who sent each message
- **Web UI**: browse chat history, toggle replies on/off per chat, live updates — disable with WEB_ENABLED=false and let the agent build your own web UI


# How it goes
I added this bot to my family group chat and kindly introduced him to everyone. We've been asking questions, sharing cheerful moments, making jokes, and of course, asking him to do us "favors".

Currently, with grwoing memories and custom tools, he's basically a sweet family member :P


---

⚠️ This project is still in early stage, feel free to create issue or pull request. Thanks.
