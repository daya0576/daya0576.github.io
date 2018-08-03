---
layout: post
title: "python_mooc笔记-高阶函数"
date: 2015-07-10 16:15:41 +0800
comments: true
tags: [python, study]
---
 
> 最近看了慕课网上的一个课程，    
感觉还不错，做点笔记，以后忘了看看    

<!--more-->
   

### 字符串的一些处理：   
**将字符串中的大小写转换：**   
``` python
strlwr(sStr1)
sStr1 = sStr1.upper()
sStr1 = sStr1.lower()
print 'JUST TO TEST IT'.capitalize()
```


**字符串的首字母转换成大写， 其余转换成小写：**   
``` python
print 'JUST TO TEST IT'.title() 
```  
**字符串中所有单词的首字母转换成大写， 其余转换成小写**   
Just to test it >>> Just To Test It   


**把函数作为参数:**   
``` python
import math
def add(x, y, f):
    return f(x) + f(y)

print add(25, 9, math.sqrt)
```


**map()函数:**   
``` python
输入：['adam', 'LISA', 'barT']
输出：['Adam', 'Lisa', 'Bart']
def format_name(name):
    return name.capitalize()

print map(format_name, ['adam', 'LISA', 'barT'])
```


**reduce()函数:**   
``` python
输入：[2, 4, 5, 7, 12]
输出：2*4*5*7*12的结果
def prod(x, y):
    return x*y

print reduce(prod, [2, 4, 5, 7, 12])
```


**filter()函数: **  
请利用filter()过滤出1~100中平方根是整数的数，即结果应该是：
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
``` python
import math
def is_sqr(x):
    return math.sqrt(x)%1 == 0

print filter(is_sqr, range(1, 101))
```


**自定义排序函数:**   
输入：['bob', 'about', 'Zoo', 'Credit']   
输出：['about', 'bob', 'Credit', 'Zoo']   
```python
def cmp_ignore_case(s1, s2):
    t1=s1.upper()
    t2=s2.upper()
    if t1 > t2:
        return 1
    if t1 < t2:
        return -1
    else:
        return 0

print sorted(['bob', 'about', 'Zoo', 'Credit'], cmp_ignore_case)
```


**闭包:**   
```python
def count():
    fs = []
    for i in range(1, 4):
        def f(i):
            def g():
                return i*i
            return g
            
        r = f(i)
        fs.append(r)
        
    return fs

f1, f2, f3 = count()
print f1(), f2(), f3()
```


**匿名函数:**   
（晕死， 原来匿名函数的英文是lambda，我说这个东西怎么这么熟悉   
今天面试的题目，没有答出来，好可惜。）    
```python
print filter(lambda s:s and len(s.strip()) > 0, ['test', None, ', 'str', '  ', 'END'])
```

**decorator注释器:**     
```python
import time

def performance(f):
    def fn(*args, **kw):
        t1 = time.time()
        r = f(*args, **kw)
        t2 = time.time()
        print 'call %s() in %fs' % (f.__name__, (t2 - t1))
        return r
    return fn

@performance
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))

print factorial(10)
```
