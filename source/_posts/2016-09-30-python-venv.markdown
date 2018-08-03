---
layout: post
title: "Python Virtual Environments Note"
date: 2016-09-30 01:27:57
comments: true
tags: [python, venv]
---


> 写程序写久了, 你会发现前人留下来的道理总是有那么几分道理的, which will make ur life much easier, 比如每次稍微花点时间建个python的虚拟环境, 会对以后的管理有很大的方便, 节约未来无数的时间~~    

<!--more-->
   

reference: [https://gist.github.com/evansneath/4582716](https://gist.github.com/evansneath/4582716)

```sh
To install virtualenv via pip
$ pip3 install virtualenv

Note that virtualenv installs to the python3 directory. For me it's:
$ /usr/local/share/python3/virtualenv

1. Create a virtualenvs directory to store all virtual environments
$ mkdir ~/.virtualenvs/<project-name>


2. Make a new virtual environment with no packages
$ virtualenv ~/.virtualenvs/<project-name> --no-site-packages


3. To use the virtual environment
$ cd somewhere/virtualenvs/<project-name>/bin
$ source activate
OR
$ source ~/.virtualenvs/unswco_test/bin/activate


4. You are now using the virtual environment for <project-name>. To stop:
$ source deactivate
```

For python3 or python2   
```
virtualenv --python=/usr/bin/python3 <project-name>
```
