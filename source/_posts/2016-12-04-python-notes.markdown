---
layout: post
title: "Python Personal Note"
date: 2016-12-04 13:08:59
comments: true
tags: [python, study]
---

Planning to figure out problems of Python that confused me for a long phase.      
The blog trace the steps of my study.    

<!--more-->
  


## Handling int()
Official explain about this build-in function: [https://docs.python.org/3/library/functions.html#int](https://docs.python.org/3/library/functions.html#int)     
Just found out that there is an arguement called `base`,  e.g., int('010', 2).       
In the past, when I was handling the value of form from user in web application, the program was quite not robust. For example, the program will easily crash if user input twelve in the register form of age.      
So exception could be used to solve this problem:     
```python
try:
    value = int(value)
except ValueError:
    pass  # it was a string, not an int.

```


## Lambda, filter, reduce and map
Summary: [http://www.python-course.eu/lambda.php](http://www.python-course.eu/lambda.php)     
**filter a list:**
```python
In [10]: list(filter(lambda x:x>0, a))
Out[10]: [1, 2, 3, 5]
```
In Python 2.x, `filter` returned a list, but in Python 3.x, it returns an iterator.      
iterator: [https://docs.python.org/3/tutorial/classes.html#iterators](https://docs.python.org/3/tutorial/classes.html#iterators)     
Or     
```python
In [23]: [i for i in l if i>0]
Out[23]: [1, 2, 3, 5]
```

**filter a dict:**
```python
from random import randint

d = {x: randint(0, 10) for x in range(10)}
{0: 10, 1: 1, 2: 8, 3: 1, 4: 3, 5: 7, 6: 7, 7: 2, 8: 7, 9: 9}

{k: v for k, v in d.items() if v>5}
```
`random.randint(a, b):` Return a random integer N such that **a <= N <= b**. Alias for randrange(a, b+1).      

**filter a set:**
`Python3 Set: `[https://docs.python.org/3/tutorial/datastructures.html#sets](https://docs.python.org/3/tutorial/datastructures.html#sets)     


## enum for tuple
**1. global variable:**    
NAME, AGE, EMAIL = range(3)     
**2. namedtuple:**      
doc: [https://docs.python.org/3/library/collections.html?highlight=namedtuple#collections.namedtuple](https://docs.python.org/3/library/collections.html?highlight=namedtuple#collections.namedtuple)    
```python
from collections import namedtuple

Student = namedtuple('Stu', ['name', 'age', 'gender', 'email'])
s = Student('Henry', 24, 'm', 'daya0576@gmail.com')

s.name
```

## Dictionary
**Sorting a dictionary by value:**    
```python
sorted(data.items(), key=lambda x:x[1], reverse=True)
```
**Finding matching keys of dictionaries**    
```python
from random import randint, sample
from functools import reduce

d1 = {x:randint(1, 4) for x in sample('abcdefg', randint(3, 6))}
d2 = {x:randint(1, 4) for x in sample('abcdefg', randint(3, 6))}
d3 = {x:randint(1, 4) for x in sample('abcdefg', randint(3, 6))}

keys_lists = list(map(lambda x:x.keys(), [d1, d2, d3]))
result = reduce((lambda x, y:x&y), keys_lists)
```
**OrderedDict**
doc: [https://docs.python.org/3/library/collections.html?highlight=ordereddict#collections.OrderedDict](https://docs.python.org/3/library/collections.html?highlight=ordereddict#collections.OrderedDict)    


## Random-sample:
random: [https://docs.python.org/3/library/random.html](https://docs.python.org/3/library/random.html)      
**random.sample:**   
```python
In [107]: l = 'abcdefg'

In [108]: from random import sample

In [109]: sample(l, 3)
Out[109]: ['c', 'f', 'a']
```


## Python list implementation
[http://www.laurentluce.com/posts/python-list-implementation/](http://www.laurentluce.com/posts/python-list-implementation/)   
