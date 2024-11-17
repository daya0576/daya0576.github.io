---
title: 使用 Buddy 实现博客持续部署
date: 2018-12-09 12:59:32
categories:
- 奇技淫巧
---

每次写完博客后, 需要手动执行自定义的`deploy.sh`脚本进行手动部署. 虽然已经做到一键发射了, 但作为一名 SRE, 内心还是有几分惭愧的. 特别是每次深夜等待部署的那么两三分钟, 都会陷入无尽的沉思🤔. 毕竟以自动化工具为荣，以人肉操作为耻 XD

**所以理想情况下: 当 push 代码成功之后, 就可以合上笔记本呼呼大睡了**. 稍微调查了一下, 主要有三个解决方案进入的我的视野, 请容我一一道来.

<!--more-->

# 背景
简单阐述一下自己写博客的 pipline:
1. 编写一篇博客, 或修改一些主题样式
2. push 至 GitHub 仓库
3. 本地运行 deploy shell 脚本:
    - hexo generate
    - python 脚本处理 atom.xml(图片lazyload的问题)
    - rsync 到服务器
4. 漫长的等待 zZ

# 之前的探索
从 Octopress 迁移到 Hexo 之后, 就一直在探索最优的部署方式. 尝试过 google oss, 但没法解决 https 的问题, 尝试过 Netlify. 但自动部署在 cloudflare 上的, 国内的速度感人.
- [部署Hexo静态博客(上) - Google Cloud Platform OSS之旅](/blog/20180819/deploy-hexo-blog-to-gcp-oss/)
- [部署Hexo静态博客(下) - 偶遇Netlify, 优雅地持续部署你的博客](/blog/20180819/deploy-hexo-blog-to-netlify/)

# 解决方案
## Jenkins
第一个想到的工具是 Jenkins, 可以利用 GitHub 的 Webhooks 触发执行部署. 方案上貌似可行性挺高的, 而且也可以 docker 一件部署 Jenkins. 但总觉得哪里不太对, 总觉得依赖太重? 暂时放弃了.

其实可以写个专门部署用的 dockerfile, 也是个挺不错的选择.

## Travis
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

## Buddy
最后快速吸引我眼球的自动化部署工具叫做 [Buddy](https://app.buddy.works), 每次 GitHub 更新代码后就会自动触发执行部署:
![](/images/blog/171216_cicd/15450540893764.jpg)

Buddy 的个性化流程编排的交互做的很好: 这样可以把每一步的边界可以分的很清楚, 让人身心愉悦. 而且因为用的 docker, 所以第一次缓存后, 之后每次执行的速度也特别的快.
![](/images/blog/171216_cicd/15450634864348.jpg)

Perfect~

## GitHub Actions
[链接](https://github.com/features/actions)，申请试用中...    
![](/images/blog/171216_cicd/15524872888810.jpg)



