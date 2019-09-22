---
title: 一个博客与 Cloudflare 有关的 Bug
tags:
---

> 一个 bug 只要能在本地重现， 基本上就解决 90% 了。

最近另一篇排查 bug 的文章引用了上面那段话，没想到瞬间就打脸了：博客升级 Hexo 主题版本(v7.4.0)后，在 cloudflare 端托管的**线上页面显示异常**（页面左下脚怎么也加载不出来），但**本地就是百分百正常**。困扰了两个星期终于解决了。。特此写一篇博客“纪念”一下。
![](/images/blog/190922_cloudflare_and_next_bug/15691592217110.jpg)


<!--more-->


# 排查过程：
## 是否为 Cloudflare 的问题？
因为本地加载正常，为了验证是否为 Cloudflare 自身缓存的问题，开启了 Development Mode，但并无变换，说明不是缓存的问题。
![](/images/blog/190922_cloudflare_and_next_bug/15691606345852.jpg)

但是直接修改 host 把域名指到服务器不走 Cloudflare, bug 消失了？？说明确实是 Cloudflare 的问题。真的是百思不得其解。

## 在哪里出错了
![](/images/blog/190922_cloudflare_and_next_bug/15691601888251.jpg)


click event listener 没有加上去

next-boot.js 文件并没有执行


 window.addEventListener 可以执行到，但 DOMContentLoaded 并没有触发
![](/images/blog/190922_cloudflare_and_next_bug/15691575296785.jpg)

DOMContentLoaded 是什么？推荐这篇文章：<https://zhuanlan.zhihu.com/p/25876048>

和 load 事件的区别？？
<https://testdrive-archive.azurewebsites.net/HTML5/DOMContentLoaded/Default.html>


和 cloudflare 的 Rocket Loader 有关？
怀疑在对 DOMContentLoaded 注册的时候，就已经过了这个事件了。


实锤了。。

<https://dash.cloudflare.com/a6456374e093cf85fbab7c7f1d331498/changchen.me/speed/optimization>

Rocket rocker is incompatible with `window.addEventListener('DOMContentLoaded', () => {}`.

—

Rocket Loader is a feature by Cloudflare that can help with page load time. Unfortunately, the method in which it does this is very aggressive, is a beta product, and can often break JavaScript (including Mediavine ads).


解决办法
1. 直接关闭 Rocket rocker
2. 如果 DOMContentLoaded 就在 console 加一个 warning
3. 


<https://support.cloudflare.com/hc/requests/1756050>


逻辑 & 一步步接近真相











