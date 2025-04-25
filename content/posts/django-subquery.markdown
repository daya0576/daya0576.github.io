---
layout: post
title: "Django 子查询(Subquery)"
date: 2015-12-27 22:09:03
comments: true
tags: [django]
---

今天实现了一个难题，就是在Django中实现子查询。      

<!--more-->
   

今天碰到一个**问题**: 一个表叫做answers一个叫category。    answer中有个category的外键，用来对应answer是哪个category的。   
我现在获得了所有的category，但是也想获得每个category的回答数.   

如果用普通的sql语句可以这么写：   
``` sql
select id, name,(select count(*) from rango_answers a where a.category_id = b.id) as answer 
from rango_category b order by answer desc;
```

但是在django中最后我是这么写的：
``` python
cats = Category.objects.filter(subject=subject).extra(
    select={
        'answer_count': 'select count(*) from rango_answers where rango_answers.category_id = rango_category.id'
    },
).order_by('-answer_count', '-likes', 'level')
```



最后的效果：   
<img src="/images/blog/151227_django_subquery/sub.jpg">    
