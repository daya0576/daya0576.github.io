---
layout: post
title: "设置百度 ueditor默认字体"
date: 2016-06-25 18:11:17 +1000
comments: true
tags: [ueditor]
---

想把编辑器的默认字体设成微软雅黑，但找了好久都没找到解决的方法。    
终于成功了，小激动，纪念一下。    
感谢这位博主：[http://m.blog.csdn.net/article/details?id=46697997](http://m.blog.csdn.net/article/details?id=46697997)



<!--more-->
   

在`ueditor.config.js`中，关键是要加p定义段落的字体就可以了，    
这是我的设置：    
``` css
initialStyle:'p{line-height:1em; font-size: 14px;font-family:Microsoft YaHei;'   
//编辑器层级的基数,可以用来改变字体等
```













