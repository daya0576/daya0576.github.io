---
layout: post
title: "Octopress,jekyll多说分享插件设置"
date: 2015-10-16 19:56:06 +0800
comments: true
tags: [octopress, duoshuo]
---

偶然看到多说也推出了自家的分享插件，原来我用的是百度的分享插件，但它自带了一个对网站中所有图片鼠标划过时显示分享的效果，感觉有些鸡肋。换用多说的分享插件试试，感觉还不错。             
官方链接：[“期待已久分享插件上线”](http://dev.duoshuo.com/threads/549a781ff07c81f20daba426)    
<!--more-->
 

代码(注释的是原来百度的分享代码):    
还是直接截图好了，不然一些参数直接显示了。    
<img class="lazy" data-original="/images/blog/151014_diary/bsharing.png">    

<i class="fa fa-bug"></i>**其中碰到一个困难：**   
就是在配置data-url的时候需要的是完整的页面url    
原来是想拼接一下字符串，但感觉有些麻烦，   
后来看到了这个回答：[http://stackoverflow.com/questions/10100565/how-to-get-absolute-path-of-jekyll-bootstrap-page](http://stackoverflow.com/questions/10100565/how-to-get-absolute-path-of-jekyll-bootstrap-page)    
于是就可以这么写：<img class="lazy" data-original="/images/blog/151014_diary/bsharing_part.png">（site开头的是_config.yml中自定义配置的参数）     

<i class="fa fa-hand-spock-o"></i>附jekyll中的参数说明：[http://jekyllrb.com/docs/variables/](http://jekyllrb.com/docs/variables/)    



