---
layout: post
title: "Django单元测试大提速(250s→5s)"
date: 2018-02-04 19:59:42
comments: true
tags: [django, unittest]
---

新的一年有新的开始, 决定使用TDD进行开发! **但第一个问题就是: 执行一次单元测试需要200多秒**, 快速地测试执行俨然成为了当务之急!(正经脸🤭)   
用这篇博客记录一些django单元测试提速的实用小技巧:    
<img style="max-height:300px" src="/images/blog/180203_unittest_speedup/api_v1_test.gif">
<!--more-->
  

# 测试加速技巧🚀🚀🚀:

### 1. 不每次执行migration(200s→30s)
拖累单元测试的罪魁祸首是每次初始化数据库耗费的时间(因为我们数据库中有四百多张表, 所以特别的慢)    
解决方法: pytest的`--reuse-db`参数(默认的测试也有[`--keepdb`](https://docs.djangoproject.com/en/2.0/ref/django-admin/#cmdoption-test-keepdb)参数)    


### 2. 新建用户时密码加密的方式(30s→5s)
这是我最为诧异的一个提升点, 在测试的设置中, 覆盖`PASSWORD_HASHERS` = ['django.contrib.auth.hashers.MD5PasswordHasher',], 竟然将测试的效率提升了6倍左右.        # TODO: 研究一下两种加密方式的具体实现.  


### 3. 并行运行(5s→90s???)
开启pytest的并行运行, 总执行时间竟然从5s变为了90s... 是我打开方式不对吗???   
```
pip install pytest-xdist
pytest tests/api_v1/ --reuse-db -n 4
```


### 4. 其他:
- 使用`setUpTestData`去初始化数据, 而不是`setUp`. 这样在下图中的测试中, 数据只会初始化一次而不是三次:   
<img style="max-height:200px" src="/images/blog/180203_unittest_speedup/setUpTestData.jpg">
- 使用内存型数据库, e.g. sqlite
- 在`INSTALLED_APPS`中去除不需要的app.
- ...
 


# 最终效果:
<img style="max-height:300px" src="/images/blog/180203_unittest_speedup/api_v1_test.jpg">   
用pycharm执行的话慢了好多.. 愁人呀.   
<img style="max-height:400px" src="/images/blog/180203_unittest_speedup/api_v1_test_pycharm.jpg">   


# 完整的配置: 
``` python
# -*-coding:utf-8 -*-
from settings import *
from django.db import OperationalError, connections


os.environ["TEST"] = "true"
DEBUG = False

# TODO: remove unnecessary apps
INSTALLED_APPS = list(INSTALLED_APPS)

TEST_DB_NAME = 'test.db'
DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': TEST_DB_NAME,
            'TEST': {'NAME': TEST_DB_NAME}
        }
}

# --------------------- pytest 配置----------------------------
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEST_RUNNER = 'tests.runner.PytestTestRunner'

with connections['default'].cursor() as cursor:
    try:
        cursor.execute('SELECT ID FROM configs_usergroup LIMIT 1')
    except OperationalError:
        # 第一次数据库为空的情况.
        import django; django.setup()
        from django.core.management import call_command
        call_command("migrate", interactive=False)

# 改变用户生成密码的加密方式, 总执行时间 30s --> 5s ...
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

```



# reference: 
- http://www.obeythetestinggoat.com/speeding-up-django-unit-tests-with-sqlite-keepdb-and-devshm.html
- https://docs.djangoproject.com/en/2.0/topics/testing/overview/#speeding-up-the-tests

