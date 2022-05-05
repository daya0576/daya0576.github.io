---
title: 部署Hexo静态博客(下) - 偶遇Netlify, 优雅地持续部署你的博客
date: 2018-08-19 22:27:15
categories:
- 奇技淫巧
---

接[上篇博客](/blog/20180819/deploy-hexo-blog-to-gcp-oss/), 尝试在GCP的OSS上部署静态博客受挫之后, 痛定思痛, 决定先做一个小小的调查, 再敲定最终的部署方案. 这时候搜到一篇非常棒的文章: [静态网站托管服务平台的横向方案比较](https://blog.csdn.net/grackanil/article/details/81196931). 正是在这篇文章中, 我第一次了解到了[Netlify](https://www.netlify.com/). 并一见钟情了, **因为在Net整个部署过程中, 你只需要提交代码, 其余的master部署预览(包括MR的预览), HTTPS证书, 静态资源的优化与CDN加速, 部署消息通知, 等等都不用再操心. 真的是太优雅了XD**    

<!--more-->

# 创建项目
在Netlify注册后的第一次创建项目, 然后授权选择GitHub分支时, 就把我惊艳到了: Netlify会自动检测到该repo为hexo项目, 并自动配置`build command`和`publish directory`. **非常的人性化**.   

# 点点鼠标三步上线网站
![](../images/blog/180819_hexo_to_gcp_netlify/15346905025065.jpg)


## 第一步: 自动部署
不用做任何设置, 每次master分支有更新代码, Netlify就会帮你自动部署代码. 图中左下角为master分支的每次部署记录, 右下角为每个PR的部署, 而且和master分支一样, 会次部署会提供url供用户预览网站效果.   
![](../images/blog/180819_hexo_to_gcp_netlify/15346905884358.jpg)
实时看到部署的日志:
![](../images/blog/180819_hexo_to_gcp_netlify/15346911202648.jpg)
监测到我刚开始写博客时, 一些外链图片的http与https混用, 太酷了:
![](../images/blog/180819_hexo_to_gcp_netlify/15346911557201.jpg)


## 第二步: 修改cname绑定域名
![](../images/blog/180819_hexo_to_gcp_netlify/15346942823694.jpg)

## 第三步: 开启HTTPS
自动生成Let’s Encrypt的证书, 也支持上传自己的证书.   
文档: https://www.netlify.com/docs/ssl/   
![](../images/blog/180819_hexo_to_gcp_netlify/15346942384652.jpg)


# 其他优势:
## 提供webhook的形式触发部署
![](../images/blog/180819_hexo_to_gcp_netlify/15347783952164.jpg)

## 自动在每个页面注入html代码, 适用于一些验证的场景.
![](../images/blog/180819_hexo_to_gcp_netlify/15347784904890.jpg)

## 自动优化
其中例如图片的无损压缩感觉还是挺有意义的.
![](../images/blog/180819_hexo_to_gcp_netlify/15346938018934.jpg)

## 通知:   
部署成功/失败可以通过各种形式传递到用户. 
![](../images/blog/180819_hexo_to_gcp_netlify/15346943108245.jpg)

## 一键HTTPS
![](../images/blog/180819_hexo_to_gcp_netlify/15347785789379.jpg)


## (TODO: 其他优点)


# 缺点:
当然世界上没有什么东西是完美的, netlify也有一些相对的缺点:
1. 速度和阿里云的ecs或oss比起来还是要一些差距的.
2. 不能检测到git submodule的变更. 

