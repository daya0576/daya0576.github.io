---
title: 工作七年的你知道如何将字符串转换成数字吗？
tags:
  - java
---

> 今天面试让一个工作7年的候选人写 str to int，写不出来。我快哭了

昨天在 tg 上看到这么一段聊天吐槽🤔，虽然字符串转化逻辑看上去简单，但可以快速考察候选人编码风格与实战能力。尝试自己实现的过程中，刚好发现 java 自带原生实现。这篇文章将简单的分享，阅读对应源码的一些感受 ：）

<!--more-->

### 一、需求说明
需求：输入一个字符串，转换比输出一个整数，e.g. "101" -> 101

### 二、逻辑整理
java 源码参考：`java.lang.Long#parseLong(java.lang.String)`   

![parseLong](/images/blog/2021-09-04-jvm-note/parseLong.svg)


整体逻辑整理如上，虽然并不复杂，但值得注意的是：

#### 1）参数防御检验
方法 `parseLong` 中包含了非常小心的防御校验，例如入参非空判断、字符阿拉伯数字判断、数值越界判断等等，短短约 50 行代码中竟共出现 10 次异常分支！

**为什么需要防御式编程？**   
因为你永远也无法预测用户的行为，例如这个视频🤣🤣：
<iframe src="//player.bilibili.com/player.html?aid=848061318&bvid=BV1dL4y1b74D&cid=409381878&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>

话说刚接触 java 时，对 NPE 十分“恐惧”，如果负责编写的代码发生 NullPointException，虽然无人指责，却也感觉奇耻大辱（这也可能是静态类型过于安全的“副作用”：在以前编写 python 代码时，我们总是以 100% 的但愿测试覆盖率为荣，但用 java 编写一些工具代码时，能通过编译的代码一般不会出错，单元测试的投入产出比不高，反而导致了代码质量的下滑）

**言归正传，所以如何适度进行防御性编程？**    
总不能在每个函数，对参数进行校验吧！？这个问题困扰了我很久...

在《代码大全》第八章中，给出了“标准答案”：

1. **隔离：** 外部数据检查并进入内部类后，类的私有方法就可以假定数据都是安全的，例如任何东西被允许进入手术室前，都需要进行严格的消毒处理，因此手术室内的任何东西都可以被认为是安全的。 ![](/images/blog/2021-09-04-jvm-note/16332362571817.jpg)
2. **健壮性 vs 正确性：** 处理错误的方式要根据应用场景而定，如果你的程序对「正确性」要求极高，例如银行内的大额转账，直接返回错误，比持续的运行下去更加合适。

#### 2）关于越界判断

> Accumulating negatively avoids surprises near MAX_VALUE

阅读源码中，最让我困惑的一个点：为什么累加数字时，`result` 是按负数计算的 ？？？
```java
// java.lang.Long#parseLong(java.lang.String, int)
public static long parseLong(String s, int radix)
          throws NumberFormatException
{
    // ...
    long limit = -Long.MAX_VALUE;
    int digit;

    if (len > 0) {
        // ...
        while (i < len) {
            // Accumulating negatively avoids surprises near MAX_VALUE
            digit = Character.digit(s.charAt(i++),radix);
            if (result < multmin) {
                throw NumberFormatException.forInputString(s);
            }
            result *= radix;
            if (result < limit + digit) {
                throw NumberFormatException.forInputString(s);
            }
            // 按负数进行累加
            result -= digit;
        }
    } else {
        throw NumberFormatException.forInputString(s);
    }
    return negative ? result : -result;
}
```

为了搞清楚这个问题，我们先来看包装类 Long 中的最大值和最小值：
```java
public final class Long extends Number implements Comparable<Long> {
     // -2^63
    @Native public static final long MIN_VALUE = 0x8000000000000000L;

    // 2^63 - 1
    @Native public static final long MAX_VALUE = 0x7fffffffffffffffL;
```

不难发现，因为 0 的存在，**最大值和最小值不是对称的**，abs(最小值) + 1 = 最大值，所以如果用正整数计算，则无法转化 `-2^63`

### 三、关于粗心一些思考

记得读书期间，数学考试总是因为粗心导致不理想的分数，后来看到知乎上的一句话才恍然大悟：“粗心，并不是态度问题，而是能力的缺失”。

写代码也是一样，常常因为粗心导致 npe，逻辑不严谨的漏洞等等，但粗心既然是能力的缺失，只要通过努力，就有办法提升。

例如像做数学题一样，永远不要在细枝末节上偷懒（**不跳步**），反复检查编写用例。

### 四、其他

btw，阅读代码的时候，意外😯发现原来 java 中也能一行定义两个变量 0.0
```java
// java
int i = 0, len = s.length();
// 对应 python 的写法
i, j = 0, 0
i = j = 0
```

### 参考
1. https://stackoverflow.com/questions/40167218/why-does-the-integer-paseint-algorithm-calculate-negative-result-finally-in-su
2. https://leetcode-cn.com/problems/ba-zi-fu-chuan-zhuan-huan-cheng-zheng-shu-lcof/solution/mian-shi-ti-67-ba-zi-fu-chuan-zhuan-huan-cheng-z-4/
3. https://dedao.cn/eBook/lxaVvndNG6D4kgLJ2OKxqVMmE1zXPwVvODwAdjyQeYR75vbaBnr9ol8pZERLg1my
4. ..

