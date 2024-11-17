---
layout: post
title: "饿了吗 一道面试题分享和思考~"
date: 2017-05-15 12:46:27
comments: true
tags: [ele, django, database]
---

之前在上海面试后端开发的时候, 面试官问了一个数据库相关的问题:   
有这么一张表: 里边存着所有用户的登录信息, 例如用户名和登录时间.   
请问如何找出**所有用户最近登录**的记录呢?   
<!--more-->
  
### sql:
用sql其实很简单, 就是先按时间排个序, 再按用户id groupby一下就行了.        


### orm:
在django的orm中也是一个道理, 可以用annotate:   
<img style="max-height:500px" class="lazy" data-original="/images/blog/170515_ele/annotate.png">    


### 举个栗子:
献个丑, 上周写的公司报表部分的代码:   
```python
for register, queryset in queryset_by_register.items():
    # 根据value和次级维度进行groupby, 生成以它们为索引的字典.
    fields_compute = [Sum(x) for x in self.header.index_action]
    queryset = queryset.values(*self.groupby).annotate(*fields_compute)

    result[register] = queryset
```


