---
layout: post
title: "熟悉的陌生人: Python format用法大全~"
date: 2017-08-10 11:04:03
comments: true
tags: [python]
---

今天看到[官方文档](https://docs.python.org/3/library/string.html#format-string-syntax)的时候, 突然发现format()这个方法这么强大, 有好多原先不知道的用法. 用这篇博客总结了一下.    
<!--more-->   
  



# 语法总结(1.field_name 2. conversion 3. format_spec)   
``` python
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"

field_name        ::=  arg_name ("." attribute_name | "[" element_index "]")*
arg_name          ::=  [identifier | integer]
attribute_name    ::=  identifier
element_index     ::=  integer | index_string
index_string      ::=  <any source character except "]"> +

conversion        ::=  "r" | "s" | "a"

format_spec       ::=  <described in the next section>
``` 
第一眼可能给有些头晕, 但每个选项都懂了之后, 就会发现官方文档总结的**非常清晰**.   
见第一行, 语法主要由**三部分**组成: **1.field_name 2. conversion 3. format_spec**,   
下文也将从这三部分出发, 一一解析每个选项的含义.   



# field_name
1. **关键字(attribute_name):**   
<img style="max-height:80px" class="lazy" data-original="/images/blog/170810_python_format/attribute_name.png">     
这个地方其实有个小技巧, 就是一开头语法总结中的arg_name和element_index:   
arg_name: keyword.name → `getattr()`   
element_index: keyword[index] → `__getitem__`   
**举个栗子🌰: **   
<img style="max-height:110px" class="lazy" data-original="/images/blog/170810_python_format/1.1_arg_name.png">     
<p></p>
2. **数字(element_index):**   
用数字来表示参数的位置, 默认的`{} {} {}..`其实就等同于`{0} {1} {2}..`     
这样稍微简洁一些, 而且可以重复渲染字符串:    
<img style="max-height:43px" class="lazy" data-original="/images/blog/170810_python_format/element_index.png">   



# conversion
<p></p>
1.  !s: str()   
2. !r: repr()   
3. !a: ascii()   

**官方例子:**   
``` python
"Harold's a clever {0!s}"        # Calls str() on the argument first
"Bring out the holy {name!r}"    # Calls repr() on the argument first
"More {!a}"                      # Calls ascii() on the argument first
```



# format_spec
``` python
format_spec     ::=  [[fill]align][sign][#][0][width][grouping_option][.precision][type]

fill            ::=  <any character>
align           ::=  "<" | ">" | "=" | "^"
sign            ::=  "+" | "-" | " "
width           ::=  integer
grouping_option ::=  "_" | ","
precision       ::=  integer
type            ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"
```

下边对上图的每个选项做解释(默认为空):    

1. **fill:**   
填充的字符, 默认为空字符串, 但前提是必须先指定align: `[[fill]align]`.    
2. **align:**    
`'<'`: 向左对齐    
`'>'`: 向右对齐   
`'='`: Forces the padding to be placed after the sign (if any) but before the digits. 意思就是说, 在符号(sign)的后边, 但在数字的前边做填充. 为了实现`+000000120`里, '+'和'120'的补零: `'{:0=+8}'.format(123)`     
`'^'`: 向中对齐:    
    
    **举例**   
    `'{:-^30}'.format('Text')`    
    Out[3]: '-------------Text-------------'    

3. **sign:**    
这个参数只读数字起效, 它有三个选项:    
`'-'`: 1 → '1'(默认选项)   
`'+'`: 1 → '+1'   
`' '`: 1 → ' 1'   
-1话, 都是渲染为'-1'
4. **width:**   
字符串最后的**总长度**   
5. **grouping_option:**   
对数字分段:   
'{:,}'.format(1234567890)   
'1,234,567,890'   
6. **precision:**   
控制精度, 截取浮点型数值小数点后的位数, eg. `{:.2}.format(3.1415926)`   
7. **type:**    
1) 将整数转化为不同的进制.   
2) 将浮点数渲染成不同的格式, 例如百分比形式, 指数形式...



# One more
给大家留一个小问题, 如何在这种情况下输出大括号呢?     
`'???{}'.format('test')`
 






