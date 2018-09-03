---
title: 记我为Hexo Next主题提交的第一个PR
date: 2018-09-03 22:42:33
tags:
---

用了Hexo的主题一个月了, 本文记录一下我为Hexo Next主题提交的第一个PR: [Safari中无法lazyload Disqus的评论框](https://github.com/theme-next/hexo-theme-next/pull/406). 

<!--more-->

## 背景
Next主题在Disqus评论框的配置中的有一个选项: 开启lazyload, Disqus评论框只有出现在当前窗口内的时候,才会开始加载. 

```yaml
# Disqus
disqus:
  enable: true
  shortname: daya0576
  count: true
  lazyload: true
```

但在iPhone上打开时, 突然发现不管怎么往下拉, 评论框都不会开始加载. 怀疑是浏览器的问题, 果然在电脑上的Safari重现了. 


## 分析代码
Disqus lazyload逻辑的代码如下: 
```js
{% if theme.disqus.lazyload %}
    $(function () {
      var offsetTop = $('#comments').offset().top - $(window).height();
      if (offsetTop <= 0) {
        // load directly when there's no a scrollbar
        loadComments();
      } else {
        $(window).on('scroll.disqus_scroll', function () {
          var scrollTop = document.documentElement.scrollTop;
          if (scrollTop >= offsetTop) {
            $(window).off('.disqus_scroll');
            loadComments();
          }
        });
      }
    });
{% else %}
    loadComments();
{% endif %}
```

### 首先声明几个概念:
- 网页顶部: 整个网站页面的最高点. 
- 游览器窗口顶部: 当前游览器可视窗口的最高点. 

### 代码逻辑
`var offsetTop = $('#comments').offset().top - $(window).height();` 获取的是: 评论框与网页顶部的距离 - 当前游览器窗口高度. 如果这个距离小于0(`offsetTop <= 0`), 说明没有滚动条(评论框与网页顶部的距离小于游览器窗口的高度), 所以可以直接加载评论框.   

如果`offsetTop > 0`, 就要在用户滚动页面窗口时, 实时的去取当前游览器窗口顶部与网页顶部的距离 `scrollTop = document.documentElement.scrollTop`. 当这个值超过`offsetTop`(可以理解为: `$(offsetTop + windowHight >= '#comments').offset().top`), 就去加载评论框. 

说的有点绕了, 总结就是当Disqus评论框开始进入游览器窗口时, 才会去加载. 但在Safari中, 实时的去取当前游览器窗口顶部与网页顶部的距离 `scrollTop = document.documentElement.scrollTop`时, 返回的永远是0. 导致了永远不会加载评论框的bug.


## 解决问题
主要做了两个改动: 
- 将`scrollTop = document.documentElement.scrollTop`替换为Safari兼容的`scrollTop = $(window).scrollTop();`. 
- 实时的去获取`$('#comments').offset().top - $(window).height()`, 因为在调试的过程中, 发现这个值总是不准确, 原来是很多未加载的图片(lazyload)没有高度造成的. 而且用户可能动态的去改变游览器的窗口大小, 所以感觉这个改动还是挺合理的.
![](/images/blog/1800903_hexo_next_first_pr/15359887018737.jpg)


具体代码: 
```js
{% if theme.disqus.lazyload %}
    $(function () {
      var offsetTop = $('#comments').offset().top - $(window).height();
      if (offsetTop <= 0) {
        // load directly when there's no a scrollbar
        loadComments();
      } else {
        $(window).on('scroll.disqus_scroll', function () {
          // offsetTop may changes because of manually resizing browser window or lazy loading images.
          var offsetTop = $('#comments').offset().top - $(window).height();
          var scrollTop = $(window).scrollTop();

          // pre-load comments a bit? (margin or anything else)
          if (offsetTop - scrollTop < 60) {
            $(window).off('.disqus_scroll');
            loadComments();
          }
        });
      }
    });
{% else %}
    loadComments();
{% endif %}
```

-eof-

