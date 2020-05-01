---
title: 《Head First 设计模式》学习笔记
tags:
  - 读后感
---

> OO 原则是我们的目标，而设计模式是我们的做法。

刚转 java 半年，虽然这门语言看上去有一丝笨重和啰嗦，但和设计模式遇上，就好像咖啡与牛奶的融合，变成一杯香醇的拿铁🤔。本文做为个人的读书笔记（~~水一篇博客~~），同时如果能帮到你就更好啦！

<!--more-->

# 章节 
## 第一章：策略模式 - 整合鸭子的行为
将易变的属性，做为一个对象变量去初始化**组合**（行为也是一种对象）
![1. Duck Behaviors](/images/blog/200104_japan_travel/1.%20Duck%20Behaviors.png)


## 第二章：观察者模式 - The Decorator Pattern
稍微解释一下，不同的 Display 在实例的时候注册在 WeatherData 中作为「观察者」统一管理，当被观察者（气象数据）发生变化时，进行统一通知。目的：让观察者和被观察者，尽可能的解耦。  
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

## 第三章：组合 - The Decorator Pattern
当遇到继承无法解决的问题，使用组合之后：
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
A: 因为需要在一开始就创建好对象，但实际一直没有用到，造成资源的浪费

Q. 什么需要单例呢？
A: 确保一个类只有一个实例，并提供一个全局访问点。

![5. Singleton](/images/blog/200104_japan_travel/5.%20Singleton.png)

效果：
```java
// 有个小细节：Singleton 的构造器是私有的，意味着无法被直接 new 出来（实例只能通过工厂模式创造出来）
Singleton instance = Singleton.getInstance();
```

## 第六章：命令模式 - The Command Pattern:
RemoteLoader 可能有点困惑，其他它就是 `main` 函数，将 Light 和 LightOnCommand 绑定，并将 command 与 remoteControl 绑定：
![](/images/blog/200104_japan_travel/15883270132958.jpg)

效果：
```java
remoteControl.setCommand(0, livingRoomLightOn, livingRoomLightOff);
remoteControl.setCommand(1, kitchenLightOn, kitchenLightOff);
 
remoteControl.onButtonWasPushed(0);
remoteControl.onButtonWasPushed(1);
remoteControl.offButtonWasPushed(1);
```

不太对这个模式感冒，但值得一题的是 log4j 日志貌似也是用的这个设计模式：


# 其他

