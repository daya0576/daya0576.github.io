---
title: Java BlockingQueue 学习小记
tags:
  - java
date: 2022-02-03 12:50:34
---

最近一周作息发生了一些微妙的变化，晚上 11 点睡觉清晨 7 点自然醒，身体状况明显好转的同时，也明白了什么叫做一天之际在于晨：起床后去门口吃麦当劳早餐的同时，看一会书，感觉一天多活了一个多小时。

这篇文章简单记录今早 java BlockingQueue 学习小记～

<!--more-->

# 目录

- [前言](#前言)
- [接口定义](#接口定义)
- [接口实现](#接口实现)
  - [1. LinkedBlockingQueue](#1-linkedblockingqueue)
    - [1.1 数据结构](#1-1数据结构)
    - [1.2 新增操作](#1-2新增操作)
    - [1.3 获取并删除](#1-3获取并删除)
  - [2 ArrayBlockingQueue](#2-arrayblockingqueue)
    - [2.1 数据结构](#2-1数据结构)
    - [2.2 获取元素](#2-2获取元素)
  - [3. SynchronousQueue](#3-synchronousqueue)
  - [4 DelayQueue](#4-delayqueue)
    - [4.1 定义延迟执行任务：](#4-1定义延迟执行任务：)
    - [4.2 执行任务](#4-2执行任务)
- [总结](#总结)
- [参考](#参考)

# 前言
> java.util.concurrent.BlockingQueue
> 
> A Queue that additionally supports operations that wait for the queue to become non-empty when retrieving an element, and wait for space to become available in the queue when storing an element.

参考官方注释，`BlockingQueue` 是 `java.util.concurrent` 中的一个接口。顾名思义：**Queue** 表示先进先出的队列，多个线程同时放入对象而其他线程获取对象（解耦输入与输出），**Blocking** 代表当队列满了或者为空时，尝试放入或获取元素的线程会进入阻塞状态。

## 举个例子
有点抽象，举个例子：当队列为空时，获取元素 
```java
ArrayBlockingQueue#take
└── AQS#await（挂起线程进入 WATTING 状态，直到被 singal 通知或者线程中断）
    └── LockSupport#park
        └── sun.misc.Unsafe#park（native 方法）
            └── 调用操作系统具体实现
```

## park 底层实现?
native 方法可以理解为另一个层面的接口，供非 java 代码实现底层逻辑。

首先根据 `sun.misc.Unsafe#park` 搜索[源代码](https://github.com/JetBrains/jdk8u_hotspot)：
![](/images/blog/16439469274665.jpg)

我们发现 `Unsafe#park` 实际调用当前线程 `Parker` 对象的 `park` 方法
![](/images/blog/16439468851293.jpg)

继续寻找 `Parker::park` 方法..
![](/images/blog/16439473688366.jpg)

以 linux 实现为例，当超时时间为 0 时，Parker::park 方法最终调用标准库 `pthread_cond_wait`（`# include <pthread.h>`），挂起线程，等待被唤醒。
![](/images/blog/16439611572855.jpg)


# 接口定义

官方文档解释的很清楚，以获取队列第一个元素为例（如果队列为空）：

- `remove()`: 立即抛出异常 java.util.NoSuchElementException
- `poll()`: 立即返回 null
- `take()`: waiting if necessary
- `pull(timeout, unit)`: waiting + timeout

![](/images/blog/16407823699079.jpg)
p.s. Special value 特殊值指的 false/null 等.. 

\-

为了更好理解，参考博主绘制的 uml 图，`BlockingQueue` 接口在 `Queue` 的基础之上，扩展了 `take`&`put` 两个阻塞方法：
![blockingqueue](/images/blog/blockingqueue.svg)


# 接口实现

一图胜千言，简单绘制常见几种官方队列数据结构（下面将根据源码一一说明）：

![java_queue_diff](/images/blog/java_queue_diff.svg)


## 1. LinkedBlockingQueue

顾名思义底层是由链表实现，特性为先入先出，同时没有长度限制

### 1.1 数据结构
三个部分组成：链表 + 锁 + 迭代器
```java
// 一、链表
static class Node<E> {
    E item;
    Node<E> next;
    Node(E x) { item = x; }
}
//链表头 & 链表尾（注意 head 不是真实的元素，i.e. 虚拟节点）
transient Node<E> head;
private transient Node<E> last;

public LinkedBlockingQueue(int capacity) {
    if (capacity <= 0) throw new IllegalArgumentException();
    this.capacity = capacity;
    // 参考这个赋值，初始化时，head 指向一个空节点
    last = head = new Node<E>(null);
}

// 二、锁
// 两把锁：put/take，两种操作同时进行，互不影响。
//take 时的锁
private final ReentrantLock takeLock = new ReentrantLock();
// take 的条件队列，condition 可以简单理解为基于 ASQ 同步机制建立的条件队列
private final Condition notEmpty = takeLock.newCondition();

// 三、迭代器
private class Itr implements Iterator<E> {}
```

### 1.2 新增操作
put 操作触发链表 enqueue：
```java
// java.util.concurrent.LinkedBlockingQueue#put
public void put(E e) throws InterruptedException {
    int c = -1;
    Node<E> node = new Node<E>(e);
    final ReentrantLock putLock = this.putLock;
    final AtomicInteger count = this.count;
    putLock.lockInterruptibly();
    try {
        // 等待其他线程 take 成功后，被信号唤醒
        while (count.get() == capacity) {
            notFull.await();
        }
        // 真正执行出列（见下面的方法）
        enqueue(node);
        // 如果还没有满 -> 发送通知
        c = count.getAndIncrement();
        if (c + 1 < capacity)
            notFull.signal();
    } finally {
        putLock.unlock();
    }
    // 不等于 -1 表示 put 成功 -> 唤醒待 take 的线程
    if (c == 0)
        signalNotEmpty();
}

private void enqueue(Node<E> node) {
    // 很巧妙：下面这行代码从右往左执行
    last = last.next = node;
}
```

### 1.3 获取并删除
```java
// java.util.concurrent.LinkedBlockingQueue#dequeue
private E dequeue() {
    Node<E> h = head;
    Node<E> first = h.next;
    h.next = h;
    // 关键一步：
    // 还记得上文 head 为虚拟节点，此时将 head 指向下一个节点
    // 同时将 item 置为空（帮助垃圾回收？）
    head = first;
    E x = first.item;
    first.item = null;
    return x;
}
```

## 2 ArrayBlockingQueue
一句话：有界阻塞数组（队列满后，继续放入阻塞），容量不变化。

### 2.1 数据结构
底层数据结构，仅简单一个数组（参数1控制大小）
```java
public ArrayBlockingQueue(int capacity, boolean fair) {
    if (capacity <= 0)
        throw new IllegalArgumentException();
    // 底层数据结构，仅简单一个数组（参数1控制大小）
    this.items = new Object[capacity];
    // 可重入锁：通过参数2控制是否公平
    // - 公平：锁的获取符合绝对时间（保证先来先到）
    // - 否则：降低一定线程切换，提升性能（随机获取）
    lock = new ReentrantLock(fair);
    
    // 利用 await & signal 两个条件作为红绿灯
    notEmpty = lock.newCondition();
    notFull =  lock.newCondition();
}
```

### 2.2 获取元素
新增与获取操作比较类似，以 take 获取元素为例：
```java
// java.util.concurrent.ArrayBlockingQueue#take
public E take() throws InterruptedException {
    final ReentrantLock lock = this.lock;
    // ReadLock#lock 优先考虑获取锁，待获取锁成功后，才响应中断
    // 而 lockInterruptibly 直接中断线程
    lock.lockInterruptibly();
    try {
        while (count == 0)
            // AQS 的 await 方法（阻塞当前线程直到被 singal 通知或者线程中断）
            //   `LockSupport.park()` -> `sun.misc.Unsafe#park` - native 方法
			  //     调用linux系统，标准的阻塞接口（^^原理？？？^^）
            notEmpty.await();
        return dequeue();
    } finally {
        lock.unlock();
    }
}

// 阻塞后何时被唤醒？ 当队列入列后：
private void enqueue(E x) {
    final Object[] items = this.items;
    // 不难理解，计算放入的 index 并赋值
    items[putIndex] = x;
    if (++putIndex == items.length)
        putIndex = 0;
    count++;
    // 发送队列不为空信号
    notEmpty.signal();
}
```

## 3. SynchronousQueue

一句话：**放入数据队列的行为**是阻塞的，只有等消费后才会同步返回结果。

如果有困惑可以运行下面的 demo 代码试试：
```java
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.SynchronousQueue;

public class SynchronousQueueTest {
    private final static SimpleDateFormat s = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    public static void main(String[] args) {
        SynchronousQueue<Integer> queue = new SynchronousQueue<>();

        Thread t1 = new Thread(() -> {
            try {
                Thread.sleep(3000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            log("t1 take..");
            Integer take1 = null;
            try {
                take1 = queue.take();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            log("t2 toke: " + take1);
        });

        Thread t2 = new Thread(() -> {
            log("t2 put..");
            try {
                queue.put(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            log("t2 put done");
        });

        t1.start();
        t2.start();
        // 2022-02-03 12:32:36 t2 put..
        // 2022-02-03 12:32:39 t1 take..
        // 2022-02-03 12:32:39 t2 toke: 1
        // 2022-02-03 12:32:39 t2 put done
    }

    private static void log(Object content) {
        System.out.println(s.format(new Date()) + " " + content.toString());
    }
}
```

## 4 DelayQueue

一句话：延迟执行 

### 4.1 定义延迟执行任务：
```java
import java.util.concurrent.Delayed;
import java.util.concurrent.TimeUnit;

class DelayedEvent implements Delayed {
    private long id;
    private long executeTime;

    public DelayedEvent(long id, long delayTime, TimeUnit unit) {
        super();
        this.id = id;
        this.executeTime = System.currentTimeMillis() + unit.toMillis(delayTime);
    }

    public long getId() {
        return id;
    }

    @Override
    public int compareTo(Delayed that) {
        long result = this.getDelay(TimeUnit.NANOSECONDS) - that.getDelay(TimeUnit.NANOSECONDS);
        if (result < 0) {
            return -1;
        } else if (result > 0) {
            return 1;
        }
        return 0;
    }

    @Override
    public long getDelay(TimeUnit unit) {
        return unit.convert(executeTime - System.currentTimeMillis(), TimeUnit.MILLISECONDS);
    }

    @Override
    public String toString() {
        return "DelayedEvent [id=" + getId() + "]";
    }
}
```

### 4.2 执行任务
```java
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.DelayQueue;
import java.util.concurrent.TimeUnit;

public class DelayedQueueEvent {

    private final static SimpleDateFormat s = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    public static void main(String[] args) throws InterruptedException {
        DelayQueue<DelayedEvent> queue = new DelayQueue<>();

        queue.put(new DelayedEvent(1, 1, TimeUnit.SECONDS));
        queue.put(new DelayedEvent(2, 3, TimeUnit.SECONDS));

        s.format(new Date());

        log("taking...");
        DelayedEvent take1 = queue.take();
        log(take1);
        DelayedEvent take2 = queue.take();
        log(take2);

        // 2022-02-03 12:27:01 taking...
        // 2022-02-03 12:27:02 DelayedEvent [id=1]
        // 2022-02-03 12:27:04 DelayedEvent [id=2]
    }

    private static void log(Object content) {
        System.out.println(s.format(new Date()) + " " + content.toString());
    }
}
```


# 总结

以上 BlockingQueue 针对不同场景的复杂实现，背后都是灵活使用继承与组合后，基于非常简单的数据结构。希望自己有一天也能写出优雅的面向对象代码。


# 参考
1. https://gorden5566.com/post/1027.html
2. https://kkewwei.github.io/elasticsearch_learning/2018/11/10/LockSupport%E6%BA%90%E7%A0%81%E8%A7%A3%E8%AF%BB
3. https://zeral.cn/java/unsafe.park-vs-object.wait/