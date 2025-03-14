---
title: Java JVM 内存管理 - SRE 的必修课 
date: 2021-09-04 16:31:21 
categories:
- SRE
---

在过去三年 SRE 的经历中，遇到过多起因为 JVM OOM 导致的线上故障。其中印象最深的一次排查经历：收到故障外呼后，几个大男人现场梳理业务链路，大眼瞪小眼，最后发现根因竟然是部分网关机器动态加载数据库中的 groovy
脚本，导致 `Metaspace out of memory` 报错，影响了部分 XX 商户的代扣业务，最终落了一个 P4 故障 T…T

但是之后很长一段时间内，都不太明白 Metaspace 是什么，为什么会耗尽？和 perm 区的关系是？不同线程本地变量和全局对象的关系？

正好趁这次机会，系统性的整理和分享一下 ：）

- [一、走近 Java](#一、走近java)
- [二、自动内存管理](#二、自动内存管理)
    - [Java 内存区域](#java内存区域)
    - [关键点说明](#关键点说明)
        - [1. 关于 Perm 区 & Metaspace](#1关于-perm区-metaspace)
        - [2. 关于栈帧（Stack Frame）](#2关于栈帧（-stack-frame）)
        - [3. 关于运行时常量池（Run-Time Constant Pool）](#3关于运行时常量池（-run-time-constant-pool）)
- [三、垃圾收集器与内存分配策略](#三、垃圾收集器与内存分配策略)
- [The End](#the-end)
- [参考](#参考)

<!--more-->

## 一、走近 Java

首先预热一下，简单解释几个常见名词：`JVM` -> `JRE` -> `JDK`

- `JVM（Java Virtual Machine）`：Java虚拟机，它实现了一次编译到处运行，例如 HotSpot 等
- `JRE（Java Runtime Environment）`，JRE是支持Java程序运行的标准环境。包含 Java SE API 子集 / 虚拟机
- `JDK（Java Development Kit）`：Java程序开发的最小环境。包含 程序语言 / 虚拟机 / 基础类库等，例如 OpenJDK 等

书中有一段总结挺有意思的，分享一下：*“Oracle收购Sun是Java发展历史上一道明显的分界线。在Sun掌舵的前十几年里，Java获得巨大成功，同时也渐渐显露出来语言演进的缓慢与社区决策的老朽；而在Oracle主导Java后，引起竞争的同时也带来新的活力，Java发展的速度要显著高于Sun时代。Java的未来是继续向前、再攀高峰，还是由盛转衰、锋芒挫缩，你我拭目以待”*


## 二、自动内存管理
进入正文！🎉🎉🎉 

### Java 内存区域
网上很多文章因为 java 版本的问题，存在不同程度的过时。

所以花了一点时间，尝试通过「栈」和「堆」两个视角，将 java8 的内存分布重新绘制一遍加深理解：
![](/images/blog/2021-09-04-jvm-note/16307787626886.jpg)
（p.s. 如果有不对的地方辛苦帮忙指正）

 
### 关键点说明
#### 1. 关于 Perm 区 & Metaspace
为了解决 持久代内存溢出 & 不同虚拟机融合等目的，持久代（PermGen）在 1.8 以后被 Metaspace 取代。

我个人理解最大不同在于：1.8 之前，持久代与 Heap & Stack 都归属**虚拟机内存**，而 Metaspace 侧使用的**本地内存**（native memory），**默认不做限制**。

**既然没有限制，文章开头故障为什么还会发生呢？？**   
因为通常还是习惯设置 `-XX:MaxMetaspaceSize` 参数。。所以如果代码编写不当，类占据的空间还是很可能超过指定的空间大小，造成`java.lang.OutOfMemoryError: Metaspace` 异常 :(

#### 2. 关于栈帧（Stack Frame）
程序运行本质上是方法的套娃调用，也就是不断入栈与出栈的过程。

而每个栈帧（Stack Frame）中，本地变量（Local Variables）与 Heap 的关系如下：
![](/images/blog/2021-09-04-jvm-note/16307786911033.jpg)

#### 3. 关于运行时常量池（Run-Time Constant Pool）
##### 1）首先理解 class 文件的常量池（Constant Pool）& 符号应用
参考下面的例子，通过 `javac`  + `javap`查看编译后的 `.class` 文件：
```java
public class Scratch {
    int num = 10;
    public void methodA(){
        System.out.println("methodA()....");
    }
    public void methodB(){
        System.out.println("methodB()....");
        methodA();
        num++;
    }
}

// 1. javac Scratch.java 
// 源代码转化为字节码（byte code = 1111_1111），
// 2. javap -v Scratch.class
// The `javap` tool is used to get the information of any class or interface.
➜  test git:(master) ✗ javap -v Scratch      
Warning: Binary file Scratch contains test.Scratch
Classfile /Users/henry/IdeaProjects/Head-First-Design-Patterns/src/test/Scratch.class
  Last modified Aug 15, 2021; size 554 bytes
  MD5 checksum 1dac5a22a5ccc66bfd64ee3185a1587e
  Compiled from "Scratch.java"
public class test.Scratch
  minor version: 0
  major version: 52
  flags: ACC_PUBLIC, ACC_SUPER
Constant pool:
   #1 = Methodref          #9.#20         // java/lang/Object."<init>":()V
   #2 = Fieldref           #8.#21         // test/Scratch.num:I
   #3 = Fieldref           #22.#23        // java/lang/System.out:Ljava/io/PrintStream;
   #4 = String             #24            // methodA()....
   #5 = Methodref          #25.#26        // java/io/PrintStream.println:(Ljava/lang/String;)V
   #6 = String             #27            // methodB()....
   #7 = Methodref          #8.#28         // test/Scratch.methodA:()V
   #8 = Class              #29            // test/Scratch
   #9 = Class              #30            // java/lang/Object
  #10 = Utf8               num
  #11 = Utf8               I
  ...
```

可以看到 class 文件包含一段 `Constant pool` 区域，用于存放编译期生成的各种字面量（ Literal ）和 符号引用（Symbolic References）。不难理解，在编译阶段，并不知道所引用类/方法的地址（实际地址），所以将**符号引用**保存至变量池（Constant pool）

1. 其中第一列 `#1`，`#2` 等等代表**符号引用**（symbolic references）
2. methodB 调用 methodA 对应的指令是 `9: invokevirtual #36 // Method methodA:()V`

##### 2）所以 Run-Time Constant Pool 是什么？
先来回顾 jvm 加载一个类时，会经历 **加载 -> 连接(验证|准备|解析) -> 初始化** 三个阶段。

首先在第一步 **加载阶段**：虚拟机加载 Class 文件后，会在内存方法区中生成这个类的 java.lang.Class 对象，供外部访问。同时将上文常量池中的符号引用（字段/方法/类的引用）转移至 Run-Time Constant Pool 中。

然后将对应的「符号引用」转化为「直接引用」（实际运行时内存布局中的入口地址），这个过程叫做“方法调用”，而它又分为以下两种：
1. **解析调用**：在**连接**最后一步的**解析**阶段，完成直接引用的转化。
   例如静态方法、私有方法、实例构造器、父类方法，以及被 final 修饰的实例方法，在程序真正运行之前就有一个可确定的调用版本，并且这个方法的调用版本在运行期是不可改变的，所以在类加载时就能完成直接引用的转化。
2. **分派调用**（Dispatch）：每一次运行期间确认直接引用 
   1. 静态分派：重载（Oveload）- 根据静态类型决定重载的版本
   2. 动态分派：重写（Override）- 根据对象的实际类型，选择重写的方法 

##### 3）总而言之
运行时常量池（Run-Time Constant Pool）保存的是 class 文件常量池构建的符号引用，同时包含翻译后真实内存地址的直接引用。

p.s. 我们常说的 **动态连接**（Dynamic Linking）：指的是在开头内存分布大图中，栈帧 （Stack Frame） 存在一个指向 Run-Time Constant Pool 的连接

## 三、垃圾收集器与内存分配策略

1. 对象是否存活？
  - 引用计数算法：引用为0的对象可以被当作垃圾收集（循环引用 & 线程安全等问题）
  - 可达性分析法：从 gc roots 开始，引用关系遍历对象图，能被遍历到的对象就判定为存活的，其余的对象判定为死亡。
    gc roots 是什么？
    例如全局引用（例如静态变量）& 执行的上下文（栈帧中的本地变量）
2. 分代收集理论：
  - 对象初始化 -> **Eden**
  - Eden 空间不足 -> **Minor GC(YGC)** - 标记+复制
    - Young Generation = eden(80%) + S0(10%) + S1(10%)
    - 新生代垃圾回收步骤：
      1. `Eden` -> `S0` 
      2. `Eden` -> `S1`，`S0`->`S1`（交互触发年龄+1）
      3. `Eden` -> `S0`，`S1`->`S0`（同上年龄+1）
      4. 若对象未回收 && 年龄超过阈值：`S0&S1` -> (老年代)
  - 老年代空间不足 -> **Major GC** - 标记+整理
    - （避免碎片的情况）
  - heap 满了 -> **Full GC** - metaspace & 整个heap 进行回收

关于垃圾回收相关的知识网上遍布都是，就简单 copy 了一下自己的读书笔记，暂时不展开班门弄斧了。

## The End
java 小白历险记，文中如有错误请多包涵，欢迎指正交流。
![3FB01AAE-67BF-4755-B6ED-0A301FFB3B36_1_105_c](/images/blog/2021-09-04-jvm-note/3FB01AAE-67BF-4755-B6ED-0A301FFB3B36_1_105_c.jpeg)


## 参考

1. [《深入理解 JVM 虚拟机》](https://www.dedao.cn/eBook/qPKdG1m9B8MaveyJdxRzNnKYlqgVZ3k4Jlwo5pL7E4m1r26kQjXDAPObGkYgJ4pN)
2. [《解析与分派》](https://www.yuque.com/wanghuaihoho/aw880k/zsgm3i)
3. [JEP 122: Remove the Permanent Generation](http://openjdk.java.net/jeps/122)
4. ...


