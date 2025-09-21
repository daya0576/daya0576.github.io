---
title: "[Python] 如何在 Python 中合理的使用继承"
date: 2023-01-22 10:32:24
---

最近两年由于工作需要接触 Java，也遇到很多将继承抽象用的出神入化的小伙伴。而自己却总是东施效颦，写出的代码杂乱无章。特别面向新增的需求改动，在扩展等方面差强人意。

逐步的，大脑中也慢慢浮现出一丝模模糊糊的经验。尝试将这些浅薄的想法，整理为这篇文章供自己不断积累进化。

<!--more-->

# 继承的优缺点

继承最大的好处在于变量与方法的代码共享，这种强大的便利，也很容易造成“反噬”。

想象下面这个例子：公司同时生产汽车 Car 和卡车 Truck，车辆可能是电动车 Electric 或 汽油车 Combustion; 所有车型都配备了手动控制 Manual control 或 自动驾驶 Autopilot 功能：
![](/images/blog/2021-09-04-jvm-note/16724872128989.jpg)

如上多层继承关系耦合错综复杂，给后续代码的改动与阅读造成了极大困扰：
1. 若属性 A 被多个子类复写后，很难一步找到真实的归属，只能通过 debug 小心翼翼修改代码；
2. 同时每个方法都归属于 self，一次调用在各个子类父类之间旋转跳跃，更不用说多重继承的 MRO，让人晕头转向。

雪上加霜的是，软件系统是长出来的。不断膨胀并妥协加入的子类，会导致代码复杂度指数增高，最终超出人类理解和控制的范围。

# 何时使用继承

但是，继承是否一无是处？答案肯定是否定的，因为上面几个问题，更多是人为不合理操作引入。

继承适用于 稳定且具备严格的层次结构：
```python
电子邮箱账户 - 数据库中的 ID 和邮箱地址  
  - 电子邮箱：pwd 密码作为登录信息（必选）  
  - 转发邮箱：targets 转发目标地址  

# 组合
class EmailAddr:
    id: UUID
    addr: str

class Mailbox:
    email: EmailAddr
    pwd: str

class Forwarder:
    email: EmailAddr
    targets: list[str]

# 基类继承
class EmailAddr:
    id: UUID
    addr: str

class Mailbox(EmailAddr):
    pwd: str

class Forwarder(EmailAddr):
    targets: list[str]
```

回到开头公司汽车的案例，单纯追求代码复用的**多层继承**，则使用组合更为合理（继承多个 mixin 也是一种特殊的组合，但不推荐）。
![](/images/blog/2021-09-04-jvm-note/16724888878107.jpg)

面对 subclass explosion，更多解决思路：[《The Composition Over Inheritance Principle》](https://python-patterns.guide/gang-of-four/composition-over-inheritance/)

# THE END
继承是把双刃剑，强大却也具备极强的破坏力。秉承着打不过就逃跑的策略，日常还是优先考虑组合来替代。

# 参考
1. https://hynek.me/articles/python-subclassing-redux/
2. https://python-patterns.guide/gang-of-four/composition-over-inheritance/
3. https://refactoring.guru/design-patterns/bridge