---
title: Hexo 特殊字符的解决办法
date: 2019-03-02 15:24:51
tags:
---

用了 Hexo 这个博客框架快半年了, 不管是文档还是各种体验都还是挺友好的, 除了特殊字符([不占位数并且不可见的字符](https://en.wikipedia.org/wiki/Zero-width_space), e.g. `\u2028`)报错的问题... 找到了一个一劳永逸的办法分享一下.    

<!--more-->

# bug重现:   
执行 `hexo s --debug` 的时候报错:   
> Template render error: (unknown path) 
>    SyntaxError: Invalid or unexpected token
![](/images/blog/190302_uwsgi_with_threading_bug/15515115013020.jpg)

# 解决办法
在 [WebStorm](https://www.jetbrains.com/webstorm/) 中安装插件: [Zero Width Characters locator](https://plugins.jetbrains.com/plugin/7448-zero-width-characters-locator):   
![](/images/blog/190302_uwsgi_with_threading_bug/15515120638235.jpg)

## 实时提示
安装后打开文件时, 就会实时提示文件中有哪些不可见的字符:   
![](/images/blog/190302_uwsgi_with_threading_bug/15515118874778.jpg)

## 全局扫描
1) 第一步: 执行 inspect:
![](/images/blog/190302_uwsgi_with_threading_bug/15515125320948.jpg)

2) 第二步: 查看结果并修正:
![](/images/blog/190302_uwsgi_with_threading_bug/15515126741490.jpg)


