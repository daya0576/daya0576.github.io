---
title: 部署Hexo静态博客(上) - Google Cloud Platform OSS之旅
date: 2018-08-19 18:03:33
categories:
- 奇技淫巧
---

众所周知, 要使用国内的云服务, 不管是vps也好, cdn加速也好, 域名都是要备案的. 但对于我来说, 备案是不可能备案的，这辈子不可能备案的. 

正好前段时间工作中接触了aliyun的oss, 就萌生了将网站部署到Google Cloud Platform的OSS上的想法💡.
![](/images/blog/180819_hexo_to_gcp_oss/15346829618992.jpg)

**结论:**    
GCP的OSS速度看上去还是很优秀的, 但部署步骤繁琐, https比较棘手, 还是放弃了这种部署方式.   
最终选择了Netlify, 见下一篇博客: 

<!--more-->

# 新建bucket
## 验证对网站的所有权
创建前要先在search console中验证这个网站是你的, [验证链接](https://www.google.com/webmasters/tools/home?hl=en). 
有很多种验证的方法, 如果你使用的是hexo的next主题, 可以在`_config.yml`中配置`google_site_verification`字段就ok了. 
![](/images/blog/180819_hexo_to_gcp_oss/15346836448137.jpg)
## 注意bucket的名字
如果要serve静态网站的话, **名字要和域名保持一致.**
![](/images/blog/180819_hexo_to_gcp_oss/15346836542164.jpg)

## 地区:
记得地区选Asia哟.
![](/images/blog/180819_hexo_to_gcp_oss/15346836624305.jpg)


# 上传文件
## gsutil安装
安装gsutil
`pip install gsutil`
不支持python3??? 
![](/images/blog/180819_hexo_to_gcp_oss/15346836717853.jpg)

## gsutil简易版步骤
创建bucket(或者手动创建, 这个不知道如何定制地区)   
`gsutil mb gs://www.hypers.me`
全部bucket的权限默认为公共读:   
`gsutil defacl set public-read gs://www.hypers.me`
上传文件:   
`gsutil rsync -R local-dir gs://www.example.com`
设置index&404:   
`gsutil web set -m index.html -e 404.html gs://www.hypers.me`


# 配置DNS, 添加CNAME记录
文档: [https://cloud.google.com/storage/docs/hosting-static-website?hl=en\_US&\_ga=2.265398415.-1885452353.1527271271](https://cloud.google.com/storage/docs/hosting-static-website?hl=en_US&_ga=2.265398415.-1885452353.1527271271)
```
NAME                  TYPE     DATA
www.example.com       CNAME    c.storage.googleapis.com.
```


# 测速
**GCP OSS(左)** VS **Aliyun香港 OSS(右)**   
![](/images/blog/180819_hexo_to_gcp_oss/15346837142907.jpg)

**GCP OSS(左)** VS **Aliyun香港 ECS(右)**
![](/images/blog/180819_hexo_to_gcp_oss/15346837319940.jpg)


# https
文档: [https://cloud.google.com/storage/docs/troubleshooting#https](https://cloud.google.com/storage/docs/troubleshooting#https)
提供了三种解决方案:
- [set up a load balancer](https://cloud.google.com/compute/docs/load-balancing/http/adding-a-backend-bucket-to-content-based-load-balancing)
- 用cloudflare之类的第三方工具
- 放弃gcp, 在[Firebase Hosting](https://firebase.google.com/docs/hosting/)上serve你的网站

要哭了T^T




# reference:
- 官方文档: https://cloud.google.com/storage/docs/hosting-static-website

