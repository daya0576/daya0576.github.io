---
title: Quote of the Day (QOTD) Protocol 实践小记
date: 2022-05-05 22:51:07
tags:
---

周末读《TCP/IP详解：协议》，学到一个非常神奇的协议：RFC 865 - Quote of the Day (QOTD) Protocol

<!--more-->


### 协议简介

> One quote of the day service is defined as a connection based
   application on TCP.  A server listens for TCP connections on TCP port
   17.  Once a connection is established a short message is sent out the
   connection (and any data received is thrown away).

简而言之，通过端口 17 输出每日名人名言。


### 协议实现

受教主的启发，有没有可能亲手实践该协议，实现 github profile 的动态更新？

代码如下，配合 github action 每日定时更新：
```python3
def get_quote():
    addr = (ADDRESS, 17)
    conn = socket.create_connection(addr)
    quote = conn.recv(4096)

    return quote.decode("utf-8")
```

最终效果：


---

BTW, this post & profile repo are both created by vim :p 


