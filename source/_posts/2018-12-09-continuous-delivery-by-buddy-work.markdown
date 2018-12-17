---
title: 使用 Buddy 实现博客持续部署
date: 2018-12-09 12:59:32
tags: cd, hexo, git
---

每次写完博客后, 需要手动执行自定义的`deploy.sh`脚本进行手动部署. 虽然已经做到一键发射了, 但作为一名 SRE, 内心还是有几分惭愧的. 特别是每次深夜等待部署的那么两三分钟, 都会陷入无尽的沉思🤔. 毕竟以自动化工具为荣，以人肉操作为耻 XD   

**所以理想情况下: 当 push 代码成功之后, 就可以合上笔记本呼呼大睡了**. 稍微调查了一下, 主要有三个解决方案进入的我的视野, 请容我一一道来. 

<!--more-->  

# 背景
简单阐述一下自己写博客的pipline:
1. 编写一篇post, 或修改一些主题样子
2. git commit + git push
3. 本地运行 deploy shell 脚本:  hexo generate → 处理 atom.xml → 
4. 漫长的等待.

# Jenkins 
第一个想到的工具是 Jenkins, 可以利用 GitHub 的 Webhooks 触发执行部署. 方案上貌似可行性挺高的, 而且也可以 docker 一件部署 Jenkins. 但总觉得哪里不太对, 总觉得依赖太重? 暂时放弃了. 

其实可以写个专门部署用的 dockerfile, 也是个挺不错的选择. 

# Travis
之后尝试是大名鼎鼎的 Travis. 但个人说实话不太喜欢这个东西, 一是感觉配置文件毫无头绪, 上手困难, 二是本地也不知道如何去执行测试, 简直是个21世纪无比反人类的东西呀! 

首先还是理解一下 [travis 的 lifecycle](https://docs.travis-ci.com/user/job-lifecycle/#the-job-lifecycle), 主要分为如下两大部分:

1. **install: 安装所有的依赖**
    - OPTIONAL Install [`apt addons`](https://docs.travis-ci.com/user/installing-dependencies/#installing-packages-with-the-apt-addon)
    - OPTIONAL Install [`cache components`](https://docs.travis-ci.com/user/caching)
    - `before_install`
    - `install`

2. **script: 执行部署的脚本**
    - `before_script`
    - `script`
    - OPTIONAL `before_cache` (for cleaning up cache)after_success or after_failure
    - OPTIONAL `before_deploy`
    - OPTIONAL `deploy`
    - OPTIONAL `after_deploy`
    - `after_script`

于是葫芦画瓢, 简单写了一个 travis 的配置文件:   
```
language: node_js

install:
  - npm install hexo-cli -g
  - npm install

deploy:
  provider: script
  skip_cleanup: true
  script: ./deploy.sh
  on:
    branch: master
```

这时候问题在于: 网站编译成功后, 如何 rsync 到指定的服务器上? 🤔 

# Buddy
最后快速吸引我眼球的自动化部署工具叫做 [Buddy](https://app.buddy.works), 每次 GitHub 更新代码后就会自动触发执行部署: 
![](/images/blog/171216_cicd/15450540893764.jpg)

Buddy 的个性化流程编排的交互做的很好: 这样可以把每一步的边界可以分的很清楚, 让人身心愉悦. 
![](/images/blog/171216_cicd/15450548531301.jpg)

而且因为用的 docker, 所以第一次缓存后, 之后每次执行的速度也特别的快.



完美~

