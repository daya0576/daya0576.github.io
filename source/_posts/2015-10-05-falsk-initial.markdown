---
layout: post
title: "flask安装配置遇到的问题"
date: 2015-10-05 13:34:24 +0800
comments: true
tags: [flask, python, virtualenv]
---


> 最近开始看一看flask开发，结果出师不利，一开始就碰到了问题。    
在运行 virtualenv venv 创建一个虚拟环境的时候报错了。    
（我的python是2.7的。）   
<!--more-->

错误信息：   
```
F:\git\flask\myproject>virtualenv wtf
New python executable in wtf\Scripts\python.exe
Installing setuptools, pip, wheel...
  Complete output from command F:\git\flask\myproject\wtf\Scripts\python.exe -c "import sys, pip; sys...d\"] + sys.argv[1:]))" setuptools pip wheel:
  Ignoring indexes: https://pypi.python.org/simple
Collecting setuptools
  ...
warning and allow it anyways with '--trusted-host None'.
  Could not find a version that satisfies the requirement setuptools (from versions: )
No matching distribution found for setuptools
----------------------------------------
...Installing setuptools, pip, wheel...done.
Traceback (most recent call last):
  File "I:\Program Files (x86)\python27\Scripts\virtualenv-script.py", line 9, in <module>
    load_entry_point('virtualenv==13.1.2', 'console_scripts', 'virtualenv')()
  File "I:\Program Files (x86)\python27\lib\site-packages\virtualenv-13.1.2-py2.7.egg\virtualenv.py", line 832, in main
    symlink=options.symlink)
  File "I:\Program Files (x86)\python27\lib\site-packages\virtualenv-13.1.2-py2.7.egg\virtualenv.py", line 1004, in create_environment
    install_wheel(to_install, py_executable, search_dirs)
  File "I:\Program Files (x86)\python27\lib\site-packages\virtualenv-13.1.2-py2.7.egg\virtualenv.py", line 969, in install_wheel
    'PIP_NO_INDEX': '1'
  File "I:\Program Files (x86)\python27\lib\site-packages\virtualenv-13.1.2-py2.7.egg\virtualenv.py", line 910, in call_subprocess
    % (cmd_desc, proc.returncode))
OSError: Command F:\git\flask\myproject\wtf\Scripts\python.exe -c "import sys, pip; sys...d\"] + sys.argv[1:]))" setuptools pip wheel failed with error code 1
```

注意最后一行:   
<a style="color:red">"OSError: Command F:\git\flask\myproject\wtf\Scripts\python.exe -c "import sys, pip; sys...d\"] + sys.argv[1:]))" setuptools pip wheel failed with error code 1"</a>

在网上找到了别人的一个解决方法:   
[http://stackoverflow.com/questions/21826859/setting-up-a-virtualenv-no-module-named-pip](http://stackoverflow.com/questions/21826859/setting-up-a-virtualenv-no-module-named-pip)：
和我的错误一样，但是python3.3的一个bug，不知道为什么我会出现这个错误。    
但总算解决了，希望接下来不会有问题。   

## 解决方法
- Run virtualenv venv --no-setuptools
- Activate that virtualenv (venv\Scripts\activate)
- Download and run [get-pip.py](/images/blog/151005_flask_init/get-pip.py) to manually install pip & setuptools into this virtualenv
- Continue as normal    

**总结：**遇到问题的时候要找到关键的错误信息，在最短时间搜到解决方法。    
不要浪费时间在漫无目的寻找答案上。   




