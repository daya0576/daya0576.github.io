---
title: linux 反向查找日志
date: 2020-11-08 16:21:50
tags:
- linux
---


当我们在黑屏排查线上问题的时候，经常会遇到一些又臭又长的日志文件（动辄好几个 G）。如果直接用 `grep` 去搜索内容，不仅等待时间长，甚至可能占用机器资源，影响线上业务请求 😓

那有什么更好的办法吗？线上日志按照规约，会按「日」进行轮转切割，但故障发生的时候，我们期望的那条日志一般在"最近十分钟"之内，所以如果可以“反向 grep” 日志，是否可以大大提高查询的性能？🤔

<!--more--> 


# 为什么 grep 这么快？
虽然在好几个 GB 的文件面前，grep 命令有一丝疲软，但不可否认 grep 命令高效。主要由以下两个关键的原因：

## 1. fast search（Boyer–Moore 搜索算法）
简单记录一下自己的一点理解。当然可以直接跳过，推荐参考下面官方的解释。

在 B 文本中，搜索 A 关键字:

- 最后一个字符(c)不匹配：
    - c 不在 A 中 -> 直接跳过
    - c 在 A 中，平移 A 并对齐
- 部分匹配取以下两步中的最大值：
    - 直觉: 对不匹配的*单个字符*，重复第一步
    - 优化: 利用*重合的 substring* 获取(排除本此外)的**上一次（从后往前）**最大 occurrence，然后平移 

算法的精髓除了不用比较每个字符，还提前对待搜索的关键字做了计算，i.e. 生成一个字典，其中保存了关键字中每个字符，及所有 substring 对应的待平移距离。

官方可视化 demo: 
[https://www.cs.utexas.edu/~moore/best-ideas/string-searching/fstrpos-example.html](https://www.cs.utexas.edu/~moore/best-ideas/string-searching/fstrpos-example.html)  

## 2. fast input
1. 使用原生的系统调用（raw Unix input system calls），避免读取数据的时候做复制操作
2. 未按行分割原始文件（不同于 java/python 的 readlines 方法），因为这样意味着要对文件每个字符做扫描。     相反的，grep 会将文件内容分段读取到一个固定大小的 buffer 中（page-sized read chunks），进行搜索。

> The key to making programs fast is to make them do practically nothing. ;-) 

参考作者的精彩回复：[https://lists.freebsd.org/pipermail/freebsd-current/2010-August/019310.html](https://lists.freebsd.org/pipermail/freebsd-current/2010-August/019310.html)

# 如何反向 grep 

扯远了，回到正题，如何**\*反向搜索\***文件中的一条记录呢？ 
![](../images/blog/200104_japan_travel/16048220830172.jpg)


workload 为一个真实的线上日志：

```
$ wc -l tracelog/rpc-server-digest.log.2020-11-02
93828 tracelog/rpc-server-digest.log.2020-11-02
```

当直接去 grep 的时候，花费约 30ms
```
$ time (grep 21885857160436159747673092289 tracelog/rpc-server-digest.log.2020-11-02)
XXXX

real    0m0.032s
user    0m0.019s
sys     0m0.013s
```

一个直觉的优化为先 tail 最后 10000 行日志，再进行 grep
虽然大大提升了速度，但比较挫，有没有更好的做法呢？
```
$ time (tail -n10000 tracelog/rpc-server-digest.log.2020-11-02 | grep 21885857160436159747673092289)
XXX

real    0m0.007s
user    0m0.003s
sys     0m0.009s
```

搜索资料后，有一个 tac 命令可以反向对文件做输出，但为什么耗时一夜回到解放前呢？
```
$ time (tac tracelog/rpc-server-digest.log.2020-11-02 | grep 21885857160436159747673092289)
XXX

real    0m0.081s
user    0m0.048s
sys     0m0.093s
```

定睛一想，原理很简单，虽然反向搜索了，但还是对全文进行了遍历，效率自然很低（这里有个细节：反向比正向搜索多出了一倍多的时间）

所以假如我们只需要最后一条匹配的记录🤔 添加 `-m1` 参数后，终于达到了预期的效果：

```
$ time (tac tracelog/rpc-server-digest.log.2020-11-02 | grep -m1 21885857160436159747673092289)
XXX 

real    0m0.002s
user    0m0.001s
sys     0m0.002s
```


# 其他
1. 当然黑屏操作日志排查问题，是上个世纪的做法。特别是分布式部署的架构下，例如使用 zsearch 或 sls 白屏操作才是正解～
2. 文中提到的操作其实比较初级，你要是有什么好的建议，欢迎留言交流学习。

# 彩蛋：
Q: tac 的全称是什么 XD
A: cat <-> tac 




