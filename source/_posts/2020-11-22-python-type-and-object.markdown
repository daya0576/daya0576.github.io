---
title: 浅谈 Python Metaclass（上）：type 与 object 原理介绍
date: 2020-11-22 14:57:50
tags:
- python
---


我们都知道 python 中有一个特性叫做「万物皆对象」，而个人一直对其中的 type 与 object 对象一知半解。刚好周末看到一篇很不错的文章：[《Python Types and Objects》](https://www.eecg.utoronto.ca/~jzhu/csc326/readings/metaclass-class-instance.pdf)，特此学习记录一下～

<!--more-->

[《浅谈 Python Metaclass（下）：Django ORM 应用与实践》](/blog/20201121/metaclass-with-django-orm/)

# 一、名词定义
## 继承 & 实例：
* **继承**：之类继承于父类，e.g. 蛇继承于爬行动物
通过 `__base__` 属性查看父类
* **实例**：例如小明是一个 instance of human
通过 `__class__` 查看某个 instance 的类型

这两种关系，分别对应 UML 中两种画法：
![](/images/blog/200104_japan_travel/16054349536454.jpg)

## 新式类 & 旧式类
新式类保持 class 与 type 的统一，i.e. Creating a new class creates a new type of object
python3 中默认都是新式类，文本中的例子也都是基于 python3.7


# 二、object 与 type

## 两大元老之间的关系
python 中万物皆对象，可以看到 `object` 与 `type` 为两个内置对象(primary object)：
```python
>>> object
<class 'object'>
>>> type
<class 'type'>
```

`object` 并没有父类(所以它是所有父类的顶端)，但它是由 `type` 实例化未来的：
```python
>>> object.__base__
>>> object.__class__
<class 'type'>
```

不出意外，`type` 的父类是 `object`，同时 `type` 是由它自己实例化而来的（*why？为什么一个对象的实现使它自己？？*）。 
```python
>>> type.__base__
<class 'object'>
>>> type.__class__
<class 'type'>
```

emmm，有点绕，这时候就需要画个图：
![](/images/blog/200104_japan_travel/16054299808003.jpg)


## 内置数据类型
再看下其他内置对象，与 type 还有 object 的关系？

```
>>> list.__class__
<class 'type'>
>>> list.__base__
<class 'object'>
```

list 与 dict 继承于 object，由 type 实例化而来：
![](/images/blog/200104_japan_travel/16054303136575.jpg)

## 自定义对象
再实例化一个 list 和一个自定义类(MyClass)看看。
注意这时候 my_class 与 自定义列表 都是没有父类的：

```python
>>> l.__class__
<class 'list'>
>>> l.__base__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'list' object has no attribute '__base__'


>>> class MyClass:
...     pass
...
>>> my_class = MyClass()
>>> my_class.__base__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'MyClass' object has no attribute '__base__'
```

![](/images/blog/200104_japan_travel/16054322270354.jpg)

这个地方有两个小问题自问自答一下：

1. Q: 「实例化」这个行为，具体代表什么含义呢？它都做了什么？ A: python 内部实例化一个新的对象时，它其实都使用了自身的 type 属性，并创造一个新的实例对象（调用 `__new__` & `__init__` 方法）。   
2. Q: 当 MyClass 在代码中定义时，其实默认继承了 object，但为什么它**自动**变成 type 的实例化对象呢？🤔    A: (见文末总结第二点)

## 元类

基于上面的介绍，我们发现其实可以给所有的对象分为三大类（metaclass / class / instance）：
![](/images/blog/200104_japan_travel/16054350983201.jpg)

而 `type` 其实就是一个内置的 metaclass。这时引出这篇文章的下篇：《浅谈 Python Metaclass（下）：Django ORM 应用与实践》


突如其来的幽默感🤣：
> Q:When should I use a __metaclass__?
> A:Never (as long as you're asking this question anyway :)


# 三、总结

稍微有点绕，还是需要一些时间消化。但个人总觉得需要将继承与实例化区分开后（例如 type 是实例化维度，而 object 是继承时间的产物），再去看待他们之间的关系。

嘿嘿，读原文时，刚好也存在类似的解释：
> There are two kinds of objects in Python:
> 
> - Type objects: can create instances, can be subclassed. 
> - Non-type objects: cannot create instances, cannot be subclassed.

更进一步，「实例化」与「继承」其实都是创建一个新对象的“两种手段”：

1. **继承**：通过 `class` 语法（指定父类或默认 object），来创建一个 type 对象。所以 `class A: pass` 与 `A = type("A", (), {})` 是等同的。
2. **实例化**：使用 `()` 语法，基于某个 type 对象进行对象的新建。返回一个 type 对象或 非 type 对象（metaclass 与 class 的区别）。
3. 其他：存在其他特殊的语法糖，快速创建对象：例如 `l = [1, 2, 3]`


# 参考
- https://www.zhihu.com/question/38791962
- https://www.eecg.utoronto.ca/~jzhu/csc326/readings/metaclass-class-instance.pdf
- https://yifei.me/note/831/
- https://medium.com/@dboyliao/%E6%B7%BA%E8%AB%87-python-metaclass-dfacf24d6dd5

