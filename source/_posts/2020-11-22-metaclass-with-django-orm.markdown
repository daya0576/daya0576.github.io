---
title: 浅谈 Python Metaclass（下）：Django ORM 的应用
date: 2020-11-22 14:58:16
tags:
---


用了这么多年 django，原来其中强大的 ORM 即 metaclass 的一种最佳实践，让我们一探其中的奥秘吧✨

p.s. 文本默认你对 Django 的 ORM 已有一定的概念了解与实践～

[《浅谈 Python Metaclass（上）：type 与 object 原理介绍》](/blog/20201115/python-type-and-object/)

<!--more-->

# 继承关系

在 Django ORM 中，编写三行代码构建 model 类 -> 就可以通过 `migrate` 让框架帮你创建对应的数据库表（甚至包含索引等所有属性）。同时还可以根据它快速做一系列的**增删改查**操作：  

```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
```

翻下 Django 的源码不难看出，上面定义的 `Student` 类继承了 `models.Model`，而它又继承于 `ModelBase`（**是一个由 type 继承而来 metaclass!**）  
![](/images/blog/200104_japan_travel/16059273576073.jpg)

参考：[django/blob/master/django/db/models/base.py#L72](https://github.com/django/django/blob/master/django/db/models/base.py#L72)
```python
class ModelBase(type):
    """Metaclass for all models."""
    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super().__new__

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        # ...
```

# 类的初始化

如果阅读了上篇，不难理解普通类在定义时，默认使用 `type` 作为生成类的 metaclass。而 ORM 类继承于 `ModelBase`，并利用它进行类的初始化：

```python
# 1. 普通类（继承于 object）
class Student: pass
Student() <-> type("Student", (), {})()
# 2. ORM 类（继承于 ModelBase）
class Student(models.Model): pass
Student() <-> ModelBase("Student", (), {})()
```

## 后者执行顺序：

1. `ModelBase.__prepare__`: 此方法只在 metaclas 中有效，用于**初始化**命名空间(namespace)，供后续保存类中所有属性，e.g. 类中的方法。并支持“注入”额外的属性，最后供下一步的 `__new__` 方法使用（但 django 中并未重写，默认返回一个空字典）
2. `ModelBase.__new__`: 以 ModelBase(cls) 和 待创建的类名称作为参数，创建并返回一个类(class)
3. `ModelBase.__init__`: 对创建的类，做一些初始化操作
4. `ModelBase.__call__`: 当上一步返回的类被调用时**`()`**触发(类似方法调用)，这时也会触发 `Student` 与 `Model`的 `init` 方法。
    1. `Student.__init__`
        1. `Model.__init__`
   

## Django 特性

Django 主要对 `django.db.models.base.ModelBase.__new__` 方法做了大量定制化操作

**分为两个部分**：

1. 前置初始化操作：
  - Student 的父类（`models.Model`）被实例化
  - 获取所有定义的字段，例如 `{'name': <django.db.models.fields.CharField>}`
  - 获取 Meta 中的属性：例如 `abstract`，`verbose_name` 等
2. 创建新类并返回：
    - 在创建之前还做了一系列验证操作，例如一个 app 内不能有相同名字的 model 等等

如下图所示，熟悉的 objects(`<class 'django.db.models.manager.Manager'>`)，也会在第二步被动态生成：
![](/images/blog/200104_japan_travel/16060245107097.jpg)

而所有定义的表字段(fields)被存储在 `new_class._meta.fields` 之中，在写入的过程中也会动态生成 `get_{field}_display` 方法😃：
![](/images/blog/200104_japan_travel/16060241730731.jpg)

    
# 总结

Django ORM 利用 Python metaclass 的强大特性动态的去创建类，改变了类初始化时的行为。将复杂留给了自己，大大降低了用户的学习和使用成本。  

# 参考：

1. [《How Django Uses Metaclasses For Data Modelling》](https://medium.com/swlh/how-django-use-data-descriptors-metaclasses-for-data-modelling-14b307280fce)
2. [PEP 3115 -- Metaclasses in Python 3000](https://www.python.org/dev/peps/pep-3115/#invoking-the-metaclass)


