---
layout: post
title: "面试算法题 - 二分查找搜索范围"
date: 2017-03-06 12:45:09 +0800
comments: true
tags: [inteview, algorithm]
---

去再惠面试的时候, 问了我一道二分查找的变种题, 我当时答的并不是特别清楚, 用这篇日志整理记录一下.      
<!--more-->
  

##问题的定义
**input:**    
1. 给定一个升序排列的自然数数组, eg. [1, 3, 3, 5, 7, 7, 7, 7, 8, 14, 14]   
2. 任意自然数, eg. 7    
**output:**   
数组内 值为7区域的左右边界index: [1, 3, 3, 5, **7, 7, 7, 7**, 8, 14, 14]   
这个例子中就是**(4, 7)**   


## 我的思路
我首先想到的是生成**inverted index**再去查找, 或者用**Galloping search**.   
后来才想到考官想考察的是binary search.     
于是我的思路就变成先用binary找到那个值的区域里的随机一点, 然后用两个while去找左右的边界.     
但如果这个区域太大, 时间复杂度又变成O(n)了.     
最后考官提醒我可以对二分查找做一下改动就可以啦.    


##原版的二分查找(返回index和val)     
```python
A = [1, 2, 4, 4, 4, 6, 7]
B = [1, 3, 3, 3, 3, 3]


def bin_search(val, l, left=None, right=None):
    if left is None or right is None:
        left, right = 0, len(l)-1

    # 终止条件
    if left > right:
        return -1
  
    mid = (left + right) // 2
    if l[mid] > val:
        return bin_search(val, l, left, mid-1)
    elif l[mid] < val:
        return bin_search(val, l, mid+1, right)
    else:
        return mid, val


print(bin_search(4, A))
```



## 改动后的二分查找
思路:   
在找**左边界**的时候:   
`if left > right: return left`   
`if ｌ(mid) >= val: (left, mid-1)`   
`elif l(mid) <= val: (mid+1, right)`   
找右边界思路同上   
```python
def bin_search_l(val, l, left=None, right=None):
    if left is None or right is None:
        left, right = 0, len(l) - 1

    if left > right: return left

    mid = (left + right) // 2
    if l[mid] >= val:
        return bin_search_l(val, l, left, mid-1)
    elif l[mid] < val:
        return bin_search_l(val, l, mid+1, right)


def bin_search_r(val, l, left=None, right=None):
    if left is None or right is None:
        left, right = 0, len(l) - 1

    if left > right: return right

    mid = (left + right) // 2
    if l[mid] > val:
        return bin_search_r(val, l, left, mid-1)
    elif l[mid] <= val:
        return bin_search_r(val, l, mid+1, right)


def bin_search(val, l):
    left, right = bin_search_l(val, l), bin_search_r(val, l)

    if left > right:
        return -1
    else:
        return left, right


if __name__ == '__main__':
    A = [1, 4, 4, 4, 4, 4, 6, 6]
    print("Input:", A)
    print("Output:", bin_search(4, A))

    # Input: [1, 4, 4, 4, 4, 4, 6, 6]
    # Output: (1, 5)

```


## 总结
看起来算法好像很复杂, 但核心的思想其实就那么几句伪代码.    
还是那句永恒不变的真理: `先想请思路再下笔!`   


## 几个月后重写的一个
``` python
def binary_search_l(l, v):
    left, right = 0, len(l) - 1

    while left <= right:
        mid = (left + right) // 2
        if l[mid] < v:
            left = mid + 1
        else:
            right = mid - 1

    if l[left] == v:
        return left


def binary_search_r(l, v):
    left, right = 0, len(l) - 1

    while left <= right:
        mid = (left + right) // 2
        if l[mid] <= v:
            left = mid + 1
        else:
            right = mid - 1

    if l[right] == v:
        return right


def range_search(l, v):
    return binary_search_l(l, v), binary_search_r(l, v)


if __name__ == '__main__':
    print(range_search(A, 7))
```




