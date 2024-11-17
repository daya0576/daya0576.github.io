---
layout: post
title: "Note of 《Effective Python》(第六章)"
date: 2017-02-13 12:18:54
comments: true
tags: [python]
---

记得以前上大学的时候, 去图书馆借了一本《代码简洁之道》. 虽然大部分的内容都忘得差不多了, 但里边的一些思想至今还是收益颇深.     
最近开始看一本书叫做《Effective Python: 59 Specific Ways to Write Better Python》, 把里边一些印象深刻的东西记录在这篇日志里.     
**这篇文章记录的是第六章: <<Built-in modules>>**

<!--more-->
   

###Chapter 6: Built-in modules:    
- **Item 42: Define Function Decorators with functools.wraps.**     
主要就是Python中要是用decorator的话, 会有一些小问题.    
比如用一个helper去装饰fibonacci函数提高性能的话, `help(fibonacci)`显示的是decorator的信息.    
我写的一个wraps在fibonacci中应用例子方便理解:     
```python
from functools import wraps


def memo(f):
    c = {}

    '''wrapper function will copy all of the important metadata about the inner function to the outer function.
       ref: effective python - item 42
       print(fibonacci.__name__)
    '''
    @wraps(f)
    def helper(*args):
        if args not in c:
            c[args] = f(*args)
        return c[args]

    return helper


@memo
def fibonacci(n):
    if n <= 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```
   
   


- **Item 43: Consider contextlib and with Statements for Reusable try/finally Behavior**      
这个和之前看到的一个面试题挺有关系的, 就是with语句为什么会自己关闭. The `with` statement in Python is used to indecate when code is running in a special context. `with` 语句的诞生其实就是为了不重复写try/finally.       
这章讲的主要是上下文管理器, 我之前也很迷惑, 上下文管理器(context manager)到底是什么呢?     
我把我的理解写到下边这个自定义的方法里:    
```python
from contextlib import contextmanager
from urllib.request import urlopen

@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()


with closing(urlopen('http://www.python.org')) as page:
    for line in page:
        print(line)
```
上下文大致的意思就是: 代码块执行前的准备，代码块执行后的收拾.    
一个类的实现:     
```python
# Implementing the Context Manager as a Class
class Saved(object):
    def __init__(self, cr):
        self.cr = cr

    def __enter__(self):
        self.cr.save()
        return self.cr

    def __exit__(self, type, value, traceback):
        self.cr.restore()
```
   
   


- **Item 44: Make `pickle` Reliable with `copyreg`**   
"The pickle built-in module can serialize Python objects into a stream of bytes and deserialize bytes back into objects. "    
有时候你要是看书看得云里雾里的时候不妨实践一下代码, 就能很快地理解了:    
```python
import pickle

class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4

state = GameState()
state.level += 1
state.lives -= 1

state_path = '/tmp/game_state.bin'
with open(state_path, 'wb') as f:
    pickle.dump(state, f)

with open(state_path, 'rb') as f:
    state_r = pickle.load(f)

print(state_r.__dict__)  # {'level': 1, 'lives': 3}


# 但是问题来了, 如果类的属性扩展了, 那些旧的已保存的类要怎么办呢?
# solution就是用copyreg built-in module.
import copyreg

class GameState(object):
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)


def unpickle_game_state(kwargs):
    return GameState(**kwargs)


copyreg.pickle(GameState, pickle_game_state)

state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)  # {'level': 0, 'points': 1000, 'lives': 4}


class GameState(object):
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic

# deserializing an old GameState object:
state_after = pickle.loads(serialized)
print(state_after.__dict__)  # {'points': 1000, 'level': 0, 'lives': 4, 'magic': 5}
```
Versioning Classes(略).    
Stable Import Paths(略).    



- Item 45: Use datetime Instead of time for Local Clocks.
Python有两种处理time zone的方法:    
    - 旧方法: `time` built-in method, but is disastrously error conversions.    
    - 新方法: `datetime` built-in module, work greatly with community-built package named `pytz`   
```python
from time import mktime
from datetime import datetime, timezone

# convert UTC to computer's local time
now = datetime(2017, 2, 13, 15, 00, 00)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()
print(now_local)

# convert local time back to a UNIX timestamp in UTC
time_str = '2017-02-14 12:00:00'
parse_format = '%Y-%m-%d %H:%M:%S'

now = datetime.strptime(time_str, parse_format)
time_tuple = now.timetuple()
utc_now = mktime(time_tuple)
print(utc_now)


# pytz
import pytz

# Step 1: Convert local times to UTC first
arrival_nyc = '2014-05-01 23:33:24'
nyc_dt_naive = datetime.strptime(arrival_nyc, parse_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
print(utc_dt)

# Step 2: Convert to local time
pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
print(sf_dt)

```

