---
title: "读 Python behind the scenes #6: how Python object system works"
date: 2026-09-06T09:37:20+08:00
categories:
- Python behind the scenes
- Python
series:
- CPython
---

![A7B8DA89-597C-4297-BC23-E4CC882BA89C_1_105_c](/images/blog/global/A7B8DA89-597C-4297-BC23-E4CC882BA89C_1_105_c.jpeg)

碎碎念：上周六参加了 pycon 2026，令人印象深刻的是：语言特性的分会场有两位高中生嘉宾；最火热的话题是 free threading。但相比 Agent 分会场的座无虚席，这边显得过分冷清，倒是令人嘘唏。

---

> https://tenthousandmeters.com/blog/python-behind-the-scenes-6-how-python-object-system-works/

从第一天学习 Python 开始，我们便知道 Python 中万物皆对象，这篇文章将介绍 Python 对象的实现原理（cpython3.9）。

## 背景

想象下面的一段代码中在 cpython 中是怎么处理的呢？第一时间映入你脑中的大概率是 `__add__()` 方法。

```python
def f(x):
    return x + 7
```

然而，实际情况会稍微复杂一点，因为 `x` 可能是一个类，也可能是一个 builtin type int ------ 也就是说不会调用任何魔术方法（special methods）。

## Python 对象与类型
在追踪源码前，先了解 ==Python 对象== 与 ==Python 类型== 在 cpython 中的定义：

### PyObject

```c
typedef struct _object {
    _PyObject_HEAD_EXTRA    // macro 宏 - 供调试使用
    Py_ssize_t ob_refcnt;   // 引用计数
    PyTypeObject *ob_type;  // 对象类型
} PyObject;
```

float 对象定义的例子：
```c
typedef struct {
    PyObject ob_base;
    double ob_fval;
} PyFloatObject;
```

### PyTypeObject
万物皆对象的一个好处：VM 不需要去写一堆 if/else 判断类型，直接调用「类型」 `PyTypeObject` 已经定义的操作执行。

简而言之，「类型」不仅仅只定义了类型，还具体定义了 python 对象的「行为」：
```c
struct _typeobject {
    // 类型本质上也是一个 python object
    PyVarObject ob_base;
    ...
    // 类型定义一组数值操作，例如 相加/相减/...
    PyNumberMethods *tp_as_number;
    ...
};
```
`PyNumberMethods` 定义了行为的具体实现：
```c
typedef struct {
    binaryfunc nb_add;
    binaryfunc nb_subtract;
    binaryfunc nb_multiply;
    ...
} PyNumberMethods;
```

## BYTECODE

按照惯例，从 bytecode 开始，看看 VM 具体的执行逻辑：

1. `LOAD_FAST`：首先将 `x` 的 value 放入 value stack 中
2. `LOAD_CONST`：同上将 `7` 常量放入 stack
3. `BINARY_ADD`：将前两个值从 stack 中 pop 出来，相加后，放回 stack
4. `RETURN_VALUE`：最终将值从 stack 中 pop 并返回

```shell
$ python -m dis f.py
...
  2           0 LOAD_FAST                0 (x)
              2 LOAD_CONST               1 (7)
              4 BINARY_ADD
              6 RETURN_VALUE
```

P.S. `BINARY_ADD` ------ 对于 VM 而言，不管是变量 `x` 还是常量 `7`，都是 Python 对象（`PyObject`），所以 VM 只需让不通类型的对象来执行操作，例如 int 类型自己知道如何相加 integers。

## BINARY_ADD

下面是 `BINARY_ADD` opcode 在 [Python/ceval.c](https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1684) 中的定义

```c
case TARGET(BINARY_ADD): {
    PyObject *right = POP();
    PyObject *left = TOP();
    PyObject *sum;
    /* NOTE(haypo): Please don't try to micro-optimize int+int on
        CPython using bytecode, it is simply worthless.
        See http://bugs.python.org/issue21955 and
        http://bugs.python.org/issue10044 for the discussion. In short,
        no patch shown any impact on a realistic benchmark, only a minor
        speedup on microbenchmarks. */
    if (PyUnicode_CheckExact(left) &&
                PyUnicode_CheckExact(right)) {
        // 1. String 的特殊优化（fast path）
        // >>> output = "abc"
        // >>> output += "def"                                                                                                
        // 'abcdef'
        sum = unicode_concatenate(tstate, left, right, f, next_instr);
        /* unicode_concatenate consumed the ref to left */
    }
    else {
        // 2. 主流的入口
        sum = PyNumber_Add(left, right);
        Py_DECREF(left);
    }
    Py_DECREF(right);
    SET_TOP(sum);
    if (sum == NULL)
        goto error;
    DISPATCH();
}
```

## PyNumber_Add

继续追踪 `PyNumber_Add` 的实现：
```c
PyObject *
PyNumber_Add(PyObject *v, PyObject *w)
{
    // 1. 尝试数字相加 -> nb_add
    PyObject *result = binary_op1(v, w, NB_SLOT(nb_add));
    
    // 2. 尝试序列相拼 -> sq_concat
    if (result == Py_NotImplemented) {
        PySequenceMethods *m = Py_TYPE(v)->tp_as_sequence;
        Py_DECREF(result);
        if (m && m->sq_concat) {
            return (*m->sq_concat)(v, w);
        }
        result = binop_type_error(v, w, "+");
    }
    
    return result;
}
```

## binary_op1

进一步追踪 `binary_op1()` ------ 这一步主要决策调用 a 还是 b 的 `nb_add`

```c
static PyObject *
binary_op1(PyObject *v, PyObject *w, const int op_slot)
{
    PyObject *x;
    binaryfunc slotv = NULL;
    binaryfunc slotw = NULL;

    // 假设执行 a + b：
    // v = a，w = b，op_slot 用于定位具体操作（例如 nb_add）。
    
    // a 和 b 类型相同 -> slotv = type(a) 的 nb_add
    if (Py_TYPE(v)->tp_as_number != NULL)
        slotv = NB_BINOP(Py_TYPE(v)->tp_as_number, op_slot);
    // a 和 b 类型不同 -> slotw = type(b) 的 nb_add
    if (!Py_IS_TYPE(w, Py_TYPE(v)) &&
        Py_TYPE(w)->tp_as_number != NULL) {
        slotw = NB_BINOP(Py_TYPE(w)->tp_as_number, op_slot);
        if (slotw == slotv)
            slotw = NULL;
    }
    
    if (slotv) {
        // 1. 如果 b 的类型是 a 类型的子类，优先调用子类 b 的实现
        if (slotw && PyType_IsSubtype(Py_TYPE(w), Py_TYPE(v))) {
            x = slotw(v, w);
            if (x != Py_NotImplemented)
                return x;
            Py_DECREF(x); /* can't do it */
            slotw = NULL;
        }
        // 2. 默认尝试左操作数 a 的实现。
        x = slotv(v, w);
        if (x != Py_NotImplemented)
            return x;
        Py_DECREF(x); /* can't do it */
    }
    // 3. 尝试右操作数 b 的 slot（i.e. a 没有实现 slot）
    if (slotw) {
        x = slotw(v, w);
        if (x != Py_NotImplemented)
            return x;
        Py_DECREF(x); /* can't do it */
    }
    Py_RETURN_NOTIMPLEMENTED;
}
```

## nb_add

两种定义定义/创建「类型」的方式，决定了最终不同的底层实现：

### 1）静态定义的类型

例如内置类型 float：
```c
PyTypeObject PyFloat_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "float",
    sizeof(PyFloatObject),
    0,
    (destructor)float_dealloc,                  /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    ...
    &float_as_number,                           /* tp_as_number */
    ...
};
```

通过 `tp_as_number` 变量定义加减乘除操作：
```c
static PyNumberMethods float_as_number = {
    float_add,          /* nb_add */
    float_sub,          /* nb_subtract */
    float_mul,          /* nb_multiply */
    // ... more number slots
};
```

`nb_add` 的具体实现：
```c
static PyObject *
float_add(PyObject *v, PyObject *w)
{
    double a,b;
    CONVERT_TO_DOUBLE(v, a);
    CONVERT_TO_DOUBLE(w, b);
    a = a + b;
    return PyFloat_FromDouble(a);
}
```

### 2）动态创建的类型

参考以前的两篇文章：
- [浅谈 Python Metaclass（上）：type 与 object 原理介绍](/blog/20201122/python-type-and-object/)
- [浅谈 Python Metaclass（下）：Django ORM 的应用](/blog/20201122/metaclass-with-django-orm/)

我们都知道一个 instance 由 python class 创建，而一个 class 本身则是由 metaclass 实例化得到。当我们定义 `class A: ...` 只需要一行代码，是因为 cpython 提前定义了一个内置的：`PyType_Type` ------ 也就是 metaclass `type` 的底层实现！

```c
PyTypeObject PyType_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "type",                                     /* tp_name */
    sizeof(PyHeapTypeObject),                   /* tp_basicsize */
    ...
    // type()
    (ternaryfunc)type_call,                     /* tp_call */
    type_init,                                  /* tp_init */
    type_new,                                   /* tp_new */
    ...
};
```

具体步骤：
```
class A: ...  -> builtins.__build_class__() -> type(name, bases, namespace)

type()
  -> PyType_Type.tp_call 
    -> PyType_Type.tp_new // create new class object (PyHeapTypeObject)
    -> PyType_Type.tp_init 
      -> class A
```

#### 魔术方法

了解 class 定义创建的原理后，让我们继续探索最后一个问题：魔术方法 `__add__` 与底层的 slot `nb_add` 到底是如何关联的？

```python
class A:
    def __add__(self, other):
        ...
```

简而言之，cpython 在，维护了一张映射表：
1. 定义阶段：`A.__add__ -> slotdefs -> nb_add = slot_nb_add`
2. 运行阶段：`a + b -> nb_add -> slot_nb_add (A.__add__)`

```c
#define TPSLOT(NAME, SLOT, FUNCTION, WRAPPER, DOC) \
    {NAME, offsetof(PyTypeObject, SLOT), (void *)(FUNCTION), WRAPPER, \
     PyDoc_STR(DOC)}

static slotdef slotdefs[] = {
    // ...
    BINSLOT("__add__", nb_add, slot_nb_add, "+"),
    RBINSLOT("__radd__", nb_add, slot_nb_add,"+"),
    // ...
}
```

## 总结

```
a + b
  -> BINARY_ADD
  -> PyNumber_Add(a, b)
  -> binary_op1(a, b, NB_SLOT(nb_add)) 
                      ^ slot offset

  -> Py_TYPE(a/b) -> PyTypeObject.tp_as_number + offset -> nb_add
  
      -> float_add // built-in type
      or
      -> __add__() // user-defined class
```
