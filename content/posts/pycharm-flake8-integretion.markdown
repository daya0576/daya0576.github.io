---
title: Pycharm集成flake8检查 (External Tools)
date: 2018-08-30 21:06:05
tags:
  - python
  - pycharm
categories:
  - PYTHON
---

在我们的项目中, 每次 push 代码后, gitlab 的 runner 会自动执行一次 flake8 代码静态检查. 当然在本地也可以在终端中手动触发, 但缺点是如果检查出 10 个问题, 我要重复 10 次复制粘贴文件路径在 Pycharm 中修改的操作.
![](/images/blog/180829_ios12_review/15357044080367.jpg)

今天突然发现可以在 Pycharm 中利用 External Tools 集成 flake8 检查, 点点鼠标就能到具体的代码位置。
![](/images/blog/180829_ios12_review/15357030899815.jpg)

<!--more-->

# 在 settings 中配置 External Tools

![](/images/blog/180829_ios12_review/15357040869027.jpg)

# 添加配置:

![](/images/blog/180829_ios12_review/15357042026629.jpg)
配置详情:

- Program: `$PyInterpreterDirectory$/python`
- Arguments: `-m flake8 --show-source --statistics $ProjectFileDir$`
- Working directory: `$ProjectFileDir$`
- Output Filter: (留空就可以了, pycharm 能自动识别路径.)

# 触发 flake8 静态检查:

![](/images/blog/180829_ios12_review/15357028577407.jpg)

# 结果: 是不是很酷

![](/images/blog/180829_ios12_review/15357030899815.jpg)
