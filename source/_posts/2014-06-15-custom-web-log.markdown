---
layout: post
title: "my web log"
date: 2014-06-15 00:50:08
comments: true
tags: [octopress]
---

修改网页的log ~   
   
</br>
<p>为了避免各种不可用的说明，先说明一下，<mark style="color: #9d261d;"> 本博客只支持 Google Chrome, Mozilla Firefox, Apple Safari,Opera等现代浏览器</mark>。</p>


<!--more-->
> **long long ago**   
*在[http://blog.alex-oberhauser.com/](http://blog.alex-oberhauser.com/)  中学到了网页中间的那一条bar  很好看 *  
——    
*full-article （read on）那个按钮的修改 也挺简单就是用了渐变和圆边框两个属性。   *



> **14/06/14 **  
*增加前一篇后一篇的样式*   
——      
*增加分享功能（虽然也没有人会分享）*     



> **14/06/16**   
*优化打开速度*   
——      
都是在自己电脑上打开网页     
已经有了缓存 所以特别快就打开了。   
有一天在机房打开网站 半天才打开    
一看原来是jquery和google font 的文件没有响应   
都是request google网址中的文件   404了（应该是万恶的qiang吧）  
——      
写了个搜索小程序查看哪里调用这两个文件   
——      
在head中 删掉了 google font 但是删掉jquery的话头像就出不来了  
就调用了本地的jquery1.91
ok了    
搜索目录下所有文件内容的小代码   

``` python
import os
path = "F:\git\octopress\source"

def search_files(path):
    all_files = []
    for root, dirs, files in os.walk( path ):
        for file in files:
            all_files.append(root + "/" + file)
            
    return all_files        

all_files = search_files(path)

def read_lines_from_file(filename):
    file_object = open(filename)
    lines = 0
    try:
        lines = file_object.readlines()
    finally:
        file_object.close()
    return lines

for file in all_files:
    lines = read_lines_from_file(file)
    if len(lines) > 0:
        for line in lines:
            if "min.map" in line:
                print file
                break
```

> **14/07/20**   
*用html5加入音乐*   
——      
bugs   
游览器兼容   
页面跳转
