---
layout: post
title: "Python - Note of Garbage Collection"
date: 2017-02-14 15:30:18
comments: true
tags: [Python, interview]
---

阅读了一篇Python垃圾回收的文章, 用这篇日志记录一下. 原文地址: [http://www.digi.com/wiki/developer/index.php/Python_Garbage_Collection](http://www.digi.com/wiki/developer/index.php/Python_Garbage_Collection)    

<!--more-->
  

###Introduction to Python Memory Management
不像c和c艹, Python的内存分配和释放是完全自动的.     

Python的两个内存管理策略:
1. reference counting
2. garbage collection
在Python 2.0之前, 只用reference counting作为内存管理.   
原理: 记录一个对象被其他对象引用的次数. 当对这个对象的引用移除了, 引用计数也减小了. 要是减到0了, 这个对象也就被释放了.   

这种方法很高效, 但也有一些caveat(警告, 缺点的意思吧). 例如它无法解决reference circle的问题(有种死锁的味道):   
```python
def make_cycle():
    l = [ ]
    l.append(l)

make_cycle()
```  



### Automatic Garbage Collection of Cycles
由于有上边这个reference circle的问题, 所以需要scheduled activity去自动收集垃圾.   
原理: 当 `分配的值 - 释放的值 > 阈值` 的话: the garbage collector就会自动运行了. 它会运行gc模块去查找阈值.        
```python
import gc
print "Garbage collection thresholds: %r" % gc.get_threshold()
# Garbage collection thresholds: (700, 10, 10)

# 我们可以看到这里默认的阈值是700
```
但要**注意**的是如果Python已经把内存爆了的话, automatic garbage collection是不会执行的. 这时候你需要去处理抛出的异常, 或者程序已经崩溃了.    
'''This is aggravated by the fact that the automatic garbage collection places high weight upon the NUMBER of free objects, not on how large they are. Thus any portion of your code which frees up large blocks of memory is a good candidate for running manual garbage collection.
'''   


### Manual Garbage Collection
对于一些长时间运行的服务器应用或者嵌入式应用, 自动的垃圾回收可能就有局限性了.     
虽然在编码中reference cycle是要尽量去避免的, 但还是要有怎么去解决他们的办法.    
手动地回收垃圾是个释放reference cycle垃圾内存的好方法.     
手动回收垃圾的方法:    
```python
import gc
gc.collect()
```
`gc.collect()`返回所有被回收的对象:    
```python
import gc
collected = gc.collect()
print "Garbage collector: collected %d objects." % (collected)
```
创建了几个reference cycle的实例:    
```python
import sys, gc

def make_cycle():
    l = { }
    l[0] = l

def main():
    collected = gc.collect()
    print "Garbage collector: collected %d objects." % (collected)
    print "Creating cycles..."
    for i in range(10):
        make_cycle()
    collected = gc.collect()
    print "Garbage collector: collected %d objects." % (collected)

if __name__ == "__main__":
    ret = main()
    sys.exit(ret)
```
有两种调用手动回收垃圾的策略(很好理解就不解释了):    
1. Time-based
2. Event-based:  For example, when a user disconnects from the application or when the application is known to enter an idle state.    


### 几点建议
1. 不要太随意地去进行垃圾回收, 会严重影响性能(因为要去evalute每一个memory object).   
2. 在你的应用启动并趋于稳定后, 再进行手动地垃圾回收.    
3. Run manual garbage collection after infrequently run sections of code which use and then free large blocks of memory. 最好在这时运行手动的垃圾回收: 当一段不常用的代码使用并释放了大量内存的是时候.
4. 当一段代码对timing很敏感的时候, 手动回收垃圾最好在它之前或之后运行.
_   
原版的描述:   
1.Do not run garbage collection too freely, as it can take considerable time to evaluate every memory object within a large system. For example, one team having memory issues tried calling gc.collect() between every step of a complex start-up process, increasing the boot time by 20 times (2000%). Running it more than a few times per day - without specific design reasons - is likely a waste of device resources.   
2.Run manual garbage collection after your application has completed start up and moves into steady-state operation. This frees potentially huge blocks of memory used to open and parse file, to build and modify object lists, and even code modules never to be used again. For example, one application reading XML configuration files was consuming about 1.5MB of temporary memory during the process. Without manual garbage collection, there is no way to predict when that 1.5MB of memory will be returned to the python memory pools for reuse.   
3.Run manual garbage collection after infrequently run sections of code which use and then free large blocks of memory. For example, consider running garbage collection after a once-per-day task which evaluates thousands of data points, creates an XML 'report', and then sends that report to a central office via FTP or SMTP/email. One application doing such daily reports was creating over 800K worth of temporary sorted lists of historical data. Piggy-backing gc.collect() on such daily chores has the nice side-effect of running it once per day for 'free'.   
4.Consider manually running garbage collection either before or after timing-critical sections of code to prevent garbage collection from disturbing the timing. As example, an irrigation application might sit idle for 10 minutes, then evaluate the status of all field devices and make adjustments. Since delays during system adjustment might affect field device battery life, it makes sense to manually run garbage collection as the gateway is entering the idle period AFTER the adjustment process - or run it every sixth or tenth idle period. This insures that garbage collection won't be triggered automatically during the next timing-sensitive period.   
