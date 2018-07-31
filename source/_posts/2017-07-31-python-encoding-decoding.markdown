---
layout: post
title: "Python的编码问题笔记(搞清原理, 一劳永逸)"
date: 2017-07-31 20:59:46 +0800
comments: true
categories: [python3, unicode, encoding]
---

近日常常python的编码问题纠缠的生活不能自理. 昨天终于静下心来看了看文档, 把Python3中的编码搞清, 用这篇文章分享记录一下**(包括utf-8的原理)**.    
<img class="lazy" style="max-height:200px" data-original="/images/blog/170801_encoding/h.png">    
<!--more-->



### 提示:
下文中都是以**python3**为栗子🌰.   
因为python3慢慢变成主流, 而且用python2的话我一般会写成兼容的模式:   
`>>> from __future__ import print_function, unicode_literals`



> ### 编码在python2和3中的区别(_可跳过, 最后回过头来看_):
摘自*Effective Python*那本书:   
_   
**In Python3: **    
1. **bytes**: sequences of 8-bit values.   
2. **str**: sequences of Unicode characters.   
bytes and str instances can’t be used with operators(like > or +)   
_   
**In Python 2:**    
1. **str**: contains sequences of 8-bit values.   
2. **unicode**: contains sequences of Unicode characters.    
str and unicode can be used together with operators if the str only contains 7-bit ASCII characters.   
_   
但说实话在今天前, 我对上边那段话的理解还是停留在python3 有两种类型(str和bytes)的地步😓.    




### 1. Python3 str类型(unicode)
python3的str字符串, 默认就代表**unicode字符组成的序列**.    
```python
In [1]: s = '哈哈哈'   
In [2]: type(s)   
Out[2]: str   
```

**_那问题来了, 到底什么是unicode呢?_**   
大家都知道ASCII编码, 它用7位bits代表128个字符.    
但一个字节不够用的时候, 很多聪明的人就发明了很多的扩展的字符集.   
可是这时候碰到了一个问题, 就是一台电脑在美利坚可能用的好好的, 但如果收到日本的邮件, 那就GG了, 因为两台电脑的**编码方式不同**.   

所有后来更聪明的人就想到了unicode:   
它对**世界上所有的字符**进行收集, 每个字符指向一个code point(简单理解为一个唯一的数字), 这样全世界交流也不会乱码了, 棒棒哒.   
所以unicode的一个中文名也叫`万国码`.



### 2. Python3 bytes类型(字节)
bytes和str一样都是内置的类型:  
```python 
In [7]: s = b'haha'
In [8]: type(s)
Out[8]: bytes   
```
个人理解, 它代表的就是以字节(byte)为单位存储的二进制, i.e. 一坨的bytes   



### 3. Encoding/decoding: 
搞清楚python中的str和bytes类型, 这个问题就迎刃而解了.   

1. **Encoding:**   
**str → bytes**   
因为str只是一堆unicode字符(数字).   
所以简单的说, encoding就是把一堆数字, 按特定的编码算法X(例如utf-8), 用字节的方式存储在计算机上.   

2. **Decoding:**   
**bytes → str**   
举个栗子🌰:   
<div style='margin-left: 20px'>

```python
In [9]: s = '哈哈'

In [10]: s.encode('utf-8')
Out[10]: b'\xe5\x93\x88\xe5\x93\x88'

In [11]: s.encode().decode('utf-8')
Out[11]: '哈哈'
```
</div>



### 4. UTF-8编码(encoding)
简单的说下unicode是如何通过utf-8编码转化为bytes, 以帮助更好的理解什么是编码(encoding).    
**utf-8**其实属于 动态长度编码(variable length encoding).   

举个**动态长度编码简单的栗子**, 假如说有这么一个二进制序列:   
1001000**1**, 1000000**1**, 1011001**0**, 1011001**0**   
我们就可以利用每个byte的最后一位(标志位, 1代表继续, 0代表结束), 来判断读几个bytes.   

utf-8也是类似的思想, 但不同于上边, 它是用每个字节**开头的几位**, 当作标志位, 如下表所示:    
<table>
	<thead>
		<tr>
			<th>1st Byte</th>
			<th>2nd Byte</th>
			<th>3rd Byte</th>
			<th>4th Byte</th>
			<th>可用的Bits</th>
			<th>最大值</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>0xxxxxxx</td>
			<td></td>
			<td></td>
			<td></td>
			<td>7</td>
			<td>007F hex (127)</td>
		</tr>
		<tr>
			<td>110xxxxx</td>
			<td>10xxxxxx</td>
			<td></td>
			<td></td>
			<td>(5+6)=11</td>
			<td>07FF hex  (2047)</td>
		</tr>
		<tr>
			<td>1110xxxx</td>
			<td>10xxxxxx</td>
			<td>10xxxxxx</td>
			<td></td>
			<td>(4+6+6)=16</td>
			<td>FFFF hex (65535)</td>
		</tr>
		<tr>
			<td>11110xxx</td>
			<td>10xxxxxx</td>
			<td>10xxxxxx</td>
			<td>10xxxxxx</td>
			<td>(3+6+6+6)=21</td>
			<td>10FFFF hex (1,114,111)</td>
		</tr>
	</tbody>
</table>
(生动活泼形象的编码例子见下图↓)


   

### 总结
为此我专门画了一张图, 总结了一下:   
<figure class="code"><figcaption><span></span></figcaption><div class="highlight"><table><tbody><tr><td class="gutter"><pre class="line-numbers"><span class="line-number">1</span>
<span class="line-number">2</span>
<span class="line-number">3</span>
<span class="line-number">4</span>
<span class="line-number">5</span>
<span class="line-number">6</span>
<span class="line-number">7</span>
<span class="line-number">8</span>
<span class="line-number">9</span>
</pre></td><td class="code"><pre><code class="python"><span class="line"><span class="o"> </span>
</span><span class="line">             <span class="s">'unicode: 01010110 00111111'</span>
</span><span class="line"><span class="o">        </span> <span class="o">+---</span>  <span class="n">_str</span> <span class="o">=</span> <span class="s">'嘿'</span>               <span class="o">&lt;---+</span>
</span><span class="line"><span class="o">        </span> <span class="o">|</span>                                   <span class="o">|</span>
</span><span class="line"><span class="n">encoding</span> <span class="o">|</span>                                   <span class="o">|</span> <span class="n">decoding</span>
</span><span class="line"><span class="o">        </span> <span class="o">|</span>                                   <span class="o">|</span>
</span><span class="line"><span class="o">        </span> <span class="o">+---&gt;</span> <span class="n">_bytes</span> <span class="o">=</span> <span class="n">b</span><span class="s">'</span><span class="se">\xe5\x98\xbf</span><span class="s">'</span>  <span class="o">----+</span>
</span><span class="line">             <span class="s">'utf-8: (1110)0101 (10)011000 (10)11 1111'</span>
</span><span class="line">
</span></code></pre></td></tr></tbody></table></div></figure>  
**!注意utf-8编码中我用括号括起来的部分, 去对照上边的表格(第三排).   **



### Reference:
-  https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/ (推荐一读, 特别逗)
- https://docs.python.org/3/library/stdtypes.html#bytes



