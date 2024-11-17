---
title: 记一次Hexo Next主题的小小小升级(v6.3.0 → v6.4.0)
date: 2018-09-01 16:17:01
categories:
- 奇技淫巧
---

> 软件维护有两种截然不同的思路，一种所有的依赖都追踪最新版，一旦出最新版立即开始试用，出问题马上反馈社区或者解决，这样虽然经常需要适配新版，但每次都是小问题，很快就能解决。这是活着的软件，虽然每天都要吃饭很麻烦，但你能看见它的新陈代谢。
> 
> 另一种所有的依赖都选择一个不会变的固定版本，能不升级就不升级，旧版本的bug想办法workaround，这种软件的开发者害怕改变，能推到明天的工作绝对不在今天做，并且喜欢以“项目规模太大，客户要求严格，风险太高”为理由，得过且过，这种是死掉的项目，只是还没有埋而已，在这种项目上你会发现做变更也特别困难，许多现代项目里非常常见的功能根本加不进去（因为依赖库不支持）
> 
> 活着的项目可能会死，死掉的项目是几乎不可能再活过来的，落后太多版本，一旦升到最新版就发现到处都是问题修不过来了，因为没有跟踪过依赖的版本变更，也搞不清楚可能是什么问题。像JDK这种已经算好的了，不兼容的情况一般比较少，但JDK都不肯升，依赖库肯定也全是JDK6版本的了，要把依赖库直接升到10，只能选择死亡了。
> 
> 作者：灵剑
链接：https://www.zhihu.com/question/30137699/answer/476916096

以上为知乎上的一个回答. 个人觉得如果对于自己非常熟悉的第三方依赖, 并可以把握风险的话, 还是会不断的去追求最新版本. 毕竟对于新事物的好奇心是活在一个优秀程序员血液里的东西. 

本文简单记录了Hexo Next主题升级版本(v6.3.0 → v6.4.0)的完整过程.  

<!--more-->

# 本地添加远程仓库(upstream)
博主本地的`theme/next`文件夹是fork下来到自己的仓库, 再通过submodule管理的: 
![](/images/blog/1800901_hexo_next_update/15357925972575.jpg)

所以第一次更新主题版本时, 要添加远程仓库(upstream): `git remote add upstream git@github.com:theme-next/hexo-theme-next.git`

下图可以看到`origin`对应的是个人仓库, `upstream`对应的是Next项目的仓库. 
![](/images/blog/1800901_hexo_next_update/15463587822040.jpg)

# 拉取Next最新代码
`git fetch upstream`拉取Next项目最新的代码:   
![](/images/blog/1800901_hexo_next_update/15357928615366.jpg)

# 合并分支
`git merge v6.4.0`合并代码:
![](/images/blog/1800901_hexo_next_update/15357931212528.jpg)

可以看到`post-reward.styl`文件出现冲突(conflict)了.    
解决冲突后, 马上就大功告成了!!!    
![](/images/blog/1800901_hexo_next_update/15357932201665.jpg)

# git记录
`git log`可以清楚的看到 合并Next主题代码和本地代码合并的记录:
![](/images/blog/1800901_hexo_next_update/15357933184002.jpg)

# 其他
升级后NexT的版本还是显示`v6.3.0`, 
![](/images/blog/1800901_hexo_next_update/15358741539618.jpg)

在telegram的群里问里一下, 竟然是..发布tag的时候忘记改version了.   
![](/images/blog/1800901_hexo_next_update/15358762828266.jpg)

那么问题来了, 这个version变量是哪里来的呢? 再了解了一下, 原来是从`package.json`里取的(`themes/next/scripts/helpers.js`):
![](/images/blog/1800901_hexo_next_update/15358846331974.jpg)


cheers, 笔芯❤️

-eof-


