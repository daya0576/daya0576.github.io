---
title: "读 Python behind the scenes #5: how variables are implemented in CPython"
date: 2026-07-19T11:17:11+08:00
draft: true
categories:
- Python behind the scenes
- Python
series:
- CPython
---

> https://tenthousandmeters.com/blog/python-behind-the-scenes-5-how-variables-are-implemented-in-cpython/

下面这一行简短的 python 代码背后，到底发生了什么呢？

```python
a = b
```

## 字节码

首先将代码片段转化为字节码：

```
$ echo 'a = b' | python3.9 -m dis
  1           0 LOAD_NAME                0 (b)
              2 STORE_NAME               1 (a)
...
```

从上一章中了解到，CPython VM 通过 value stack 来管理计算：通常一个 bytecode 从 stack 中弹出一个值，计算后，重新压入 stack。上面 bytecode 中的 `LOAD_NAME` 和 `STORE_NAME` 就是这个模式最好的例子：
- 首先 `LOAD_NAME` 获取 `b` 变量的值，并压入 stack 中；
- 然后 `STORE_NAME` 从 stack 中弹出值，并赋值给 `a`。

上一章，我们还学习到，每个字节码对应 [Python/ceval.c](https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1464) 大循环中的一个 `switch` 语句。所以可以通过源码快速查看 `STORE_NAME` 的实现原理：

```c
case TARGET(STORE_NAME): {
    // 1. names 是 co_names 的“缩写” - 编译后 code object 的一个 tuple 变量
    // oparg -> 字节码的参数（index 位置）
    PyObject *name = GETITEM(names, oparg);
    // 2. 从 value stack 中 pop 一个值
    PyObject *v = POP();
    // 3. f_locals 是当前 frame object 对象的变量，存放了
    PyObject *ns = f->f_locals;
    int err;
    if (ns == NULL) {
        _PyErr_Format(tstate, PyExc_SystemError,
                      "no locals found when storing %R", name);
        Py_DECREF(v);
        goto error;
    }
    // 关联 name 与 value 并写入本地变量（f_locals[name] = v;）
    if (PyDict_CheckExact(ns))
        err = PyDict_SetItem(ns, name, v);
    else
        err = PyObject_SetItem(ns, name, v);
    Py_DECREF(v);
    if (err != 0)
        goto error;
    DISPATCH();
}
```

