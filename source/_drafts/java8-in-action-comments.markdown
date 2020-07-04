---
title: 《Java 8 实战》读书笔记 - 函数式编程 
tags:
---

时光飞逝，还记得大二开始接触 java 时，那时主流的是 jdk1.6 与 eclipse 的天下。没想到转眼间 java8 也发布快六年了，其中 Lambda、方法引用、stream 这些新特性，每次看到都云里来雾里去。正好拜读一下《Java 8 实战》这本书一探究竟～

<!--more-->


# 第一部分：基础知识
## 第一章：Why java8

Stream API：灵感源自 linux 命令的管道流(|)  ->  好处：天然的并行(执行的时候分块)

函数式编程：方法引用 -> lambda


## 第二章：通过行为参数化传递代码

了解过「策略设计模式」的同学，都知道将「行为」作为参数，可以增加代码的灵活性与可读性，但代码看上去还是有一丝累赘🤔
``` java
// capture2/predict/ApplePredict.java
public interface ApplePredict {
    boolean test(Apple apple);
}

// capture2/predict/impl/AppleHeavyPredict.java
public class AppleHeavyPredict implements ApplePredict {

    @Override
    public boolean test(Apple apple) {
        return apple.getWeight() > 200;
    }
}

// capture2/Main.java
public class Main {
    public static List<Apple> filterApples(List<Apple> apples, ApplePredict predict) {
        List<Apple> result = new ArrayList<>();
        for (Apple apple : apples) {
            if (predict.test(apple)) {
                result.add(apple);
            }
        }
        return result;
    }

    public static void main(String[] args) {
        List<Apple> apples = Arrays.asList(
                new Apple("red", 10),
                new Apple("green", 10)
        );

        List<Apple> heavyApples = filterApples(apples, new AppleHeavyPredict());
        System.out.println(heavyApples);

        List<Apple> greenApples = filterApples(apples, new AppleColorPredict());
        System.out.println(greenApples);
    }
}
```

使用 lambda 之后，代码肉眼可见的变少：

``` java
// lambda
List<Apple> lambdaGreenApples = filterApples(apples, (Apple apple) -> "green".equals(apple.getColor()));
List<Apple> lambdaHeavyApples = filterApples(apples, (Apple apple) -> apple.getWeight() > 1);
```

进一步将 List 抽象，不止于 Apple，而适用于所有类型的列表：

``` java
public class Main {
    public static <T> List<T> filter(List<T> list, Predict<T> p) {
        List<T> result = new ArrayList<>();

        for (T t : list) {
            if (p.test(t)) {
                result.add(t);
            }
        }

        return result;
    }

    public static void main(String[] args) {
        List<Apple> apples = Arrays.asList(
                new Apple("red", 11),
                new Apple("green", 10)
        );
        // lambda
        List<Apple> lambdaGreenApples = filter(apples, (Apple apple) -> "green".equals(apple.getColor()));
        System.out.println(lambdaGreenApples);
        
        // 将List􏲪􏳋􏲙􏲚化
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        List<Integer> evenNumbers = filter(numbers, i -> i % 2 == 0);
        System.out.println(evenNumbers);
    }
}
```

## 第三章：lambda 表达式 

### 基本语法如下：

```java
(Apple a1, Apple a2) -> a1.getWeight().compareTo(a2.getWeight());
```

主要分为三部分:

- 参数列表：两个 Apple
- 箭头：将「参数列表」与 「Lambda 主体」区分开
- Lambda 主体：比较两个苹果的重量（注意控制流语句需用大括号包围：例如`return "Hello" + i`）

### 使用场景

函数式接口？
原名叫做 functional interface，为只有一个抽象方法的接口。  

java8 还专门给抽象方法 `@FunctionalInterface` 注解，在编译阶段做检查。

举个例子：

```java
// 官方的 Runnable 接口
@FunctionalInterface
public interface Runnable {
    public abstract void run();
}


public static void main(String[] args) {
    Runnable r1 = () -> System.out.println("Hello World");
    r1.run();
}
// 最终输出 Hello World
```

### 3.4 函数式接口

`java.util.function` 中几个函数式的接口：

- Predict(`T->boolean`) -> 输入一个参数，返回 boolean，用于例如列表中元素的筛选
- Compare(`(U,T)->R`) -> 输入两个参数，返回 boolean，用于排序
- Consumer(`T->void`) -> 返回 void，用于例如打印一个列表中的所有元素
和 Runnable的区别？？Runnable 是没有参数的 
- Supplier(`()->T`): 用于实例化多个对象
- Function(`T->R`) -> 返回任意泛型的结果，用于获取一堆苹果对应的重量  

### 方法引用

以下两种写法是等价的：

```java
// lambda
inventory.sort((Apple a1, Apple a2)
-> a1.getWeight().compareTo(a2.getWeight()));

// 引用
inventory.sort(comparing(Apple::getWeight));
```

引用又分为三种：

1. 静态方法，e.g. Integer::parseInt
2. 类型 - 实例方法，e.g. String::length
3. 实例对象 - 实例方法，e.g. expensiveTransaction::getValue  












