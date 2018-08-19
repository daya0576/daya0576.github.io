title: 博客搬家小记(Octopress → Hexo)
tags:
  - hexo
  - blog
categories:
  - blog
date: 2018-08-07 13:43:00
---

从2014年开始, 不知不觉用[Octopress](http://octopress.org/)写博客已经四年多了. 用的主题叫做[Greyshade](https://shashankmehta.in/archive/2012/greyshade.html), 陆陆续续做了很多小改动, 同时也使整个项目一团糟, 慢慢的变得难以维护, 编写一篇新博客的成本也越来越高了, 终于下定决心给博客搬个家. 

调研过一些博客框架, 例如车亮亮做的基于Django的博客系统([GitHub主页](https://github.com/liangliangyy/DjangoBlog)), Jekyll, Ghost, 但最后还是选择了现在最火的Hexo. 本文主要记录了使用hexo的心路历程, 至于如何部署可以参考这篇blog: [在vps上部署你的静态博客(网站)
](/blog/20170729/octopress-nginx-vps/)   


<!--more-->

放一张图纪念一下老博客:
![](/images/blog/180807_octopress_to_hexo/old_blog.png)


# Octopress几个痛点
## toc支持差
toc: table of content, 虽然在老博客上可以在文章开头手动生成, 但体验肯定没有hexo上原生支持的好:
![-w1074](/images/blog/180807_octopress_to_hexo/15336334210310.jpg)


## 痛苦的编辑:
虽然有一些小技巧提升实时预览的响应速度: [Octopress rake generate 命令的大提速🚀](/blog/20170812/rake-trick-octopress/), 但每插入一张图片都需要手动的编辑标签(为了支持lazy-load), 例如: 
```html
<img style="max-height:350px" class="lazy" 
    data-original="/images/blog/180315_git_internal/6993E92A-CB86-4BB9-9063-F3134BDC94D3.png">
```
直接抹杀了我更博的速度, 而hexo因为比较好的生态支持, 有hexo-admin, HexoEditor之类的工具, 可以解决上面说到的问题.

## octopress生态不行
已经三年没有更新了.
![](/images/blog/180807_octopress_to_hexo/github_octopress.png)   


# 从迁移Octopress
官方文档: [https://hexo.io/docs/migration.html#Octopress](https://hexo.io/docs/migration.html#Octopress)

## 基本配置
- [x] Template render error: (unknown path)!!!!!!   
![-w890](/images/blog/180807_octopress_to_hexo/15336323445390.jpg)
官方提示: [https://hexo.io/docs/troubleshooting.html#Template-render-error](https://hexo.io/docs/troubleshooting.html#Template-render-error)
日志`hexo s --debug`
最后发现竟然是`\u2028`的问题, 是一个不占位数, 不可见的字符..
![-w364](/images/blog/180807_octopress_to_hexo/15336324014527.jpg)
- [x] 图片(lazyload & fancybox):    
[https://github.com/Robin-front/hexo-lazyload](https://github.com/Robin-front/hexo-lazyload)
fancybox和lazyload的自定义配置!!!: `themes/next/source/js/src/utils.js`
- [x] 目录: toc自动生成
- [x] 基本的config: [https://hexo.io/docs/configuration.html](https://hexo.io/docs/configuration.html)
- [x] 打赏 (Done)
- [x] RSS (Done)
- [x] Local Search (Done): [https://guahsu.io/2017/12/Hexo-Next-LocalSearch-cant-work/](https://guahsu.io/2017/12/Hexo-Next-LocalSearch-cant-work/)
- [x] Instagram/wechat social icon

## 个性化配置
目标: 让人感觉不到是在用Hexo的Next主题.
- [ ] 首页文章显示为块状 
- [ ] 关于我的页面
- [x] 主题颜色
- [x] font-awesome icons: https://fontawesome.com/v4.7.0/icons/
- [ ] algolia search
- [ ] 背景图片
- [ ] github CI   






