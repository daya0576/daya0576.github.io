---
title: 使用 GitHub Actions 实现 Hexo 博客的 CICD
categories:
- 奇技淫巧
date: 2019-09-23 20:36:32
---

CI/CD(continuous integration and continuous deployment) 被提出很久了并逐步流行，因为它确实有很多的好处：例如小而快的迭代可以尽早发现 bug 并更加轻易地修复，代码合并也不会那么痛苦。但说到底还是因为「懒」，当 push 代码成功的那一刻，只想合上笔记本闭上眼睛，静静地等待自动部署成功后滴的一声通知，然后安然入睡 zZ

<!--more-->

身为一名 SRE, 之前对自己博客的 CICD 做过不少尝试（感兴趣可以看看）：

1. [《使用 Buddy 实现博客持续部署》](/blog/20181209/continuous-delivery-by-buddy-work/)
2. [《部署 Hexo 静态博客 (上) - Google Cloud Platform OSS 之旅》](/blog/20180819/deploy-hexo-blog-to-gcp-oss/)
3. [《部署 Hexo 静态博客 (下) - 偶遇 Netlify, 优雅地持续部署你的博客》](/blog/20180819/deploy-hexo-blog-to-netlify/)

最近几个月一直用的 [Buddy](https://buddy.works/)，页面炫酷操作友好，但美中不足的是有点"小气"：免费版的内存有 1G 的限制，让人每次操作都有点小心翼翼。。正好 GitHub Action 的 Public Beta 终于排上了号！「喜新厌旧」的程序员又开始折腾起来了。
![](../images/blog/190915_github_actions/15685554780026.jpg)



# GitHub Actions 部署配置
明人不说暗话，直接看代码应该就明白啦：
```yaml
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
1. **灵活(flexibility):** 脚本而不是界面配置的模式，可以很灵活的满足软件开发的完整生命周期(build, test, package, release, or deploy)
2. **大气:** 毕竟大厂出品，还是很良心的，每个 vm 的配置：
    - 2 core CPUs
    - 7 GB of RAM memory
    - 14 GB of SSD disk space
3. **Action Marketplace:** 有很多官方和个人的 action 在不断完善并可以轻松的引用（[链接](https://github.com/marketplace?type=actions)），例如有 rsync 的 action 可以直接引用，只需要输入参数即可，它会帮你处理所有用户授权的细节。类似 [Docker Hub](https://hub.docker.com/)
4. ...

## 缺点：
- **上手略难：**灵活和用户友好是一对 tradeoff, 和 buddy 拖拖鼠标的填填配置的无脑操作比起来，灵活的 Github actions 还是牺牲了一定的易用性，但毕竟用户都是程序员，应该也不是什么大问题。突然想起来，之前最早宣传的时候，那个炫酷的图为什么再也没看到了，是被放弃了吗？？![](../images/blog/190922_cloudflare_and_next_bug/15691581294746.jpg)

- **调试不友好：**不知道是不是我姿势不太对，只能不断的 commit/push 触发 action. 理想情况应该可以在本地直接 debug, 并且只对失败的那一步重试。
- **慢：**执行一次需要 1m44s. 因为没有缓存，每次都是重新构建，感觉还是有很大提升空间的。
- **bug多：**不知道是不是公测版的原因，经常碰到奇奇怪怪的 bug...![](../images/blog/190922_cloudflare_and_next_bug/15695951675917.jpg)


 

