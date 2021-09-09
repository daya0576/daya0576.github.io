---
layout: post
title: "Django 登录或注销后跳转到之前的页面"
date: 2015-12-16 10:42:43
comments: true
tags: [django, python]
---

今天终于解决了项目中的一个问题，就是登录成功后跳转到原先的页面。       

<!--more-->
   

找了好久的资料，终于有一个比较完善的解决方案,   
[http://stackoverflow.com/a/1711592/3538280](http://stackoverflow.com/a/1711592/3538280)
   
1.在setting中引入request：   
``` python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.request",

            ],
        },
    },
]
```

2.总体的思路是登录成功后，跳转到上一个页面：   
（晕，文档中包含url字段就报错，直接放图片了，点击可以放大）   
<img class="lazy" data-original="/images/blog/151216_django_next/code_next.jpg">

3.模板中就可以和原来一样不做修改了：    
<img class="lazy" data-original="/images/blog/151216_django_next/form.jpg">   
**但是有一个问题：**就是我加了一行`<input type="hidden" name="next" value="{{ next }}" />`
不知道为什么logout成功了，但login的话一定要加这一行代码。   
