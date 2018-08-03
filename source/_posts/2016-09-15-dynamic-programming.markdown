---
layout: post
title: "Fibonacci number(Recursive, DP and Decorator)"
date: 2016-09-15 10:52:49 +1000
comments: true
tags: [study, dynamic programming]
---

I found a [fatastic video](https://www.youtube.com/watch?v=OQ5jsbhAv_M) about Dynamic Programming, it can be used to solve Fibonacci number problem efficiently. Decorater can also be used to make code elegent ^o^      

<!--more-->



# Fibonacci number: 1, 1, 2, 3, 5, 8, 13...

###1. Original recursive implementation   
``` python
def fib(n):
    if n<=2: f = 1
    else: f = fib(n-1) + fib(n-2)

    return f
```



###2. Improvement: memoization  
- Reuse solutions to **sub-problems** to solve the problem    
- So time = #sub-problems * O(sub-problem)     
``` python
#!/usr/bin/python3
from collections import defaultdict
import sys

n = int(sys.argv[1])
mem = defaultdict(lambda: 0)

def fib(n):
    global mem
    # print(n)
    if mem[n]:
        return mem[n]

    if n<=2: f = 1
    else: f = fib(n-1) + fib(n-2)

    mem[n] = f
    print(f)
    return f


def fib_con(n):
    mem = {}
    for k in range(1, 1+n):
        if k<=2:
            mem[k] = 1
        else:
            mem[k] = mem[k-1] + mem[k-2]

        print(mem[k])
    return mem[n]

fib(n)
fib_con(n)

```
**Video link**: [https://www.youtube.com/watch?v=OQ5jsbhAv_M](https://www.youtube.com/watch?v=OQ5jsbhAv_M)    
`DP = recursion + memorization + guessing`   


###3. Problem of the improvement above:
The disadvantage of this method is that the clarity and the beauty of the original recursive implementation is lost.     
So we use a helper function to handle the fib() function, the idea of .    
``` python
def memoize(f):
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]

    return helper


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


fib = memoize(fib)
print(fib(40))
```
That is Decorator: `@memoize`      
U can check this website for more information:    
[http://www.python-course.eu/python3_memoization.php](http://www.python-course.eu/python3_memoization.php)   
``` python
@memoize
def fib(n):
    ...

print(fib(40))
```


###4. Generator version   
```python
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a+b

for i in fib(10):
    print(i)
```
