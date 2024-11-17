---
title: SQLAlchemy 与 Pyright 相爱相杀的故事
date: 2023-05-03 21:05:49
tags:
categories:
- PYTHON
---

Pyright 作为一款功能强大的静态类型检查器，深得我心。但近日使用 SQLAlchemy 时，Pyright 提示的类型检查报错，却让我陷入困扰。

本篇文章将简单分享解决思路以及背后的原理。

<!--more-->

## 背景
假设有如下 python 代码：
```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)


def print_username(name: str):
    print(name)


if __name__ == "__main__":
    user = User(id=42, name=42)
    print_username(user.name)
```

Pyright 认真负责给出如下报错提示：`[Pyright reportGeneralTypeIssues] Argument of type "Column[str]" cannot be assigned to parameter "name" of type "str" in function "print_username" [E]`
![](/images/blog/2021-09-04-jvm-note/16831164151732.jpg)


## 解决办法
很简单，本地安装 [sqlalchemy-stubs](https://pypi.org/project/sqlalchemy-stubs/) 后，报错消失。

Pyright 可正确识别 `user` 实例的 `name` 属性为 `str` 类型，而不是代码定义的 `Column` 类型。

小技巧：无需引用，直接使用 `reveal_type` 方法调试类型：
![](/images/blog/2021-09-04-jvm-note/16831174091876.jpg)


## WHY???
### 为什么安装 stub 包后，无需任何配置，即可直接对 pyright 生效？
> Try to resolve using **stubs or inlined types found within installed packages**.
> 
> For a given package, try to resolve first using a **stub package**. Stub packages, as defined in [PEP 561](https://www.python.org/dev/peps/pep-0561/#type-checker-module-resolution-order), are named the same as the original package but with “-stubs” appended.

参考 [pyright 文档](https://github.com/microsoft/pyright/blob/main/docs/import-resolution.md)，默认根据包名 `-stubs` 后缀自动识别。

### 为什么安装 stub 包后，可正确识别 name 的类型？
首先安装前，pyright 根据 sqlalchemy 的源代码，解析对应的类型，自然将 `user.name` 当作 `Column` 类型。安装 sqlalchemy-stubs 后，优先通过 stub 中定义的接口类型解析。

具体实现参考 `sqlalchemy-stubs/sql/schema.pyi::Column`，关键代码如下。

简而言之类似 java 中的泛型（generics），当 Column 的类型定义为 `Type[TypeEngine[_T]]` 时，强制约束返回的类型为 `T`。
```python
_T = TypeVar('_T')

class Column(SchemaItem, ColumnClause[_T]):
    __visit_name__: str = ...
    key: str = ...
    primary_key: bool = ...
    nullable: bool = ...
    default: Optional[Any] = ...
    server_default: Optional[Any] = ...
    server_onupdate: Optional[FetchedValue] = ...
    index: Optional[bool] = ...
    unique: Optional[bool] = ...
    system: bool = ...
    doc: Optional[str] = ...
    onupdate: Optional[Any] = ...
    autoincrement: Union[bool, str] = ...
    constraints: Set[Constraint] = ...
    foreign_keys: Set[ForeignKey] = ...  # type: ignore  # incompatible with ColumnElement.foreign_keys
    info: Optional[Mapping[str, Any]] = ...
    comment: Optional[str] = ...
    table: Table = ...  # TODO: double-check this.

    # Now without a name argument.
    @overload
    def __init__(self, type_: Type[TypeEngine[_T]], *args: Any, autoincrement: Union[bool, str] = ...,
                 default: Any = ..., doc: str = ..., key: str = ..., index: bool = ..., info: Mapping[str, Any] = ...,
                 nullable: bool = ..., onupdate: Any = ..., primary_key: bool = ..., server_default: Any = ...,
                 server_onupdate: Union[FetchedValue, FunctionElement] = ..., quote: Optional[bool] = ..., unique: bool = ...,
                 system: bool = ..., comment: str = ...) -> None: ...
    
    @overload
    def __get__(self, instance: None, owner: Any) -> Column[_T]: ...
    @overload
    def __get__(self, instance: object, owner: Any) -> _T: ...
```


## 参考
1. https://microsoft.github.io/pyright/#/type-concepts?id=debugging-types
2. https://github.com/dropbox/sqlalchemy-stubs/issues/140
3. https://github.com/microsoft/pyright/blob/main/docs/import-resolution.md