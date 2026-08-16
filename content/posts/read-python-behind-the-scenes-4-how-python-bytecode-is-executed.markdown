---
title: "读 Python behind the scenes #4: how Python bytecode is executed"
date: 2026-07-05T20:00:00+08:00
categories:
- Python behind the scenes
- Python
series:
- CPython
---

> https://tenthousandmeters.com/blog/python-behind-the-scenes-4-how-python-bytecode-is-executed/

上一章我们从源码中了解到：如果 `pyc` 文件存在，CPython 会跳过编译，直接加载文件中 code object，丢给 `_PyEval_EvalFrameDefault()` 运行（[Python/ceval.c](https://github.com/python/cpython/blob/0bbaf5de9744ae1acea3e2c9ad2257d1cc68e847/Python/ceval.c#L920)）。

这个函数是整个 CPython VM 的核心，也是这篇需要学习的重点：

```c
PyObject* _Py_HOT_FUNCTION
_PyEval_EvalFrameDefault(PyThreadState *tstate, PyFrameObject *f, int throwflag)
{
```

在开始前，先看一眼 frame object 的数据结构（变量 `PyCodeObject *f_code`）：

```c
// typedef struct _frame PyFrameObject; in other place
struct _frame {
    PyObject_VAR_HEAD
    struct _frame *f_back;      /* previous frame, or NULL */
    PyCodeObject *f_code;       /* code segment */
    PyObject *f_builtins;       /* builtin symbol table (PyDictObject) */
    PyObject *f_globals;        /* global symbol table (PyDictObject) */
    PyObject *f_locals;         /* local symbol table (any mapping) */
    PyObject **f_valuestack;    /* points after the last local */
    /* Next free slot in f_valuestack.  Frame creation sets to f_valuestack.
       Frame evaluation usually NULLs it, but a frame that yields sets it
       to the current stack top. */
    PyObject **f_stacktop;
    PyObject *f_trace;          /* Trace function */
    char f_trace_lines;         /* Emit per-line trace events? */
    char f_trace_opcodes;       /* Emit per-opcode trace events? */

    /* Borrowed reference to a generator, or NULL */
    PyObject *f_gen;

    int f_lasti;                /* Last instruction if called */
    int f_lineno;               /* Current line number */
    int f_iblock;               /* index in f_blockstack */
    char f_executing;           /* whether the frame is still executing */
    PyTryBlock f_blockstack[CO_MAXBLOCKS]; /* for try and loop blocks */
    PyObject *f_localsplus[1];  /* locals+stack, dynamically sized */
};
```

code object 也是一个 Python object，数据结构如下。其中最重要的字段是 `co_code`，也就是一直提及的 bytecode（用 Python bytes object 表示）------ 顾名思义，两个 byte 表示的指令，其中 opcode 和 argument 各占一个 byte。


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
    /* The rest aren't used in either hash or comparisons, except for co_name,
       used in both. This is done to preserve the name and line number
       for tracebacks and debuggers; otherwise, constant de-duplication
       would collapse identical functions/lambdas defined on different lines.
    */
    Py_ssize_t *co_cell2arg;    /* Maps cell vars which are arguments. */
    PyObject *co_filename;      /* unicode (where it was loaded from) */
    PyObject *co_name;          /* unicode (name, for reference) */
    PyObject *co_lnotab;        /* string (encoding addr<->lineno mapping) See
                                   Objects/lnotab_notes.txt for details. */
    void *co_zombieframe;       /* for optimization only (see frameobject.c) */
    PyObject *co_weakreflist;   /* to support weakrefs to code objects */
    /* Scratch space for extra data relating to the code object.
       Type is a void* to keep the format private in codeobject.c to force
       people to go through the proper APIs. */
    void *co_extra;

    /* Per opcodes just-in-time cache
     *
     * To reduce cache size, we use indirect mapping from opcode index to
     * cache object:
     *   cache = co_opcache[co_opcache_map[next_instr - first_instr] - 1]
     */

    // co_opcache_map is indexed by (next_instr - first_instr).
    //  * 0 means there is no cache for this opcode.
    //  * n > 0 means there is cache in co_opcache[n-1].
    unsigned char *co_opcache_map;
    _PyOpcache *co_opcache;
    int co_opcache_flag;  // used to determine when create a cache.
    unsigned char co_opcache_size;  // length of co_opcache.
};
```

## evaluation loop 概况

执行 bytecode 的逻辑似乎很简单，无脑线性执行即可。事实的确如此：一个 while 循环中，包含一个超大的 switch 语句，每个 case 语句对应一个 opcode 的处理逻辑。在 CPyhon 中 bytecode 指令使用 `uint16_t[]` 数组存放，每次执行一条指令后，通过 `next_instr` index 指向下一条。

```c
PyObject*
_PyEval_EvalFrameDefault(PyThreadState *tstate, PyFrameObject *f, int throwflag)
{
    // ... declarations and initialization of local variables
    // ... macros definitions
    // ... call depth handling
    // ... code for tracing and profiling

    for (;;) {
        // ... check if the bytecode execution must be suspended,
        // e.g. other thread requested the GIL

        // NEXTOPARG() macro
        _Py_CODEUNIT word = *next_instr; // _Py_CODEUNIT is a typedef for uint16_t
        opcode = _Py_OPCODE(word);
        oparg = _Py_OPARG(word);
        next_instr++;

        switch (opcode) {
            case TARGET(NOP) {
                FAST_DISPATCH(); // more on this later
            }

            case TARGET(LOAD_FAST) {
                // ... code for loading local variable
            }

            // ... 117 more cases for every possible opcode
        }

        // ... error handling
    }

    // ... termination
}

```

### 跳出循环

当前线程跳出循环，停止执行字节码的几种可能：
1. 信号处理：例如常使用 `signal.signal()` 来设置超时时间
2. pending calls：通过 C API [Py_AddPendingCall()](https://docs.python.org/3.9/c-api/init.html#c.Py_AddPendingCall) 方法，插入一个 c 函数执行
3. 异步异常：例如从主线程向其他线程，通过 PyThreadState_SetAsyncExc() 方法，向其他线程注入 SystemExit 异常。
4. GIL 释放

上面每种事件都有各自的标志位，例如下面是所有 interpreter 共享的 signals_pending 和 GIL 状态（runtime state）：

```c
struct _ceval_runtime_state {
   _Py_atomic_int signals_pending;
   struct _gil_runtime_state gil; // GIL 本身的状态
};

struct _gil_runtime_state {
    unsigned long interval;       // 切换间隔,默认 5ms
    unsigned long switch_number;
    PyCOND_T cond;
    PyMUTEX_T mutex;
```

但为了提升性能，CPython 首先检查 `eval_breaker` 总开关（各个标志位 OR 的缓存结果），只有在非零的时候才 逐个检查具体原因（interpreter state）：

```c
struct _ceval_state {
   int recursion_limit;
   int tracing_possible;
   _Py_atomic_int eval_breaker;      // 总开关
   _Py_atomic_int gil_drop_request;
   struct _pending_calls pending;
};
```

<u>检查的频率？</u> 每条指令运行前都会检查（除了下一章的 `FAST_DISPATCH`）
```c
/* _PyEval_EvalFrameDefault() main loop */
main_loop:
   for (;;) {
       ...
       if (_Py_atomic_load_relaxed(eval_breaker)) {
           /* ... handle signals, pending calls, GIL drop ... */
       }

       /* execute next opcode */
       switch (opcode) {
           ...
       }
   }
```

## computed GOTOs

evaluation loop 的代码中，定义大量的宏，例如 `TARGET()` 和 `DISPATCH()`。目的并不是让代码变得紧凑，而是在故意在每条 bytecode 处理完成后，使用 FAST_DISPATCH（computed goto）直接跳到下一条执行（无需再经过 switch 语句）。从而利用了 CPU 的（[分支预测技术](https://en.wikipedia.org/wiki/Branch_predictor)）优化性能。

```c
// 触发一次真实跳转：
DISPATCH:
    -> goto *opcode_targets[POP_TOP] 
    -> TARGET(op) -> TARGET_##op -> TARGET_POP_TOP

switch (opcode) {
    case TARGET(LOAD_FAST): {
       DISPATCH();   // 地址 A,这是第 1 份拷贝
    }
    case TARGET(CALL): {
       FAST_DISPATCH();   // 地址 B,这是第 2 份拷贝
   }
```

TARGET：
```c
#define TARGET(op) \
    op: \
    TARGET_##op
```

DISPATCH -> FAST_DISPATCH -> `TARGET_POP_TOP` (TARGET_##op)：
```c
#define DISPATCH() \
    { \
        // 判断是否需要中断 loop
        if (!_Py_atomic_load_relaxed(eval_breaker)) { \
            FAST_DISPATCH(); \
        } \
        continue; \
    }
    
#define FAST_DISPATCH() \
    goto *opcode_targets[opcode]; \
    
// opcode_targets 是一个 256 长度的数组，维护了每个 bytecode 
// 数组定义：
static void *opcode_targets[256] = {
    &&_unknown_opcode,
    &&TARGET_POP_TOP,
```

## Value stack

VM 执行 bytecode 字节码时，通过 value stack 完成计算：
```
LOAD_FAST  a      # push a          栈: [a]
LOAD_FAST  b      # push b          栈: [a, b]
BINARY_ADD        # pop b, peek a,  栈: [a+b]
                  # 栈顶替换为 a+b
STORE_FAST c      # pop 结果存入 c   栈: []
```

## 异常处理

### try/catch

```python
try:
    1 + "42"
except Exception:
    x = 1

Traceback (most recent call last):
  File "<string>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

C 语言不像 Python 直接一路向上抛出异常，所以 `PyNumber_Add()` 返回 `NULL` 用于表示异常；然后找到对应的 exception handler 进行处理（对应一个 `except` 代码块）：

```c
case TARGET(BINARY_ADD): {
    // ... 
    sum = PyNumber_Add(left, right);
    // ...
    if (sum == NULL)
        goto error;
    DISPATCH();
}
```

一个 exception handler 对应一个 `PyTryBlock` 数据结构：
```c
typedef struct {
    int b_type;                 /* what kind of block this is */
    int b_handler;              /* where to jump to find handler */
    int b_level;                /* value stack level to pop to */
} PyTryBlock;
```

完整路径：
1. 编译：
    - `1 + "42"` -> 编译器 -> `BINARY_ADD`
    - `except` -> 编译器 -> `exception handler 字节码`
2. 运行：
    - `BINARY_ADD` -> `PyNumber_Add(1, "42")` -> `NULL` -> goto error -> `PyTryBlock` -> `exception handler`

完整的字节码解释：
```shell
  1        0 SETUP_FINALLY   12 (to 14)      # 压入 PyTryBlock
                                             #   b_type    = SETUP_FINALLY
                                             #   b_handler = 14
                                             #   b_level   = 0 

  2        2 LOAD_CONST       0 (1)          # 值栈：[1]
           4 LOAD_CONST       1 ('42')       # 值栈：[1, '42']
           6 BINARY_ADD                      # 执行：
                                             #   PyNumber_Add(1, "42") -> NULL -> goto error
                                             #   按 PyTryBlock.b_handler 跳到 14
           8 POP_TOP                         
          10 POP_BLOCK                       # 正常路径：
          12 JUMP_FORWARD    22 (to 36)      # 绕过 handler，跳到 36

  3       14 DUP_TOP                         # 异常路径 开始
          16 LOAD_NAME        0 (TypeError)  
          18 JUMP_IF_NOT_EXC_MATCH   34 
          20 POP_TOP                         
          22 POP_TOP
          24 POP_TOP
  4       26 LOAD_CONST       2 (1) 
          28 STORE_NAME       1 (x)
          30 POP_EXCEPT
          32 JUMP_FORWARD     2 (to 36)      # 继续执行
          34 RERAISE

          36 LOAD_CONST       3 (None) 
          38 RETURN_VALUE
```

### try/finally

但假如没有 `try/except` 的情况下，为什么最后也会抛出打印异常呢？？
```shell
$ python -q
>>> try:
...     1 + '41'
... finally:
...     print('Hey!')
... 
Hey!
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

通过对应的字节码可以看到，finally 的代码被复制两份（路径1，路径2），如果出现异常会重新抛出：
```shell
$ python -m dis try-finally.py

 0 SETUP_FINALLY  20 (to 22)
                             
 2 LOAD_CONST     1 (1)      # ...
 4 LOAD_CONST     2 ('41')   # ...
 6 BINARY_ADD                # 执行 1 + '41'
 8 POP_TOP
10 POP_BLOCK

12 ... print('Hey!')         # 路径1：执行 finally
20 JUMP_FORWARD   10         

22 ... print('Hey!')         # 路径2：执行 finally + 重新抛出异常
30 RERAISE
```

## 总结

作者最后表示，如果你想深入学习 CPython 源码，第一选择就是 evaluation loop，例如：
- `x + y` -> `BINARY_ADD`
- `with` 语句 -> `SETUP_WITH`
- function call -> `CALL_FUNCTION`
- ...

下一章，我们将尝试用这个方法，学习 Python 变量的实现原理。