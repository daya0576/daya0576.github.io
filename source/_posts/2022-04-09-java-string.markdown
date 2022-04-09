---
title: 关于 Java 字符串的秘密 tags:

- JAVA date: 2022-04-09 14:37:58

---

最近对 java 字符串（`java.lang.String`）的部分行为感到困惑，抽空查阅资料后，直呼原来是这样？！忍不住写一篇博客纪念一下

<!--more-->

## 一、不变性

从源码中不难看出：

- `class` 用 final 修饰：不能被继承 & override
- `value` 变量是 final + private 的：一旦被赋值，无法被更改内存地址（禁止重新赋值），同时外部无法访问内部数组进行修改。

```java
public final class String
        implements java.io.Serializable, Comparable<String>, CharSequence {
    /** The value is used for character storage. */
    private final char value[];
}    
```

## 二、新的困惑

既然 `java.lang.String` 是一个类（对象），为什么通过新的引用赋值后，实际值未发生改变呢？？

```java
// string
String stringFoo="foo";
        String stringBar=stringFoo;
        stringBar+=" bar";
        System.out.printf("[intFoo]：%s%n[intBar]：%s%n%n",stringFoo,stringBar);

// [intFoo]：foo
// [intBar]：foo bar
```

揭开谜团前，先来看看 primary type 与 reference type 的区别：

```java
// int
int intFoo=1;
        int intBar=intFoo;
        intBar++;
// array
        char[]arrayFoo=new char[]{'f','o','o',' ',' ',' '};
        char[]arrayBar=arrayFoo;
        arrayBar[4]='x';
        arrayBar[5]='x';

// 输出
// [intFoo]：1
// [intBar]：2
// [arrayFoo]：[f, o, o,  , x, x]
// [arrayBar]：[f, o, o,  , x, x]
```

不难理解，int 作为[原始型別](https://zh.wikipedia.org/wiki/%25E5%258E%259F%25E5%25A7%258B%25E5%259E%258B%25E5%2588%25A5)，在 stack
frame 中，变量与 value 一一对应，而引用类型（reference type）顾名思义，仅保存堆（Heap）中实例对象的内存地址。

参考去年发布的[博客](/blog/20210904/jvm-note/)：
![](../images/blog/2021-09-04-jvm-note/16494818796482.jpg)

## 三、揭开谜团

[官方教程](https://docs.oracle.com/javase/tutorial/java/data/strings.html) 中提到由于 string 不可变的特性，针对它的任何修改操作会返回一个新的 string 对象：

参考 `java.lang.String#concat` 实现：

```java
public String concat(String str){
        int otherLen=str.length();
        if(otherLen==0){
        return this;
        }
        int len=value.length;
        char buf[]=Arrays.copyOf(value,len+otherLen);
        str.getChars(buf,len);
        return new String(buf,true);
        }
```

但是相比于 concat 方法，String 两两相加（`+`）的操作符，具体发生了什么呢？

编译后我们发现，原来在 java8 中，两两相加会被编译器自动优化为 `StringBuilder` 实现，所以最终返回一个新的 `String` 对象。

```java
// 1. javac Scratch.java 
// 源代码转化为字节码（byte code = 1111_1111），
// 2. javap -v Scratch.class
// The `javap` tool is used to get the information of any class or interface.

public static void main(java.lang.String[]);
        descriptor:([Ljava/lang/String;)V
        flags:ACC_PUBLIC,ACC_STATIC
        Code:
        stack=2,locals=3,args_size=1
        0:ldc           #2          // 常量池获取 "foo"
        2:astore_1                  // 赋值引用：String stringFoo = "foo";

        3:aload_1                   // 加载引用
        4:astore_2                  // 赋值引用： String stringBar = stringFoo; 

        5:new           #3          // sb = new StringBuilder();
        8:dup                       // 返回实例引用
        9:invokespecial #4          // 初始化
        12:aload_2

        13:invokevirtual #5          // sb.app(stringBar)
        16:ldc           #6          // 常量池获取 "bar"
        18:invokevirtual #5          // sb.app("bar")
        21:invokevirtual #7          // sb.toString() 新建 String 对象
        24:astore_2
        25:return
```

### Python 实现对比

有趣发现 Python 中，字符串 string 类型逻辑，与 java 惊人的保持一致：

```python
// 不可变性
>>> a = '123'
>>> a[0] = '1'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
>>> b = a
>>> b += " 123
>>> b
'123 123'
>>> a
'123'

>>> a = '123' * 100000
>>> b = '123' * 100000
>>> a is b
False
>>> a = '123' * 10
>>> b = '123' * 10
>>> a is b
True
```

## 四、总结

基于对 JVM 内存管理，与字节码的探索，终于进一步理解 java 不可变的特性，以及为什么针对它的修改操作会返回一个新的 string 对象。

期望你也有所收获 ：）