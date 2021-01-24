---
title: 如何对一棵树进行可视化（python anytree 简易实现）
tags:
  - python
date: 2021-01-24 15:10:08
---


Python 中有个很酷的第三方包叫做 [anytree](https://github.com/c0fec0de/anytree)，全名 Any Python Tree Data，i.e. 期望用来表示任何树的数据结构。   

而其中的可视化功能，每次都令人印象深刻。这篇文章简单分享，个人解决问题的思考路径 & 简易实现～

<!-- more -->

```python
>> ...
>> r = RenderTree(root)
>> print(r)
Node('/A')
├── Node('/A/B')
│   ├── Node('/A/B/D')
│   │   └── Node('/A/B/D/F')
│   │       └── Node('/A/B/D/F/G')
│   └── Node('/A/B/E')
└── Node('/A/C')
```

# 1 问题拆解

一开始看到这个问题，可能有些没有头绪，但有没有可能对该问题进行分解🤔   
.   
.   
.   
.   
.   
.      
.   
.   
.

**一棵树的可视化** ，分解为：

1. 每一行的显示，由三个部分组成
    1. 填充(`│   `)
    2. 前缀(`├── ` or `└── `)
    3. 节点自身
2. 从上至下打印的顺序（深度优先遍历）

# 2 实现

## 2.1 定义「行」的数据结构
行(Row)与节点一一对应，其中包含两个元素：

1. `node` 代表树的节点 
2. `continues` 中每个元素表示：根节点至当前节点路径中的每个节点，**是不是对应层级中的最后一位**。 用来生成每行的前缀

```python
from dataclasses import dataclass
from typing import List

from anytree import Node

LAST_NODE_PRE = "╰── "
NODE_PRE = "├── "

INDENT = "│   "
BLANK = "    "


@dataclass
class Row:
    node: Node
    continues: List[int]

    @property
    def pre(self):
        # 根结点特殊处理
        if len(self.continues) == 0:
            return ""

        indent = "".join([INDENT if x else BLANK for x in self.continues[:-1]])
        branch = NODE_PRE if self.continues[-1] else LAST_NODE_PRE
        return indent + branch

    def __str__(self):
        return self.pre + self.node.name
```

## 2.2 深度遍历(DFS)

一般会使用 `stack` 先入后出的特性，这里简单利用生成器，即 `yield` 关键字实现一版：


```python
from typing import Tuple
from anytree import Node
from row import Row


def dfs(root: Node, continues: Tuple[bool] = None):
    if continues is None:
        continues = tuple()

    yield Row(root, continues)

    if not root.children:
        return
    for child in root.children:
        is_last = root.children[-1] == child
        for grandchild in dfs(child, continues + (not is_last,)):
            yield grandchild
```

## 2.3 初始化树&打印


```python
from anytree import Node, RenderTree
from render import dfs


def init_tree():
    a = Node("A")
    b = Node("B", parent=a)
    c = Node("C", parent=a)

    d = Node("D", parent=b)
    e = Node("E", parent=b)

    f = Node("F", parent=d)
    g = Node("G", parent=f)

    return a


if __name__ == '__main__':
    root = init_tree()
    for x in dfs(root):
        print(x)
    """
    A
    ├── B
    │   ├── D
    │   │   ╰── F
    │   │       ╰── G
    │   ╰── E
    ╰── C
    """
```

# 总结
具体的实现在对**问题拆解**后，设计好对应的**数据结构和算法**，就能比较容易清晰的实现：

当然你也可以直接查看 anytree 的源码：`anytree.render.RenderTree`，其中有更多可扩展性的设计，例如样式主题，打印的模式等。

🍻cheers! have a gooood day~~

