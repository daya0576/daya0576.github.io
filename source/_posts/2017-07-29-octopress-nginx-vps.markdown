---
layout: post
title: "在vps上部署你的静态博客(网站)"
date: 2017-07-29 14:10:26 +0800
comments: true
tags: [octopress, vps]
---

昨晚博客搬到香港的vps上了. 在这篇文章把简单的几个步骤, 总结分享一下( 本文主要以Octopress为例子, 但流程其实都是共通的).      
<img style="max-height:300px" class="lazy" data-original="/images/blog/170729_hoster/boost1.png">
<!--more-->
   






# 背景   
这个[博客](https://changchen.me)原先是部署在Github Page服务上的, 优缺点很明显:        

**优点:**  

1. 免费!!!

**缺点:** 

1. 大陆和美利坚毕竟跨着一个太平洋, 延迟还是有些高的.
2. 无法配置证书(之前用的cloudflare解决方案, 但必须要用它家的cdn, 感觉不能掌控的因素太多了).
3. 其实最重要的一点是, 如果博客放在github的page服务上, 是**无法被百度收录**的.    



# 第一步 购买VPS
我用的是一个香港的vps供应商, 比较小众, 选择它只是因为被他们的主页萌到了 (๑•ᴗ•๑):    
[http://www.hostker.com/](http://www.hostker.com/)     
可以点我的[**推广链接**](https://i.hostker.com/flag/8397)获取优惠:   
_通过邀请链接注册的新用户完成手机绑定可以获得 0.5K 贝壳(相当于 5 元.)_   
<img style="max-height:300px" class="lazy" data-original="/images/blog/170729_hoster/shell.png">   

**选择vps的另一个原因:**   

1. 可以把自己**别的网站**, e.g. [unsw.co](https://www.unsw.co) 也放到这个vps上.     
2. 选的香港vps, 肯定还可以做别的事情.    

所以在节省别的开销的情况下, 这主机的钱💰个人觉得还是值得的.    
<img style="max-height:200px" class="lazy" data-original="/images/blog/170729_hoster/server.png">



# 第二步 同步网站内容
因为是静态网站, 所以只要把生成的静态内容, 放到vps上供访问就行了.   
Octopress提供了原生的同步方法: 只需将`rake deploy`的模式从默认的push改为Rsync, 再允许`rake deploy`就会将代码同步到远程的服务器上, 具体的配置如下:   
```yaml
## -- Rsync Deploy config -- 
# Be sure your public key is listed in your server's ~/.ssh/authorized_keys file
ssh_user       = "username@vps的IP地址"
ssh_port       = "22"
document_root  = "~/zblog/"
rsync_delete   = false
rsync_args     = ""  # Any extra arguments to pass to rsync
deploy_default = "rsync"
```    



# 第三步 配置Nginx
将访问的域名代理 --> vps上同步的文件夹.    
我的nginx配置供参考:

1. 将www.changchen.me 302 --> changchen.me   
2. 将changchen.me --> ~/zblog/
```
server {
    server_name www.changchen.me;
    rewrite ^/(.*)$ https://changchen.me/$1 redirect;
}

server {
        listen 80;
        root ~/zblog/;
        index index.html index.htm;
        server_name changchen.me;
}
```


 
# 第四部 配置DNS
我用的是Dnspod, 只需新建两个A记录, 将`changchen.me`和`www.changchen.me`都指向你的VPS的IP地址, 然后nginx会根据上边的配置去反向代理.   



# 第五步 配置证书
DNS生效需要一会时间, 刚好可以等待期间为你的博客加上免费的SSL证书.    
我用的是[Let's Encrypt](https://certbot.eff.org/), 真的是无脑一键配置.   



# 总结
你的博客就顺利搭建起来了🎉    
`changchen.me --> DNS --> VPS IP --> 302 --> blog dir.`   

相比以前跨越半个地球去访问网站, 速度刷刷刷的上去了~   
<img style="max-height:300px" class="lazy" data-original="/images/blog/170729_hoster/boost1.png"><img style="max-height:300px" class="lazy" data-original="/images/blog/170729_hoster/boost2.png">   


