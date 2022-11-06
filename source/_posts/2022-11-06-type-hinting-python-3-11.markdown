---
title: Python 3.11 类型注解新特性
tags:
  - Python
date: 2022-11-06 09:51:05
---


第一次接触 java 时是无比震惊的，修改大几百行代码，编译通过直接发布至预发部署后，竟运行的无比丝滑。静态类型的绝对优势，对我的 TDD 价值观都带来了极大的冲击。

万幸 Python 虽然是动态类型语言，但经过多年的发展，[类型注解](https://docs.python.org/3/library/typing.html#relevant-peps)已逐步成熟。刚好十月底 [Python 3.11.0 发布](https://www.python.org/downloads/release/python-3110/)，让我们一起看看又引入了哪些新特性呢？

<!--more-->
![](../images/blog/2021-09-04-jvm-note/16677087604976.jpg)

TOC:
- [**PEP 673**: Self type](#pep-673-https-peps-python-orgpep-0673-self-type引入-self类型)
- [**PEP 646**: Variadic Generics](#pep-646-https-peps-python-orgpep-0646-variadic-generics)
- [**PEP 675**: Arbitrary Literal String Type](#pep-675-https-peps-python-orgpep-0675-arbitrary-literal-string-type)
- [**PEP 655**: Marking individual TypedDict items as required or potentially missing](#pep-655-https-peps-python-orgpep-0655-marking-individual-typeddict-items-as-required-or-potentially-missing)
- [**PEP 681**: Data Class Transforms](#pep-681-https-peps-python-orgpep-0681-data-class-transforms)


---

### [**PEP 673**](https://peps.python.org/pep-0673/): Self type

痛点：15 行 `set_scale` 方法返回基类 `Shape`，若继续调用 16 行 `set_radius` 方法，会导致静态类型检查器报错：提示找不到该方法。

``` python
from __future__ import annotations

class Shape:
    def set_scale(self, scale: float) -> Shape:
        self.scale = scale
        return self

Shape().set_scale(0.5)  # => Shape

class Circle(Shape):
    def set_radius(self, r: float) -> Circle:
        self.radius = r
        return self

Circle().set_scale(0.5)  # *Shape*, not Circle
Circle().set_scale(0.5).set_radius(2.7)
# => Error: Shape has no attribute set_radius
```

解法：引入 `Self` 关键字规避该问题。
``` python
from __future__ import annotations
from typing import Self

class Shape:
    def set_scale(self, scale: float) -> Self:
        self.scale = scale
        return self

class Circle(Shape):
    def set_radius(self, radius: float) -> Self:
        self.radius = radius
        return self
```

---

### [**PEP 646**](https://peps.python.org/pep-0646/): Variadic Generics

痛点：虽然入参已提示为 `Array` 类型（任意维度），但需进一步明确类型为 `Array[int]` or `Array[int, str, float]`
``` python
def add_dimension(arrar: Array): ...
```
解法：新引入 `TypeVarTuple` 关键字代表可变长度的一坨类型（number of types），并支持使用 `*` 关键字展开。
``` python
from __future__ import annotations
from typing import Generic, TypeVar, TypeVarTuple, reveal_type

T = TypeVar("T")
Ts = TypeVarTuple("Ts")
  
class Array(Generic[*Ts]):
    def multiple(self, x: int) -> Array[*Ts]: ...
    def add_dimension(self, x: T) -> Array[*Ts, T]: ...

a: Array[float, int, str] = Array()
reveal_type(a.multiple(2)) # Array[float, int, str]
reveal_type(a.add_dimension(2)) # Array[float, int, str, int]
```

---

### [**PEP 675**](https://peps.python.org/pep-0675/): Arbitrary Literal String Type
痛点：如何规避 sql 注入等问题（特别是 f-string）。

仅通过文档提示用户是远远不够的，有没有可能直接在静态检查中显性提示用户？（#6）
``` python
def run_query(sql: str, *params: object) -> ...:
    ...
  
def caller(name: str):
    # ⚠️存在注入风险，无警告提示
    run_query(f"SELECT * from users where id = {name}")
    # ✅无注入风险
    run_query("SELECT * from users where id = %s", name)
```
解法：新引入 `LiteralString` 关键字，代表仅接受文字字符串类型，实现静态的注入风险异常提示（#8）
``` python
from typing import LiteralString
  
def run_query(sql: LiteralString, *params: object) -> ...:
    ...
  
def caller(name: str):
    # ✅异常提示："str" is incompatible with "LiteralString"
    run_query(f"SELECT * from users where id = {name}")

caller("user123; DROP TABLE users")
```

---

### [**PEP 655**](https://peps.python.org/pep-0655/): Marking individual TypedDict items as required or potentially missing
针对 [PEP 589](https://peps.python.org/pep-0589/) 引入的 `TypedDict`，新增 `Required` & `NotRequired` 关键字。

如下若属性 `year` 标记为必填，静态检查则会直接报错。
``` python
from typing import Required, TypedDict
  
class Movie(TypedDict):
    title: str
    year: Required[int]
  
movie: Movie = {"title": "Blade Runner"} 
    # "year" is required in "Movie"
```

---

### [**PEP 681**](https://peps.python.org/pep-0681/): Data Class Transforms
痛点：第三方库的数据类(例如 Django 中的 ORM model、attr 库等)，各自提供类似 `@dataclass` 的语法，但静态类型解析器不可能一一适配。
```python
import attr

@attr.s(frozen=True)
class Coordinates:
    x: int
    y: int
```

解法：引入了 `dataclass_transform` 提供统一的“协议标准”后，自动“合成”对应的类型注解，让静态类型检查器将第三方库的数据类当作 `dataclass` 一样统一处理，包含：
1. 自动合成 `__init__` 方法
2. 自动合成 `__eq__`, `__ne__`, `__lt__` 等魔法方法（可选）
3. 支持 `frozen` 选项的静态解析，字段是否不可变
4. 支持 `field specifiers`，e.g. 字段是否提供了默认值

举个例子：
``` python
from typing import dataclass_transform

@dataclass_transform()
class ModelBase:
    ...

class CustomerModel(ModelBase, frozen=True):
    id: int
    name: str

c = CustomerModel()
    # ERROR: Arguments missing for parameters "id", "name"
c.name = "foo"
    # ERROR: Cannot assign member "name" for type "CustomerModel"
    #          "CustomerModel" is frozen
```

题外话  
- 震惊1：[pyright 项目](https://github.com/microsoft/pyright)中天天吭哧吭哧提交代码，辛勤认真回复 issue 的维护者 [Eric Traut](https://github.com/erictraut)，竟然是微软的 Technical Fellow
- 震惊2：无意中搜索到，该 PEP 681 proposal 的初心是为了解决 pyright 无法正确解析 attr 库静态类型的问题（[#146](https://github.com/microsoft/pyright/issues/146)），而作者就是 Eric ... https://github.com/microsoft/pyright/discussions/1782  
![](../images/blog/2021-09-04-jvm-note/16677087604976.jpg)

