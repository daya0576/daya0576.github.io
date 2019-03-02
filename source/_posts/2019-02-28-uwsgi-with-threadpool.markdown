---
title: 我的 python 线程为什么执行到一半就消失了!!!
date: 2019-02-28 13:23:04
tags:
---

> 如果一个bug可以在本地重现, 那基本上已经解决了一半. 

最近遇到一个无法在本地重现的多线程bug, 花了一个星期终于解决了, 真的是更深的理解了上面这句话.   

<!--more-->

# 背景
在我们的Django应用中, 一个完整http请求的处理链路如下:    
![](/images/blog/190302_uwsgi_with_threading_bug/15515110409824.jpg)

最后三步(view + 线程池 + method)的代码逻辑如下:    
```python
from concurrent.futures import ThreadPoolExecutor
alarm_handler = ThreadPoolExecutor(max_workers=22, thread_name_prefix="alarm_handler")

def method(request):
   try:
       # do some post requests
       pass
   except Exception as e:
	...

def view(request):  # noqa
   future = method(_handle_new_alarm, request)
   # Add a callback to raise Exception when future.result is Exception
   tools.raise_when_error(future)
```

多么完美的处理流程呀! 但诡异的是, 经常会发现有请求处理到一半中断的情况, 但重跑却没有任何异常!!!     

# 排查
## 线索一: 日志
遇到这类线上问题, 第一步肯定是去查看日志. 花了一些时间尝试多打印日志定位问题, 但诡异的是, 我发现发现每个线程的日志会在流程最后一步中(抛给线程池并执行的method)中随机中断, 并且没有抛出任何异常(之前修复过这个问题, 如果抛出 Exception, 就会在 future 加上 [callback](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task.add_done_callback)进行处理, 并被 sentry 捕捉到).   
![](/images/blog/190302_uwsgi_with_threading_bug/15515109847118.jpg)

**但是!** 有个重要的细节当时被忽略掉了: 线程处理中断的时候, 线程id没有改变, 但进程id新起了一个, 这个点为未来埋下了伏笔
![](/images/blog/190302_uwsgi_with_threading_bug/15515183233503.jpg)


## 线索二: 重现的频率
发现这个bug后, 第一时间新建了一个错误数的监控, 发现整体上涨的趋势其实比较平稳, 并有一定趋势的(每五分钟发生一次). 

# 猜猜猜
基于上述两个线索, 机智的同事猜到了 bug 的原因: 我们在 uwsgi 的配置文件中设置了 [max-requests=5000](https://uwsgi-docs-additions.readthedocs.io/en/latest/Options.html#max-requests), 也就是说每个 worker 如果收到超过 5000 个请求, 就会被杀掉并且重启(killed and restart):    
![](/images/blog/190302_uwsgi_with_threading_bug/15515147365023.jpg)

一般情况下, 这是没有什么问题的, 因为 worker 每次 respawn(重生)的时候, 会等它处理完所有的请求. 但我们的view把任务抛到线程池处理直接返回了, 导致uwsgi 认为请求处理完毕并reload worker 了.   

可以用 [uwsgitop](https://pypi.org/project/uwsgitop/) 看到最后一次 respawn的时间(最后一列):   
```
uwsgi-2.0.18 - Thu Feb 28 12:25:11 2019 - req: 11910 - RPS: 0 - lq: 0 - tx: 1.3M                                                                                      [0/632]
node: 127.0.0.1 - cwd: /home/admin/takachiho - uid: 0 - gid: 0 - masterpid: 78568
 WID    %       PID     REQ     RPS     EXC     SIG     STATUS  AVG     RSS     VSZ     TX      ReSpwn  HC      RunT    LastSpwn
 16     49.5    78647   5890    0       0       0       idle    2ms     0       0       667.2K  1       0       15407.579       12:24:02
 15     29.6    78645   3524    0       0       0       idle    1ms     0       0       399.2K  1       0       8387.575        12:24:02
 14     13.3    78643   1588    0       0       0       idle    2ms     0       0       179.9K  1       0       3803.439        12:24:02
 13     4.1     78641   494     0       0       0       idle    2ms     0       0       56.0K   1       0       1781.118        12:24:02
 12     1.2     78639   147     0       0       0       idle    2ms     0       0       16.7K   1       0       1187.85 12:24:02
 11     0.5     78637   62      0       0       0       idle    2ms     0       0       7.0K    1       0       727.257 12:24:02
 10     0.3     78635   35      0       0       0       idle    2ms     0       0       4.0K    1       0       926.492 12:24:02
 5      0.2     78624   27      0       0       0       idle    2ms     0       0       3.1K    1       0       1192.372        12:24:02
 7      0.2     78628   26      0       0       0       idle    2ms     0       0       2.9K    1       0       578.925 12:24:02
 3      0.2     78619   23      0       0       0       idle    3ms     0       0       2.6K    1       0       566.568 12:24:02
 4      0.2     78621   23      0       0       0       idle    2ms     0       0       2.6K    1       0       1024.521        12:24:02
 6      0.2     78626   23      0       0       0       idle    2ms     0       0       2.6K    1       0       473.923 12:24:02
 9      0.2     78633   18      0       0       0       idle    2ms     0       0       2.0K    1       0       427.194 12:24:02
 8      0.1     78631   17      0       0       0       idle    2ms     0       0       1.9K    1       0       447.082 12:24:02
 2      0.1     78617   8       0       0       0       idle    8ms     0       0       928     1       0       889.387 12:24:02
 1      0.0     78615   5       0       0       0       idle    55ms    0       0       580     1       0       1141.444        12:24:02
```

# 本地重现
起一个本地的 uwsgi 进程, 并设置 `--max-requests` 为 5, 可以看到第五次请求的时候, 进程会被 killed and respawned:   
```
[pid: 88900|app: 0|req: 5/5] 127.0.0.1 () {40 vars in 549 bytes} [Sat Mar  2 16:49:47 2019] POST /new_alarm => generated 194274 bytes in 303 msecs (HTTP/1.1 500) 1 headers in 63 bytes (2 switches on core 0)
...The work of process 88900 is done. Seeya!
worker 1 killed successfully (pid: 88900)
Respawned uWSGI worker 1 (new pid: 89687)
```

# 反思
借官方文档的一段话:   

> Finally: Do not blindly copy & paste!
> Please, turn on your brain and try to adapt shown configs to your needs, or invent new ones.
> 
> Each app and system is different from the others.
> 
> Experiment before making a choice.

