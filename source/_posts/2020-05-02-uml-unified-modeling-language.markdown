---
title: 解决关于 UML 类图在心中深藏多年的若干疑惑
tags:
  - 学习
  - 学习笔记
  - uml
date: 2020-05-02 01:47:11
---


> UML (Unified Modeling Language) is a graphical language for modeling the structure and behavior of object-oriented systems.

最近在学习经典的设计模式，竟然被类图(UML Class Diagram)深深的吸引了。总之个人一直以来，对各种「可视化」都是情有独钟（可能是老年人记忆力比较差，而图像可以在脑中快读投影与记忆）。当然正好也趁这个机会，对 uml 类图有个全面更深的理解，顺便消除之前的好几个困惑。

想起以前看过的一篇文章，说的是两种写代码的风格：有的人喜欢提前规划，将每个细节思考清晰后再动手，而另一类人则像我高中语文考试写作文，信手拈来，写到哪算哪。个人还是期望做第一类，因为代码说到底只是一种将想法落地的方式，特别是当代码复杂度远远超过我大脑内存时，一份完整详尽的系分设计文档就格外重要（包含类图/sequence/用例等），为后续理解和重构代码都有很大的好处，不然 `code and fix` 浪费的时间将是指数级翻倍的。当然网上也有很多反对的声音，例如 uml 无用论等🤔 你是怎么觉得的呢？或者可以等读完这篇文章后再发布你的想法。

<!--more-->

# 正文
分为三个部分，分别为 类的表示 / 继承 / 关联

## 类的表示
不难理解三个方格分别代表：

- 类名
- 属性
- 方法

![](../images/blog/200104_japan_travel/15883547566041.jpg)

P.S. 其中前缀分别代表：

* Public (+)
* Private (-)
* Protected (#)
* Package (~)
* Derived (/)
* Static (underlined)

## 继承关系
网上针对以下两种的叫法五花八门，但如果直接叫 `extend` 与 `implement` 就比较好理解了：
![](../images/blog/200104_japan_travel/15883538437292.jpg)

## 关联关系
![16178121126738](../images/blog/2021-09-04-jvm-note/16178121126738.jpg)



**Q: composition & aggregation & association 的区别？？**
A: 本质上是一个包含的关系：Association > Aggregation > Composition

- **dependency(依赖)**: 「教授(A)」依赖于「课程资料(B)」 如果「课程资料」的属性或方法被修改，会导致「教授」代码实现崩溃（不一定是类成员变量）
- **associate(关联)**: 「教授(A)」对「学生(B)」进行授课指导 A 知道 B。类 A 依赖于类 B（**与上面「依赖」的区别：接口参数级别的依赖，而不仅仅是代码引用**）。
- **aggregate(聚合)**: 「院系(A)」包含「教授(B)」 A 知道 B、 由 B 构成。类 A 依赖于类 B。
- **component(组合)**: 「大学(A)」由「院系(B)」组成 A 知道 B、由 B 构成而且管理着 B 的生命周期。类 A 依赖于类 B。 
p.s. 组合与其他关系的区别在于组件仅能作为容器的一部分存在。

---

笑了，文中的一句话：
> If you have difficulty distinguishing among association, aggregation and composition relationships, don't worry! So does everybody else!

# 个人的一点思考
不必过于纠结于细节和严格的标准，只要能方便理解即可，怎么舒服怎么来。不然反而与最早的愿景背道而驰了。 

# 参考：
- https://www.visual-paradigm.com/guide/uml-unified-modeling-language/uml-class-diagram-tutorial/
- http://www.cs.utsa.edu/~cs3443/uml/uml.html
- http://umlgreatchina.org/_templates/main.aspx?sname=faq&section=q1


