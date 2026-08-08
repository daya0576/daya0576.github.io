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

## LOAD_NAME & STORE_NAME

首先将代码片段转化为字节码：

```
$ echo 'a = b' | python3.9 -m dis
  1           0 LOAD_NAME                0 (b)
              2 STORE_NAME               1 (a)
...
```

从上一章中了解到，CPython VM 通过 value stack 执行计算：
1. `LOAD_NAME` 获取 `b` 变量的值，并压入 stack 中
2. `STORE_NAME` 从 stack 中弹出值，并赋值给 `a`

上一章中还提到，每个字节码对应 [Python/ceval.c](https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1464) 大循环中的一个 `switch` 语句。所以我们可通过源码快速查看 `STORE_NAME` 分支的实现原理：

```c
// "2 STORE_NAME               1 (a)"
case TARGET(STORE_NAME): {
    // 1. 通过字节码的参数 oparg（index 位置），获取变量名（string 对象）
    PyObject *name = GETITEM(names, oparg);
    // 2. 从 value stack 中 pop 一个值（python 对象的引用）
    PyObject *v = POP();
    PyObject *ns = f->f_locals;
    int err;
    if (ns == NULL) {
        _PyErr_Format(tstate, PyExc_SystemError,
                      "no locals found when storing %R", name);
        Py_DECREF(v);
        goto error;
    }
    // 3. 关联 `*name` & `*v`
    // P.S. 通过 frame object 中的 f_locals 变量维护 mapping 关系 
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

`LOAD_NAME` 相对更加复杂一些，因为 VM 会从 f_locals 以及多个位置获取变量的值：

```c
case TARGET(LOAD_NAME): {
    // 1. 同上获取变量名
    PyObject *name = GETITEM(names, oparg);
    PyObject *locals = f->f_locals;
    PyObject *v;

    if (locals == NULL) {
        _PyErr_Format(tstate, PyExc_SystemError,
                        "no locals when loading %R", name);
        goto error;
    }

    // 2. 首先在 f -> f_locals 中查找变量值
    // p.s. f 是一个 frame
    // f = _PyFrame_New_NoTrack(tstate, co, globals, locals);
    if (PyDict_CheckExact(locals)) {
        v = PyDict_GetItemWithError(locals, name);
        if (v != NULL) {
            Py_INCREF(v);
        }
        else if (_PyErr_Occurred(tstate)) {
            goto error;
        }
    }
    else {
        v = PyObject_GetItem(locals, name);
        if (v == NULL) {
            if (!_PyErr_ExceptionMatches(tstate, PyExc_KeyError))
                goto error;
            _PyErr_Clear(tstate);
        }
    }

    // 3. 如果不存在，继续查找：
    // 3.1 `f->f_globals`：全局变量
    // 3.2 `f->f_builtins`：内置类型/方法/异常与常量，例如 int, next, ValueError and None
    if (v == NULL) {
        v = PyDict_GetItemWithError(f->f_globals, name);
        if (v != NULL) {
            Py_INCREF(v);
        }
        else if (_PyErr_Occurred(tstate)) {
            goto error;
        }
        else {
            if (PyDict_CheckExact(f->f_builtins)) {
                v = PyDict_GetItemWithError(f->f_builtins, name);
                if (v == NULL) {
                    // 4. 如果找不到，抛出 `NameError` 异常
                    if (!_PyErr_Occurred(tstate)) {
                        format_exc_check_arg(
                                tstate, PyExc_NameError,
                                NAME_ERROR_MSG, name);
                    }
                    goto error;
                }
                Py_INCREF(v);
            }
            else {
                v = PyObject_GetItem(f->f_builtins, name);
                if (v == NULL) {
                    if (_PyErr_ExceptionMatches(tstate, PyExc_KeyError)) {
                        format_exc_check_arg(
                                    tstate, PyExc_NameError,
                                    NAME_ERROR_MSG, name);
                    }
                    goto error;
                }
            }
        }
    }
    // 4. 如果找到了，将值 push 到 stack 中
    PUSH(v);
    DISPATCH();
}
```

所以是不是用 `LOAD_NAME` 与 `STORE_NAME` 就能覆盖所有的赋值情况呢？

一个稍微复杂一点的例子：
```python
x = 1

def f(y, z):
    def _():
        return z

    return x + y + z

```

可以看到，下面的字节码中，并没有出现 `LOAD_NAME`：
```
$ python -m dis global_fast_deref.py
...
  7          12 LOAD_GLOBAL              0 (x)
             14 LOAD_FAST                0 (y)
             16 BINARY_ADD
             18 LOAD_DEREF               0 (z)
             20 BINARY_ADD
             22 RETURN_VALUE
...
```

为了更好的理解 `LOAD_GLOBAL`、`LOAD_FAST` 和 `LOAD_DEREF`，我们需要先理解两个重要概念：namespace & scope。

## Namespaces and scopes