---
title: 大牙的 Java 入门经历分享（持续更新）
date: 2021-09-11 23:24:57
categories:
- JAVA
---

有人建议说教游泳的最好办法是直接把那个孩子扔到水里？🤔 在你心中关于 Java 入门的最佳路径是什么呢？

这篇博客将记录个人学习 Java 的一些经历与思考，希望同在迷茫的你读到，可以有所收获 ：）

<!--more-->

# 1. 个人编程经历
简单分享一下个人 一波三折的编程经历：

1. 首先缘起高校期间的师生合作项目，在老师的建议下接触 Python🐍
2. 之后通过 [Tango with Django](https://www.tangowithdjango.com/) 教程，迷上 Web 开发，并尝试构建一些个人小项目🥰
3. 基于之前的经历，毕业后顺利寻得一份 Python 后端开发相关的工作（[Hypers 每周小结](/blog/20170321/hypers-first-week-summary/)）
4. 当第一份工作满一年之际，机缘巧合加入“大厂”为一名 SRE💪

但很可惜当前公司的技术栈中， Java 才是一等公民。在一次又一次“拥抱变化”之后，开始使用 Java 作为工作的主力语言。

![EF1EF453-2586-4FC7-8E9F-BA8CF47D25B9_1_105_c](/images/blog/2021-09-04-jvm-note/EF1EF453-2586-4FC7-8E9F-BA8CF47D25B9_1_105_c.jpeg)


# 2. Java 学习路径
在[《Google SRE》](/blog/20180403/impressions-of-google-sre/)的第 28 章中，谈论了如何让一个 SRE 新手（newbie）快速开始进入 on-call 的队伍：有人建议说教游泳的最好办法是直接把那个孩子扔到水里，但文中并不太赞同这个观点，成为一名合格的 sre 需要**体系化**的学习和实践。

学习一门编程语言也是一个道理，除了大胆的上手实践，系统化的学习更为关键。下面将按时间顺序，分享个人 Java 的入门路径，以及受益匪浅的学习资料。

## 2.1 掌握基本语法
### 2.1.1 官方文档 -> 《The Java™ Tutorials》
基于以往的编程经历中，不难发现一门编程语言质量最高的入门教程，往往出自官网（因为是对这门语言最了解的人撰写的？）

这里推荐[《The Java™ Tutorials》](https://docs.oracle.com/javase/tutorial/java/index.html)👍👍👍：
1. 首先不要被 Tutorial 这个词迷惑了😄，其中例如 Annotations 和 Generic 等部分有很多深入浅出和无死角的说明。
2. 更为关键是，每一个 topic 的结尾，附上课后练习，可以很方便的进一步巩固和掌握知识。


### 2.1.2 好书推荐 - 《Java 8 实战》
假如你和我一样在学生期间接触过 java（jdk1.6 与 eclipse 的时代），重拾后发现现在的 java8 和以前竟然不是一个东西？？？总是被 Stream API、Lambda、方法引用等新特性，绕的云里来雾里去。

那么恭喜你！有一本秘籍叫做[《Java 8 实战》](https://book.douban.com/subject/26772632/)，帮忙你快速掌握 Java 8 的新特性。
![](/images/blog/2021-09-04-jvm-note/16313756701798.jpg)


### 2.1.3 编程规范 - 《阿里编程规范》
有些瞬间觉得 Java 的 “表达能力” 远不如 Python（有力使不上的感觉）

例如下面的例子，简单将一个嵌套的二维数组打平的需求。
Python 实现的版本不管是在直观的“代码篇幅”，还是“可读性”上都明显占优：
```python
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

但是。。Java 的“笨重”反而又是它最大的优势：在多人（很多人）协作开发的场景，通过各种条条框框，可以更好的保证代码质量的下限 👀

而《阿里编程规范》即“条条框框”的集大成者。。~~但说实话没有必要花太多时间细读~~，因为其中 90% 以上的规范或者最佳实践，已经沉淀在 IDEA 的插件中（[链接🔗](https://plugins.jetbrains.com/plugin/10046-alibaba-java-coding-guidelines)），强烈建议安装获取实时提醒。

收回上面不需要细读的话，放假前摸鱼认真阅读时，还是有很多收获。建议仔细阅读，成为一个莫得感情的代码生成机器。

例如 集合处理 章节中，阐述了编译阶段不会发现的报错：

1. 数组调用 `subList` 后得到的其实是 `java.util.ArrayList.SubList`。⚠️注意这时对父集合元素的增加或删除，会导致报错！！
2. 集合 -> 数组：最佳实践为 `list.toArray(new String[0]);`，动态创建与size相同的数组，性能最好。
3. 数组 -> 集合：调用 `Arrays.asList()` 后，同时⚠️注意不能对处理后的集合，进行增删改查的操作。

## 2.2 编写更加优雅的代码
### 2.2.1 相见恨晚的《Effective Java》
虽然插件会给出实时的 WARNING 提示，但很可惜，目前还无法提示更加「优雅」的代码。

阅读《Effective Java》书后，唯一的一个感觉就是相见恨晚，因为其中每个章节都似曾相识（对应同事曾经给我的 CR 建议 😂）

举其中一个章节为例：`Item 53: Use varargs judiciously（明智地使用可变参数）`
```java
// 需求：子程序接收可变参数，但长度必须大于 1

// 下面写法的缺点：1）运行时而不是编译时失败 2）不美观：必须包含对 args 的显式有效性检查
// The WRONG way to use varargs to pass one or more arguments!
static int min(int... args) {
    if (args.length == 0)
        throw new IllegalArgumentException("Too few arguments");
    int min = args[0];
    for (int i = 1; i < args.length; i++)
        if (args[i] < min)
    min = args[i];
    return min;
}

// 正确的写法
static int min(int firstArg, int... remainingArgs) {
    int min = firstArg;
    for (int arg : remainingArgs)
        if (arg < min)
          min = arg;
          return min;
}

// 性能优化：解决大部分场景下，调用创建数组的成本 
public void foo() { }
public void foo(int a1) { }
public void foo(int a1, int a2) { }
public void foo(int a1, int a2, int a3) { }
public void foo(int a1, int a2, int a3, int... rest) { }
```

尝试过阅读英文原版，但太啰嗦了。。推荐[《中英文翻译》](https://github.com/clxering/Effective-Java-3rd-edition-Chinese-English-bilingual)，高效的学习和记录要点。


## 2.3 面向对象 

掌握基本语法后，还是很容易写出 [面条代码 (Spaghetti Code)](https://zh.wikipedia.org/wiki/%25E9%259D%25A2%25E6%259D%25A1%25E5%25BC%258F%25E4%25BB%25A3%25E7%25A0%2581)

这时你需要尝试开始用「面向对象」来思考和组织你的代码，最终管理好整个项目代码的复杂度（~~谨防为了OO而OO~~）。

### 2.3.1 UML

> Item 19: Design and document for inheritance or else prohibit it

《Effective Java》中有个很有意思的一个建议：如果要使用接口和抽象类，请先写好设计文档。我理解即画好 UML 类图和时序图。

*参考之前的一篇博客感受一下：[《解决关于 UML 类图在心中深藏多年的若干疑惑》](/blog/20200502/uml-unified-modeling-language/)*

### 2.3.2 设计模式

软件最重要的一个使命：管理复杂度。而 Java 遇到设计模式就像咖啡遇到牛奶，变成一杯香醇的拿铁～ 深有体会在真实项目中，如果合理的使用构造器、观察者等实用模式，将会有效提升代码的复用性，降低耦合度。

尝试阅读过 《First Head 设计模式》，《Refactoring Guru》，《设计模式：可复用面向对象软件的基础》后，个人的一点点感悟：**掌握一个设计模式很简单，但如何在真实的场景中，恰到好处的使用才是关键和难点。** 所以建议不要纸上谈兵，抓住每一次写代码的机会，不断的实践练习和提高对代码的要求。

参考：*[《Head First 设计模式》学习笔记](/blog/20200614/design-pattern/)、[《Python 不需要设计模式？》](/blog/20201114/why-u-dont-need-design-pattern-in-python/)*

## 2.4 JVM 虚拟机
### 2.4.1 [WIP] 《深入理解 JVM 虚拟机》

虽然 java 天天被黑，但 JVM 还是很优秀的。更难得有一本深入浅出的书供大众学习，不像难产多年的《Python源码剖析》每年圣诞节的梗 😊

虽然书中绝大部份知识，看似在日常中派不上用场（确实例如 class 文件格式每个字段的内容），但很多知识会产生潜移默化提升个人能力，例如：

- 理解内存管理和垃圾回收的机制，让你排查线上问题和性能调优时，更加如鱼得水
- 学习「解析」与「分派」在 JVM 侧的原理，更好的理解 override 与 overload 的行为
- .. 

*参考近日的一篇博客：[《Java 内存管理 - SRE 的必修课》](/blog/20210904/jvm-note/)*

### 2.5 LATER

侥幸入门后还有很长很长很长的路要走，以下为待读的书单：

- 各种源码阅读：例如 ThreadLocal、ArrayList 等等。阅读源码在好处多多，在了解语言内部实现的同时，帮忙耳濡目染学习更加优雅的代码实现～
- 《Java并发编程实战》
- ...

# 3. 关于坚持

上周地铁上看了一本书，名叫[《为什么你总是半途而废》](https://book.douban.com/subject/35492252/)。虽然有一丝丝鸡汤... 但借着其中关于如何坚持到底的几个观点分享一下：

> 听我讲座的人中有一个舞蹈老师，他曾跟我说：“能够学好舞蹈的人往往都是那些本身就喜欢舞蹈的人，喜欢练习跳舞的人。”相反，学不好的人往往想的是学会舞蹈以后既能扩大自己的交际圈，又能锻炼身体、丰富人生等，他们更多想的是学会舞蹈之后的好处。比起练习的过程，他们更希望感受结果的喜悦，显然很难坚持下去。减肥也是同样的道理，只重视结果的人即便能瘦下来，最终还是会反弹

享受过程：下半年给自己的一个目标：尝试用 Java 技术栈做一个小项目（code for fun），利用解决现实中的问题，帮助他人的成就感，不断自我驱动。

> 容易半途而废的人总是想独自完成事情，而坚持到底的人却善于借助外力

所以如果你也在学习 Java，可以直接留言联系我，相互监督打卡，持之以恒提一起升编码能力 ：）

> 先从整件事的1%着手

入门一门语言，警惕花一周时间甚至更久，整理出一个完美细致的学习计划。因为通常只是三分钟热度（个人观点）。

还不如把这份热情用于简单找一本经典书籍或教程直接开学，如果能沉下心来啃完，基本上已经超过绝大部分人了。

# THE END

一直有一个困惑：Java 这门语言是否适合我？（甚至自己是否适合做技术？）   
给自己的答复是：因为目前还没有及格的掌握这门语言，所以有这个困惑。希望有一天可以对这门语言运用自如，并找到相关的热情点～

---

TODO：招聘帖 