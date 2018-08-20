---
title: 部署Hexo静态博客(下) - 偶遇Netlify, 优雅地持续集成你的博客
date: 2018-08-19 22:27:15
tags: 
    - oss
    - netlify
    - hexo
categories:
  - blog
---

尝试在GCP的OSS上部署静态博客受挫之后([见上篇博客](/blog/20180819/deploy-hexo-blog-to-gcp-oss/)). 俺痛定思痛, 决定先做一个小小的调查, 再进行最终部署方案的选择. 这时候偶遇了一篇非常棒的文章: [静态网站托管服务平台的横向方案比较](https://blog.csdn.net/grackanil/article/details/81196931). 在这篇文章中, 我第一次了解到了[Netlify](https://www.netlify.com/)这个平台. 

**划重点: 在整个部署过程中, 完全是全自动化, 并且免费, 太酷了🆒!!!**    

# 创建项目
在Netlify注册后的第一次创建项目, 并选择GitHub分支时, 就把我惊艳到了: 图下方的`build command`和`publish directory`的配置是自动生成的.    
![](/images/blog/180819_hexo_to_gcp_netlify/15346902374971.jpg)

<!--more-->

# 三步上线网站
![](/images/blog/180819_hexo_to_gcp_netlify/15346905025065.jpg)

## 第一步: 自动部署
不用做任何设置, 每次master分支有更新代码, Netlify就会帮你自动部署代码. 图中左下角为master分支的每次部署记录, 右下角为每个PR的部署, 而且和master分支一样, 会次部署会提供url供用户预览网站效果.   
![](/images/blog/180819_hexo_to_gcp_netlify/15346905884358.jpg)
实时看到部署的日志:
![](/images/blog/180819_hexo_to_gcp_netlify/15346911202648.jpg)
监测到我刚开始写博客时, 一些外链图片的http与https混用, 太酷了:
![](/images/blog/180819_hexo_to_gcp_netlify/15346911557201.jpg)


## 第二步: 修改cname绑定域名
![](/images/blog/180819_hexo_to_gcp_netlify/15346942823694.jpg)

## 第三步: 开启HTTPS
自动生成Let’s Encrypt的证书, 也支持上传自己的证书.   
文档: https://www.netlify.com/docs/ssl/   
![](/images/blog/180819_hexo_to_gcp_netlify/15346942384652.jpg)


# 其他优势:
## 自动优化: 
其中例如图片的无损压缩感觉还是挺有意义的.
![](/images/blog/180819_hexo_to_gcp_netlify/15346938018934.jpg)
## 通知:   
部署成功/失败可以通过各种形式传递到用户. 
![](/images/blog/180819_hexo_to_gcp_netlify/15346943108245.jpg)

## (TODO: 其他优点)


# 缺点:
当然世界上没有什么东西是完美的, netlify也有一些相对的缺点:
1. 速度和

