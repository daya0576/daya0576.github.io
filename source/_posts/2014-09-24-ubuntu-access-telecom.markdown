---
layout: post
title: "天津工业大学软件园 ubuntu电信网设置。"
date: 2014-09-24 19:40:01
comments: true
tags: [ubuntu, study]
---

CSDN以前写的博客   
原地址： [http://blog.csdn.net/dayadaya/article/details/20144941](http://blog.csdn.net/dayadaya/article/details/20144941 "http://blog.csdn.net/dayadaya/article/details/20144941")

<!--more-->
  
<h1>
        <span class="link_title"><a href="http://blog.csdn.net/dayadaya/article/details/20144941">
        天津工业大学软件园 ubuntu电信网设置。
        </a></span>
</h1>    
<div id="article_content" class="article_content">

<p>作者：daya0576 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>
<p>首先学校提供了一个drlinuxclient.bin的东西。</p>
<p>可以上网，但是连上之后用的serverip是10.0.2.5</p>
<p>但电信网只有10.1.5才能连上。so。。</p>
<p>
</p>
<p>下午去办网那问了一下，让他把我的帐号改为网页登陆。</p>
<p>本以为要卖个萌求他一下才能给我改，没想到左边那个戴眼镜的叔叔爽快的答应了</p>
<p>（顺便鄙视一下那些 &nbsp; &nbsp;偷用网页帐号上电信的人 ==）</p>
<p>用网页登陆之后～～～开始正题</p>
<p></p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
1. 添加PPA</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
sudo apt-add-repository ppa:seriy-pr/network-manager-l2tp</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
2. 刷新软件包缓存</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
sudo apt-get update</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
3. 安装network-manager-l2tp</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
sudo apt-get install network-manager-l2tp-gnome</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
安装完之后不要忘记运行以下命令</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
sudo service xl2tpd stop&nbsp;</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
sudo update-rc.d xl2tpd disable</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
重启机器</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">

</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
这时候新建VPN就能够选l2tp选项了。 &nbsp;&nbsp;</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
填上221.239.126.9</p>
<p style="margin-top:0px; margin-bottom:0.714285em; padding-top:0px; padding-bottom:0px; border:0px; line-height:22px; font-size:14px; color:rgb(51,51,51); font-family:tahoma,宋体; background-color:rgb(239,239,239)">
你的帐号和密码</p>
<p>pppsetting那不用改 &nbsp; &nbsp; &nbsp; &nbsp;那是使用什么协议。</p>
<p>貌似用的是MSCHAPv2 &nbsp; &nbsp; &nbsp; &nbsp; 管他呢 &nbsp; &nbsp; &nbsp; 全勾上就是了</p>
<p>然后就开始欢乐的上网了 &nbsp; &nbsp; 哈哈哈～～～～～～～～～</p>
<p>
</p>
<p>
</p>
<p>
</p>
<p>
</p>
<p>
</p>
<p>
</p>

</div>



