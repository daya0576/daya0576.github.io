---
title: 大牙的 Java 入门之路分享（持续更新）
tags:
---

有人建议说教游泳的最好办法是直接把那个孩子扔到水里？🤔 在你心中的 Java 入门最佳实践是什么呢？

这篇博客将记录个人学习 Java 的一些经历与思考，希望同在迷茫的你读到，可以有所收获 ：）

<!--more-->

## 一、个人经历
简单分享一下个人的编程经历：

1. 首先从高校期间的师生合作项目开始接触 Python🐍，进行云计算放置策略的算法研究。之后通过 [Tango with Django](https://www.tangowithdjango.com/) 教程，掌握 Python Web 相关知识，并尝试构建了个人小项目🥰：[unsw.co](https://unsw.co/)
2. 基于之前的经历，毕业后顺利寻得一份 Python 后端开发相关的工作（[Hypers 每周小结](/blog/20170321/hypers-first-week-summary/)）
3. 第一份工作满一年之际，机缘巧合加入“大厂”为一名 SRE💪，但很可惜公司的技术栈中 Java 才是一等公民，在一次又一次“拥抱变化”之后，开始使用 Java 作为工作的主力语言。

TODO：IMAGE

## 二、学习路径
在[《Google SRE》](/blog/20180403/impressions-of-google-sre/)的第 28 章中，谈论了如何让一个 SRE 新手（newbie）快速开始进入 on-call 的队伍：有人建议说教游泳的最好办法是直接把那个孩子扔到水里，但文中并不太赞同这个观点，成为一名合格的 sre 需要体系化的学习和实践。

学习一门编程语言也是一个道理，除了大胆的上手实践，系统化的持续学习才是关键。**下面将按时间顺序，分享个人在学习 Java 过程中，受益匪浅的在线资料**

### 1. 官方文档 -> 《The Java™ Tutorials》
基于以往的编程经历中，不难发现一门编程语言质量最高的入门教程，往往出自官网（因为是对这门语言最了解的人撰写的？）

这里推荐[《The Java™ Tutorials》](https://docs.oracle.com/javase/tutorial/java/index.html)👍👍👍：
1. 首先不要被 Tutorial 这个词迷惑了😄，其中例如 Annotations 和 Generic 等部分有很多深入浅出和**非常完整**的说明。
2. 最为关键是每一个 topic 的结尾，附上课后练习，可以很方便的进一步巩固和掌握知识。

### 2. 好书推荐 -> 《Java 8 实战》
假如你和我一样在学生期间接触过 java（jdk1.6 与 eclipse 的时代），重拾后发现现在的 java 和以前竟然不是一个东西？？？总是被 Stream API、Lambda、方法引用 这些新特性，绕的云里来雾里去。

那么恭喜你！我这里有一本秘籍叫做[《Java 8 实战》](https://book.douban.com/subject/26772632/)，

可以快速浏览我的[读书笔记](/blog/20200822/java8-in-action-comments/)

### 4. 《阿里编程规范》
个人总觉得 Java 的“表达能力”和 Python 不是一个级别的。例如下面的例子，将一个嵌套的二维数组打平：
```
# Python
>>> matrix = [[1,2,3],[4,5,6],[7,8,9]]
>>> [x for l in matrix for x in l]
[1, 2, 3, 4, 5, 6, 7, 8, 9]

# Java
int[][] matrix = new int[][]{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
int[] l = Arrays.stream(matrix)
        .flatMapToInt(Arrays::stream)
        .toArray();
System.out.println(Arrays.toString(l));
// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

而 Java 的“笨重”反而又是它最大的优势：在多人协作开发的场景，通过各种条条框框，可以更好的保证代码质量的下限。

《阿里编程规范》就是“条条框框”的集大成者。因为其中 90% 以上的规范或者最佳实践，可以使用

### 3. [WIP] 《Effective Java》
 ide 目前还无法提醒你编写更加「优雅」的代码，所以强烈阅读这本书，而不是在 CR 的时候让你的同事一次次教你。

举最简单的例子：
1. 返回 []

参考资料

### 2. UML


> Item 19: Design and document for inheritance or else prohibit it（继承要设计良好并且具有文档，否则禁止使用）

如果你要使用接口和抽象类，请

### 3. 设计模式

软件最重要的一个使命，即管理复杂度。而 Java 遇到设计模式就像咖啡遇到



### 5. [WIP] 深入理解 JVM 虚拟机


例如：

- 对内存管理和垃圾回收机制的学习，可以让你
- 对解析与分派在 JVM 侧的原理，更好的理解 override 与 overload 的行为。


### TODO
- 《代码大全》
- 《Java并发编程实战》

---


---

最近在看一本书，叫做《为什么你总是半途而废》，虽然鸡汤

1. 如果你也在学习，期望
2. 近期的规划：做一个开源项目，就像打乒乓一样。

--- 

很幸运有个环境让自己不断成长，招人
有人建议说教游泳的最好办法是直接把那个孩子扔到水里？