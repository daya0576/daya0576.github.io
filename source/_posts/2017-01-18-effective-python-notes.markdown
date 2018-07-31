---
layout: post
title: "Note of 《Effective Python》(第一章 - 第三章)"
date: 2017-01-18 21:45:51 +1100
comments: true
categories: [python]
---

记得以前上大学的时候, 去图书馆借了一本《代码简洁之道》. 虽然大部分的内容都忘得差不多了, 但里边的一些思想至今还是收益颇深.     
最近开始看一本书叫做《Effective Python: 59 Specific Ways to Write Better Python》, 把里边一些印象深刻的东西记录在这篇日志里.     

<!--more-->
   

###Chapter 1: Pythonic Thinking:    
1. Pythonic Thinking: `import this`   
2. 讲到选择Python2还是Python3的时候, 作者还是推荐大家尽量选择Python3.      
个人觉得一个初学者总是问学Python2 和 Python3的问题真的是很蠢的一种行为, 我以后还是要慢慢去学会写兼容Python 2 和 3 代码.
3. PEP 8 Style: 如果用Pycharm的话, 风格的不合适也是会用warning提示你的, 所以这个不必担心.    
但个人认为提高Python代码可读性, 还是要代码写的很有节奏, 配上简洁明了的注释.     
例子: `if len(l) == 0: --> if not l:`
4. standard library modules > third-party modules > own modules.     
import包的顺序, 以前写java的时候也是这么推荐的.     
5. 编码的问题(two types of representing se):   
Python3: `bytes`(raw 8-bit values) and `str`(Unicode characters)   
Python2: `str`(raw 8-bit values) and `unicode`   
编码的问题原理我还是不是特别清楚, 以前上课的时候提到过Unicode编码的思想, 有空还是要深入了解一下.    
Things to remember in this chapter:   
   * In python 3, `bytes` contains sequences of 8-bit values, `str` caontains sequences of Unicode characters. `bytes` and `str` instances cann't be used with operateors(like > or +)     
   * In Python 2, `str` contains sequences of 8-bit values, `unicode` contains sequences of Unicode characters. `str` and `unicode` can be used together with operators if the `str` only contains 7-bit ASCII characters.   
   * Use `helper functions` to ensure that the inputs you operate on are the type of character sequence you expect (8-bit values, UTF-8 encoded characters, Unicode characters, etc.).
   * If you want to read or write binary data to/from a file, always open the file using a binary mode (like `'rb'` or `'wb'`)   
6. 作者推荐这类只用一行简洁的写法: `red = my_values.get(‘red’, [”])[0] or 0`    
不由的让人想起了Perl的优美使用: `open BOOK, "hp1.txt" or die "$0: open '$file' failed: $!"`   
7. 数组的slice: 最经典还是这个反转数组(字符串)操作: `somelist[::-1]`    
8. 要尽量用List Comprehension(`squares = [x**2 for x in l if x % 2 == 0`, 而且更强大) 而不是map或者filte.    
字典和set也支持Comprehension Expression: `rank_dict = {rank: name for name, rank in chile_ranks.items()}`    
9. Consider generator expressions for large comprehensions(防止消耗过大的空间):     
Bad: `value = [len(x) for x in open(‘/tmp/my_file.txt’)]`   
Good: `(len(x) for x in open(‘/tmp/my_file.txt’))`   
看了这一小章终于明白generator存在的意义了.     
generator 唯一的缺点就是它只能用一次.    
stackoverflow上的一个不错的回答: [http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do](http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do)   
10. `zip`: 唯一要关注的问题就是在Python2中, zip并不是一个generator, 所以它可能会占用很大的内存, 所以要用izip. 而且当zip的两个参数的长度不一样的时候, 一个参数长出来的部分就会消失咯.  
11. `for`循环后边要尽量不用`else`    
13. try/except/else/finally的逻辑(异常Python用的不多, 但和以前Java的结构好像并没有什么不同). 例如没有exception的话就会走else.     



###Chapter 2: Functions:   
1. 要使用exception而不是返回`None` ("return" or "return None"), 因为None, 0, [], '' 都会被当成False.   
``` python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid b') from e

if __name__ == '__main__':
    try:
        result = divide(1, 0)
    except ValueError:
        print('invalid input')
    else:
        print('result is %.1f' % result)
```
2.用一个helper方法去自定义排序.    
```python
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return 0, x
        return 1, x

    values.sort(key=helper)

l = [1, 2, 3, 4, 5, 6]
g = {4, 5}

sort_priority(l, g)
print(l)
```    
能这么做原因: 1.Python支持闭包(closures). 2.方法可以直接当做变量使用. 3.Python有自己的排序规则来自定义key.     
这一小节还讨论了一些scope的问题, 比如在helper里去改变sort_priority的变量肯定就没有效果, 要加上`nonlocal`, 不禁让人想起了`global`, 他们的作用是刚好相补的.     
但是作者还是推荐说`nonlocal`有风险, 要谨慎使用. 可以用一个类实现一样的功能或者使用list.    
为什么list可以无视scope呢, 还是不太明白?           
"The trick is that the value for found is a list, which is `mutable`. "   
_   
查了一下, 意思就是比如`x=y=1`, 改变immutable变量的值的话是会重新创建一个变量.    
如果是`x=y=[]`, 改变mutable的变量的话, x和y的值就一起变了. 可以理解为C语言中传的地址. y is a copy of x's reference.       
Stackoverflow上的详细解释: [http://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference](http://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference)   
_   
可以这么写不去改变传入的参数: `list(a)` or `a[:]` 来创建新对象.   
3.Generator, 防止内存爆掉.    
```python
def index_word_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1
```
上边说到过, 一个iterator只能用一次, 比如这个例子:
```python
print(list(it))
print(list(it))  # Already exhausted  <-- XD
```
而且你去使用一个被使用过的iterator并不会报错, 所以要格外的小心.     
可以`numbers = list(it)`提前copy一份, 但我总觉得怪怪的.    
作者最后说要用__iter__方法, 但不是很懂:    
Iterator protocol大意就是每次使用这个iterator的时候, __iter__都会创建一个新的iterator.         
```python
def normalize(numbers):
    total = sum(numbers)
    result = []

    for v in numbers:
        result.append(v/total)

    return result


class ReadVistors(object):
    def __iter__(self):
        for i in range(1, 5):
            yield i

def readVistors():
    for i in range(1, 5):
        yield i

v = ReadVistors()
# v = readVistors() # null
print(normalize(v))
```
可以用这个方法检测iterator是否可以多次使用:    
```python
if iter(numbers) is iter(numbers):
    raise TypeError('must suplly a container')
```
4.variable positional ariguments: 如果传入的参数是个未知长度数组的话, 可以这么写:    
```python
def log(message, *values):
    ...

log('My numbers are', 1, 2)
log('Hi there')
```
但是这个巧妙的用法也有一些问题:   
   * 的话会在传入参数前, 把values变成一个tuple. 所以要是传入的是一个generator的话, 内存就很有可能爆掉.    
   * 在方法中新增一个参数的话, 很可能造成一些很难发现的bugs.   
5.在使用Python的默认参数是mutable({}, [])的时候, 要格外小心, 因为这个default argument只有在初始化的时候被evaluated一次.    
最好的解决方法是用None:   
```python
def log(message, when=None):
    when = datetime.now() is when is None else when
    ...
```



###Chapter 3: Classes and Inheritance:   
- 1) 要避免字典里套字典, 可以用多个类来替换.    
2) 在考虑用class前, 可以尝试`namedtuple`作为一种轻量级的不可修改的data container.    
- Python中的方法也是和变量一样是对象, 所以可以传来传去~比如sort的key参数就是接收一个排序的方法    
- Python允许类中定义一个`__call__`方法,
```python
counter = BetterCountMissing()
result = defaultdict(counter, current) # Relies on __call__
```
- @classmethod和@statisticmethod:   
书中解释了一大堆, 不是特别懂, 大意就是要把相关的方法写到类里边. 摘Stack Overflow上的两个例子:    
```python
@classmethod
def from_string(cls, date_as_string):
    day, month, year = map(int, date_as_string.split('-'))
    date1 = cls(day, month, year)
    return date1

date2 = Date.from_string('11-09-2012')


@staticmethod
def is_date_valid(date_as_string):
    day, month, year = map(int, date_as_string.split('-'))
    return day <= 31 and month <= 12 and year <= 3999

# usage:
is_date = Date.is_date_valid('11-09-2012')
```
- Initialize Parent Classes with `super`(看了半天头都晕了)    
- Item26: 跳过.   
- Item28: collections.abc



###Chapter 4: Metaclasses and Attributes:
- Item 29:


<未完待续>
