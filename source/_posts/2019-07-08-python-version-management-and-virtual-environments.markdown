---
title: Python 版本管理 & 虚拟环境的那些事
date: 2019-07-08 18:52:56
tags:
---


好几个月前的一个月黑风高的深夜，和同事对 Python 的版本管理 & 虚拟环境进行了一些讨论。写一篇博客纪念一下，也算是作为个人的笔记。   

如果你对 `pyenv`, `virtualenv`, `virtualenv-wrapper`, `venv`, `pipenv`, `pipx` 一系列名词存在困惑，可以进来看看..

<!--more-->

# Python 版本管理管理
## pyenv
**项目主页：**https://github.com/pyenv/pyenv
**核心定位：**在一台电脑上同时管理多个 Python 版本。

下面摘录了一些个人觉得比较重要的信息。

### 1) Understanding PATH
> `/usr/local/bin:/usr/bin:/bin`
> In this example, the /usr/local/bin directory will be searched first, then /usr/bin, then /bin.

首先用上面这个例子理解 `$PATH` 的作用：在终端中可以执行的命令，都可以在这个环境变量指定的多个目录中，找到对应的可执行文件。并且搜索的规则为最先匹配。
```bash
➜  zblog git:(master) ✗ which mkdir
/bin/mkdir
➜  zblog git:(master) ✗
```

### 2) 执行过程
1. Search your PATH for an executable file named pip
2. Find the pyenv shim named pip at the beginning of your PATH
3. Run the shim named pip, which in turn passes the command along to pyenv

`pyenv` 的原理就是在 PATH 的最前面加了一层 shims(垫片)，所以当你在执行 python 命令时会自动切换至对应的版本。

### 3) 切换 python 版本
优先级：shell \> local \> global    

1. `pyenv shell` ： `$PYENV_VERSION` 环境变量, **代表current shell session!**
2. `pyenv local`： local `.python-version` 文件(向上搜索 recursively), **代表 current directory(project)**
3. `pyenv global`：`$(pyenv root)/version`, **代表系统默认的 python 版本**

### 4) Demo
```bash
➜  unswco git:(develope) ✗ pyenv install 3.7.0
➜  unswco git:(develope) ✗ pyenv versions
➜  unswco git:(develope) ✗ pyenv global 3.7.0
➜  unswco git:(develope) ✗ pyenv which python
/Users/henry/.pyenv/versions/3.7.0/bin/python
```
![](/images/blog/190707_python_env_management/15624854039065.jpg)


# 虚拟环境管理
但区分 python 版本还不够，我们希望一个 python 版本可以对应多个虚拟环境(分别对应一个pip和各种第三方包)，实现物理隔离。

## 1. virtualenv
每个 pythoner 入门时都会学习的 virtualenv, 就不多做解释了。三年前竟然还写过一个笔记，感兴趣可以看看：[链接](/blog/20160930/python-venv/)。

## 2. virtualenv-wrapper
定位为 `virtualenv` 的扩展插件，例如使用 `workon` 即可快速切换不同的 `virtualenv` 目录。

## 3. venv
Python 3.3 之后官方自带的虚拟环境管理，与 `virtualenv` 在实现上有一定不同，但看不到使用上有什么不同。
![](/images/blog/190707_python_env_management/15625545552451.jpg)
[Source](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)

## 4. Pipenv
`Pipenv` 在项目的依赖管理(application dependencies)做的还不错，比如它用了 hash 保证说你开发环境和线上的第三方包依赖是完全一致的。但个人尝试用过两次，确实体验不是很好。    

发现网上有很多争论，感兴趣可以看下，还挺有意思的🍉

1. https://chriswarrick.com/blog/2018/07/17/pipenv-promises-a-lot-delivers-very-little/
2. https://github.com/pypa/pipenv/commit/6d77e4a0551528d5d72d81e8a15da4722ad82f26
2. https://np.reddit.com/r/Python/comments/8jd6aq/why_is_pipenv_the_recommended_packaging_tool_by/


# 其他
如果你只是想用 pip 安装一些全局的小工具，那么[pipsi](https://github.com/mitsuhiko/pipsi) 或者 [pipx](https://github.com/pipxproject/pipx) 就是个不错的选择。它会为每个命令行工具自动生成一个虚拟环境：
![](/images/blog/190707_python_env_management/15625174046152.jpg)

**p.s. 推荐使用 `pipx`, 因为 `pipsi` 已经不再维护。**


# 参考
1. https://packaging.python.org/guides/installing-stand-alone-command-line-tools/
2. https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments


# 纪念
![](/images/blog/190707_python_env_management/15625174196560.jpg)




