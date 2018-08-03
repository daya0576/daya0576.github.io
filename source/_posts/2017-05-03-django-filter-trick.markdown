---
layout: post
title: "Django filter 的一个令人震惊的小细节, 不转不是中国人!(逃..)"
date: 2017-05-04 9:40:57
comments: true
tags: [django]
---

最近在看django的官方文档的时候, 看到filter()需要注意的地方:   
`Blog.objects.filter(cond1, cond2)`   
和   
`Blog.objects.filter(cond1).filter(cond2))`的结果竟然不同.    
仔细看了许久才明白其中的差异, 特写下这篇日志来分享一下.    
<!--more-->
  

关于这个topic的官方的文档: [https://docs.djangoproject.com/en/1.11/topics/db/queries/#spanning-multi-valued-relationships](https://docs.djangoproject.com/en/1.11/topics/db/queries/#spanning-multi-valued-relationships)
我简化了一下, 让它变得更加简单明了:   
笔记在线连接: [http://note.youdao.com/noteshare?id=6df5d321962c781353aa3a87dea7c215](http://note.youdao.com/noteshare?id=6df5d321962c781353aa3a87dea7c215)


### Model:
```python
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)


class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    pub_year = models.IntegerField()

```


### populate的一些数据:  
Entry:   
<img style="max-height:250px" class="lazy" data-original="/images/blog/170503_django_filter/1.png">    

Blog:    
<img style="max-height:250px" class="lazy" data-original="/images/blog/170503_django_filter/2.png">    


### 执行结构:   
<img style="max-height:250px" class="lazy" data-original="/images/blog/170503_django_filter/3.png">    

<img style="max-height:250px" class="lazy" data-original="/images/blog/170503_django_filter/4.png">    

