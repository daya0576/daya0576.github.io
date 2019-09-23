---
title: 一个与 Cloudflare 有关的博客显示 Bug
date: 2019-09-23 20:25:01
tags:
---


> 一个 bug 只要能在本地重现， 基本上就解决 90% 了。

最近在另一篇排查 bug 的文章中，引用了上面👆这段话，没想到瞬间就被打脸了：博客升级 Hexo 主题版本(v7.4.0)后，在 cloudflare 端托管的**线上页面显示异常**（页面左下脚怎么也加载不出来），但**本地就是百分百正常**。困扰了两个星期终于解决了。。特此写一篇博客“纪念”一下。
![](/images/blog/190922_cloudflare_and_next_bug/15691592217110.jpg)


<!--more-->


# 排查过程：
## 1. 谁的问题
因为博客在 Cloudflare 上托管，所以开启了`Development Mode`尝试验证是否为缓存导致，但没有任何变化，说明并不是缓存的问题。但是直接修改 host 把域名指到服务器后， bug 消失了？？又得出结论**确实是 Cloudflare 导致**，真的是百思不得其解。
![](/images/blog/190922_cloudflare_and_next_bug/15691606345852.jpg)

## 2. 调试定位问题
既然本地重现不了，那么就在线上直接调试 js 呗。刚好点击移动版左上角按钮也失灵了，怀疑同个问题导致。直接对这个按钮的点击事件添加断点：
![](/images/blog/190922_cloudflare_and_next_bug/15691601888251.jpg)

对比线上与本地的执行过程后，发现下图中的 `window.addEventListener` 的注册可以执行到，但之后的 `DOMContentLoaded` 事件并没有触发？
![](/images/blog/190922_cloudflare_and_next_bug/15691575296785.jpg)

p.s. DOMContentLoaded 是什么？   
推荐这篇文章：[https://zhuanlan.zhihu.com/p/25876048](https://zhuanlan.zhihu.com/p/25876048)

## 3. 接近真相
和 cloudflare 的 [Rocket Loader](https://www.cloudflare.com/features-optimizer) 有关？
怀疑在对 `DOMContentLoaded` 注册的时候，就早已触发过这个事件了：
![Enabling-Rocket-Loader-animation](/images/blog/190922_cloudflare_and_next_bug/Enabling-Rocket-Loader-animation.gif)

实锤了。。下图中的 蓝线 代表 `DOMContentLoaded`，红线 代表 `Load`（[两者的区别](https://testdrive-archive.azurewebsites.net/HTML5/DOMContentLoaded/Default.html)）。js 文件被延迟加载，导致其中注册的 `DOMContentLoaded` 事件永远也不会触发😢：
![](/images/blog/190922_cloudflare_and_next_bug/Pasted%20Graphic%204.png)

而本地的正常加载过程是这样的：
![](/images/blog/190922_cloudflare_and_next_bug/15692441554625.jpg)


### 什么是 Rocket Loader?
那么问题来了，这个炫酷的 Rocket Loader 到底是什么呢？简单说原理就是在加载页面时先暴力注释了 js，让页面先显示内容，再去加载和执行 js 脚本以到达页面加载加速的效果。但官方文档也说到这是个比较**激进**的特性，可能会有一些兼容问题。

> Rocket Loader is a feature by Cloudflare that can help with page load time. Unfortunately, the method in which it does this is very aggressive, is a beta product, and can often break JavaScript (including Mediavine ads).

# 问题修复
1. 暴力直接关闭 Rocket rocker
2. 如果 DOMContentLoaded 就在 console 加一个 warning
3. 开启 Rocket rocker，但对特定的资源加一个 false flag: `<script data-cfasync="false" src="/javascript.js"></script>`












