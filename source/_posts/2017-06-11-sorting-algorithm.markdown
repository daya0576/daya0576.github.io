---
layout: post
title: "排序算法总结(Python实现附带思路)"
date: 2017-06-11 00:04:35
comments: true
tags: [python, algorithm]
---

最近开始看<算法导论>, 一开始就是讲的就是插入排序和merge sort,    
之前面试的时候, 也被问起过排序算法, 一紧张只想到了两三个,    
所以乘这个机会回顾了一下大部分的排序算法, **并自己用Python实现了一遍.**    
<!--more-->   
     

### 各个算法的时间和空间复杂度:
以前大二的时候, 看到这张图的时候真的头晕, 但现在看起来这个表格真的很精华.   
理解各个算法后就慢慢明白各个算法三种情况(最优, 平均和最坏)的复杂度, 还有空间复杂度都不一样.    
所以不同不算法都有各自的优势和应用的场景.    
<img class="lazy" data-original="/images/blog/170610_sorting/time_complexity.png">       


### 直接把每个算法实现的解释和感想写在代码的注释里了.    
ps. 代码是用python3.5写的.
```python
def bubble_sort(l):
    """冒泡排序:

    哈哈, 这个算法真的是满满的回忆, 记得以前大二开算法课接触的最早的几个算法.
    那时是用C写的, 熟练的直接默写出来了.
    当时还没有`l[i], l[j] = l[j], l[i]`这种写法, 需要用tmp来交换两个数字, 也是可以不用tmp哦 :p
    """
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            if l[j] < l[i]:
                l[i], l[j] = l[j], l[i]
    return l


def insert_sort(l):
    """插入排序:

    从左到右遍历数组, 将每个元素插入它左边的那个(已排好序)数组里
    """
    for i, v in enumerate(list(l)):
        # j: the index of item to compare
        j = i - 1
        while j >= 0 and l[j] > v:
            l[j+1] = l[j]
            j -= 1
        l[j+1] = v
    return l


def selection_sort(l):
    """选择排序:

    和插入排序不同的是, 它是在遍历数组时, 将元素和它右边数组里的最小值进行交换.   
    """
    for i in range(len(l)):
        min = i
        for j, v in enumerate(l[i+1:], start=i+1):
            if v <= l[min]: min = j

        l[i], l[min] = l[min], l[i]
    return l


def merge_sort(l):
    """归并排序:

    去google picture搜一下merge sort的图, 你就明白这个算法了.    
    """
    def merge(a, b):
        l = []
        while a and b:
            l.append(a.pop(0)) if a[0] <= b[0] else l.append(b.pop(0))
        return l + a + b

    if len(l) >= 2:
        return merge(merge_sort(l[::2]), merge_sort(l[1::2]))
    else:
        return l


def quick_sort(l):
    """快速排序:

    step 1. 随机选择一个数作为基准, 将输入的数组分为两半
    step 2. 对两个子数组, 继续用step 1的方法进行处理,
            直到到达递归结束的条件: 输入数组长度小于等于1.   
    """
    if len(l) <= 1:
        return l
    else:
        base = l[0]
        left = [i for i in l[1:] if i <= base]
        right = [i for i in l[1:] if i > base]
        return quick_sort(left) + [base] + quick_sort(right)


def heap_sort(l):
    """堆排序:

    这段代码是摘自Python heapq的官方文档.
    先把所有元素push(O(log n))到heap里, 生成一个min-heap.
    """
    from heapq import heappush, heappop
    h = []
    for value in l:
        heappush(h, value)
    return [heappop(h) for _ in range(len(h))]


if __name__ == '__main__':
    a = [5, 2, 4, 6, 1, 3]
    print("Built-in sort:   {} --> {}".format(a, sorted(a)))
    print("Bubble sort:     {} --> {}".format(a, bubble_sort(list(a))))
    print("Insert sort:     {} --> {}".format(a, insert_sort(list(a))))
    print("Selection sort:  {} --> {}".format(a, selection_sort(list(a))))
    print("Merge sort:      {} --> {}".format(a, merge_sort(list(a))))
    print("Heap sort:       {} --> {}".format(a, heap_sort(list(a))))
    print("Quick sort:      {} --> {}".format(a, quick_sort(list(a))))

```
<img class="lazy" data-original="/images/blog/170610_sorting/result.png">



