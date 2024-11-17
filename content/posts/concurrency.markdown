---
title: 多进程/多线程/协程 零零散散的记录
date: 2019-02-12 11:06:26
categories:
- PYTHON

---

日常 Python 编程若遇到性能瓶颈, 大部分还是由于 [I/O 密集型](https://en.wikipedia.org/wiki/I/O_bound) 的操作导致, 例如调用外部接口请求数据超时, 造成整个处理流程的阻塞. 一般会采用多线程来解决这类问题, 但不知道就为什么陷入了多进程, 多线程, 协程的迷惑之中. 用这篇文章记录自己零零星星的学习和思考.

<!--more-->

**Threading, Multiprocessing & Coroutine 直接的关联关系?**
看完这篇文章后, 再看下面这张图, 真的会有恍然大悟的感觉:
![](/images/blog/190212_concurrency/15499416082221.jpg)


# 多线程
在Linux中，线程是由进程来实现，线程就是共享内存的轻量级进程.

**调度的策略?**
1. 时间片轮转(Round-robin)
2. 先入先出(FIFO), 除非有更高优先级的线程进入
3. 分时调度: 优先级随线程的运行时间而动态改变，以确保所有具有SCHED_OTHER策略的线程公平运行

**python 实现**
个人倾向用 [concurrency.future](https://docs.python.org/3/library/concurrent.futures.html) 实现, 一个小 demo:
```python
from concurrent.futures import ThreadPoolExecutor

pool_executor = ThreadPoolExecutor(max_workers=20)
# 获取每个检查项的结果
results = pool_executor.map(_check, risk_items)
```

# 协程 Coroutine
1. **从名字上看:** `co` 其实就是相互协作的意思, **async IO is a single-threaded, single-process design: cooperative multitasking**, 精髓就是在一个进程一个线程内的协作.
2. **和多线程对比:** 多线程是在操作系统去调度, 控制执行的顺序. 协程更多的是从代码层面announcing when they are ready to be switched out. 可以参考下面这张图, 很清晰:
![](/images/blog/190212_concurrency/15499750511455.jpg)


**实现原理:**
event loop, controls how and when each task gets run. 假设只有两种状态: Ready & Waiting. 把两种状态的 event 放到对应的list, 不断维护并消费, 直到~~

**调度策略:**
优先执行等的最久的 event. 所以是个 queue?

**优势:**
This allows us to share resources a bit more easily in asyncio than in threading. You don’t have to worry about making your code thread-safe.

**小 demo:**
```python
import asyncio

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
```


# 一些疑惑
1. 为什么不能直接用在 requests 库中?
Requests 库是同步的, 会阻塞事件循环. 可以看下 asyncio.tasks.sleep 的实现.
2. async 和 await 的具体含义?
The keyword await passes function control back to the event loop.


# 总结：

|  | 优点 | 缺点 | 使用场景 |
| --- | --- | --- | --- |
| process | independent state | enormous communication cost |  |
| threads | shared state | managing race conditions & cost of switch |  |
| async | the cost of task switches is very low 并且不需要锁, 程序不容易出错 | 必须添加“yield” or “await” 关键字告诉任务切换. |  |



# Ref
1. https://realpython.com/async-io-python/
2. https://www.youtube.com/watch?v=9zinZmE3Ogk"Your weakness is ur strength and ur weakness is ur strength." 哈哈

