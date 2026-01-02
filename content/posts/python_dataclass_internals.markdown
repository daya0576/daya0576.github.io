---
title: "Python Dataclass 工作原理"
date: 2026-01-02T10:05:17+08:00
categories:
- Python
- 编程
---

近日 [PyCoder's Weekly](https://pycoders.com/issues/715) newsletter 中看到的一篇好文章，简单分享一下阅读的笔记。

# 基本概念
从下面的代码不难看出，dataclass 作为一个装饰器，接受用户自定义的类 cls 作为参数，进行一顿改动后返回。
```python
def dataclass(cls):
    # Modify cls...
    return cls

@dataclass
class Example:
    Pass
```

上面改动的核心逻辑依赖 `__annotations__` 与 `exec` 方法：
```python
# 1. to get names of the variables and the type hints
print(Example.__annotations__)  # {'name': str, 'age': int}

# 2. to create the methods required for the class
namespace = {}
exec('x = 1', None, namespace)
print(namespace)  # Output: {'x': 1}
```

## 简易版 `__init__`

1. 首先依赖 cls 的 annotations 获取所有变量
2. 通过变量名称，组装 init 方法*字符串*
3. 通过 exec 方法，将上一步字符串生成方法，并最终塞入 cls 中

```python
def _create_fn(cls, name, func):
    ns = {}
    exec(func, None, ns) # {'__init__': <function __init__ at 0x109c12cf0>}
    method = ns[name] 
    setattr(cls, name, method)

def _init_fn(cls, fields): # cls.__annotations__.keys()
    args = ', '.join(fields)

    lines = [fself.{field} = {field}' for field in fields]
    body = '\n'.join(f'  {line}' for line in lines)

    txt = f'def __init__(self, {args}):\n{body}'
    # def __init__(self, first_name, last_name, age):
    #   self.first_name = first_name
    #   self.last_name = last_name
    #   self.age = age

    _create_fn(cls, '__init__', txt)
```

# 总结
文中还提供了其他方法实现的例子（例如 Frozen Argument 与 `__repr__` 等），但由于大同小异便不再赘述，如果读者感兴趣，可以继续阅读[参考](#参考)中的链接。

# 参考
1. https://jacobpadilla.com/articles/python-dataclass-internals 
2. https://github.com/python/cpython/blob/6b9a6c6ec3bbc9795df67b87340e2ea58f42b3d4/Lib/dataclasses.py#L720-L725