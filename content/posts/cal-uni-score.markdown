---
layout: post
title: "爬教务处成绩代码log"
date: 2014-08-01 00:05:13
comments: true
tags: [study, python]
---

打包好的exe：[http://pan.baidu.com/s/1nt9eTYh](http://pan.baidu.com/s/1nt9eTYh)   
源代码在github上:[python代码](https://github.com/daya0576/140730-Tianji_Polytechnic_uni_cal_score)   
https://github.com/daya0576/140730-Tianji_Polytechnic_uni_cal_score.git

代码有由3部分组成
-
1. 用urllib登陆教务处，返回html
2. 用beautifulsoup对html的parse
3. 最后用p2exe打包为可执行文件

<!--more-->

以前写过一个登陆教务处网站的小程序。   
写程序中大部分的时间都用到乱码的处理和beautifulsoup的使用了...   
还有py2exe的安装学习   
真的是浪费了 好多时间，如果有好的规划，应该会节省更多时间吧、

###---最后的结果---   
![](/images/blog/140801_web_score_log/console.jpg)   
![](/images/blog/140801_web_score_log/result.jpg)  




