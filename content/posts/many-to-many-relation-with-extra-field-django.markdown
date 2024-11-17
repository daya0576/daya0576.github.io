---
layout: post
title: "Django ORM的多对多关系 (每个关系有附加的属性)"
date: 2017-04-06 20:44:02
comments: true
tags: [django]
---

最近写公司的业务代码, 碰到这么一个问题:      
**一个User对应多个Account, 而每个Account又可以分享给多个user**, 典型的多对多的关系.    
但问题在于每个关系, 都有一个permissionsharing的属性: 0: 只读 / 1: 读写 / 2: 自身创建.    
晚上我尝试着用django的orm来实现这个需求.    
<!--more-->
  

### Model的定义:
```python
from django.db import models

from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=128)
    accounts = models.ManyToManyField(Account, through='PermissionSharing')

    def __str__(self):
        return self.name


class PermissionSharing(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.SmallIntegerField()

```



### 多对多关系的创建:
**user --> account[permission]**   
u1 --> a1[1], a2[2]   
u2 --> a1[2], a3[2]   
```python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manytomany.settings')

import django
django.setup()

from a1.models import Account, User, PermissionSharing

a1 = Account.objects.create(name='a1')
a2 = Account.objects.create(name='a2')
a3 = Account.objects.create(name='a3')

u1 = User.objects.create(name='u1')
u2 = User.objects.create(name='u2')

PermissionSharing.objects.create(user=u1, account=a1, permission=1)
PermissionSharing.objects.create(user=u1, account=a2, permission=2)
PermissionSharing.objects.create(user=u2, account=a1, permission=2)
PermissionSharing.objects.create(user=u2, account=a3, permission=2)
```



### 相互获取对方set的方法和filter方法:
```python
# 相互获取对应的set
print(u1.accounts.all())
print(a1.user_set.all())

# filter
print(User.objects.filter(accounts__name='a1', permissionsharing__permission=1))
print(Account.objects.filter(user=u1, permissionsharing__permission=1))

# 获取relation的属性(extra field: permission)
# 1)
ps = PermissionSharing.objects.get(user=u1, account=a1)
print(ps.permission)
# 2)
ps = a1.permissionsharing_set.get(user=u1)
ps = u1.permissionsharing_set.get(account=a1)
print(ps.permission)


# clear
u1.accounts.clear()

Account.objects.all().delete()
User.objects.all().delete()
PermissionSharing.objects.all().delete()
```
