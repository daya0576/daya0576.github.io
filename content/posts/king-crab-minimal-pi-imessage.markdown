---
title: "Introducing `@kingcrab/pi-imessage` - 🦀 A minimal and self-managing iMessage bot"
date: 2026-03-13T15:41:08+08:00
categories:
- AI
- 编程
---

![Xnip2026-03-13_16-13-22](/images/blog/global/Xnip2026-03-13_16-13-22.png)

P.S. [Paipai](/blog/20250727/paipai_two_months_old/#%E5%90%8D%E5%AD%97%E7%94%B1%E6%9D%A5) is the name of my little boy :p


# Background
> Pi also is a collection of little components that you can build your own agent on top. That's how OpenClaw is built, and that's also how I built my own little Telegram bot and how Mario built his mom. If you want to build your own agent, connected to something, Pi when pointed to itself and mom, will conjure one up for you. - Pi: The Minimal Agent Within OpenClaw

When using OpenClaw, the complexity of the software makes me overwhelmed and the debugging process is painful.. 

So I decided to build a minimal and self-managing iMessage bot without extra dependencies.


# Features

- **Minimal**: No BlueBubble, no webhooks, no extra dependencies
- **Self-managing**: Turn the agent into whatever you need. He builds his own tools without pre-built assumptions
- **Transparent**: tool calls and reasoning are sent to your iMessage chat, so you can see exactly what it's doing and why
- **iMessage Integration**: Responds to DMs, SMS, and group chats; identifies who sent each message
- **Web UI**: browse chat history, toggle replies on/off per chat, live updates — disable with WEB_ENABLED=false and let the agent build your own web UI


# Getting Started

Simply install and go
```
npm install -g @kingcrab/pi-imessage

pi-imessage             # run in foreground
pi-imessage install     # install as launchd service (auto-start on boot, restart on crash)
```


# How It Works

```
  ~/Library/Messages/chat.db
        │
  (poll every 2s for new rows)
        │
        ▼
┌──────────────────────────────────────────────────┐
│              pi-imessage                         │
│                                                  │
│  Watcher (chat.db polling)                       │
│    │                                             │
│    ├─ Filter: is_from_me=0, no reactions         │
│    ├─ Deduplicate via seenRowIds                 │
│    ├─ Read attachments from local disk           │
│    │                                             │
│    ▼                                             │
│  AsyncQueue<IncomingMessage>                     │
│    │                                             │
│    ▼                                             │
│  SessionManager (pi-coding-agent)                │
│    │  per chatGuid, persistent on disk           │
│    │  └─ data/<chatGuid>/                        │
│    │       ├─ log.jsonl      (full history)      │
│    │       └─ context.jsonl  (LLM context)       │
│    │                                             │
│    ▼                                             │
│  Agent loop (pi-agent-core)                      │
│    │                                             │
│    │  ┌─ outer: follow-up messages ────┐         │
│    │  │  ┌─ inner: tool calls +      ┐ │         │
│    │  │  │  steering messages        │ │         │
│    │  │  └───────────────────────────┘ │         │
│    │  └────────────────────────────────┘         │
│    │                                             │
│    ▼                                             │
│  Collect assistant reply text                    │
│    │                                             │
│    ├─ sendMessage (AppleScript → Messages.app)   │
│    └─ save logs (messages, digests)              │
│                                                  │
└──────────────────────────────────────────────────┘
        │
        ▼
  iMessage (user receives reply via Messages.app)
```
