---
layout: post
title: "Python MRO(Method Resolution Order)笔记 "
date: 2017-03-21 2:16:15
comments: true
tags: [python]
---

来Hypers上班的第一周, 俊哥提到Python的继承很灵活, 调用class内的方法的话, 有自己的一套MRO(Method Resolution Order).    
我找了资料仔细阅读了一下, 这篇日志是我做的笔记.         
<!--more-->
  


###Method Resolution Order
1. 经典类（classic class）MRO
    * 深度遍历
        + [D, B, A, C, A]
            + **[D, B, A, C]**

    ![http://xblog.qiniudn.com/assets/2013-07-25-python-mro/class_diamond.svg][1]

2. 新式类(new-style class) MRO
它仍然采用从左至右的深度优先遍历，但是如果遍历中出现重复的类，**只保留最后一个**。   
[D, B, A, object, C, A, object] --> [D, B, C, A, object]   
![http://xblog.qiniudn.com/assets/2013-07-25-python-mro/newclass_diamond.svg][2]

3. 类型冲突
违反了线性化的「 **单调性原则** 」   
`class A(X, Y): pass`   
`class B(Y, X): pass`   
**B 和 A 的 MRO 不一样**   
_   
B 被 C 继承时,  C的MRO顺序和B不一样了, 很容易导致不易察觉的错误。
所以引用了C3 MRO, 会产生一个异常.    
![此处输入图片的描述][3]

Reference: http://hanjianwei.com/2013/07/25/python-mro/


  [1]: http://xblog.qiniudn.com/assets/2013-07-25-python-mro/class_diamond.svg
  [2]: http://xblog.qiniudn.com/assets/2013-07-25-python-mro/newclass_diamond.svg
  [3]: http://xblog.qiniudn.com/assets/2013-07-25-python-mro/class_conflict.svg
