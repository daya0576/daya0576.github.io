---
layout: post
title: "Python - Note of Variable Scope"
date: 2017-02-20 09:34:57
comments: true
tags: [scope, python]
---


> Watched an awesome video about python scope: 
[https://www.youtube.com/watch?v=QVdf0LgmICw](https://www.youtube.com/watch?v=QVdf0LgmICw)

<!--more-->
   

My clear summery of the video:   
```python
''' LEGB:
Local, Enclosing, Global, Built-in
'''

''' Build-in variables '''
# import builtins
# print(dir(builtins))

x = 'global x'


def outer():
    x = 'outer x'

    def inner():
        x = 'inner x'

```
