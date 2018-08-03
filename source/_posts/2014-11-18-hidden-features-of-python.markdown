---
layout: post
title: "hidden features of Python笔记"
date: 2014-11-18 11:30:26 +0800
comments: true
tags: [study, python]
---

## 最近看了关于python的两个很不错的资料 

1. <a href="http://legacy.python.org/dev/peps/pep-0008/#blank-lines" >PEP 8 （Style Guide for Python Code）</a>   

1. <a href="http://stackoverflow.com/questions/101268/hidden-features-of-python">Hidden features of Python [closed]</a>

#### <a style="background-color:#2783F3;color:#fff">做一下第二个的笔记 加深印象</a>
<!--more-->

<h3>Quick links to answers:</h3>
<ul>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#111176">Argument Unpacking</a></li>
'*' 不就是c语言里取指针的值  
直接把list和dictionary里的值变成函数的参数了  
但实际很少用到把 
```python
def draw_point(x, y):
    # do some magic

point_foo = (3, 4)
point_bar = {'y': 3, 'x': 2}

draw_point(*point_foo)
draw_point(**point_bar)
```
</br>

<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#112303">Braces</a></li>
运行的结果：     
from __future__ import braces    
SyntaxError: not a chance    
貌似是个玩笑， 想要引入c语言style的花括号    
结果是not a chance、、     
```python
from __future__ import braces
```
</br>


<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#101945">Chaining Comparison Operators</a></li>
连续的比较符吧，实际中还是挺有用的      
突然想到的：     
if A and B in L: → if (A and B) in L:     
```python
>>> x = 5
>>> 1 < x < 10
True
>>> 10 < x < 20 
False
>>> x < 10 < x*10 < 100
True
>>> 10 > x <= 9
True
>>> 5 == x > 4
True
```
</br>

<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#101447">Decorators</a></li>
装饰器，之前也从来没有用过，以后尝试一下       
看了一篇装饰器的文章，写的挺好的     
大致明白了原理和应用      
<a href="http://www.cnblogs.com/coderzh/archive/2010/04/27/python-cookbook33-Decorators.html">http://www.cnblogs.com/coderzh/archive/2010/04/27/python-cookbook33-Decorators.html</a>
```python
>>> def print_args(function):
>>>     def wrapper(*args, **kwargs):
>>>         print 'Arguments:', args, kwargs
>>>         return function(*args, **kwargs)
>>>     return wrapper

>>> @print_args
>>> def write(text):
>>>     print text

>>> write('foo')
Arguments: ('foo',) {}
foo
```   


<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#113198">Default Argument Gotchas / Dangers of Mutable Default arguments</a></li>
I found this a lot easier to understand when I learned that the default arguments live in a tuple that's an attribute of the function,     
e.g. foo.func_defaults. Which, being a tuple, is immutable.     
还是不太明白     
```python
>>> def foo(x=[]):
...     x.append(1)
...     print x
... 
>>> foo()
[1]
>>> foo()
[1, 1]
>>> foo()
[1, 1, 1]
Instead, you should use a sentinel value denoting "not given" and replace with the mutable you'd like as default:

>>> def foo(x=None):
...     if x is None:
...         x = []
...     x.append(1)
...     print x
>>> foo()
[1]
>>> foo()
[1]
```


<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#102062">Descriptors</a></li>
Python描述符（descriptor）解密
<a href="http://www.geekfan.net/7862/">http://www.geekfan.net/7862/</a>

<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#111970">Dictionary default <code>.get</code> value</a></li>
前一种如果不包含键值，会报错，后一种会返回第二个参数的值。
```python
sum[value] = sum.get(value, 0) + 1
```


<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#102065">Docstring Tests</a></li>
不懂啥意思   



<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python/112316#112316">Ellipsis Slicing Syntax</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#117116">Enumeration</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#114420">For/else</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#102202">Function as iter() argument</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#101310">Generator expressions</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#101276"><code>import this</code></a></li>
这个吊。。
<code><span class="kwd">import</span><span class="pln"> this
</span><span class="com"># btw look at this module's source :)</span></code>
<p><a href="http://svn.python.org/view/python/trunk/Lib/this.py?view=markup" rel="nofollow">De-cyphered</a>:</p>
<blockquote>
  <p>The Zen of Python, by Tim Peters    </p>
  
  <p>Beautiful is better than ugly.
  Explicit is better than implicit.
  Simple is better than complex.
  Complex is better than complicated.
  Flat is better than nested.
  Sparse is better than dense.
  Readability counts.
  Special cases aren't special enough to break the rules.
  Although practicality beats purity.
  Errors should never pass silently.
  Unless explicitly silenced.
  In the face of ambiguity, refuse the temptation to guess.
  There should be one-- and preferably only one --obvious way to do it.
  Although that way may not be obvious at first unless you're Dutch.
  Now is better than never.
  Although never is often better than <em>right</em> now.
  If the implementation is hard to explain, it's a bad idea.
  If the implementation is easy to explain, it may be a good idea.
  Namespaces are one honking great idea -- let's do more of those!  </p>
</blockquote>

<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#102037">In Place Value Swapping</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#101840">List stepping</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#112286"><code>__missing__</code> items</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#101537">Multi-line Regex</a></li>
多行正则表达式
有机会要学一下
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#113164">Named string formatting</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#101549">Nested list/generator comprehensions</a></li>
双重循环生成list
炫酷。。
```python
[(i,j) for i in range(3) for j in range(i) ]      
((i,j) for i in range(4) for j in range(i) )  
```
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#108297">New types at runtime</a></li>


<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#113833"><code>.pth</code> files</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#1024693">ROT13 Encoding</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#143636">Regex Debugging</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#101739">Sending to Generators</a></li>
生成器(generator) 有时间要深入学习一下
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#168270">Tab Completion in Interactive Interpreter</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#116480">Ternary Expression</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#114157"><code>try/except/else</code></a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#3267903">Unpacking+<code>print()</code> function</a></li>
<li><a href="http://stackoverflow.com/questions/101268/hidden-features-of-python#109182"><code>with</code> statement</a></li>
</ul>

