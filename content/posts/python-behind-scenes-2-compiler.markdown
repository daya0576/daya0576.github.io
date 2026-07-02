---
title: "读 Python behind the scenes #2: how the CPython compiler works"
date: 2026-06-07T15:06:31+08:00
toc: true
categories:
- Python behind the scenes
- Python
series:
- CPython
---

[上一章](/blog/20260530/read-python-behind-the-scenes-1-cpython-vm/)中，我们讨论了 Python 代码运行的三部曲。这一章我们将进一步深入理解 python 编译器是如何生产出最终执行所需的 code object（bytecode）。

> https://tenthousandmeters.com/blog/python-behind-the-scenes-2-how-the-cpython-compiler-works/

## 什么是 CPython compiler？

传统编译器（例如 [LLVM](https://aosabook.org/en/v1/llvm.html)），目标是同时支持多种源代码，通过同一套 intermediate representation (IR) 解耦后，编译为不同指令集的机器码：
```text
   C/C++ -> Clang frontend  ┐
   Rust  -> rustc frontend  ├──> LLVM IR -> x86/ARM/RISC-V machine code
   Swift -> Swift frontend  ┘
 ```

而 CPython 编译器，只需要处理 Python 一种源代码，但还是按照传统的「三阶段」进行设计：

{{< figure src="/images/blog/global/cpython-capture2.svg" alt="传统编译器（多前端 + LLVM IR + 多后端）与 CPython 编译器（单前端 + AST + 单后端）的三阶段架构对比" caption="传统编译器 vs CPython 编译器" >}}

## 总览

上图中编译器由两大块组成（对应接下来两章节）：
1. **源代码 -> AST**：frontend 接收 Python 代码生成 AST（核心是 parser）
2. **AST -> bytecode**：backend 进而将 AST 转化为 code object（bytecode 保存在 code object 的一个属性中）。所以从某种意义上来说，CPython 编译器又可以称之为“code object 生成器”。

举个更有体感的例子：下面常见的 Python 代码语法错误异常，就是由 front 中的 parser，在处理时抛出的（「语法」具体是什么将在下文详细展开）：

```python
x = y = = 12
        ^
SyntaxError: invalid syntax
```

## 源代码 -> AST

> https://github.com/we-like-parsers/pegen_experiments
> https://www.youtube.com/watch?v=QppWTvh7_sI

⚠️ 原文过于晦涩难懂.. 尝试配合使用 Guido 写的 ToyParser 理解并解释如何将 源代码 转化为 AST 的。

### 1 旧 parser

> 😂Guido 描述 pgen（旧 parser） 的另一个优点：由于它本身的各种限制，成为了很好拒绝部分新特性的“借口” --- 你希望引入的语法用 pgen 太难实现了 ------ 是否也意味着对于普通人太那理解了。

前文提到从 Python3.9 开始，CPython 中同时存在两个 parser（下文简单称之为 新 parser & 旧 parser）。CPython 默认使用新 parser，当然也可以通过 `-X oldparser` 参数开启旧 parser。但从 Python3.10 开始，旧 parser 被完全的移除。

（略）

### 2 tokenizer

Python 是一门复杂的语言，但语法相对简单，仅包含 63 个 TOKEN（[Grammar/Tokens](https://github.com/python/cpython/blob/0bbaf5de9744ae1acea3e2c9ad2257d1cc68e847/Grammar/Tokens#L1)）。

下面的输出（tokens）就是 parser 眼中的代码：
- tokenizer 每次读一个字符，并尝试匹配一个完整 token（w → wh → whi → whil → while）。
- parser 每次向 tokenizer 请求并处理一个 token。
```
def x_plus(x):
    if x >= 0:
        return x
    return 0

$ python -m tokenize example2.py 
0,0-0,0:            ENCODING       'utf-8'        
1,0-1,3:            NAME           'def'          
1,4-1,10:           NAME           'x_plus'       
1,10-1,11:          OP             '('            
1,11-1,12:          NAME           'x'            
1,12-1,13:          OP             ')'            
1,13-1,14:          OP             ':'            
1,14-1,15:          NEWLINE        '\n'           
2,0-2,4:            INDENT         '    '         
2,4-2,6:            NAME           'if'         
...
```

P.S. tokenizer 是如何处理不同的编码呢？首先通过 `io` 模块检测编码类型，统一把源码解析为 unicode 文本。但 CPython 内部，最终都会统一转成 UTF-8 处理。

P.S. tokenizer 会将缩进转化为 `INDENT`/`DEDENT`（不包括例如多行括号内部的缩进），方便下个阶段 parser 处理（利用缩进栈维护上下文）。

### 3 新 parser

新的 parser 对应的新的语法：[Parsing Expression Grammar](https://en.wikipedia.org/wiki/Parsing_expression_grammar) (PEG)。PEG 最早由 Bryan Ford 在 2004 年提出，作为一种描述语言的工具，可以根据语法描述，自动生成 parser 代码。

但在 CPython 中，Guido 重头实现 `parser generator` 的逻辑（号称 just for fun）。

```
                                                tokens
                                                  | 
                                                  v 
PEG grammar ---> [ parser generator ] ---> [ Syntax parser ]
                                                  |
                                                  v
                                                 tree
```

#### 3.1 PEG grammar

简易版语法解释👇：
1. 每行代表一条语法规则（名字：内容）：`|` 表示多个备选项。例如第一行 `statement` 可以是赋值语句、表达式语句或 `if` 语句。
    - expr 表达式支持加减法：`x+1`，`x-1`，`x+y-2`，... 
    - 同时支持==左递归==：
        - `expr '+' term | expr '-' term | term`
        - `x - y - z` -> `(x - y) - z`。
2. `NAME` 和 `NUMBER` 是提前定义好的 token；单引号 `'+'` 和 `'if'` 是 grammar 中的 literal token，参考 [cpython/Grammar/Tokens](https://github.com/python/cpython/blob/871047dbb82ab9a89f364a4ec62cf05f94706124/Grammar/Tokens)。

```
statement: assignment | expr | if_statement
expr: expr '+' term | expr '-' term | term
term: term '*' atom | term '/' atom | atom
atom: NAME | NUMBER | '(' expr ')'
assignment: target '=' expr
target: NAME
if_statement: 'if' expr ':' statement
```

挑战：在解析语法 `answer = 42` 时，是逐个 TOKEN 解析的（`answer` -> `=` -> `42`），但在下面的例子中，解析到第一个 token `answer` 时，无法判断是 `assignment` 还是 `expr`。所以 Guido 引入了 infinite lookahead buffer，也就是说不用只看一个 token 做决定，可以先尝试一条分支（无限个 token），失败了就回退原始位置，再试另一条（==backtracking==）。

```python
class Tokenizer:
    def __init__(self, tokengen):
        """Call with tokenize.generate_tokens(...)."""
        self.tokengen = tokengen
        self.tokens = []
        self.pos = 0
    def mark(self):
        return self.pos
    def reset(self, pos):
        self.pos = pos
    def get_token(self):
        token = self.peek_token()
        self.pos += 1
        return token
    def peek_token(self):
        if self.pos == len(self.tokens):
            self.tokens.append(next(self.tokengen))
        return self.tokens[self.pos]
```

tradeoff：30 年前内存非常珍贵，但现在我们选择在解析前将整个程序加载到内存中，挣脱内存的束缚，最终让一切变得更加简单。

P.S. 新 parser 的生成流程中，跳过了 parse tree，直接生成 AST 树。
- 旧 parser：tokens -> (old parser) -> parse tree -> AST -> bytecode
- 新 parser：tokens -> (PEG parser) -> AST -> bytecode

#### 3.2 parser generator

基于上面的三个挑战和思路，Guido 决定自己用 python 实现了一套 PEG 语法解析的逻辑（输入语法 grammar，自动输出生成 parser）。

分解为两步：
##### 3.2.1 语法 -> 结构化数据

```
[
  Rule('statement', [['assignment'], ['expr'], ['if_statement']]),
  Rule('expr', [['expr', "'+'", 'term'],
                ['expr', "'-'", 'term'],
                ['term']]),
  ...
]
```

##### 3.2.2 结构化数据 -> parser
最简陋版本的 parser generator：
```
def generate_parser_class(rules):
    print(f"class ToyParser(Parser):")
    for rule in rules:
        print()
        print(f"    @memoize")
        print(f"    def {rule.name}(self):")
        print(f"        pos = self.mark()")
        for alt in rule.alts:
            items = []
            print(f"        if (True")
            for item in alt:
                if item[0] in ('"', "'"):
                    print(f"            and self.expect({item})")
                else:
                    var = item.lower()
                    if var in items:
                        var += str(len(items))
                    items.append(var)
                    if item.isupper():
                        print("            " +
                              f"and ({var} := self.expect({item}))")
                    else:
                        print(f"            " +
                              f"and ({var} := self.{item}())")
            print(f"        ):")
            print(f"            " +
              f"return Node({rule.name!r}, [{', '.join(items)}])")
            print(f"        self.reset(pos)")
        print(f"        return None")
```

#### 3.3 parser

从下面代码中，不难理解自顶向下，依次解析匹配候选项（通过无限缓冲区持久化复位）：
- `self.mark()` -> `token.mark()`：记录当前的索引位置，开始匹配
- `self.reset()` -> `token.reset()`：匹配失败，回到刚刚标记的位置

```python
class ToyParser(Parser):
    @memoize
    def statement(self):
        pos = self.mark()
        if (True
            and (assignment := self.assignment())
        ):
            return Node('statement', [assignment])
        self.reset(pos)
        if (True
            and (expr := self.expr())
        ):
            return Node('statement', [expr])
        self.reset(pos)
        if (True
            and (if_statement := self.if_statement())
        ):
            return Node('statement', [if_statement])
        self.reset(pos)
        return None
    ...
```

左递归：
- `'+'` -> `self.expect('+')`，代表 尝试读取一个 `+` token，失败会返回 `None` 并进入下一个分支进行匹配。
- `expr` -> `(expr := self.expr())`，尝试解析一个表达式（==递归==）。

```python
@memoize
def expr(self):
    pos = self.mark()
    if (True
        and (term := self.term())
        and self.expect('+')
        and (expr := self.expr())
    ):
        return Node('expr', [term, expr])
```

⚠️注意：普通 PEG parser 无法直接处理左递归（会无限递归 → stack overflow），传统做法是把它改写成等价的迭代形式：
- grammar：`expr: expr '+' term | expr '-' term | term` 
- 改写后： `expr: term ('+' term)*`

而 Guido 在新 parser generator 中实现了 @memoize_left_rec，让我们可以直接按自然的左递归写法去写 grammar，由装饰器在运行时处理左递归。

```python
@memoize_left_rec # 修改了缓存装饰器避免无限 overflow
def expr(self):
   pos = self.mark()
   if (True
       and (expr := self.expr())   # 左递归：(1+2)+3
       and self.expect('+')
       and (term := self.term())
   ):
       return Node('expr', [expr, term]) 
```

### 4 AST

语法抽象树 Abstract syntax tree (AST) 使用树状结构：
1. 作为源代码的一种高级表示，抽象隐藏了很多非必要的信息，例如代码缩进、标点符号，以及其他语法特性。
2. AST 的主要受益者是编译器：让编译器基于结构化的表示，更加简单地生存字节码。除了编译器，其他 Python 工具也会使用 AST：例如 pytest 会修改 AST，以便于在 `AssertionError` 抛出时提供更多信息；Bandit 通过分析 AST 来发现 Python 代码中常见的安全问题。

下面是用 python 标准 [ast](https://docs.python.org/3/library/ast.html) 模块生成的示例：

```shell
# 1 + 2 + 3

# 递归判断：
expr
├── expr
│   ├── expr
│   │   └── term 1
│   └── term 2
└── term 3

# 真实 AST 树（整个 module 作为一个 code block）
➜  tmp python3.12 -m ast xxx.py
Module(
   body=[
      Expr(
         value=BinOp(
            left=BinOp(
               left=Constant(value=1),
               op=Add(),
               right=Constant(value=2)),
            op=Add(),
            right=Constant(value=3)))],
   type_ignores=[])
```

`NUMBER token` 的文本值是如何被转化为数字的？在 ToyParser 示例中，==grammar action== 可以直接计算结果；也是 CPython 中构造 AST 节点的主力军。
```
start: expr NEWLINE { expr }
expr: expr '+' term { expr + term }
    | expr '-' term { expr - term }
    | term { term }
term: NUMBER { float(number.string) }
```

### 5 AST optimization

AST optimizer 层在 CPython 3.7 引入。举个例子：
```
# 优化前
Module
└── Expr
   └── BinOp(Add)
       ├── BinOp(Add)
       │   ├── Constant(1)
       │   └── Constant(2)
       └── Constant(3)

# 优化后（产量折叠 - 避免在运行时重新计算）
Module
└── Expr
   └── Constant(6)
```

## AST -> bytecode

CPython 不认识 AST，需要将它转化为 bytecode 后，再通过 VM 执行。

以赋值语句为例（`x = 1`），它对应的 AST 节点为 `Assign(targets=[Name(id='x', ctx=Store())], value=Constant(value=1))`。如果将它转化为 bytecode，我们需要 `LOAD_CONST` 指令存常量，用 `STORE_NAME` 指令存变量名。但问题在于，赋值时==变量 `x` 无法判断类型==，是方法内的局部变量（`STORE_FAST`），全局变量（`STORE_GLOBAL`），还是闭包变量（`LOAD_DEREF` / `STORE_DEREF`）？

### symbol table
为了解决这个问题，需在在编译前，维护好 symbol table：
1. 一个 `symtable` 对应多个 `_symtable_entry`
2. 每个 `_symtable_entry` 包含 code block 的名字和类型（module, class or function），以及其中变量的作用域和用法。
```c
typedef struct _symtable_entry {
    PyObject_HEAD
    PyObject *ste_id;        /* int: key in ste_table->st_blocks */
    PyObject *ste_symbols;   /* dict: variable names to flags */
    PyObject *ste_name;      /* string: name of current block */
    PyObject *ste_varnames;  /* list of function parameters */
    PyObject *ste_children;  /* list of child blocks */
    PyObject *ste_directives;/* locations of global and nonlocal statements */
    _Py_block_ty ste_type;   /* module, class, or function */
    int ste_nested;      /* true if block is nested */
    unsigned ste_free : 1;        /* true if block has free variables */
    unsigned ste_child_free : 1;  /* true if a child block has free vars,
                                     including free refs to globals */
    unsigned ste_generator : 1;   /* true if namespace is a generator */
    unsigned ste_coroutine : 1;   /* true if namespace is a coroutine */
    unsigned ste_comprehension : 1; /* true if namespace is a list comprehension */
    unsigned ste_varargs : 1;     /* true if block has varargs */
    unsigned ste_varkeywords : 1; /* true if block has varkeywords */
    unsigned ste_returns_value : 1;  /* true if namespace uses return with
                                        an argument */
    unsigned ste_needs_class_closure : 1; /* for class scopes, true if a
                                             closure over __class__
                                             should be created */
    unsigned ste_comp_iter_target : 1; /* true if visiting comprehension target */
    int ste_comp_iter_expr; /* non-zero if visiting a comprehension range expression */
    int ste_lineno;          /* first line of block */
    int ste_col_offset;      /* offset of first line of block */
    int ste_opt_lineno;      /* lineno of last exec or import * */
    int ste_opt_col_offset;  /* offset of last exec or import * */
    struct symtable *ste_table;
} PySTEntryObject;
```

看一个实际的例子：
```python
# example3.py
def func(x):
    lc = [x+i for i in range(10)]
    return lc
```
```shell
>>> from symtable import symtable
>>> f = open('example3.py')
>>> st = symtable(f.read(), 'example3.py', 'exec') # module's symtable entry
>>> 
>>> st.get_children()[1].get_symbols()
[
    <symbol 'x': LOCAL, DEF_PARAM>, 
    <symbol 'lc': LOCAL, USE|DEF_LOCAL>, 
    <symbol 'range': GLOBAL_IMPLICIT, USE>, # 
    <symbol 'i': LOCAL, USE|DEF_LOCAL|DEF_COMP_ITER>
]
```

<u>所以 symbol table 是什么时候生成的呢？</u> AST 生成完毕后，会遍历树，并==为每一个 code block 生成一个 symbol table entry==。

一个有趣的极端例子：在第一次遍历 AST 树时，无法判断 nested 中的 x 是什么类型的变量。为了解决这个问题，CPython 做了第二次的 AST 树遍历。
```python
def top():
    def nested():
        return x + 1
    x = 10
    ...
```

一个新的问题：下面代码中，if 分叉生成的 bytecode 是线性，最终通过跳转来处理 else 逻辑。
```python
if x == 0 or x > 17:
    y = True
else:
    y = False
...

If(
  test=BoolOp(...),
  body=[...],
  orelse=[...]
)
```

但是，在生成 `POP_JUMP_IF_FALSE` 时，else 分支的 code 还没生成，如何知道需要跳转的未来的 index 呢？
```shell
1           0 LOAD_NAME                0 (x)
            2 LOAD_CONST               0 (0)
            4 COMPARE_OP               2 (==)
            6 POP_JUMP_IF_TRUE        16
            8 LOAD_NAME                0 (x)
           10 LOAD_CONST               1 (17)
           12 COMPARE_OP               4 (>)
           14 POP_JUMP_IF_FALSE       22     # 这里

2     >>   16 LOAD_CONST               2 (True)
           18 STORE_NAME               1 (y)
           20 JUMP_FORWARD             4 (to 26)

4     >>   22 LOAD_CONST               3 (False)
           24 STORE_NAME               1 (y)
5     >>   26 ...
```

### basic blocks

为了解决这个问题，编译的时候，会将代码拆分为多个小块（block）并维护跳转关系。直到每个块的大小都生成好后，再计算 bytecode 真实的偏移量。

这里代码块的数据结构就叫做 basic blocks：
- `b_list` 指向所有 blocks。
- `b_next` 表示正常顺序执行时进入的下一个 block；条件/无条件跳转目标由具体跳转指令维护。

```c
typedef struct basicblock_ {
    /* Each basicblock in a compilation unit is linked via b_list in the
       reverse order that the block are allocated.  b_list points to the next
       block, not to be confused with b_next, which is next by control flow. */
    struct basicblock_ *b_list;
    /* number of instructions used */
    int b_iused;
    /* length of instruction array (b_instr) */
    int b_ialloc;
    /* pointer to an array of instructions, initially NULL */
    struct instr *b_instr;
    /* If b_next is non-NULL, it is a pointer to the next
       block reached by normal control flow. */
    struct basicblock_ *b_next;
    /* b_seen is used to perform a DFS of basicblocks. */
    unsigned b_seen : 1;
    /* b_return is true if a RETURN_VALUE opcode is inserted. */
    unsigned b_return : 1;
    /* depth of stack upon entry of block, computed by stackdepth() */
    int b_startdepth;
    /* instruction offset for block, computed by assemble_jump_offsets() */
    int b_offset;
} basicblock;
```

### frame blocks

另一个问题：遇到 `continue` 和 `break` 时，应该跳到哪个 basic block 呢？

引入 frame block（每个类型，对应一种特殊的 basicblock，在外面包了一层，负责 finally “擦屁股”）：
```c
enum fblocktype { WHILE_LOOP, FOR_LOOP, EXCEPT, FINALLY_TRY, FINALLY_END,
                  WITH, ASYNC_WITH, HANDLER_CLEANUP, POP_VALUE };

struct fblockinfo {
    enum fblocktype fb_type;
    basicblock *fb_block;
    /* (optional) type-specific exit or cleanup block */
    basicblock *fb_exit;
    /* (optional) additional information required for unwinding */
    void *fb_datum;
};
```

## 字节码优化

删除了冗余指令，例如永远也执行不到的语句：

```python
def foo():
    return bar
    print("hi")
```

## 总结

流水线小结：
```
# 阶段1：
source code  ->  tokenizer -> tokens
                                 |
                                 v
grammer -> parser generator -> parser -> AST -> AST (optimized)

# 阶段2：
AST -> symbol table
            |
            v
     basic blocks  -> assembler -> code object [bytecode + meta]
        (graph)                      (linear)
```

时间有限，浅浅的带过 CPython 编译的流水线，如果你感兴趣可以进一步深入了解以下话题：


- [ ] **前端（源代码 → AST）**：`@memoize` vs `@memoize_left_rec`：packrat parser 如何用 memoization 把指数级回溯变成线性？Guido 的「seed parsing / grow the seed」算法又是怎么让 PEG 直接支持左递归的？
- [ ] **前端（源代码 → AST）**：PEG grammar 中的 `{ ... }` action 在 CPython 里是如何串起 AST 节点构造的？参考 [`Grammar/python.gram`](https://github.com/python/cpython/blob/main/Grammar/python.gram)。
- [ ] **后端（AST → bytecode）**：frame block 是怎么实现 `break` / `continue` / `return` 在 `try/finally` / `with` 中的正确语义（unwind 顺序、cleanup）？


## 参考
1. https://tenthousandmeters.com/blog/python-behind-the-scenes-2-how-the-cpython-compiler-works/
2. https://aosabook.org/en/v1/llvm.html
3. https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools
4. https://github.com/we-like-parsers/pegen_experiments
5. https://github.com/python/cpython/blob/3.9/Tools/peg_generator/pegen/parser_generator.py
5. https://eli.thegreenplace.net/tag/python-internals

