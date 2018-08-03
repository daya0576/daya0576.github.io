---
layout: post
title: "面试算法题 - $1 Coke Problem"
date: 2017-02-24 09:30:51
comments: true
tags: [algorithm]
---

今天面试问到一个算法: 一个汽水是$1, 两个汽水的**空瓶**换一瓶可乐, 请问给一些钱, 最多能喝几瓶呢?     
当时思路有些乱, 算法没写清楚, 面试结束去个奶茶店, 重新写了一下.    
<!--more-->
    

### 英文的描述:    
A bottle of Coke is $1. You can exchange two empty bottles for a bottle of Coke. You have $20 now in your pocket. So how many bottles of Coke can you drink at most?    


### 1. 模拟喝汽水的过程.
当时写算法的时候, 面试官很看重的是可读性, 例如变量名的定义.     
作为一个Python程序员, 我以后也在这方面也要更加注意.    
```python
def cal_drinks(n):
    avail_drinks = n
    sum_drunk = 0
    empty_drinks = 0

    while avail_drinks > 0:
        # consume available drinks
        sum_drunk += avail_drinks
        empty_drinks += avail_drinks

        # replace empty bottles to drinks
        avail_drinks = empty_drinks // 2
        empty_drinks = empty_drinks % 2

    return sum_drunk
```


### 2. 递归
写递归最重要的就是找到那个推倒式.     
```python
# n个空瓶: f(n) = n/2 + f(n/2 + n%2)
# n块钱:  F(n) = n + f(n)
def cal_drinks_by_empty(n):
    if n <= 1:
        sum_drunk = 0
    else:
        sum_drunk = n//2 + cal_drinks_by_empty(n//2 + n%2)

    return sum_drunk


def cal_drinks(n):
    return n + cal_drinks_by_empty(n)
```


### 3: ???
就是为什么结果是n + (n-1), 是因为这个推导式有什么简化的方法吗?     



最后献上一张奶茶图留念:   
<img style="max-height:330px" class="lazy" data-original="/images/blog/170224_coke/milktea.JPG">   
