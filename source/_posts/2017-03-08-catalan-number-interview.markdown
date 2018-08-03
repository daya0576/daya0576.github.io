---
layout: post
title: "面试算法题 - 出栈次序问题 (Catalan Number)"
date: 2017-03-08 21:38:32 +0800
comments: true
tags: [interview, algorithm]
---

之前去方付通面试的时候的时候, 问了我`N个数依次入栈，出栈顺序有多少种？`的算法题, 其实是卡特兰数(Catalan)的应用.    
当时没有答出来(这要是之前没有接触过, 谁答的出来).    
现在用这篇日志重新整理记录一下.      
<!--more-->
  

##问题的定义
一个栈(无穷大)的进栈序列为1，2，3，…，n，有多少个不同的出栈序列?    

##解题思路
1. 假设进栈序列为[1, 2, 3, 4, 5, 6]   
2. 因为每个数字都可能是最后一个出栈的(独立的事件), 所以先单独分析**当k为最后一个出栈数字**的情况.    
3. 1) 当`k进栈`时, [1, 2]肯定已经出栈了, 所以他们([1, 2])的出栈序列总数为`f(k-1)`   
2) 当`k出栈`时, 因为3为最后一个出栈, [4, 5, 6]肯定也已经出栈了, 所以他们[4, 5, 6]的出栈序列总数为`f(n-k)`
4. 所以当k为出栈序列的最后一个数字时, 可能序列的总和为`f(k-1)*f(n-k)`
5. 又因为第二条中, 每个事件为独立的, 所以最后得到了这么一个推导式:    
`f(0) = f(1) = 1`   
`f(n) = f(0)*f(n-1)+f(1)*f(n-2) + ... + f(n-1)*f(0) (n>=2)`

##Reference
1. [https://en.wikipedia.org/wiki/Catalan_number](https://en.wikipedia.org/wiki/Catalan_number)   
2. [http://www.acmerblog.com/catalan-5196.html](http://www.acmerblog.com/catalan-5196.html)
3. [http://baike.baidu.com/item/%E5%8D%A1%E7%89%B9%E5%85%B0%E6%95%B0#4](http://baike.baidu.com/item/%E5%8D%A1%E7%89%B9%E5%85%B0%E6%95%B0#4)   
