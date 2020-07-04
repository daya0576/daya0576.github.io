---
title: java_generic
tags:
---


# 概念问题：
1. Generics 的中文是什么？泛型
2. Generics 中的 GenericContainer**<T>** 是什么含义？**<T>** 代表「类型参数」(type parameter)
3. T 和不同大写符号的含义：
~~T可以随便写为任意标识?常见的如T、E、K、V等形式的参数常用于表示泛型~~  
    * E: Element
    * K: Key
    * N: Number
    * T: Type
    * V: Value
    * S, U, V, and so on: Second, third, and fourth types in a multiparameter situation


# Benefits of Using Generics
总而言之，即是减少类型的强转换，避免程序在运行时报错。

1. type-checking is one of the most important, because it saves time by fending off ClassCastExceptions that might be thrown at runtime.
2. the elimination of casts, which means less code  -

# Bounded Types
<T extends UpperBoundType>
<T super LowerBoundType>

Generic Methods
public static <N extends Number> double add(N a, N b){
    double sum = 0;
    sum = a.doubleValue() + b.doubleValue();
    return sum;
}


# unknown type
public static <T> void checkList(List<?> myList, T obj){}List<? extends Number> myList

