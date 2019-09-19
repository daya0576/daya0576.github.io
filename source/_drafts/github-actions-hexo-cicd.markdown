---
title: 使用 GitHub Actions 实现 Hexo 博客的 CICD
tags:
---

CI/CD(continuous integration and continuous deployment) 是个被提出很久的概念了，它确实有很多的好处，例如小而快的迭代可以尽早的发现 bug 并轻松修复，并且代码合并也不会那么痛苦。但说到底还是因为程序员比较「懒」，当 push 代码成功的那一刻，只想合上笔记本，闭上眼睛，静静地等待自动部署成功后滴的一声通知，然后安然入睡 zZ

之前写过一篇文章：[《使用 Buddy 实现博客持续部署》](/blog/20181209/continuous-delivery-by-buddy-work/)，Buddy 是很不错，页面操作炫酷友好，但美中不足，免费版有内存 1G 的限制，让人每次操作都有点小心翼翼，正好 GitHub Action 的 Public Beta 终于排上号了！「喜新厌旧」的程序员又开始折腾起来了。
![](/images/blog/190915_github_actions/15685554780026.jpg)


# 部署配置
话不多说直接看代码就明白啦：
```
name: Hexo CICD

on:
  push:
    branches:
    - master

jobs:
  job1:
    name: hexo build & deploy
    runs-on: ubuntu-18.04
    
    steps:
    - uses: actions/checkout@master
      with:
        submodules: true
    - uses: actions/setup-node@master
      with:
        node-version: 8.x
        
    - name: Installation
      run: |
        npm install
        npm install -g hexo-cli
        
    - name: Generate
      run: hexo clean && hexo g
    
    - name: Handle img lazyload for RSS  
      run: python3 atom_plus.py && chmod 755 public/atom.xml
      
    - name: Deploy
      run: |
        mkdir -p $HOME/.ssh
        touch "$HOME/.ssh/known_hosts"
        
        echo "${{ secrets.GITHUB_ACTION_PRIVATE_KEY }}" > $HOME/.ssh/deploy_key
        chmod 700 $HOME/.ssh
        chmod 600 $HOME/.ssh/deploy_key
        chmod 600 $HOME/.ssh/known_hosts
        eval $(ssh-agent)
        ssh-add $HOME/.ssh/deploy_key
        
        ssh-keyscan 47.52.**.** > $HOME/.ssh/known_hosts
        
        hexo deploy
```

# 个人感受
## 优点：
1. 灵活(flexibility): 脚本而不是界面配置的模式，可以很灵活的满足软件开发的完整生命周期(build, test, package, release, or deploy)
2. 稳定: 毕竟大厂出品，还是很良心的，每个 vm 的配置：
    - 2 core CPUs
    - 7 GB of RAM memory
    - 14 GB of SSD disk space
3. Action Marketplace：有很多官方和个人的 action 在不断完善并可以轻松的引用（[链接](https://github.com/marketplace?type=actions)），例如有 rsync 的 action 可以直接引用，只需要输入参数即可，它会帮你处理所有用户授权的细节。
4. ...

## 缺点：
- 调试不友好：不知道是不是我姿势不太对，只能不断的 commit/push 触发 action. 理想情况应该可以在本地直接 debug, 并且只对失败的那一步重试。
- 慢：执行一次需要 1m44s. 因为没有缓存，每次都是重新构建，感觉还是有很大提升空间的。


