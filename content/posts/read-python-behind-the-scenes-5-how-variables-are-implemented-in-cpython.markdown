---
title: "读 Python behind the scenes #5: how variables are implemented in CPython"
date: 2026-07-19T11:17:11+08:00
categories:
- Python behind the scenes
- Python
series:
- CPython
---

> https://tenthousandmeters.com/blog/python-behind-the-scenes-5-how-variables-are-implemented-in-cpython/

通过这一章我们将尝试理解，下面这一行简短的 python 代码背后，究竟发生了什么？

```python
a = b
```

## 初探字节码

首先将代码片段转化为字节码：

```
$ echo 'a = b' | python3.9 -m dis
  1           0 LOAD_NAME                0 (b)
              2 STORE_NAME               1 (a)
...
```

从之前的章节了解到，CPython VM 通过 value stack 执行计算：
1. 第一步：`LOAD_NAME` 获取 `b` 变量的值，并压入 stack 中
2. 第二步：`STORE_NAME` 从 stack 中弹出值，并赋值给 `a`

### STORE_NAME

上一章的结尾提到，每个字节码对应 [Python/ceval.c](https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1464) 大循环中的一个 `switch` 语句，所以我们可通过该方法快速查看 `STORE_NAME` 对应的源码实现：

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

### LOAD_NAME

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

### 其他操作码

<u>所以是不是用 `LOAD_NAME` 与 `STORE_NAME` 就能覆盖所有的赋值情况呢？</u>

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

在理解 `LOAD_GLOBAL`、`LOAD_FAST` 和 `LOAD_DEREF` 之前，我们需要先理解两个重要概念：namespace & scope。

## Namespaces and scopes

code block 是 VM 执行的最小代码单元，VM 会针对每个代码块生成一个 [code object](/blog/20260530/read-python-behind-the-scenes-1-cpython-vm/#%E6%80%BB%E7%BB%93)，包含具体需要执行的字节码。


总共分三种（通过嵌套关系维护）：1）module 2）function 3）class 
```
module code object (<module>)
- bytecode 字节码
- 常量 function code object (foo)
    - bytecode 字节码
    - 常量 class code object (Bar)
        - bytecode 字节码
        - ...
```

### namespce

为了执行 code object，VM 创建了 frame object 维护执行的上下文，其中就包含了不同的 name/value mapping，例如 `f_locals`, `f_globals` 和 `f_builtins`。==这些 mapping 映射就是我们常提及的 namespace==

### scope

> A scope is a textual region of a Python program where a namespace is directly accessible. “Directly accessible” here means that an unqualified reference to a name attempts to find the name in the namespace.

而 ==scope 本质上代表一段代码区域==，具体可以访问/写入哪些 namespace（猛的回忆起[十年前的博客 - LEGB](/blog/20170220/python-scope/)）：Local, Enclosing, Global, Built-in。

不同的 **scope** + 不同的 **code block 类型**，决定了最终使用哪个操作码：

| LEGB / Scope             | Function                         | Module                      | Class body                          |
| :----------------------- | :------------------------------- | :-------------------------- | :---------------------------------- |
| **L — Local**            | `LOAD_FAST`<br>`STORE_FAST`      | `LOAD_NAME`<br>`STORE_NAME` | `LOAD_NAME`<br>`STORE_NAME`         |
| **E — Enclosing** | `LOAD_DEREF`<br>`STORE_DEREF`    | —                           | `LOAD_CLASSDEREF`<br>`STORE_DEREF`* |
| **G — Global**           | `LOAD_GLOBAL`<br>`STORE_GLOBAL`* | `LOAD_NAME`<br>`STORE_NAME` | `LOAD_NAME`**<br>`STORE_GLOBAL`*    |
| **B — Builtin**          | `LOAD_GLOBAL`                    | `LOAD_NAME`                 | `LOAD_NAME`                         |

<br>

参考：https://github.com/python/cpython/blob/3.9/Python/symtable.c#L497

不通操作码的含义以及存在的原因：

### `LOAD_FAST` / `STORE_FAST`

```python
def f():
    x = 1      # STORE_FAST x
    return x   # LOAD_FAST x

# 存储位置：
# frame.f_localsplus[i] -> x
```

vm 静态计算出 index，相比于 dict 更快，所以 `STORE_FAST` 的存在仅仅是为了性能考虑。原文中的测试，`STORE_NAME` vs `STORE_FAST`：

```
$ python fast_vs_name.py
STORE_NAME: 4.536s 4.572s 4.650s 4.742s 4.855s
STORE_FAST: 2.597s 2.608s 2.625s 2.628s 2.645s
```

### `LOAD_DEREF` / `STORE_DEREF`

```python
def outer():
    x = 1

    def inner():
        nonlocal x
        x = x + 1     # LOAD_DEREF + STORE_DEREF
        return x      # LOAD_DEREF

    return inner

# 存储位置：同一个 cell object（x）：
# - outer frame object -> f_localsplus -> cell
# - inner function object -> __closure__ -> same cell
```

p.s. 如果不加 `nonlocal` 关键字，编译阶段认为 `x` 是 local variable 并导致运行报错：

```
Traceback (most recent call last):
  File "/tmp/scratch/928c624be3.py", line 14, in <module>
    print(f())  # Output: 2
          ^^^
  File "/tmp/scratch/928c624be3.py", line 6, in inner
    x = x + 1     # LOAD_DEREF + STORE_DEREF
        ^
UnboundLocalError: cannot access local variable 'x' where it is not associated with a value
```

### `LOAD_GLOBAL` / `STORE_GLOBAL`

```python
x = 1

def f():
    global x
    x = 2      # STORE_GLOBAL
    return x   # LOAD_GLOBAL

# 存储位置：
# frame.f_globals["x"] -> frame.f_builtins
```

### `LOAD_NAME` / `STORE_NAME`

```python
x = 10

class A:
    y = x          # LOAD_NAME x
    z = len([])    # LOAD_NAME len

# 存储位置：
# frame.f_locals["len"] -> f_globals["len"] -> f_builtins["len"]
```

### `LOAD_CLASSDEREF`

class 包 function：
```python
class D:
    x = 1             # STORE_NAME x（存进 class body 的 f_locals）
    def method(self):
        print(x)      # LOAD_GLOBAL x -> NameError: name 'x' is not defined

D().method()
```

function 包 class（闭包）：
```python
def outer():
    x = 1             # STORE_DEREF

    class C:
        print(x)      # LOAD_CLASSDEREF

# 查找位置：
# class frame.f_locals["x"] 
#   -> C.__closure__
#     -> outter.cell -> value
```

## 总结

Python 中的变量赋值，远远比看上去的代码复杂。下一章，我们将继续学习 python 的 object system，从而更好地理解 VM 在运行**其他操作码**时，执行计算的实现原理。

