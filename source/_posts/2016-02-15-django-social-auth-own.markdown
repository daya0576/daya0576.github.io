---
layout: post
title: "django social auth插件实践"
date: 2016-02-15 17:50:22 +1100
comments: true
tags: [django, oauth]
---

一群懒人，连注册都不愿意。    
折腾了一天终于把自己的网站加上了第三方登录。    
[http://u.changchen.me/accounts/login](http://u.changchen.me/accounts/login)
<!--more-->

Facebook github和Google都搞定了，就差最后一个微博了，因为要等审核身份。。    
<img  style="max-height:300px" class="lazy" data-original="/images/blog/160215_django_social_auth/title.jpg">     


最后的效果，放弃微博登陆了，因为审核完身份，
网站没有在中国备案还不能用。。也是@#￥%&*%……     
用twitter替代了，图标是用`Fortawesome`的图标，真是方便快捷。  
<img  style="max-height:350px" class="lazy" data-original="/images/blog/160215_django_social_auth/final_django_social.jpg">     


整个效果是用[django-social-auth](https://github.com/omab/django-social-auth)这个插件实现的。    
文档在这：[http://django-social-auth.readthedocs.org/en/latest/](http://django-social-auth.readthedocs.org/en/latest/)

需要注意的几点（被各种问题折腾了一天一夜）：   
1. 要是遇到最后一步登录失败，一定要加`http://your.domain/complete/××××××/`到各个api的`Authorized redirect URIs`里。    
所以登录后跳转最后无法登陆。    
2. 一定要在本地调试好再发布到网上，用localhost替代127.0.0.1，放到`Authorized redirect URIs`就可以了。   
适用于window（stackoverflow上的一个回答）：[How to locally debug Facebook App](http://stackoverflow.com/questions/8798016/how-to-locally-debug-facebook-php-apps)   
3. 最后的时候我遇到一个bug折磨了我一个下午，就是Facebook logining works perfectly locally, but redirecting to login error page in the remote.     
Google这个也没有什么好的回答，最可怕的bug就是没有提示的bug把、、   
最后新建了一个Facebook App，把remote和local App分开，竟然就可以了，也不知道是为什么。     
4. 还有一个问题就是如何获取邮箱，文档上说是在setting里加上参数`FACEBOOK_EXTENDED_PERMISSIONS = ['email']`, 然而好像并没有什么ruan用。再研究一下。    

