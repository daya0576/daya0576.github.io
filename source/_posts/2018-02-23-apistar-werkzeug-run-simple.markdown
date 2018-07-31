---
layout: post
title: "APIStar - WERKZEUG(run_simple) 源码阅读笔记"
date: 2018-02-23 11:20:49 +0800
comments: true
categories: [apistar, werkzeug]
---

上个月研究APIStar源码, 发现启动`python app.py run`用的是**werkzeug的run_simple**方法, 仔细读了一下, 感触颇深, 用这篇日志分享一下整个执行流程.       
<!--more-->



### 大致流程:
(ps. 最好和下边的图一起看.)

1. **APIStar入口**:   
    `python app.py run` → `run_wsgi()` → `werkzeug.run_simple()`
2. **`werkzeug.run_simple()`** - *apistar/commands/run.py:26*: 因为默认启用了reloader(自动重启server), 这时会去**检查`WERKZ_RUN_MAIN`这个环境变量:**
    - **第一次为`''`**:    
        - **Step 1:** 设置该环境变量为`true`   
        - **Step 2:** 在while循环中启动一个**子进程**, 并运行**入口命令(`python app.py run`)**
    - **第二次为`true`**:
        - **Step 1:** `srv.serve_forever()`:   
        用一个thread启动一个server去处理request - *werkzeug/serving.py:702*
        - **Step 2:** `reloader.run()`:   
        用while循环每隔一秒去检查所有iter_module_files和self.extra_files, 比较每个文件的修改时间, 如果有更新的话 → `sys.exist(3)` → 结束**子进程**, 重新运行入口命令(python app.py run) (回到外边的while loop中.)
        
<img style="max-height:600px" class="lazy" data-original="/images/blog/180221_run_simple/run_simple.jpg">   


### 总结
哎, 努力写了一堆文字, 但感觉还是无法解释的很清楚, 可以看上图中**左下角有个Summary**, 是简化版的逻辑.. 会比较清晰一些.     
下次还是用画图工具, 将解释和流程图融合在一起, 效果应该会好很多.   

---  

说画就画, 但感觉死循环还是画的不够直观呀:    
<img src="/images/blog/180221_run_simple/process_flow.svg">   


