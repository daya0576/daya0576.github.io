---
layout: post
title: "数组分割(编程之美) HyperS面试题 思考与分享"
date: 2017-05-25 00:34:57 +0800
comments: true
tags: [hypers, algorithm]
---

`问题描述:` **有一个无序, 元素个数为2n的正整数数组. 要求: 如何能把这个数组分割为元素个数为n的两个数组, 并使两个子数组的和最接近.**    
当时面试的时候, 看完描述想了十秒钟, 只能想到C(2n, n)把所有情况遍历一遍, 想不到特别简单的算法, 就直接放弃了.. 面试官问我应该怎么做呢, 我只能靠直觉说用动态规划吧.    
虽然现在早就入职了, 但终于有时间重新思考这个问题, 并用这篇日志记录下来.    
<!--more-->   
  

> 这道面试题其实来自 `编程之美 2.18 数组分割`, 讽刺的是我以前很早买过这本书, 却没有仔细阅读~~   


### 方法一:
Simple greedy algorithm:

Step1: 将这个数组进行排序.   
Step2: 按奇偶划分为两个数组: l1: [a1, a3, a5, ..] 和 l2: [a2, a4, a6, ..]    
Step3: 遍历这两个数组, 找出一对数进行交换, 使得`Sum(l1)`和`Sum(l2)`的差值最小.   
Step4: 重复Step3操作, 直到找不到可以让差值更小的交换.    

**缺点: ** 这样找到的两个子数组并不能保证是最优解.   
我自己简单写了一下Python代码, 供更好的理解.   
```python
L = [1, 5, 7, 8, 9, 6, 3, 11, 20, 17]


def method1(l):
    # 先将所有元素排序, 按奇偶划分为两个数组:
    # [a1, a3, a5, ..] 和 [a2, a4, a6, ..]
    l = sorted(l)
    l1, l2 = l[::2], l[1::2]

    print('sum(l1) - sum(l2):', sum(l1) - sum(l2))
    for i in range(5):
        swp = (0, 0)
        sub = sub_tmp = sum(l1) - sum(l2)
        for i, x in enumerate(l1):
            for j, y in enumerate(l2):
                # x与y交换之后, SUM(l1) - SUM(l2):
                #   new_sum1 = sum(l1) - x + y
                #   new_sum2 = sum(l2) - y + x
                #   new_sub = new_sum1 - new_sum2 = sum(l1) - sum(l2) - 2x + 2y
                new_sub = 2 * (x - y) - sub

                if abs(new_sub) <= abs(sub_tmp):
                    swp = (i, j)
                    sub_tmp = new_sub

        if abs(sub) != abs(sub_tmp):
            i, j = swp[0], swp[1]
            l1[i], l2[j] = l2[j], l1[i]
            print('\nswapping l1[{}] and l2[{}]'.format(i, j))
            print('sum(l1) - sum(l2):', sum(l1) - sum(l2))
        else:
            break


if __name__ == '__main__':
    method1(list(L))
```



### 方法二:
分割为两个数组, 并使他们的和最接近 == 从2n个数中挑出n个数, 使他们的和最接近与所有整数的之和的一半.   
书中对这个方法二的描述也是很令人费解, 我总结了一下:   

**定义:**   
sum_set(k, i): 从k个整数中找出i个元素的和 的集合.   
令L为输入的数组, 令2N为数组长度:    

1. **sum_set(2N, 1):** 从2N个元素中取一个元素, 得到的和的集合
2. **sum_set(2N, 2N):** 从2N个元素中取2N个元素, 得到的和的集合
3. **sum_set(2N, i):** S(2N-1, i) | {x+L[k-1] for x in S(2N-1, i-1)}     
**大致意思就是sum_set(2N, i)可以分解为 第k个元素 选或者不选 的情况**   

**举个例子!!!**   
```
L = [1, 2, 3, 4]

1. sum_set(4, 1) = {1, 2, 3, 4}
2. sum_set(4, 4) = {1+2+3+4} = {10}
3. sum_set(4, 2)   
= sum_set(3, 2) | {x+4 for x in sum_set(3, 1)}    
= (sum_set(2, 2) | {x+3 for x in sum_set(2, 1)}) | {1+4, 2+4, 3+4}    
= ({1+2} | {1+3, 2+3\}\}) | {5, 6, 7}       
= {3, 4, 5, 6, 7}
```
书中是用for循环来写的, 但我感觉这种DP一般用递归会更加清晰, 就写了这个版本(当然可以加cache做优化, 但我主要是为了展示思路就懒得写了, 可以参考我[关于动态规划的这篇日志](/blog/20160915/dynamic-programming/))    
```python
def method2(k, i):
    if i == 1:
        return set(L[:k])
    if k == i:
        return {sum(L[:k])}

    # S(k, i) = S(k-1, i) U {A[k] + x | x属于S(k-1, i-1) }
    return method2(k-1, i) | {i+L[k-1] for i in method2(k-1, i-1)}


if __name__ == '__main__':
    L = [1, 5, 7, 8, 9, 6, 3, 11, 20, 17]
    N = int(len(L) / 2)

    print(method2(2*N, N))
```

因为每一步都拆成了两种情况(第k个元素 被选中|没被选中)进行递归，所以**时间复杂度为O(2^N)**.   
要是加cache了话(把计算过的结果放在字典里), 时间复杂度是O(max(k)*max(i))=O(N^2)?   

但我总觉得`{i+L[k-1] for i in method2(k-1, i-1)}`的时间复杂度是不是没有考虑进去???   

原书中的写法, 测试过了, 和递归的结果是一模一样的:   
```python
def method2_o(N, Heap, L):
    for k in range(1, 2*N+1):
        i_max = min(k-1, N-1)
        for i in reversed(range(0, i_max+1)):
            for v in Heap[i]:
                Heap[i+1].add(v+L[k-1])
```



### 方法三:   
方法二的时间复杂度是指数级的, 肯定是不能接受的.   
按照书上写了第三种方法, **时间复杂度为O(N^2*Sum)**:     
```python
from collections import defaultdict

def method3(isOk):
    # isOk[i][v]: bool(从数组中取i个数, 得到sum为v)
    for k in range(2*N):
        for i in reversed(range(1, min(k+1, N)+1)):
            for v in range(1, int(sum(L)/2+1)):
                sub = v - L[k]
                if sub >= 0 and isOk[i-1][sub]:
                    isOk[i][v] = True


if __name__ == '__main__':
    L = [1, 5, 7, 8, 9, 6, 3, 11, 20, 17]
    N = int(len(L) / 2)

    isOk = {x: defaultdict(bool) for x in range(0, N+1)}
    isOk[0][0] = True
    method3(isOk)

    [print(k, v) for k, v in isOk.items()]
```




### 总结(TODO):

1. 不知道在看这篇博客的你有没有发现一个很尴尬的问题:  
书中的解法二得到的是 取值和的集合, 解法三得到的是是否能找到答案的boolean值.   
那如何利用解法二, 解法三得到具体的子数组(最优解)呢?  
2. 解法二的我用递归的方式写的时间复杂度?   
如果我递归时, 把计算结果保存到字典里, 不去做重复计算, 那么它的时间复杂度又是多少呢?   

在知乎提的问题: [https://www.zhihu.com/question/60472041](https://www.zhihu.com/question/60472041)    
希望有好心人帮我回答, 23333


### 关于P, NP, NP-complete


### References:

1. <编程之美> 2.18 数组分割
2. [http://www.americanscientist.org/issues/pub/2002/3/the-easiest-hard-problem/2](http://www.americanscientist.org/issues/pub/2002/3/the-easiest-hard-problem/2)
