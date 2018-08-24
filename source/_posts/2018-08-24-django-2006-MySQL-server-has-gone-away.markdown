---
title: Django "(2006, 'MySQL server has gone away')"分析, 重现与解决的记录
date: 2018-08-24 15:34:44
tags:
  - django
  - mysql
categories:
  - code
---

# Introduction
最近我们的Django项目供Sofa应用进行tr调用时, 经常会出现一个异常: `django.db.utils.OperationalError: (2006, 'MySQL server has gone away')`. 本文记录了分析, 重现与解决这个bug的全过程. 

# 原因分析: 
Django在1.6引入长链接([Persistent connections](https://docs.djangoproject.com/en/2.1/ref/databases/#persistent-connections))的概念, 可以  
但我们的应用对数据库的操作**太不频繁**了, 两次操作数据库的间隔大于MySQL配置的超时时间(默认为8个小时), 导致下一次操作数据库时connection失效. 
> Our databases have a 300-second (5-minute) timeout on inactive connections. That means, if you open a connection to the database, and then you don't do anything with it for 5 minutes, then the server will disconnect, and the next time you try to execute a query, it will fail.


# 重现问题:

<!--more-->


## 设置mysql `wait_timeout`为10s
在macOS上的mysql配置文件路径: `/usr/local/etc/my.cnf`
```
# Default Homebrew MySQL server config
[mysqld]
# Only allow connections from localhost
bind-address = 127.0.0.1
wait_timeout = 10
interactive_timeout = 10
```
重启mysql:
```
➜  ~ brew services restart mysql
Stopping `mysql`... (might take a while)
==> Successfully stopped `mysql` (label: homebrew.mxcl.mysql)
==> Successfully started `mysql` (label: homebrew.mxcl.mysql)
```
检查`wait_timeout`的值是否已被更新.
```
mysql> show variables like '%wait_timeout%';
+--------------------------+----------+
| Variable_name            | Value    |
+--------------------------+----------+
| innodb_lock_wait_timeout | 50       |
| lock_wait_timeout        | 31536000 |
| wait_timeout             | 10       |
+--------------------------+----------+
3 rows in set (0.00 sec)
```

## 重现exception:
```bash
>>> XXX.objects.exists()
True
>>> import time
>>> time.sleep(15)
>>> XXX.objects.exists()
True
>>> XXX.objects.exists()
...
django.db.utils.OperationalError: (2013, 'Lost connection to MySQL server during query')
>>> XXX.objects.exists()
...
django.db.utils.OperationalError: (2006, 'MySQL server has gone away')
```
有意思的一个点是, sleep 10s 之后, 第一次操作数据库, 会出现`(2013, 'Lost connection to MySQL server during query’)`异常. 之后再操作数据库, 才会抛出`(2006, 'MySQL server has gone away’)`异常. 

## 解决问题:
第一个最暴力的方法就是增加mysql的`wait_timeout`让mysql不要太快放弃连接. 感觉不太靠谱, 因为不能杜绝这种Exception的发生.

第二个办法就是手动把connection直接关闭:   
```python
>>> Alarm.objects.exists()
True
>>> from django.db import connection
>>> connection.close()
>>> time.sleep(10)
>>> Alarm.objects.exists()
True
>>>
```
发现不会出现`(2006, 'MySQL server has gone away’)`异常了, 但总感觉还是不够优雅.  
最终决定在客户端(Django), 设置超时时间(`CONN_MAX_AGE: 5`)比mysql服务端(`wait_timeout = 10`)小:
```python
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'CONN_MAX_AGE': 5,
		<other params here>
	}
}
```

但很奇怪没有生效??? 看了源代码, 发现只有在`request_started`([HTTP request](https://docs.djangoproject.com/en/2.1/ref/signals/#request-started))和`request_finished`的时候, 在`close_if_unusable_or_obsolete`才用到`CONN_MAX_AGE`并去验证时间关闭connection.

具体代码见: `python3.6/site-packages/django/db/__init__.py#64`
```python
# Register an event to reset transaction state and close connections past
# their lifetime.
def close_old_connections(**kwargs):
	for conn in connections.all():
		conn.close_if_unusable_or_obsolete()


signals.request_started.connect(close_old_connections)
signals.request_finished.connect(close_old_connections)
```

而我的代码是处理一个任务而不是HTTP请求, 所以不会触发这个signal. 于是我写了一个装饰器, 在任务的开始和结束的时候, 关闭所有数据库连接. 
``` python
from django.db import connections


# ref: django.db.close_old_connections
def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


def handle_db_connections(func):
    def func_wrapper(request):
        close_old_connections()
        result = func(request)
        close_old_connections()

        return result

    return func_wrapper

# ------割-------
@handle_db_connections
def process_trsbrain_request(request):
    ...
```

ps. CONN_MAX_AGE默认其实为0, 意味着默认在http请求和结束时会关闭所有数据库连接.

# 其他: 
django.db中connection和connections的区别???
1. `connection`对应的是默认数据库的连接, 用代码表示就是`connections[DEFAULT_DB_ALIAS]`
2. `connections`对应的是setting.DATABASES中所有数据库的connection


# ref:
1. [官方对此issue的讨论](https://code.djangoproject.com/ticket/21597)
2. [https://zhaojames0707.github.io/post/django\_mysql\_gone\_away/](https://zhaojames0707.github.io/post/django_mysql_gone_away/)
2. ["Mysql has gone away"的几种可能](https://www.cnblogs.com/lesliexong/p/8654615.html)
3. [mysql wait\_timeout字段官方文档](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_wait_timeout)
4. [“MySQL server has gone away” in django ThreadPoolExecutor](http://www.rainybowe.com/blog/2017/01/06/MySQL-server-has-gone-away-in-django-ThreadPoolExecutor/index.html)


