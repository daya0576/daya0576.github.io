---
title: "在 Java & Python 中，如何优雅的筛选一堆苹果\U0001F914"
tags:
  - java
  - python
date: 2020-07-04 19:14:25
---


最近在看《Java 8实战》这本书，第一部分讲了很多函数式编程与 lambda 匿名函数的应用，不禁让我想起了以前写 python 对应的实现。

**需求：** 在一堆苹果中，筛选出重量大于 100g 的苹果🍎，同时也支持过滤所有绿色的苹果 

<!--more-->

# Java 版本

## 方案一：通过行为参数化传递代码

了解过「策略模式」的同学，都知道可以将「行为」作为参数，增加代码的灵活性与可读性。

但看上去有一些累赘哦。。🤔

``` java
public interface ApplePredict {
    boolean test(Apple apple);
}

public class AppleHeavyPredict implements ApplePredict {
    @Override
    public boolean test(Apple apple) {
        return apple.getWeight() > 200;
    }
}

public static List<Apple> filterApples(List<Apple> apples, ApplePredict predict) {
    List<Apple> result = new ArrayList<>();
    for (Apple apple : apples) {
        if (predict.test(apple)) { result.add(apple); }
    }
    return result;
}
	
// 获取苹果
List<Apple> heavyApples = filterApples(apples, new AppleHeavyPredict());
// 为什么不直接写个 for 循环过滤呢？
// 因为这样可以针对颜色等属性，更加灵活的过滤
List<Apple> heavyApples = filterApples(apples, new AppleColorPredict());
```

## 方案二：使用 lambda & Predicate

同时使用内置的 `Predicate` 方法代替 `ApplePredict`，然后利用匿名函数代替 `AppleHeavyPredict`，

``` java
import java.util.function.Predicate;
public static List<Apple> filterApples(List<Apple> apples, Predicate<Apple> predict) {...}

// 获取苹果
List<Apple> lambdaHeavyApples = filterApples(apples, (Apple apple) -> apple.getWeight() > 100);
```

## 方案三：使用 方法引用 

java8 支持方法的引用，分为三种：

1. 静态方法，e.g. Integer::parseInt
2. 类型 - 实例方法，e.g. String::length
3. 实例对象 - 实例方法，e.g. expensiveTransaction::getValue  

所以 lambda 又可以简化为方法引用（当然成本为在 Apple 中新增了一个`isHeavyApple`方法）：
``` java
import java.util.function.Predicate;
public static List<Apple> filterApples(List<Apple> apples, Predicate<Apple> predict) {...}

// 获取苹果
List<Apple> lambdaHeavyApples = filterApples(apples, Apple::isHeavyApple);
List<Apple> lambdaHeavyApples = filterApples(apples, Apple::isGreen);
```

## 方案四：使用 Stream

那么 filterApples 是否也可以被省略呢？利用 java8 中的 Stream 一行代码过滤出你想要的苹果：

``` java
List<Apple> heavyApples = apples.stream()
    .filter(Apple::isHeavyApple)
    .collect(Collectors.toList());
```

# Python 版本

## 方案一：lambda + filter 

虽然语法上略有不同，但大致思路与 java 的实现可以说基本一致！

```python
apples = [Apple("green", 150), Apple("red", 100)]
heavy_apples = list(filter(lambda x: x.weight > 100, apples))
```

同样支持直接将「方法引用」作为参数：

```python
def is_heavy(apple: Apple):
    return apple.weight > 100

apples = [Apple("green", 150), Apple("red", 100)]
heavy_apples = list(filter(is_heavy, apples))
```

## 方案二：列表解析 

但很久以前也不记得在哪本书上看到，不推荐 filter 而统一使用**更为直观**的 list comprehension：

```python
heavy_apples = [apple for apple in apples if apple.weight > 100]
```

# 个人感想
记得大学里学习 java 用的还是 1.6，还没有这么多骚操作。。

虽然现在双放都可以用一行代码实现需求，但个人觉得这轮比拼还是 python 的 list comprehension 更胜一筹🤔 

**因为这种特有的写法更符合人类直觉，你觉得呢？**😄

