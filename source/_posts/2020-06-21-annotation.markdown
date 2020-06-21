---
title: Annotation(Decorator) 在 Java & Python 中的应用
date: 2020-06-21 15:33:29
tags:
    - java
    - 学习
---


背景：最近在工作中发现我们 SRE 的某个 java 项目中，存在大量 annotation 的应用，虽然 java 的注解与 python 的装饰器语法非常类似，但在原理上肯定千差万别。

为了不甘一直处在一知半解的状态，所以这个周末准备全面学习一下对应语法与原理，并与 python 中的实践做一个对比，以便有一个更加**深入**的理解～

<!--more-->

# Decorator in Python(装饰器)
## 语法
常用的语法大致有两种：`不带参数` & `带参数`

### 1. 不带参数
刚好拿一个最近在写的 telegram 机器人中，接口权限管控的例子：

``` python
def admin(f):
    def wrapper(bot, update):
        # ...
        
        # 用户必须是管理员才可以操作
        if chat_member.status not in (ChatMember.CREATOR, ChatMember.ADMINISTRATOR):
            return

        f(bot, update)

    return wrapper
```

使用装饰器后，实现可插拔地控制 promote 接口只有「管理员」可以调用，达到代码解耦的目的：

```python 
@admin
def promote(bot: Bot, update: Update):
    pass
```

### 2. 带参数

python 中有一个包叫做 `retry`，就是一个很不错的例子: 
https://github.com/invl/retry/blob/master/retry/api.py

```python
def retry(exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1, jitter=0, logger=logging_logger):

    @decorator
    def retry_decorator(f, *fargs, **fkwargs):
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()
        return f(*fargs, **fkwargs) # 实际被装饰函数的调用执行

    return retry_decorator
```

源代码使用了内置的 `@decorator` 方法简化了代码，稍微有一点不太好理解，其实等同于：

```python
def retry(exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1, jitter=0, logger=logging_logger):

    def retry_decorator(f):
        def wrapper(*fargs, **fkwargs):
            args = fargs if fargs else list()
            return f(*fargs, **fkwargs) # 实际被装饰函数的调用执行
        return wrapper
        
    return retry_decorator
```

当被装饰的接口(`make_trouble`)在执行过程中，如果抛出了预期内的 exception(`(ValueError, TypeError)`)，则按提前制定好的策略进行重试：

```python
@retry((ValueError, TypeError), tries=7, delay=1, backoff=2)
def make_trouble():
    '''Retry on ValueError or TypeError, sleep 1, 2, 4, 8, ... seconds between attempts.'''
```

## 原理

看上去有一点复杂，但只要牢记以下 **两者语法的等价关系**，即可理解 Python 装饰器的核心思想了😄：

### 不带参数
```python
@admin
def promote(bot: Bot, update: Update):
    pass
    
# 等价于
admin(promote)(bot, update)
```

### 带参数
```python
@retry((ValueError, TypeError), tries=7, delay=1, backoff=2)
def make_trouble():
    '''Retry on ValueError or TypeError, sleep 1, 2, 4, 8, ... seconds between attempts.'''
    pass    

# 等价于
retry((ValueError, TypeError), tries=7, delay=1, backoff=2, 'example')(make_trouble)()
```


# Annotation in Java(注解)
## 语法
### 注解的定义
注解的定义 与 接口的定义 非常相似（**其实注解就是 `interface` 的一种**）：

```java
// 定义
public @interface ClassPreamble {
    String author();
    String date();
    int currentRevision() default 1;
    String[] reviewers();
}
```

### 注解的使用
使用方式与 python 非常类似，参考下面的例子：
```java
// 使用
@ClassPreamble(
        author = "John Doe",
        date = "3/17/2002",
        currentRevision = 6,
        // Note array notation
        reviewers = {"Alice", "Bob", "Cindy"}
)
public class Generation {}
```

但不同于 python 的是，在 java8 发布后，注解还可以在类/方法/变量的**类型**上配合使用(Type Annotations)，例如：

```java
// 1. 类的实例化
new @Interned MyObject();

// 2. 类型转换（@NonNull 指使编译器如果发现 null 的潜在可能，则抛出一个警告，以避免在运行态的时候抛出 NPE）
myString = (@NonNull String) str;

// 3. implements clause(不知道如何翻译) 
class UnmodifiableList<T> implements
    @Readonly List<@Readonly T> { ... }
        
// 4. 异常抛出的定义
void monitorTemperature() throws
        @Critical TemperatureException { ... }
```

### 内置的注解

java 还实现了一部分内置的注解

例如 `@FunctionalInterface`: 个人理解就是将一个方法的 reference 作为一个变量🤪

注解还可以直接用于其他注解的定义中😯，例如：
- `@Retention` **⚠️划重点**，注意 Retention 是保留的意思
    - SOURCE: 不对编译器可见（只保留在源码中）
    - CLASS: 在编译时发挥作用，但被 JVM 忽略（只在 class 文件保留）
    - RUNTIME: 在 JVM 运行时被保留并使用
- `@Target` 定义了使用对象的限制，例如：
    - ANNOTATION_TYPE: 只能在另一个注解上使用
    - 等等..
- `@Repeatable`: 是否可以重复在一个类上使用。
- `@Inherited`: 是否允许子类继承该注解

例如 `@FunctionalInterface` 的定义：
```java
@Documented
@Retention(value=RUNTIME)
@Target(value=TYPE)
public @interface FunctionalInterface
```

### 可重复的注解

虽然个人觉得没有太多必要，但 java 还是提供了这个选项。看了一眼实现还是挺有意思的，简单描述一下：

```java
// 第一步：定义单个 Schedule 注解
@Repeatable(Schedules.class)
public @interface Schedule {
  String dayOfMonth() default "first";
  String dayOfWeek() default "Mon";
  int hour() default 12;
}

// 第二步：定义包含可以包含多个 Schedule 的注解
public @interface Schedules {
    Schedule[] value();
}

// 第三步：具体的使用
@Schedule(dayOfMonth="last")
@Schedule(dayOfWeek="Fri", hour="23")
public void doPeriodicCleanup() { ... } 
```


## 原理
说实话写到这里，虽然大致知道了注解的用法，似乎对其原理还是毫无头绪。参考了一些文章后的理解：

### 1. 注解的本质
上文提到注解其实就是一个接口，而它的本质：继承了 Annotation 接口的接口：

对 class 文件反编译后：
``` java
// Compiled from "Hello.java"
public interface annotation.Hello extends java.lang.annotation.Annotation {
  public abstract java.lang.String value();
}
```

### 2. 注解的获取
利用了 java 的反射机制，获取一个注解类实例，并拿到对应的 value 属性。

```java
Class cls = Main.class;
Method method = cls.getMethod("main", String[].class);

// 使用反射获取一个注解类实例
Hello hello = method.getAnnotation(Hello.class);
System.out.println(hello.value());

// output: hello
```

### 3. how does it works!!!
但还是不太明白，从定义 annotation 的接口，到获取对应的实例中间，到底发生了什么呢？

查阅了一些文章后，尝试开启 saveGeneratedFiles 为 `"true"` 后，目录里出现了 `proxy.class`，而其中 `$Proxy1.class` 就是我们苦苦寻求的真相。

```
➜  annotation tree
.
├── Hello.class
├── Hello.java
├── Main.class
├── Main.java
└── com
    └── sun
        └── proxy
            ├── $Proxy0.class
            └── $Proxy1.class
```

当我们上文在调用 `getAnnotation` 获取注解实例的时候，**返回的其实是一个 jdk 通过动态代理机制生成的一个代理类 `$Proxy1`**，它实现了我们的注解接口，并将所有方法重写：
![](/images/blog/200104_japan_travel/15927097087465.jpg)

所以调用 `value` 方法的时候，本质上是调用 `AnnotationInvocationHandler#invoke`，通过方法的名称(value)作为 key，去注解的 map 中取出对应的 value:   
![](/images/blog/200104_japan_travel/15927101174836.jpg)

终于真相大白了，默默在心里说了一句：原来是这样～
![](/images/blog/200104_japan_travel/15927103964765.jpg)

p.s. 偶然翻到一个简化版的实现，感兴趣可以看看：https://gist.github.com/nathansgreen/11084652

# 总结
python 装饰器与 java 的注解，虽然使用的语法相似，但同时貌似除了语法就没有其他类似的部分了。。。

从文章的篇幅不难看出，java 的 annotation 和 python 相比「复杂」的许多。但到底是功能强大的好，还是 Simple is better than complex 呢？你的心中有没有一个答案😊 

# 参考
- https://docs.oracle.com/javase/tutorial/java/annotations/basics.html
- https://www.sczyh30.com/posts/Java/java-reflection-1/
- https://juejin.im/post/5b45bd715188251b3a1db54f#heading-3

