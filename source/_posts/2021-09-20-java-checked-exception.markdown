---
title: 天使还是恶魔！浅谈 Java 中的 checked exception 
date: 2021-09-20 16:43:42
tags:
---

记得有一次，觉得处理异常太麻烦，直接 catch 后包装一个 RuntimeException 一路抛了上去。结果被小伙伴 CR 时喷了一顿～

这篇文章将简单介绍 Java 中异常的分类，使用 checked exceptions 的最佳时机，以及为什么无脑抛 RuntimeException 不是一个好习惯。最后分享如何在 lambda 表达式中，更加优雅的处理 checked exceptions。

<!--more-->

# 异常分类
Java 中所有异常都继承自`Throwable`，一般简单将异常分为：
1. **checked exception**: 调用方必须显性处理的异常，否则编译不通过。
2. **unchecked exception**: 编译期间是无法提前检测的异常，又细分为
    1. `RuntimeException`，例如臭名昭著的 NPE
    2. `Error`: JVM 抛出异常，例如 `OutOfMemoryError` 等

![exception_checked_and_unchecked](/images/blog/2021-09-04-jvm-note/exception_checked_and_unchecked.jpg)

# 使用 Checked Exceptions 的最佳时机

参考《Effective Java》中 Item 70: 
> **Use checked exceptions for recoverable conditions and runtime exceptions for programming errors.** By throwing a checked exception, you force the caller to handle the exception in a catch clause or to propagate it outward. 
> Each checked exception that a method is declared to throw is therefore a potent indication to the API user that the associated condition is a possible outcome of invoking the method.

使用 checked exception 简单的指导原则：**异常是否可恢复**，简而言之即调用方是否有能力处理异常，并做出积极的响应，最终从异常中恢复。例如尝试打开一个不存在的文件，异常被调用方捕捉后，提示用户重新输入文件路径，也是一种所谓的 recoverable conditions。

否则如果因为编程错误等，无法恢复的情况，则使用 runtime exceptions 尽早让程序结束掉更为合适。

## 所以为什么不能无脑抛 RuntimeException？

哈哈，偶遇这个提问，如果不是翻译自 StackExchange 真的怀疑是不是我同事的困惑。
![](/images/blog/2021-09-04-jvm-note/16321269380121.jpg)

举个栗子：假如有一段线上告警后置处理的逻辑，其中一段子步骤为日志的抽样检查，但是因为网络等原因，存在小概率日志拉取失败的异常。这时套用「指导原则」需要抛出一个 checked exception，最终由调用方决定执行重试，或直接跳过该“弱依赖”，对异常进行恢复。

这时如果直接包装为 RuntimeException 无脑抛上去，则可能会中断整个告警后置处理的逻辑，甚至导致故障告警发不出来，显然是不合适的。

# 篇外：如何在 stream 中更优雅的处理异常
上文说到，针对 checked exceptions，调用方必须显性的捕捉并处理，但这也是为什么很多程序员对它深恶痛绝。

更加可恨的是，在 Java8 的 stream 中，不支持直接抛出 checked exceptions.. 所以很容易写出丑陋的代码：
```java
import java.util.Arrays;

class Scratch {
    public static void main(String[] args) {
        String[] clazzList = new String[]{"java.util.TreeSet", "2"};
        Arrays.stream(clazzList)
                .map(s -> {
                    try {
                        return Class.forName(s);
                    } catch (ClassNotFoundException e) {
                        throw new RuntimeException(e);
                    }
                })
                .forEach(System.out::println);
    }
}
```

一种解决办法是使用 vavr 包：
```java
import io.vavr.CheckedFunction1;
import io.vavr.control.Try;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;


class Scratch {
    public static void main(String[] args) {
        String[] clazzList = new String[]{"java.util.TreeSet", "2"};
        List<Try<? extends Class<?>>> collect = Arrays.stream(clazzList)
                .map(CheckedFunction1.liftTry(Class::forName))
                .collect(Collectors.toList());

        // 打印异常
        collect.forEach(x -> x.onFailure(System.out::println));
        // 打印正常结果
        collect.forEach(x -> x.onSuccess(System.out::println));
    }
}
```

# THE END
查看资料的过程中，发现大家对 Java 中的 checked exceptions 是天使还是恶魔的争论十分激烈。

但个人觉得 checked exceptions 还是利大于弊的，合理使用会有效提升接口和程序整体的健壮性。

# 参考：
1. https://web.archive.org/web/20171216175508/www.yinwang.org/blog-cn/2017/05/23/kotlin
2. 《Effective Java》Item 70 & Item 71
3. https://softwareengineering.stackexchange.com/questions/121328/is-it-good-practice-to-catch-a-checked-exception-and-throw-a-runtimeexception/121385#121385
4. https://github.com/kun-song/my-blog/issues/36