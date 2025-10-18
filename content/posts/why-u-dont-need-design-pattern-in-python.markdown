---
title: Python 不需要设计模式？
date: 2020-11-14 21:29:24
categories:
- PYTHON
- 编程
---


前两个月拜读 [《Head First 设计模式》](/blog/20200613/design-pattern/)这本书，同时系统性的重温 [UML 相关的知识](/blog/20200613/design-pattern/)，但当笔者尝试将学到的知识复用到 python 时，突然发现似乎并不是那么的适配：例如 python 中并没有「接口」与「抽象类」等的概念🤔   

观看一个 Pycon2017 的分享视频之后：[《Why you don't need design patterns in Python?》](https://www.youtube.com/watch?v=G5OeYHCJuv0)，对上面的疑惑，逐步有了一些自己的理解。首先还是先分享几个经典设计模式在 python 的具体实践。

<!--more-->

## 经典模式在 python 中的实践
### 1. Singleton 单例

使用 Python 直接套用 Java 中的经典写法：

```python
class Logger(object):
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance
```

更优雅的实践(`__new__`)：

```python
class Logger(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
```

当然也可以`@classmethod`，但视频中提到一个更好的做法（类似 spring 中的 IOC..），即 python 中原生的 `import` 就是一个 singleton 的天然实现（并且更加直观）：

```python
class Logger(object):
    pass
    
logger = Logger()

# another module
from my_code import logger 
```

### 2. FACADE 

一个分布式的微服务系统中，每个模块或应用之间，通常只会提供特定的服务与接口（interface）供上游调用，以保持应用间的耦合度，同时屏蔽各自内部复杂的实现。

而上文提到 python 中提供了 `__init__.py` 文件，天然的支持这个模式。

后来才慢慢明白，为什么以前一些同事，喜欢将模块中对外暴露的接口或实例，统一放置在 `__init__` 文件中管理，而不是「模块一」可以 任意的引用「模块二」中的任意类，这样会大大增加系统的复杂度与维护成本（**但 python 如何在系统层面，防止引入这种坏代码的味道呢？**）。

### 3. COMMAND

《Head First 设计模式》 中 java 的实现：
![](/images/blog/200104_japan_travel/15883270132958.jpg)

完整代码参考 [github](https://github.com/bethrobson/Head-First-Design-Patterns/blob/master/src/headfirst/designpatterns/command/remote/LightOnCommand.java)

效果：
```java
remoteControl.setCommand(0, livingRoomLightOn, livingRoomLightOff);
remoteControl.setCommand(1, kitchenLightOn, kitchenLightOff);
 
remoteControl.onButtonWasPushed(0);
remoteControl.onButtonWasPushed(1);
remoteControl.offButtonWasPushed(1);
```

命令模式的好处在于，允许将动作封装为命令对象，这样一来可以随心所欲并且独立的存储、传递和调用它们。

python 中万物皆对象，所以可以直接将方法（而不是类）作为参数进行传递与赋值。当然标准类也原生提供了附带参数的语法糖（**但此处如何约束不同接口的统一行为呢？比如所有的动作只接受 on/off 两个输入**）：

```python
import functools

def notify_user_with_discount(discount):
    pass

command = functools.partial(
    notify_user_with_discount, discount=0.5
)

command()
# equals to 
notify_user_with_discount(discount=0.5)
```

### 4. VISITOR 

个人理解这个模式的核心思想在于 java 中 [重载(function overloading)](https://zh.wikipedia.org/wiki/%E5%87%BD%E6%95%B0%E9%87%8D%E8%BD%BD)，即一个类中支持同时共存多个同名的函数，如果入参数量或者类型不同，对应的行为也不一样。 

而在 python 中，可以使用参数类型的字符，来获取对应不同的方法。p.s. 但个人非常不喜欢这种做法，感觉很这样的代码太“脆弱”了。。

```python
class ASTVisitor:
    def _visit_str(self):
        print("I'm a string!!")

    def _visit_int(self):
        print("I'm a int!!")

    def visit(self, node):
        normalized_type_name = type(node).__name__.lower()
        target_method_name = "_visit_" + normalized_type_name

        method = getattr(self, target_method_name)
        method()

if __name__ == '__main__':
    ast_visitor = ASTVisitor()
    ast_visitor.visit("foo")
    # I'm a string!!
    ast_visitor.visit(123)
    # I'm a int!!
```

标准库提供`@singledispath`这个注解，来实现这个模式(但有唯一一个缺陷在于目前不能用于类内的方法)：

```python
# 1. func
from functools import singledispatch

@singledispatch
def func(node):
    type_name = type(node).__name__
    raise AttributeError(f"No handler found for this {type_name}")

@func.register
def _(node: int):
    print("i'm a int")

@func.register
def _(node: str):
    print("i'm a string")
    
    
if __name__ == '__main__':
    func("foo")
    # i'm a string    
    func(123)
    # i'm a int 
```

### 5. FACTORY 

python 中的方法可以返回任何类型的实例，所以也自然没有工厂模式??😂 

That's all， 上一小节笔者举了几个「设计模式」在 python 中的具体应用，给大家一个体感。如果你想了解更多，可以收藏这个 [页面](https://python-patterns.guide)，以查看更多信息。

## 总结

我看过也写过太多糟糕的 python 代码，例如超过几百行密密麻麻的方法。当接触 java 与设计模式后，发现有很多特定的套路，可以将代码逻辑持续解耦。虽然牺牲了一定语法上的简洁性，但可读性与可维护性确实大大增加。

从文中举的几个例子可以看出，设计模式只是**提高代码复用性，可读性**的一个手段，应该结合语言特性去最简洁的实现这个「目的」。反而言之，如果设计模式只是为用而用，反而只会画蛇添足。  

> Python 里没有接口，如何写设计模式？

Python 是一门动态语言，它的方法接受任何参数，当不符合预期时，去处理对应的 exception 即可🤔

> Patterns are signs of weakness in programming languages.

这个观点我也不太认同，接触 java 后还是学到了很多，例如利于多人协同维护大型项目的最佳实践。每个语言都有自己的优势与劣势，还是可以相互借鉴的，例如蚂蚁 SOFA 工程的分层🆒：
![](/images/blog/200104_japan_travel/16053236164113.jpg)


## 其他资料：

- 知乎讨论：https://www.zhihu.com/question/31979217
- python 模式集合：https://github.com/faif/python-patterns
- [《Architecture Patterns with Python》](https://github.com/cosmicpython/book)（没看过不做评价）
- 《Python Design Patterns 1》：https://www.youtube.com/watch?v=Er5K_nR5lDQ


