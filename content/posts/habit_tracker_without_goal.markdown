---
title: "[开源] Beaver Habit Tracker 近况更新（v0.3.4）"
date: 2025-01-26T20:51:28+08:00
categories:
- PYTHON
---

[Beaver Habit Tracker](https://github.com/daya0576/beaverhabits) 是一款使用 Python 编写的习惯跟踪应用，支持自部署。由于作者希望大家尽可能生活的松弛，所以在应用中没有目标的概念 :)

# 《Atomic Habits》

为了更好的开展项目获取更多灵感，最近开始读一本书，名字叫做《Atomic Habits》

有趣的是，开篇作者的观点便与博主项目的标题不默而合：<mark>FORGET ABOUT GOALS, FOCUS ON SYSTEMS INSTEAD</mark>

文中阐述的四个目标的陷阱：
1. Winners and losers have the same goals
  - 每个运动员都希望成为奥运冠军，但真正的奥运冠军的成功，并不是因为当初制定了雄心勃勃的目标。
2. Achieving a goal is only a momentary change
  - 如果目标是让房间保持干净，仅仅一次的打扫可以达到目标，但无法做到长久的维系
3. Goals restrict your happiness.
  - 构建可持续的系统，并享受过程，而不是掉入延迟满足的陷阱。
4. Goals are at odds with long-term progress.
  - 即使咬牙坚持完成目标，是否会如同泄气的气球般，瘫倒，再也不愿继续前行

总而言之，作者呼吁：“忘记你的目标，而是专注构建系统”。是鸡汤还是干货，期待后续的读后感～

# Beaver Habits 0.3.4 更新 ✨

最新的更新新增了以下的特性：

## Daily Notes/descriptions

根据用户提出的需求，希望完成“习惯”的时候，支持添加简短的描述。例如追踪阅读的频率时，希望能够记录在那个特定时刻正在阅读的书。

参考了市面上的产品，主流的做法是全局开关：如果打开后，点击完成就会跳出 dialog 供用户输入文字。

第一版实现后，总觉得有一丝别扭，如何才能让这个功能对用户的“负担”降到最低呢？于是有了这个天才般的想法：去掉了任何的开关或编辑习惯类型，只要「长按」便可以触发添加文字，与「单击」动作相配合。最终实现自然流畅的交互：

{{< video src="/images/blog/global/Screen_Recording_2025-01-27_at_06.36.13.mov" type="video/webm" preload="auto" >}}

实现的过程中，遇到的几个问题：

1）关闭 iOS 系统 contextmenu 事件

```javascript
document.body.style.webkitTouchCallout='none';

document.addEventListener('contextmenu', function(event) {
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    return false;
});
```

2）加锁避免弹框重复触发
```python
release = asyncio.Event()

async def handle_mouse_down():
    release.clear()
    try:
        async with asyncio.timeout(0.5):
            await release.wait()
    except asyncio.TimeoutError:
        ui.notify("Hold")

async def handle_mouse_up():
    release.set()

ui.button("Hold") \
    .on("mousedown", handle_mouse_down) \
    .on("mouseup", handle_mouse_up) \
    .on("touchstart", handle_mouse_down) \
    .on("touchend", handle_mouse_up)
```

## Trusted email header

同样来自用户的诉求，期望通过 cloudflare auth 登陆并访问 tunnel 时，通过 header `Cf-Access-Authenticated-User-Email` 中的邮箱地址，自动登录。

细节不展开，感兴趣可以参考：[https://docs.openwebui.com/features/sso/#cloudflare-tunnel-with-cloudflare-access](https://docs.openwebui.com/features/sso/#cloudflare-tunnel-with-cloudflare-access)

## Add EXPOSE to Dockerfile

一行的小改动，但很高兴来自用户的 PR：https://github.com/daya0576/beaverhabits/pull/65 

