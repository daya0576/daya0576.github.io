---
title: "读 Python behind the scenes #1: how the CPython VM works"
date: 2026-05-30T15:51:33+08:00
categories:
- Python behind the scenes
- Python
series:
- CPython
---

![](/images/blog/global/17802122035248.jpg)



重返职场一周，除了不用带娃、免费的早午餐，最令人舒心的，是多了不少接触 Python 代码的机会。就像一位老朋友，不管多久未见，总是像第一次见面一样“舒服”。

虽然随着 AI 模型不断进化，代码生成的门槛越来越低，但我反而觉得，作为一名程序员，对 CPython 底层理解的能力变得越来越重要。如果你也和我一样，好奇下面 `python script.py` 执行后，背后到底发生了什么，那么可以跟着我一起阅读学习这个系列文章：[Python behind the scenes](https://tenthousandmeters.com/tag/python-behind-the-scenes/)。

## 学习路径

首先介绍 CPython VM 虚拟机的基本概念，以及 CPython 如何将 Python 代码编译成虚拟机可以执行的字节码：
- [Python behind the scenes #1: how the CPython VM works](https://tenthousandmeters.com/blog/python-behind-the-scenes-1-how-the-cpython-vm-works/)
- [Python behind the scenes #2: how the CPython compiler works](https://tenthousandmeters.com/blog/python-behind-the-scenes-2-how-the-cpython-compiler-works/)

然后阅读 CPython 源码，通过跟踪一个 Python 脚本的执行过程，进一步理解解释器的工作原理：
- [Python behind the scenes #3: stepping through the CPython source code](https://tenthousandmeters.com/blog/python-behind-the-scenes-3-stepping-through-the-cpython-source-code/)
- [Python behind the scenes #4: how Python bytecode is executed](https://tenthousandmeters.com/blog/python-behind-the-scenes-4-how-python-bytecode-is-executed/)

最后学习 Python 中一些关键特性的底层原理，看看它们在 CPython 中是如何实现的，例如 GIL 等：
- [Python behind the scenes #5: how variables are implemented in CPython](https://tenthousandmeters.com/blog/python-behind-the-scenes-5-how-variables-are-implemented-in-cpython/)
- [Python behind the scenes #6: how Python object system works](https://tenthousandmeters.com/blog/python-behind-the-scenes-6-how-python-object-system-works/)
- [Python behind the scenes #7: how Python attributes work](https://tenthousandmeters.com/blog/python-behind-the-scenes-7-how-python-attributes-work/)
- [Python behind the scenes #8: how Python integers work](https://tenthousandmeters.com/blog/python-behind-the-scenes-8-how-python-integers-work/)
- [Python behind the scenes #9: how Python strings work](https://tenthousandmeters.com/blog/python-behind-the-scenes-9-how-python-strings-work/)
- [Python behind the scenes #10: how Python dictionaries work](https://tenthousandmeters.com/blog/python-behind-the-scenes-10-how-python-dictionaries-work/)
- [Python behind the scenes #11: how the Python import system works](https://tenthousandmeters.com/blog/python-behind-the-scenes-11-how-the-python-import-system-works/)
- [Python behind the scenes #12: how async/await works in Python](https://tenthousandmeters.com/blog/python-behind-the-scenes-12-how-asyncawait-works-in-python/)
- [Python behind the scenes #13: the GIL and its effects on Python multithreading](https://tenthousandmeters.com/blog/python-behind-the-scenes-13-the-gil-and-its-effects-on-python-multithreading/)


⚠️ 注意：本系列阅读笔记会在原文基础上做较多改写，并加入个人理解；如介意，建议直接阅读原文。

## 什么是 CPython？为什么要学习 CPython？
顾名思义，CPython 是由 C 语言实现的 Python 解释器之一（PyPy、Jython、IronPython 等）。

而学习 CPython 的三个好处：
1. 对 Python 这门语言有更深、更广的理解，特别是对 Python 一些看似特别“奇怪”的行为，从底层有了重新的理解。
2. 了解对象如何存储、垃圾回收如何工作、多线程如何协作，可以帮助我们更准确地理解语言边界，并高效地进行性能优化。
3. CPython 提供了 Python/C API，用于编写 C 扩展，理解 CPython 原理可以帮助我们更好地使用这些 API。

*P.S. 本文基于 CPython 3.9。*

## 整体介绍

Python 程序执行大致分为三个阶段：1）初始化；2）编译；3）解释。

首先是**初始化**：准备数据结构、初始化内置对象与模块、设置 import 系统等。

然后进入**编译**阶段。CPython 作为解释器，不会像传统编译器那样直接产出机器码（machine code），而是先把源代码转成中间表示。这个过程其实和传统编译器很像：解析源代码 -> 构建 AST 语法树 -> 生成字节码（bytecode）并做部分优化。

P.S. 不同语言的典型执行链路（简化版）：
```
#            源代码   ->  编译/转换             ->  运行
# 1. java：   xx.java ->  xx.class（字节码）    ->  JVM 运行
# 2. python： xx.py   ->  code object（字节码） ->  CPython 虚拟机运行
#            （.pyc 只是可选缓存文件，不是执行必需品）
# 3. C：      xx.c    ->  可执行的机器码         ->  CPU 运行
```

### 字节码
可以将字节码想象为一系列指令。在 CPython 3.9 中，每条字节码指令通常占 2 个字节：1 个字节操作码（opcode）+ 1 个字节参数（oparg）。参考下面的例子：

```python
def g(x):
    return x + 3

# opcode & argument 各占一个 byte
$ python -m dis example1.py
...                                         #  opcode, argument  
2           0 LOAD_FAST            0 (x)    # (     124,        0)
            2 LOAD_CONST           1 (3)    # (     100,        1)
            4 BINARY_ADD                    # (      23,        0)
            6 RETURN_VALUE                  # (      83,        0)
```

最后一步，也是最核心的一步，是 CPython 虚拟机的**解释**执行。虚拟机利用 ==value stack== 存储和获取数据，以上面的函数为例：
1. `LOAD_FAST` 指令将一个本地变量放入 stack 中：`[x]`
2. `LOAD_CONST` 将一个常量放入 stack：`[x, 3]`
3. `BINARY_ADD` 将两个对象从 stack 中取出，相加后，放回 stack：`[x+3]`
4. `RETURN_VALUE` 将 stack 顶对象返回给调用者。

可以将 CPython 虚拟机想象为一个大的 while 循环，不断读取下一条字节码指令并执行；当代码块执行结束，或出现异常时，当前执行流程会结束或切换。

在解答下面问题前，我们需要学习 CPython 虚拟机的基本概念。

```
1. LOAD_FAST opcode 后面的参数代表什么含义？是索引吗？
2. CPython 虚拟机在 stack 中放置的是对象还是引用？
3. CPython 如何知道 x 是本地变量？
4. 假如参数过大，超过了一个 byte 怎么办？
5. 在 Python 中，int 和 string 都可以用 +（1+1 vs "a"+"b"），如果都用同一条加法指令，CPython 如何区分数字加法与字符串拼接？
```

## Code objects, function objects, frames

### Code object

让我们来看一个稍微更复杂的例子（函数定义与调用）：

```python
def f(x):
    return x + 1

print(f(1))
```

在这个例子中，模块字节码里会先构造函数 `f()`。在 CPython 中，函数体、模块体这类可独立执行的代码块会被编译成 **code object**，其中包含待执行的字节码、变量名等信息。==运行一个模块或调用一个函数，本质上都是在执行对应的 code object==（通过 frame 承载执行状态）。

```python
$ python -m dis example2.py

1           0 LOAD_CONST               0 (<code object f at 0x10bffd1e0, file "example.py", line 1>)
            2 LOAD_CONST               1 ('f')
            4 MAKE_FUNCTION            0
            6 STORE_NAME               0 (f)

4           8 LOAD_NAME                1 (print)
           10 LOAD_NAME                0 (f)
           12 LOAD_CONST               2 (1)
           14 CALL_FUNCTION            1
           16 CALL_FUNCTION            1
           18 POP_TOP
           20 LOAD_CONST               3 (None)
           22 RETURN_VALUE
...
```

### function object

一个函数除了 code object，还包含一些额外信息，例如函数名、docstring、默认参数，以及外层作用域变量（闭包）等。这些信息会和 code object 一起保存在 **function object** 中。上面字节码中的 `MAKE_FUNCTION` 指令就是用于创建它。

参考 CPython 在 function object struct 定义的注释：

{{< github-code url="https://github.com/python/cpython/blob/5b5ffce05c211a5b0b74cd95eeb4c463614ee136/Include/cpython/funcobject.h#L25-L34" >}}

```c
/* Function objects and code objects should not be confused with each other:
 *
 * Function objects are created by the execution of the 'def' statement.
 * They reference a code object in their __code__ attribute, which is a
 * purely syntactic object, i.e. nothing more than a compiled version of some
 * source code lines.  There is one code object per source code "fragment",
 * but each code object can be referenced by zero or many function objects
 * depending only on how many times the 'def' statement in the source was
 * executed so far.
 */
```

**function object** vs **code object**：1）function object 在程序**动态**运行到 `def` 语句时创建，并在 `__code__` 属性中引用一个 code object；2）code object 是偏**静态**的编译产物（源代码编译后的字节码与元信息）；3）因此，一个 code object 可以被多个 function object 引用。例如下面代码中，==`make_add_x(4)` 和 `make_add_x(5)` 在执行 `MAKE_FUNCTION` 时使用了 同一个 code object，不同参数 `x`，最终得到两个不同的 function object==（`add_4` 与 `add_5`）。

```python
def make_add_x(x):
    def add_x(y):
        return x + y
    return add_x

add_4 = make_add_x(4)
add_5 = make_add_x(5)
```

为了加深理解，在进入下个概念前，可以看一眼 code object 与 function object 的源代码定义：

```c
struct PyCodeObject {
    PyObject_HEAD
    int co_argcount;            /* #arguments, except *args */
    int co_posonlyargcount;     /* #positional only arguments */
    int co_kwonlyargcount;      /* #keyword only arguments */
    int co_nlocals;             /* #local variables */
    int co_stacksize;           /* #entries needed for evaluation stack */
    int co_flags;               /* CO_..., see below */
    int co_firstlineno;         /* first source line number */
    PyObject *co_code;          /* instruction opcodes */
    PyObject *co_consts;        /* list (constants used) */
    PyObject *co_names;         /* list of strings (names used) */
    PyObject *co_varnames;      /* tuple of strings (local variable names) */
    PyObject *co_freevars;      /* tuple of strings (free variable names) */
    PyObject *co_cellvars;      /* tuple of strings (cell variable names) */

    Py_ssize_t *co_cell2arg;    /* Maps cell vars which are arguments. */
    PyObject *co_filename;      /* unicode (where it was loaded from) */
    PyObject *co_name;          /* unicode (name, for reference) */
        /* ... more members ... */
};
```

```c
typedef struct {
    PyObject_HEAD
    PyObject *func_code;        /* A code object, the __code__ attribute */
    PyObject *func_globals;     /* A dictionary (other mappings won't do) */
    PyObject *func_defaults;    /* NULL or a tuple */
    PyObject *func_kwdefaults;  /* NULL or a dict */
    PyObject *func_closure;     /* NULL or a tuple of cell objects */
    PyObject *func_doc;         /* The __doc__ attribute, can be anything */
    PyObject *func_name;        /* The __name__ attribute, a string object */
    PyObject *func_dict;        /* The __dict__ attribute, a dict or NULL */
    PyObject *func_weakreflist; /* List of weak references */
    PyObject *func_module;      /* The __module__ attribute, can be anything */
    PyObject *func_annotations; /* Annotations, a dict or NULL */
    PyObject *func_qualname;    /* The qualified name */
    vectorcallfunc vectorcall;
} PyFunctionObject;
```

### frame object

当 CPython 执行 code object 时，需要维护变量当前值、不断变化的 value stack，以及调用/返回时的控制流状态。**frame object** 就是用来承载这些执行态信息的，也可以简称 **frame**：

```c
struct _frame {
    PyObject_VAR_HEAD
    struct _frame *f_back;      /* previous frame, or NULL */
    PyCodeObject *f_code;       /* code segment */
    PyObject *f_builtins;       /* builtin symbol table (PyDictObject) */
    PyObject *f_globals;        /* global symbol table (PyDictObject) */
    PyObject *f_locals;         /* local symbol table (any mapping) */
    PyObject **f_valuestack;    /* points after the last local */

    PyObject **f_stacktop;          /* Next free slot in f_valuestack.  ... */
    PyObject *f_trace;          /* Trace function */
    char f_trace_lines;         /* Emit per-line trace events? */
    char f_trace_opcodes;       /* Emit per-opcode trace events? */

    /* Borrowed reference to a generator, or NULL */
    PyObject *f_gen;

    int f_lasti;                /* Last instruction if called */
    /* ... */
    int f_lineno;               /* Current line number */
    int f_iblock;               /* index in f_blockstack */
    char f_executing;           /* whether the frame is still executing */
    PyTryBlock f_blockstack[CO_MAXBLOCKS]; /* for try and loop blocks */
    PyObject *f_localsplus[1];  /* locals+stack, dynamically sized */
};
```

程序启动后，第一个 frame 会负责执行 module 的 code object。之后每次函数调用，CPython 都会为这次调用创建新的 frame。==每个 frame 会引用前一个 frame，在内存中形成 call stack==（栈顶 frame 就是当前正在执行的 frame）。

这么看，CPython 虚拟机似乎只做一件事：创建并执行 frame（当然，真实实现远不止这些）。

## Threads, interpreters, runtime

### thread state

thread state 中包含线程相关数据，例如该线程的 call stack（当前 frame 链）、异常状态，以及调试配置。

下面代码中，`t.start()` 会创建一个操作系统层面的原生线程（UNIX 常见为 `pthread_create()`，Windows 为 `_beginthreadex()`）。新线程启动后，会进入 CPython 线程启动逻辑，并绑定一个新的 thread state；之后在解释器调度下参与字节码执行。

```python
from threading import Thread

def f():
    """Perform an I/O-bound task"""
    pass

t = Thread(target=f)
t.start()
t.join()
```

由于 GIL（Global Interpreter Lock）的存在，在同一个解释器里，同一时刻通常只有一个线程在执行 Python 字节码。

为了管理多个线程及其共享资源，还需要在 thread state 之上引入更高层的数据结构。

### interpreter and runtime states

每个程序运行都会包含：
- interpreter state：解释器状态，对应一组线程，并管理它们共享的资源，包括已加载模块（如 `sys.modules`）、内置命名空间（如 `builtins.__dict__`）以及 import 系统（`importlib`）。
- runtime state：运行时全局状态，保存进程级信息，例如 CPython 是否初始化完成、GIL 机制状态等。

通常来说，一个进程中的所有 Python 线程都属于同一个解释器。但在==少数场景下，也会创建子解释器（subinterpreter）来隔离线程组==。例如 [mod_wsgi](https://modwsgi.readthedocs.io/en/develop/user-guides/processes-and-threading.html#python-sub-interpreters) 会利用这一机制让不同 WSGI 应用运行在隔离解释器中。这样每个解释器都有自己独立的 `__main__` 全局命名空间。

## 总结

Python 代码运行可概括为三步：1）初始化 CPython；2）将源代码编译为 code object；3）执行 code object 中的字节码（由 CPython VM 完成）。

并介绍了 CPython 中的几个基本概念：`runtime state`、`interpreter state`、`thread state`、`frame object`、`function object` 和 `code object`：

```text
# generated with gpt-5.5
process
└─ runtime state
   ├─ interpreter state A  <-->  VM A
   │  ├─ modules / builtins / __main__
   │  └─ thread state(s)
   │     └─ call stack: frame -> frame -> frame
   │                     │
   │                     ├─ value stack, 
   │                     └─ code object (bytecode, consts, ..)
   │
   └─ interpreter state B  <-->  VM B
      └─ ...

# 一段 code object 可以被多个 function object 引用
function object
└─ __code__ ─────────────> code object
   + defaults / globals / closure / name / ...
```


下一章将进一步学习 CPython compiler 如何把源代码转化为 code object。
