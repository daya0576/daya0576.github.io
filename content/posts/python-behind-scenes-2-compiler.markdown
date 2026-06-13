---
title: "读 Python behind the scenes #2: how the CPython compiler works"
date: 2026-06-07T15:06:31+08:00
draft: true
categories:
- Python
- CPython
series:
- Python behind the scenes
---



> https://tenthousandmeters.com/blog/python-behind-the-scenes-2-how-the-cpython-compiler-works/

## 什么是 CPython compiler？

传统编译器，例如 [LLVM](https://aosabook.org/en/v1/llvm.html)，目标是通过解耦同时支持多种源代码，并编译为不同指令集的机器码：
```text
   C/C++ -> Clang frontend  ┐
   Rust  -> rustc frontend  ├──> LLVM IR -> LLVM optimizer -> x86/ARM/RISC-V machine code
   Swift -> Swift frontend  ┘
 ```

而 CPython 编译器，虽然只需要处理 Python 一种源代码，但还是按照传统的「三阶段」进行设计。下图为传统编译器 vs CPython 编译器：

![cpython-capture2](/images/blog/global/cpython-capture2.svg)

p.s. IR 的全称是 intermediate representation

区别：
1. 从 3.9 开始，CPython 开始使用全新的 PEG parser，可以从源码**直接**生成 AST 抽象语法树：
    - 3.9 之前：源码 -> 语法树（parse tree） -> AST
    - 3.9 之后：源码 -> AST
2. 与传统静态编译器相比，有些人认为 CPython 编译器做的太少了，只是算作一个 front。

## 总览

上图中编译器由两大块组成，fronter 接收 Python 代码生成 AST，backend 进而转化为 code object。所以从某种意义上来说，CPython 编译器又可以称之为“code object 生成器”。

图中 `parser` 用于检查 Python 代码的语法错误（语法具体是什么将在下文详细展开）：

```python
x = y = = 12
        ^
SyntaxError: invalid syntax
```

## 什么是 Abstract syntax tree (AST)


AST 的树节点通由 the Zephyr Abstract Syntax Definition Language (ASDL) 定义。ASDL 是一种简单的声明式编程语言，专门用于描述 IRs 树，也就是 AST。例如 `Assign` 与 `Expr` 节点在 ASDL 中的定义（[Parser/Python.asdl](https://github.com/python/cpython/blob/f2cab7b0cf019fcc3112018db5e20c00976f33d4/Parser/Python.asdl#L27)）：

```asdl
stmt = ... | Assign(expr* targets, expr value, string? type_comment) | ...
expr = ... | Call(expr func, expr* args, keyword* keywords) | ...
```

ASDL 可以清晰定义 Python AST 的结构，但 CPython 是 C 语言编写的，要怎么办呢？好在可以通过 ASDL 自动生成 C 语言的 structs 定义。

```c
struct _stmt {
    enum _stmt_kind kind;
    union {
        // ... other kinds of statements
        struct {
            asdl_seq *targets;
            expr_ty value;
            string type_comment;
        } Assign;
        // ... other kinds of statements
    } v;
    int lineno;
    int col_offset;
    int end_lineno;
    int end_col_offset;
};

struct _expr {
    enum _expr_kind kind;
    union {
        // ... other kinds of expressions
        struct {
            expr_ty func;
            asdl_seq *args;
            asdl_seq *keywords;
        } Call;
        // ... other kinds of expressions
    } v;
    // ... same as in _stmt
};
```

AST 的好处在于，抽象隐藏了很多非必要的信息，例如代码缩进、标点符号，以及其他语法特性。

AST 的主要受益者是编译器：让编译器基于结构化的表示，更加简单地生存字节码。除了编译器，其他 Python 工具也会使用 AST：例如 pytest 会修改 AST，以便于在 `AssertionError` 抛出时提供更多信息；Bandit 通过分析 AST 来发现 Python 代码中常见的安全问题。。

稍微对 AST 有点概念后，下一小节将介绍 parse 具体是如何将 源代码 转化为 AST 的。

## 源代码 -> AST

### 1 旧 parser

前文提到从 Python3.9 开始，CPython 中有两个 parser。默认使用新的 parser，但可以通过 `-X oldparser` 参数开启旧 parser。从 Python3.10 开始，旧的 parser 被完全的移除。

> https://www.youtube.com/watch?v=QppWTvh7_sI

😂Guido 描述 pgen（旧 parser） 的另一个优点：由于它本身的各种限制，成为了很好拒绝部分新特性的“借口” --- 你希望引入的语法用 pgen 太难实现了（同时也可能意味着对于普通人太那理解了）。

（略）

### 2 tokenizer

Python 是一门复杂的语言，但 Python 的语法很简单，仅有 63 个 TOKEN（[Grammar/Tokens](https://github.com/python/cpython/blob/0bbaf5de9744ae1acea3e2c9ad2257d1cc68e847/Grammar/Tokens#L1)）。

举一个简单的例子：
```python
def x_plus(x):
    if x >= 0:
        return x
    return 0
```

下面的输出就是 parser 眼中的代码：
- tokenizer 每次读一个字符，并尝试匹配一个完整 token（w → wh → whi → whil → while）。
- parser 每次向 tokenizer 请求并处理一个 token。
```
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

新的 parser 对应的新的语法：[Parsing Expression Grammar](https://en.wikipedia.org/wiki/Parsing_expression_grammar) (PEG)。PEG 最早由 Bryan Ford 在 2004 年提出，作为一种描述（编程）语言的工具，可以根据语法描述，自动生成 parser 代码。

但在 CPython 中，Guido 重头实现 `parser generator` 的逻辑（号称 just for fun）。

```
                                                         tokens
                                                           | 
                                                           v 
context free grammar ---> [ parser generator ] ---> [ Syntax parser ]
                                                           |
                                                           v
                                                          tree
```

#### 3.1 context free grammar

简易版语法解释👇：
- `NAME` 和 `NUMBER` 是提前定义好的 token（单引号 `'+'` 和 `'if'` 也是 token），参考 [cpython/Grammar/Tokens](https://github.com/python/cpython/blob/871047dbb82ab9a89f364a4ec62cf05f94706124/Grammar/Tokens)。
- 每行代表一条语法规则（名字：内容），并用 `|` 代表多个备选项。
    - 例如 expr 表达式支持加减法：`x+1`，`x-1`，`x+y-2`，... 
    - 同时支持==左递归==：`x - y - z` -> `(x - y) - z`。

```
statement: assignment | expr | if_statement
expr: expr '+' term | expr '-' term | term
term: term '*' atom | term '/' atom | atom
atom: NAME | NUMBER | '(' expr ')'
assignment: target '=' expr
target: NAME
if_statement: 'if' expr ':' statement
```

但是在 PEG 官方语法中，需要使用类似 `*` 的语法来表示左递归，guido 觉得不够符合直觉，并自己实现 parser generator 的原因之一。
```
expr: term ('+' term | '-' term)*
```

第二个挑战在于：在解析语法 `answer = 42` 时，是逐个 TOKEN 解析的（`answer` -> `=` -> `42`），但在下面的例子中，解析到第一个 token `anser` 时，无法判断是 `assignment` 还是 `expr`。所以 guido 引入了 infinite lookahead buffer，也就是说不用只看一个 token 做决定，可以先尝试一条分支（无限个 tokan），失败了就回退原始位置，再试另一条（==backtracking==）。

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

最后一个变化：新 parser 的生成流程中，跳过了 parse tree，直接生成 AST 树。
- 旧 parser：tokens -> (old parser) -> parse tree -> AST -> bytecode
- 新 parser：tokens -> (PEG parser) -> AST -> bytecode

#### 3.2 parser generator

基于上面的三个挑战和思路，Guido 决定自己用 python 实现了一套 PEG 语法解析的逻辑（输入语法 grammer，自动输出生成 parser）。

分解为两步：
##### 3.2.1 解析语法 -> 转化为结构化数据

```
[
  Rule('statement', [['assignment'], ['expr'], ['if_statement']]),
  Rule('expr', [['term', "'+'", 'expr'],
                ['term', "'-'", 'term'],
                ['term']]),
  ...
]
```

##### 3.2.2 根据数据结构生成 parser
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

不难理解自顶向下，依次解析匹配候选项（通过无限缓冲区持久化复位）：
- self.mark() -> token.mark()：记录当前的索引位置，开始匹配
- self.reset() -> token.reset()：匹配失败，回到刚刚标记的位置

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

⚠️注意：if 判断中的条件是反序的
- grammer：`expr: expr '+' term | expr '-' term | term` 
- parser： `expr: term ('+' term)*`

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

语法抽象树 Abstract syntax tree (AST) 使用树状结构，作为源代码的一种高级表示。下面是用标准 [ast](https://docs.python.org/3/library/ast.html) 模块生成的示例：

```shell
# 1 + 2 + 3

# 递归判断：
expr
├── expr
│   ├── expr
│   │   └── term 1
│   └── term 2
└── term 3

# 真实 AST 树
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

字符串 1 是如何被转化为数字的？ PEG 语法通过 action 关联 python 代码，让 parser 可以直接计算结果。
```
start: expr NEWLINE { expr }
expr: expr '+' term { expr + term }
    | expr '-' term { expr - term }
    | term { term }
term: NUMBER { float(number.string) }
```

### 5 AST optimization

AST optimizer 层在 CPython 3.7 引入。

举个个例子：
```
# 优化前
Module
└── Expr
   └── BinOp(Add)
       ├── BinOp(Add)
       │   ├── Constant(1)
       │   └── Constant(2)
       └── Constant(3)

# 优化后（避免在运行时重新计算）
Module
└── Expr
   └── Constant(6)
```

## AST -> bytecode



## 参考
1. https://aosabook.org/en/v1/llvm.html
2. https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools
3. https://github.com/we-like-parsers/pegen_experiments
4. https://github.com/python/cpython/blob/3.9/Tools/peg_generator/pegen/parser_generator.py

