---
title: JetBrains IDE 的五个编程小技巧
date: 2022-05-04 15:50:31
tags:
categories:
- JAVA
---


第四次尝试 vim 作为主力编程失败，挫败之余分享近期发现的若干 ide 小技巧（适用 intellij idea，pycharm，etc.）

<!--more-->

# 5 Tips：

## Tip1: 如何在终端打开仓库
Toolbox 中修改 scripts location 后，终端执行 `idea xx` 即可：

![](../images/blog/2021-09-04-jvm-note/16516488178925.jpg)


## Tip2: Fix all
作为一名经验丰富的 copy/paste 手工劳动者，复制代码后如何批量修复小问题：

![](../images/blog/2021-09-04-jvm-note/16471630809745.jpg)
参考：

## Tip3: File Structure
文件篇幅过大，如何快速找到当前文件内的一个变量或方法：
![](../images/blog/2021-09-04-jvm-note/16471636200710.jpg)

## Tip4：自动打开 MR 链接
其实与 ide 无关，编辑 `.git/hooks/pre-push` 文件即可（记得替换 `{{url}}` 变量）：

```
branch=$(git rev-parse --abbrev-ref HEAD)
mrUrl="{{url}}/new?source_branch=$branch&target_branch=master"
echo opening:$mrUrl
open $mrUrl
```

## Tip5：Multiple cursors

最早应该在 Sublime 体验多光标编辑，近期给同事在 idea 中演示，对方直呼真骚：

![](../images/blog/2021-09-04-jvm-note/16516497949165.jpg)





# 参考：
1. https://www.jetbrains.com/help/idea/working-with-the-ide-features-from-command-line.html#toolbox
2. https://www.jetbrains.com/help/idea/resolving-problems.html#apply-quick-fixes
3. https://www.jetbrains.com/help/idea/viewing-structure-of-a-source-file.html
4. https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
5. https://www.jetbrains.com/help/idea/multicursor.html
