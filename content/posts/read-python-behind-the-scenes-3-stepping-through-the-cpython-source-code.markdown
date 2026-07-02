---
title: "读 Python behind the scenes #3: stepping through the CPython source code"
date: 2026-06-28T13:18:30+08:00
categories:
- Python behind the scenes
- Python
series:
- CPython
---

上两章中，我们讨论了 Python 代码运行与编译背后的故事。这一章将跟随一次代码执行，快速浏览源码。

> https://tenthousandmeters.com/blog/python-behind-the-scenes-3-stepping-through-the-cpython-source-code/


## CPython 源码

获取代码：
```sh
$ git clone https://github.com/python/cpython/ && cd cpython
$ git checkout 3.9
$ ls -p
CODE_OF_CONDUCT.md  Makefile.pre.in     Programs/           configure
Doc/                Misc/               Python/             configure.ac
Grammar/            Modules/            README.rst          install-sh
Include/            Objects/            Tools/              pyconfig.h.in
LICENSE             PC/                 aclocal.m4          setup.py
Lib/                PCbuild/            config.guess
Mac/                Parser/             config.sub
```

编译 CPython
```sh
$ ./configure
$ make -j -s
```

运行测试：
```sh
$./python.exe -m test test_peepholer
0:00:00 load avg: 3.40 Run tests sequentially
0:00:00 load avg: 3.40 [1/1] test_peepholer

== Tests result: SUCCESS ==

1 test OK.

Total duration: 28 ms
Tests result: SUCCESS
```

Note：<u>为什么在 macOS 中会出现 `python.exe`？</u> 因为 macOS 中文件不区分大小写，所以用 `.exe` 后缀用于区分 `Python` 文件夹 vs `python` 可执行文件。这里与 Windows 没有任何关系。

## main()

CPython 运行的入口：[Programs/python.c](https://github.com/python/cpython/blob/3.9/Programs/python.c)，前者用于 windows 的运行。

```c
/* Minimal main program -- everything is loaded from the library */

#include "Python.h"

#ifdef MS_WINDOWS
int
wmain(int argc, wchar_t **argv)
{
    return Py_Main(argc, argv);
}
#else
int
main(int argc, char **argv)
{
    return Py_BytesMain(argc, argv);
}
#endif
```

main 函数做的就是：调用「初始化」（`pymain_init`），进而触发「编译」与「解释」。

```c
static int
pymain_main(_PyArgv *args)
{
    PyStatus status = pymain_init(args);
    if (_PyStatus_IS_EXIT(status)) {
        pymain_free();
        return status.exitcode;
    }
    if (_PyStatus_EXCEPTION(status)) {
        pymain_exit_error(status);
    }

    return Py_RunMain();
}
```

### 初始化

CPython 初始化分为三步（`pymain_init`、`pyinit_core`、`pyinit_main`）。多阶段的好处在于方便用户自定义启动流程，例如在 `preinit` 结束后，自定义 memory allocator。

```
main() -> Py_BytesMain() -> pymain_main()
1. pymain_init()              // 阶段 1：预初始化
  - 初始化 runtime state
    - 进程级状态 _PyRuntime（全局变量）
  - 读少量 argv/env
  - 设置 locale / memory allocator

2. pyinit_core()              // 阶段 2：核心初始化
  - 创建 main interpreter state
    - 准备解释器级状态 PyInterpreterState
  - 创建 main thread state
    - 准备线程级状态 PyThreadState
  - 初始化 GIL / GC
  - 初始化 builtins / sys
  - 初始化基本 import system

3. pyinit_main()              // 阶段 3：完整初始化
    - 完成 sys.path
    - 完成 import system
    - import site
    - 创建 __main__

4. `Py_RunMain()`             // 开始运行用户代码
```

看一眼全局变量 runtime state 的数据结构（一个 runtime state 对应多个 interpreter state）：
```c
/* Full Python runtime state */

typedef struct pyruntimestate {
    /* Is running Py_PreInitialize()? */
    int preinitializing;

    /* Is Python preinitialized? Set to 1 by Py_PreInitialize() */
    int preinitialized;

    /* Is Python core initialized? Set to 1 by _Py_InitializeCore() */
    int core_initialized;

    /* Is Python fully initialized? Set to 1 by Py_Initialize() */
    int initialized;

    /* Set by Py_FinalizeEx(). Only reset to NULL if Py_Initialize() is called again. */
    _Py_atomic_address _finalizing;

    struct pyinterpreters {
        PyThread_type_lock mutex;
        PyInterpreterState *head;
        PyInterpreterState *main;
        int64_t next_id;
    } interpreters;

    unsigned long main_thread;

    struct _ceval_runtime_state ceval;
    struct _gilstate_runtime_state gilstate;

    PyPreConfig preconfig;

    // ... less interesting stuff for now
} _PyRuntimeState;
```

值得一提的是，内置类型例如 `int` 初始化时，会将部分小整数放入 `small_ints` 缓存中，供未来复用。`float` 则会检测当前机器如何表示浮点数。

下面是一个简单的 float 对象结构体：
```c
typedef struct _object {
    _PyObject_HEAD_EXTRA // for debugging only
    Py_ssize_t ob_refcnt;
    PyTypeObject *ob_type;
} PyObject;

typedef struct {
    PyObject ob_base; // expansion of the PyObject_HEAD macro
    double ob_fval;
} PyFloatObject;
```

Note：在 python 中，一切都是对象，甚至「类型」以及「类型的类型」都是对象（`PyTypeObject`）。


### 运行 Python 程序（编译 & 解释）

接上一章，调用 `pymain_main -> Py_RunMain()` 方法：1）运行代码 2）结束初始化释放内存 3）调用退出函数

```c
int
Py_RunMain(void)
{
    int exitcode = 0;

    pymain_run_python(&exitcode);

    if (Py_FinalizeEx() < 0) {
        /* Value unlikely to be confused with a non-error exit status or
           other special meaning */
        exitcode = 120;
    }

    // Free the memory that is not freed by Py_FinalizeEx()
    pymain_free();

    if (_Py_UnhandledKeyboardInterrupt) {
        exitcode = exit_sigint();
    }

    return exitcode;
}
```

python 具备多种运行的方式：每种对应一个函数入口。
- `./cpython/python.exe`
- `echo "..." | python`
- `python -c "..."`
- `python -m module`
- `python script.py` -> `pymain_run_file()`
- `python <dir>` -> `__main__.py`

```c
static void
pymain_run_python(int *exitcode)
{
    ...
    
    // Run Python depending on the mode of invocation (script, -m, -c, etc.)
    if (config->run_command) {
        *exitcode = pymain_run_command(config->run_command, &cf);
    }
    else if (config->run_module) {
        *exitcode = pymain_run_module(config->run_module, 1);
    }
    else if (main_importer_path != NULL) {
        *exitcode = pymain_run_module(L"__main__", 0);
    }
    else if (config->run_filename != NULL) {
        *exitcode = pymain_run_file(config, &cf);
    }
    else {
        *exitcode = pymain_run_stdin(config, &cf);
    }
    
    ...
}
```

以 `python script.py` 为例：
- 首先判断 pyc 文件是否存在，是否用当前 cpython 版本进行的编译，如果是则直接执行 pyc 文件（code object），直接跳过源码编译阶段。
- 否则调用 `PyRun_FileExFlags` 函数，进入编译阶段

```c
int
PyRun_SimpleFileExFlags(FILE *fp, const char *filename, int closeit,
                        PyCompilerFlags *flags)
{
    ... 
    
    // Check if a .pyc file is passed
    len = strlen(filename);
    ext = filename + len - (len > 4 ? 4 : 0);
    if (maybe_pyc_file(fp, filename, ext, closeit)) {
        FILE *pyc_fp;
        /* Try to run a pyc file. First, re-open in binary */
        if (closeit)
            fclose(fp);
        if ((pyc_fp = _Py_fopen(filename, "rb")) == NULL) {
            fprintf(stderr, "python: Can't reopen .pyc file\n");
            goto done;
        }

        if (set_main_loader(d, filename, "SourcelessFileLoader") < 0) {
            fprintf(stderr, "python: failed to set __main__.__loader__\n");
            ret = -1;
            fclose(pyc_fp);
            goto done;
        }
        v = run_pyc_file(pyc_fp, filename, d, d, flags);
    } else {
        /* When running from stdin, leave __main__.__loader__ alone */
        if (strcmp(filename, "<stdin>") != 0 &&
            set_main_loader(d, filename, "SourceFileLoader") < 0) {
            fprintf(stderr, "python: failed to set __main__.__loader__\n");
            ret = -1;
            goto done;
        }
        v = PyRun_FileExFlags(fp, filename, Py_file_input, d, d,
                              closeit, flags);
    }
```


如果是 .py 文件，`PyRun_SimpleFileExFlags` 进而触发 peg parser 的执行，生成 AST -> code object，并最终执行：

```ascii
如果是 .py
└─ PyRun_FileExFlags()
   ├─ 创建 PyArena
   ├─ parser
   │  └─ source code -> AST
   │
   └─ run_mod()
      ├─ PyAST_CompileObject()
      │  └─ AST -> code object
      │
      └─ run_eval_code_obj()
         └─ PyEval_EvalCode()
            └─ _PyEval_EvalCode()
               ├─ 创建 PyFrameObject
               │  └─ code object + globals / locals
               │
               ├─ 初始化 frame
               │  └─ args / defaults / closure
               │
               ├─ 如果是 generator / coroutine
               │  └─ 返回 generator/coroutine object
               │     └─ frame 暂停保存在对象里
               │
               └─ 否则进入 _PyEval_EvalFrame()
                  └─ _PyEval_EvalFrameDefault()
                     └─ evaluation loop
                        └─ 逐条执行 bytecode
```

最终 `_PyEval_EvalFrameDefault` 对应 [Python/ceval.c](https://github.com/python/cpython/blob/57c6cb5100d19a0e0218c77d887c3c239c9ce435/Python/ceval.c#L1741) 中的代码:

```c
   PyObject *
   _PyEval_EvalFrameDefault(PyThreadState *tstate, PyFrameObject *f, int throwflag)
   {
       ...
       for (;;) {
           ...
           opcode = _Py_OPCODE(*next_instr);
           oparg = _Py_OPARG(*next_instr);
           next_instr++;

           switch (opcode) {
               case LOAD_CONST:
                   ...
                   break;

               case LOAD_FAST:
                   ...
                   break;

               case CALL_FUNCTION:
                   ...
                   break;

               case RETURN_VALUE:
                   ...
                   return retval;
           }
       }
   }
```

## 总结

最后让我们尝试关联前两章的概念：
1. 编译生成 code object
2. 运行创建 frame 放入 thread state 的 call stack 中
3. ==evaluation loop== 从 frame 中一条条运行 bytecode，同时更新 frame 状态

```ascii
Compile time                            | Runtime
----------------------------------------|-----------------------------------------
source code                             | runtime state
└─ tokenizer / parser                   | └─ interpreter state / VM
  └─ AST                                |    └─ thread state
     └─ symbol table / CFG / assembler  |       └─ call stack
        └─ code object                  |          └─ frame
           ├─ bytecode                  |             ├─ code object -> 包含bytecode
           ├─ consts                    |             ├─ instruction ptr
           ├─ names                     |             ├─ value stack
           └─ metadata                  |             ├─ locals / globals
                                        |             └─ exception state
```

<u>谁来负责依次创建和运行 frame 呢？</u> evaluation loop 仅负责执行当前 frame，如果 frame1 碰到函数调用，就会把新的 frame2 push 到 call stack 中，执行完后回到 frame1。

## 参考
1. https://devguide.python.org/getting-started/setup-building/index.html#compiling
2. https://tenthousandmeters.com/blog/python-behind-the-scenes-3-stepping-through-the-cpython-source-code/

