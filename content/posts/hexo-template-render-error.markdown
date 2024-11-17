---
title: Hexo - Template render error(Solved!!)
date: 2019-03-03 13:09:25
tags:
  - hexo
---

Moving my blog from Octopress to Hexo for almost half a year, everything is quit user-friendly(docs, writing experience, etc.), except the `Template render error` caused by [invisible zero width characters](https://en.wikipedia.org/wiki/Zero-width_space), e.g. `\u2028`!!!   

There is [official troubleshooting solution](https://hexo.io/docs/troubleshooting.html#Template-render-error) for this issue, but does not mention the main root cause and solution. 

<!--more-->

# BUG!   
Exception raised by `hexo s --debug`:   
> Template render error: (unknown path) 
>    SyntaxError: Invalid or unexpected token
![](/images/blog/190302_uwsgi_with_threading_bug/15515115013020.jpg)

# Solution
Install plugin [Zero Width Characters locator](https://plugins.jetbrains.com/plugin/7448-zero-width-characters-locator) in [WebStorm](https://www.jetbrains.com/webstorm/) :   
![](/images/blog/190302_uwsgi_with_threading_bug/15515120638235.jpg)

## 1. Realtime inspection
This plugin will remind u all the invisible zero width characters in realtime:   
![](/images/blog/190302_uwsgi_with_threading_bug/15515118874778.jpg)

## 2. Inspecting globally
1. Step 1: trigger searching actions(`⌘ + shift + A`):
![](/images/blog/190302_uwsgi_with_threading_bug/15515125320948.jpg)
2. Step 2: find all annoying zero width unicode characters and fix them!!!
![](/images/blog/190302_uwsgi_with_threading_bug/15515126741490.jpg)



EOF


