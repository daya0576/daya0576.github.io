---
title: 我的 python 线程为什么执行到一半就消失了!!!
date: 2019-02-28 13:23:04
tags:
---

> 如果一个bug可以在本地重现, 那基本上已经解决了一半. 

最近遇到一个无法在本地重现的多线程bug, 真的是更深的理解了上面这句话.   

# 背景
完整处理的链路如下:    
![](/images/blog/190302_uwsgi_with_threading_bug/15515110409824.jpg)

最后三步(view + 线程池 + method)的代码逻辑如下:    
```python
from concurrent.futures import ThreadPoolExecutor
alarm_handler = ThreadPoolExecutor(max_workers=22, thread_name_prefix="alarm_handler")

def method(request):
   try:
       # do some post requests
       logger.info(“start”)
       ???
       logger.info(“end”)
   except Exception as e:
	...

def view(request):  # noqa
   future = method(_handle_new_alarm, request)
   # Add a callback to raise Exception when future.result is Exception
   tools.raise_when_error(future)
```


![](/images/blog/190302_uwsgi_with_threading_bug/15515109847118.jpg)




