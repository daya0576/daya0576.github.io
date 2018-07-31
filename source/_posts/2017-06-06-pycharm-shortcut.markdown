---   
layout: post   
title: "PyCharm 收藏多年快捷键分享~"   
date: 2017-06-06 22:43:18 +0800   
comments: true   
categories: [pycharm, shortcut]   
---   

> 介绍一些Pycharm中大幅度提高生产力的快捷键, 不看后悔一辈子! (逃)      
大部分的快捷键在同系列的IDE(JetBrains全家桶)上应该都是能通用的     
<img style="max-height:250px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/license-min.png">     
<!--more-->   
     

> **友情提示:** 点击图片, 可显示大图~     
**声明:** 因为这些快捷键都是可以自定义的, 而且在不同的操作系统里也不同, 所以我每个都给出了操作的标题, 大家可以在设置里查找对应的快捷键:    
<img style="max-height:200px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/declare.png">       
**最新基于** Pycharm 2017.02



# 快速搜索
<p></p>
### 1. Find in Path...
`Ctrl+Shift+F/Ctrl+Shift+R` | `⇧⌘F/⇧⌘R`: 
在整个项目中 或 指定目录里 进行**全局搜索/替换**:      
<img style="max-height:300px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/0.png">       


### 2. Find Action by Name
`Ctrl+Shift+A` | `⇧⌘A`: text --> 执行一些action(git pull/commit等等等等), 潜力无限, 有待开发.   
<img style="max-height:300px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/2.png">       


### 3. Search Everywhere
`Shift(Double-press)`: 双击shift, 我每天使用频率很高的一个快捷键, 可以按最近使用过的**文件名, 类名, 方法名等**去搜索定位!    
最棒的是它会记住你的搜索历史, 并将最常用的显示在最上边.      
<img style="max-height:300px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/4.png">     


### 4. Main menu | Navigate | File...
`Ctrl+N` | `⌘O`: 查找类Class   
`Ctrl+Shift+Alt+N` | `⌥⌘O`: 查找所有Symbol(不知道如何解释, 包括变量, 表名, 等等)   
`Ctrl+Shift+N` | `⇧⌘O`: 查找文件或目录(比双击shift快很多)   
<img style="max-height:150px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/search_file.jpg">     
<img style="max-height:150px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/search_file.png">     
但这个搜索文件有个很尴尬的地方, 模糊搜索的时候一定要带斜杠来分割文件夹, 我发邮件给了客服, 竟然刚刚实现这个功能, 下个版本就有咯, cheers~   
<img style="max-height:200px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/email.png">     



# 代码自动化
<p></p>
### 1. Declaration
`Alt+Enter`: **自动import**, 还会做自动优化, 妈妈再也不用担心依赖关系啦    
<img style="max-height:200px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/3.png">     


### 2. Code | Insert Live Template....
`Ctrl+Alt+Shift+J` | `⌘J`: 插入一段提前配置好的**代码模板**!    
e.g. `import ipdb; ipdb.set_trace(context=20)`...   
<img style="max-height:250px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/5.png">   
[https://www.jetbrains.com/help/pycharm/creating-code-constructs-by-live-templates.html](https://www.jetbrains.com/help/pycharm/creating-code-constructs-by-live-templates.html)



# 导航
<p></p>
### 1. Other | Switcher
`Ctrl+Tab`: 和chrome一样的切换标签      


### 2. Main menu | Navigate | Back/Forward
`Alt + Left|Right`: **移动光标**到上一次编辑或者返回移动之前的位置.   
在错综复杂的代码中更为重要, 再也不担心迷路了咯.   



# 快速编辑
<p></p>
### 1. Delete Line
`Ctrl+x`: 不用选择, 直接**删除整行**代码   


### 2. Duplicate Line or Selection
`Ctrl+shift+d`: 直接**重复一行**或**重复生成选中的内容**   


### 3. Code/Folding/Expand (All)|Collapse(All)
`Ctrl(shift) + +/-`: 折叠一个方法的代码或整个文件的代码.    
我一般喜欢, 先折叠整个文件的代码, 然后再打开一个类去看它的结构.      

    
### 4. Move Line Up|Down
`Alt + Up/Down`: 可以上下移动整行或整块(e.g. 一个if的block)代码   


### 5. Editor Actions | Unindent Line or Selection: 
`Shift + Tab`: 对一行或多行(选中内容)的**逆向缩进**!   



# 同时编辑多处: 
<p></p>
### 1. Add or Remove Caret
`Alt + 鼠标` or `Shift + Crtl + Alt + 鼠标`: 选择多处进行同时编辑, 要是能像sublime那样alt+enter直接选中所有的查找结果就好了(已解决, 见下一条).      
<img style="max-height:250px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/6.png">     
找到解决办法了!    
Pycharm中的快捷键**Select All Occurrences**就等同于sublime里的全选所有符合搜索的结果(`ctrl+回车`)!    


### 2. 正则搜索的妙用
Perl中$0就代表全部匹配(本身), 所以就能实现同时替换所有搜索结果, 和多处同时编辑异曲同工:          
(见下图)   
<img style="max-height:250px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/7_1.png">   
按**Replace all**之后:     
<img style="max-height:250px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/7_2.png">     


---


# 其他奇技淫巧: 
<p></p>
###Annotate
查看当前文件每一行代码是谁是哪个commit贡献的(gitbub/gitlab上的blame view, 这个名字好形象)
<img style="max-height:400px" class="lazy" data-original="/images/blog/170606_pycharm_shortcut/annotation.jpg">  

(持续更新中...)   
如果你有什么更好的华丽操作, 记得给我留言哦~~   

