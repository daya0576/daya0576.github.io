---
title: 记一次 Matplotlib 解决多线程画图的故事
categories:
- PYTHON
date: 2019-02-04 19:37:24
---


说起运维, 大家可能想到的第一个词就是“苦逼”🤔。 但近些年来, 这个职位发生了翻天覆地的变化: 人肉运维(PE) → 自动化运维(DevOps) → 智能运维(AIOps)。 身为SRE 大军中的一员([什么是 SRE](/blog/20180403/impressions-of-google-sre/)), 也在智能运维的边缘试探: 希望打造监控告警「智能降噪」, 「根因定位」, 「自愈」的处理流程, 终极目标就是让每个人都睡个好觉。    

而上述流程中不是核心, 却不可或缺的一部分就是投递告警时, 将隐晦的告警消息(文字)可视化，转化为生动的图片与诊断结果。 由于我们的整个平台是由 Python 搭建的, 关于绘图调研过多个第三方工具, 但不是太慢就是依赖过重, 最终选择了经典的 [Matplotlib](https://matplotlib.org/).


<!--more-->


# 问题:
处理告警是 I/O 密集型的场景(拉取数据等操作), 自然而然的开启了多线程提升处理效率. 但有一次发生故障, 并导致报警疯狂投递时, 发现了一件诡异的事情: 消息里的图片是全白的或者错位了 :(

# 重现:
根据多年的经验(pingganjue), 发现引入的 `import matplotlib.pyplot as plt` 是个全局变量.. 应该就是它引起的线程不安全.    
写了个小 demo 重现了一下:    
```python
import time
from concurrent.futures.thread import ThreadPoolExecutor


def draw_image(label, sleep=0):
    print(f"plot {label}")
    time.sleep(sleep)
    print(f"save {label}")


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 线程不安全的问题
        executor.submit(draw_image, "A", sleep=1)
        executor.submit(draw_image, "B", sleep=0)
# Output:
# plot A
# plot B
# save B
# save A
```
如果 `plot A` 和 `plot B` 都是画一条线的话, 第三步保存的时候, 就会把画了两条线的图保存了.   

# 解决:
在说解决方案前, 需要了解一个概念: 原子操作(atomic operation) 

python 中很有趣的一点: `sort` 是原子操作, 而`+=`不是原子操作。 详情可以阅读这篇文章, 写的很好: [《深入理解 GIL：如何写出高性能及线程安全的 Python 代码》](http://python.jobbole.com/87743/)    

用 matplot 画图绝对不是个原子操作, 那要怎么解决线程的安全的问题呢? 要是觉得不安全, 就加个锁🔒呗   
```python
import logging
import time
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock, RLock

logger = logging.getLogger(__name__)

lock = Lock()
rlock = RLock()


def draw_image_with_lock(label, sleep=0):
    with lock:
        print(f"plot {label}")
        time.sleep(sleep)
        print(f"save {label}")


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 加锁 Lock
        # 缺点: 容易出现 deadlock 的情况, 需要注意
        executor.submit(draw_image_with_lock, "A", sleep=1)
        executor.submit(draw_image_with_lock, "B", sleep=0)

# Output: 
# plot A
# save A
# plot B
# save B
```

从 Output 可以看到, A&B 画图和保存的顺序没有错乱了。 当加锁会导致 deadlock 的情况, 这个 case 不太容易出现, 但还是要格外的小心。    


# 其他:
分享一下我用 matplotlib 画的酷酷的图💪:    
![](/images/blog/190204_matplot_thread_safing/15492804797787.jpg)

![](/images/blog/190204_matplot_thread_safing/ibaymax.jpg)




