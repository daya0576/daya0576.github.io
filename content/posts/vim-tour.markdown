---
layout: post
title: "我和VIM的故事"
date: 2018-02-23 15:41:28
comments: true
tags: [vim]
---

和VIM相爱的故事要从我的笔记本**上下键**坏了开始..哈哈   
![](/images/blog/180223_vim/apple.png)
虽然大二的时候学过vim, 但一直用的IDE. 今年强迫自己用了三天vim之后, 彻底的爱上用VIM写代码的感觉.   
**用这篇博客分享一下自己从VIM小白一路不断学习的历程.**  

<!--more-->

## vimtutor
**学会VIM的秘诀: 练习+练习+练习**   
**VIM入门**最好的教程就是VIM的官方tutorial: **直接在命令行输入`vimtutor`**.   
<img style="max-height:200px" src="/images/blog/180223_vim/vimtutor_pre.jpg">   
因为在这个教程中, 每个技巧都附带了可供实际操作的练习:    
<img style="max-height:200px" src="/images/blog/180223_vim/vimtutor.jpg">   
> It is important to remember that this tutor is set up to teach by use.  That means that you need to execute the commands to learn them properly.  If you only read the text, you will forget the commands!


### 下边是我做的一些笔记:    
1. **删除操作:**    
    * `dd`: 删除一行   
    * `3dd`: 删除三行   
    * `dw`: 删除一个word   
    * `d2w`: 删除两个words   
    * `d$`(D): 删除到行末   
2. **undo/redo**
    * `u(U)`: undo(大写的U会undo这一行里的所有历史改动)   
    * `ctrl-r`: redo   
3. **Change**(类似于上边的删除):    
    * `ce`: To change until the end of a word   
    * `c$`:  to change to the end of a line   
    * `ci"`: Change in "abcdef"
4. **Search**:   
    * `/ —> n(N)`: 跳到下一个/上一个匹配的地方.   
    * `CTRL-O` takes you back to older positions, `CTRL-I` to newer positions.
5. **快速进入insert mode**   
    * `A`: edit at end of the line.   
    * `I`: edit at beginning of the line.   
    * (类似的还有大写的`C`, 经常用到.)   
6. **replace mode**:   
    * `R`: R Enter “replace mode”, which is like insert mode except you will overwrite characters instead of insert between them. (就是.)   
7. **复制**:   
    * `yw`: 复制一个word
8. **Navigation**:   
    * `ctrl-y/ctrl-e`: 忽略光标位置, 上下移动一行屏幕.    
    * `ctrl-u/ctrl-d`: down/up, 上下移动半页.    
    * `ctrl-b/ctrl-f`: forward/backward, 上下移动一页.    



## Pratical Vim

**学完vimtutor后, 继续读了一本很不错的书: Practical Vim**   
但是很遗憾只看了一半, 书中有段话挺有意思的: 就是说写程序就像画画, 艺术家大部分的时间其实都是在构图, 思考, 真正用画笔接触画布的时间其实占比很小. 这就像VIM, 大部分停留在Normal Mode, 说的还挺有道理的.   

- **Part I: Modes**
- **Part II: Files**
- **Part III: Getting Around Faster**
- Part IV: Registers
- Part V: Patterns
- Part VI: Tools


**分享当时记的一些笔记:**

* `.`  -->  repeat last action    
(因为我们大部分的工作都是重复的, 所以可以巧妙利用这个`.`, 做到never repeat yourself)
* 在一行中查找一个字符: 
    - f{char} 
    - F{char}: 从右边开始找. 
    - p.s. (可以使用`;`/`,`做到repeat和reverse上边的两个操作)
* `<C-x><C-a>`: Number Formats(就是对当前行中第一个数字做+1/-1操作, 不知道为什么有这种操作)
* Operator + Motion = Action
    - `daw`: delete a complete word(与dw的区别: 只要光标在这个word中就可以整个word)    
    - `c3w`(not work for ideavim): change 3 words
    - `dap`: delete a complete paragraph
* Operator + t + {char}:
    - `dt{`: delete to {
    - `yt,`: 复制 直到 最近的逗号
* `tip 11`: Don’t Count If You Can Repeat(这个tip挺有意思的, 就是有时候去数一数有几个word还不如直接重复几次来得快)
* Insert Mode:    
`<c-o>`: 在insert模式, 执行一次normal模式的操作:   
例子: <C-o>zz: 在insert模式中, 让cursor回到屏幕中央
* Visual Mode    
    - `viw`: 在一个word中间选中整个词    
    - 3-submodules:
        -  v: character-wise
        - V: line-wise 
        - <C-v>: block-wise Visual mode
    - `o`: go to start/end of highlightened text(跳到选中的开始).  
    - `~`: swap case (only if 'tildeop' is set)
    - `gu/gU`: 改为大写或小写
* Getting Around Faster
    - `禁用方向键`: 在vimrc中将方向键禁用, 改掉一个坏习惯最好的办法就是完全禁止自己去做这件事.
    - 在一行中查找一个字符: 
        - f{char} 
        - F{char}: 从右边开始找. 
        - p.s. (可以使用`;`/`,`做到repeat和reverse上边的两个操作)
    - `W/E/B`: 根据空格进行移动
    - `%`:   
    <img style="max-height:200px" src="/images/blog/180223_vim/move_faster_pair.png">   
    - `[count]G`/`:[count]`: 跳到某一行.
    - `H/M/L`: 让光标跳到屏幕的开始/中间/最后
    - `zz/ze/zb`: try it.  


## Learn Vimscript the Hard Way: 
读的第三本秘籍叫做[Learn Vimscript the Hard Way](http://learnvimscriptthehardway.stevelosh.com/)    

只看了三分之一, 感觉挺不错的, 对各种概念原理解释的**很全面**, 关键是每章有课后题, 自己动手才能真正理解.   
剩下如果坚持看完的话应该就可以自己编写插件了.   

**以下是我的笔记:**
 
- Echoing Messages
    1. echo/echom: 都是打印, 但echom会记录每次的输出, 可以之后再`:messages`中查看.
    2. 注释用的是冒号: `"`
- Setting Options
    例子: :set number numberwidth=6
    1. boolean:  
        - set number: on
        - set number !: off
        - set number ?: 检查当前设置
    2. value(设置具体的值):   
        - relativenumber
        - numberwidth
        - wrap (wrap long lines)
        - shiftround → (round indence)
        - showmatch/matchtime ({})
- Basic Mapping/Modal Mapping/Strict Mapping
    1. map: `map _ dd`
    2. nmap/vmap/imap: 在normal/visual/insert模式下的map
    3. *noremap(划重点):    
    例如`:nmap dd O<esc>jddk`这个mapping, 加上`nore`后, 会避免循环调用了!
- Leaders   
    就是vimrc中的<leader>, 当然也可以自定义: `let mapleader="_"`
- Abbreviations
    例如`iabbrev adn and`, 输入adn就会自动转化为and.   
- Training your finger:
    1. `inoremap jk <esc>`: 在插入模式中输入jk时, 回到正常模式. 说实话, 感觉还是挺好用的 :) 
    2. `inoremap <esc> <nop>`: 废掉esc键. 好暴力.
        作者说: "就像和生活中一样, 如果我们彻底改掉一个坏习惯, 那就让它难以或完全不可能被做."
- Buffer-Local Options and Mappings
    例子: `nnoremap <buffer> <leader>d dd`, 多了<buffer>, 就是只在定义这条命令的buffer(文件?)生效.  
- Autocommands
    例如在修改vimrc文件之后, 自动source一下:     
    `:autocmd BufferWritePost .vimrc soure %`   
- Operator-Pending Mappings
    可以map一个动作, 试试第三个例子: 
    1. `:onoremap p i(`: dp(d: action, p: movement)
    2. `:onoremap b /return<cr>`: db
    3. `:onoremap in( :<c-u>normal! f(vi(<cr>`: 当光标在`print foo(bar)`括号之外时, 输入`cin(`. 
    4. `:onoremap il( :<c-u>normal! F)vi(<cr>`: "inside last parentheses" 
- More Operator-Pending Mappings   
    其他的一些可以mapping的operations
    1. `:normal`: 进到normal mode
    2. `?^==\+$`: performs a search backwards for any line that consists of two or more equal signs and nothing else.
    3. `:nohlsearch`: clears the search highlighting from the search
    4. `kvg_`
- Variables
    1. 赋值:   
    `let foo="bar" / let foo=42`
    2. options as variable:   
    `set textwidth=80`   
    `let &textwidth = &textwidth + 10`    
    `set textwidth?`
    3. local buffer / currentbuffer:   
    `let &l:number=1 / let b:hello="world"`
- Conditionals:   
    <img style="max-height:200px" src="/images/blog/180223_vim/Conditionals.jpeg">   
    哈哈, 这个章节的作业: Drink a beer to console yourself about Vim's coercion of strings to integers.
- Comparisons
    当设置`set ignorecase`的时候, `"foo" == "FOO"`为True.   
    所以作者说在写plugin的时候, 最好使用:   
    - `==?`: 不区分大小写
    - `==#`: 比较时区分大小写
- Functions:   
    ....
- (TODO)

(未完待续)

