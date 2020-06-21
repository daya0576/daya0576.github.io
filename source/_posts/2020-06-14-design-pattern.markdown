---
title: 《Head First 设计模式》学习笔记
tags:
  - 读后感
  - java
date: 2020-06-14 01:05:14
---


> OO 原则是我们的目标，而设计模式是我们的做法。

刚从 python 转 java 半年多，虽然这门语言看上去有一丝笨重和啰嗦，但和设计模式遇上，就好像咖啡与牛奶的融合，变成一杯香醇的拿铁🤔。本文做为个人的读书笔记（~~水一篇博客~~），同时如果能帮到你就更好啦！

<!--more-->

# 分类
大家应该还知道一本书，叫做 [《设计模式：可复用面向对象软件的基础》](https://book.douban.com/subject/1052241/)，其中非常精辟的将设计模式分为三类（持续学习更新中）：

1. 创建型模式：
    - 简单工厂模式（Simple Factory） -> **第四章：工厂模式**
    - 工厂方法模式（Factory Method）
    - 抽象工厂模式（Abstract Factory）
    - 创建者模式（Builder）
    - 原型模式（Prototype）
    - 单例模式（Singleton） -> **第五章：单例**
2. 结构型模式
    - 外观模式/门面模式（Facade门面模式）
    - 适配器模式（Adapter） -> **第七章：适配器模式**
    - 代理模式（Proxy） -> **第十一章：代理模式**
    - 装饰模式（Decorator） -> **第三章：装饰者模式**
    - 桥梁模式/桥接模式（Bridge）
    - 组合模式（Composite）
    - 享元模式（Flyweight）
3. 行为模式
    - 模板方法模式（Template Method） -> **第八章：模版方法模式**
    - 观察者模式（Observer） -> **第二章：观察者模式**
    - 状态模式（State） -> **第十章：状态模式**
    - 策略模式（Strategy）
    - 职责链模式（Chain of Responsibility）
    - 命令模式（Command） -> **第六章：命令模式**
    - 访问者模式（Visitor）
    - 调停者模式（Mediator）
    - 备忘录模式（Memento）
    - 迭代器模式（Iterator） -> **第九章：迭代与组合模式**
    - 解释器模式（Interpreter）

# 章节 
## 第一章：策略模式 - 整合鸭子的行为
将易变的属性，做为一个对象变量去初始化进行**组合（行为也是一种对象！）**

![1. Duck Behaviors](/images/blog/200104_japan_travel/1.%20Duck%20Behaviors.png)


## 第二章：观察者模式 - The Observer Pattern
稍微解释一下：不同的 Display 在实例化时，会在 WeatherData 中被注册为「观察者」统一管理，当「被观察者」（气象数据）发生变化时统一触发通知。   

**目的：**让观察者和被观察者，尽可能的解耦。  

![2. Observer Pattern](/images/blog/200104_japan_travel/2.%20Observer%20Pattern.png)

效果：

```java
WeatherData weatherData = new WeatherData();

CurrentConditionsDisplay currentConditions = new CurrentConditionsDisplay(weatherData);
StatisticsDisplay statisticsDisplay = new StatisticsDisplay(weatherData);
ForecastDisplay forecastDisplay = new ForecastDisplay(weatherData);

weatherData.setMeasurements(80, 65, 30.4f);
// 更新 weatherData 后，会主动通知所有观察者 
// Forecast: Improving weather on the way!
// Avg/Max/Min temperature = 80.0/80.0/80.0
// Current conditions: 80.0F degrees and 65.0% humidity
```

## 第三章：装饰者模式 - The Decorator Pattern
当遇到继承无法解决的问题，可以尝试使用更为优雅的装饰者模式：

![3. The Decorator Pattern: Decorating Objects](/images/blog/200104_japan_travel/3.%20The%20Decorator%20Pattern:%20Decorating%20Objects.png)

最终效果如下，但初始化的方式有点简陋。文中也提到后续 “工厂” & “生成器” 模式，将有更好的方式建立被装饰对象。
``` java
// 来一杯 Espresso
Beverage beverage = new Espresso();
System.out.println(beverage);
// Espresso$1.99

// 来一杯调料为豆浆，摩卡，奶泡的 HouseBlend 咖啡
Beverage beverage1 = new HouseBlend();
beverage1 = new Soy(new Mocha(new Whip(beverage1)));
System.out.println(beverage1);
// HouseBlend, Whip, Mocha, Soy$1.39
```


## 第四章：工厂模式 - The Factory Pattern

再熟悉不过了，就不多做解释了。

> 简单工厂其实不是一个设计模式，反而更像是一种编程习惯。

![4. The Factory Pattern](/images/blog/200104_japan_travel/4.%20The%20Factory%20Pattern.png)

效果：
``` java
SimplePizzaFactory factory = new SimplePizzaFactory();
PizzaStore store = new PizzaStore(factory);

Pizza pizza = store.orderPizza("cheese");
System.out.println("We ordered a " + pizza.getName() + "\n");
System.out.println(pizza);
```

章节中还提到了抽象工厂模式，本质上是两层的 factory，感觉有点太花了。。感兴趣可以阅读原文。

## 第五章：单例 - Singleton
再熟悉不过的老朋友，就不多说了。简单回答两个问题：

Q: 为什么不直接使用全局变量呢？
A: 因为需要在一开始就创建好对象，但实际一直没有用到，造成资源的浪费。有种类似 lazyload 的意思。

Q. 什么需要单例呢？
A: 确保一个类只有一个实例，并提供一个全局访问点。

![5. Singleton](/images/blog/200104_japan_travel/5.%20Singleton.png)

效果：
```java
// 注意有个小细节：Singleton 的构造器是私有的，意味着无法被直接 new 出来（实例只能通过工厂模式创造出来）
Singleton instance = Singleton.getInstance();
```

## 第六章：命令模式 - The Command Pattern:
RemoteLoader 可能有点困惑，其他可以简单将它理解为 `main` 函数，将 Light 和 LightOnCommand 绑定，并将 command 与 remoteControl 绑定：
![](/images/blog/200104_japan_travel/15883270132958.jpg)

效果：
```java
remoteControl.setCommand(0, livingRoomLightOn, livingRoomLightOff);
remoteControl.setCommand(1, kitchenLightOn, kitchenLightOff);
 
remoteControl.onButtonWasPushed(0);
remoteControl.onButtonWasPushed(1);
remoteControl.offButtonWasPushed(1);
```

命令模式的思考在于，允许将动作封装为命令对象，这样一来可以随心所欲的存储、传递和调用它们。

## 第七章：适配器模式 - adapter
Target 理解为鸭子，拥有 fly 与 quack 的接口。  
Adaptee 是火鸡，只有 fly 和 gobble 接口。   
Adaptor 继承了 Target 接口，并根据火鸡的特效实现了对应的鸭子接口。  

最终达到与 client 交互时，可以直接把它当作一只鸭子。   

![7. Adaptor ](/images/blog/200104_japan_travel/7.%20Adaptor%20.png)

三个的区别：
- decorator: 将一个接口转成另外一个接口
- adaptor: 不改变接口，但加入责任
- facade: 让接口更简单（对一个复杂子系统包装，只暴露一个干净的外观）

最终目的：当设计一个系统时，尽可能的降低客户与系统之间的耦合

效果：
``` java
Duck duck = new MallardDuck();

// 让不会汪汪叫的 turkey 也能「适配」实现鸭叫的接口
WildTurkey turkey = new WildTurkey();
Duck turkeyAdaptor = new TurkeyAdapter(turkey);

System.out.println("The duck says...");
duck.quack();
duck.fly();
System.out.println("The TurkeyAdaptor says...");
turkeyAdaptor.quack();
turkeyAdaptor.fly();
```

## 第八章：模版方法模式 - The Template Method Pattern
想起了公司业务代码中的 ServiceTemplate，一个道理。   

**⚠️注意抽象类中 brew 和 addCondiments 方法 是用斜体标示的，需要让子类实现对应细节。**而抽象类统一管理统一的处理流程与子步骤，并暴露给客户代码（减少整个系统的依赖）。

![8. Template](/images/blog/200104_japan_travel/8.%20Template.png)


## 第九章：迭代与组合模式 - The Iterator and Composite Patterns
迭代器模式，针对底层不同的 数组、列表、散列表等，统一为迭代器的对外接口。
![um](/images/blog/200104_japan_travel/uml.png)



## 第十章：状态模式 - The State Pattern

状态机。最近在做一个 telegram 群组管理的机器人，对于用户状态的管理，刚好也可以用到这个设计模式：
       
![](/images/blog/200104_japan_travel/15920333438139.jpg)

效果：
```java
GumballMachine gumballMachine = new GumballMachine(5);
System.out.println(gumballMachine);

gumballMachine.insertQuarter();
gumballMachine.ejectQuarter();
System.out.println(gumballMachine);

gumballMachine.insertQuarter();
gumballMachine.turnCrank();
gumballMachine.insertQuarter();
gumballMachine.turnCrank();
System.out.println(gumballMachine);

// GumballMachine{state=capture10.status_machine.NoQuarterState@6bf256fa, count=5}
// You inserted a quarter!
// Quarter returned
// GumballMachine{state=capture10.status_machine.NoQuarterState@6bf256fa, count=5}
// You inserted a quarter!
// You turned..
// A gumball comes rolling out the slot..
// You inserted a quarter!
// You turned..
// A gumball comes rolling out the slot..
// GumballMachine{state=capture10.status_machine.NoQuarterState@6bf256fa, count=3}
```

## 第十一章：代理模式 - The Proxy Pattern 

没太懂，找了几个 proxy 模式的应用场景：

- 银行账号：通过该账号管理我们的资金。目标为 controls and manage access to the object they are "protecting".
- db 连接的 client，相关配置需要提前被初始化好。
- 但命令一个程序员去写代码的时候，在完成需求 crud 的同时，还要补充文档！

静态 proxy：
![](/images/blog/200104_japan_travel/15920354270766.jpg)

动态 proxy：
- TODO

## 第十二章：模式的模式 - Compound Pattern

相当于将上面讲解过的设计模式复合使用，刚好跟着敲一遍代码，复习一下。   

但像文中说的那样，有种牛刀杀鸡的感觉。。



