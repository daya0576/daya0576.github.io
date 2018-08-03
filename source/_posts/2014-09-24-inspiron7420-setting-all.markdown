---
layout: post
title: "inspiron7420装ubuntu13.04后的设置"
date: 2014-09-25 18:59:15
comments: true
tags: [ubuntu, study]
---

CSDN以前写的博客   
原地址： [http://blog.csdn.net/dayadaya/article/details/20140765](http://blog.csdn.net/dayadaya/article/details/20140765 "http://blog.csdn.net/dayadaya/article/details/20140765")   
   
<!--more-->
  
<div id="article_content" class="article_content">

<div>
<p>（部分代码摘自互联网）</p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif"><strong>1.修复引导项</strong></span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">如果只是纯粹的装了win7/win8后没有了引导项 可以在win7/win8中用easybcd把/boot添加回来就行了。</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">要是。。完全把引导弄坏了。可以看一下下面这篇文章。</span></p>
<div><span style="color:rgb(128,128,128); font-size:12pt; font-family:times new roman,times,serif">Reinstall / Recover GRUB from Ubuntu live CD / USB</span></div>
<div><span style="color:rgb(128,128,128); font-size:12pt; font-family:times new roman,times,serif">http://www.howopensource.com/2012/05/reinstall-recover-grub-from-ubuntu-12-04-live-cd-usb/</span></div>
<div><span style="font-size:12pt; font-family:times new roman,times,serif">用ubuntu live装一个叫做boot-repair的东西&nbsp;&nbsp; 点修复&nbsp; 等运行完点ok就行了</span><br clear="none">
</div>
<div>
<pre style="margin-top:0px; margin-bottom:10px; padding:0px; border:0px; outline:0px; font-size:16px; vertical-align:baseline; background-color:rgb(199,199,184); font-family:'Courier New',monospace; color:rgb(51,51,51); line-height:16px"><span style="font-size:12pt; font-family:times new roman,times,serif">sudo add-apt-repository ppa:yannubuntu/boot-repair</span></pre>
<pre style="margin-top:0px; margin-bottom:10px; padding:0px; border:0px; outline:0px; font-size:16px; vertical-align:baseline; background-color:rgb(199,199,184); font-family:'Courier New',monospace; color:rgb(51,51,51); line-height:16px"><span style="font-size:12pt; font-family:times new roman,times,serif">sudo apt-get update</span></pre>
<pre style="margin-top:0px; margin-bottom:10px; padding:0px; border:0px; outline:0px; font-size:16px; vertical-align:baseline; background-color:rgb(199,199,184); font-family:'Courier New',monospace; color:rgb(51,51,51); line-height:16px"><span style="font-size:12pt; font-family:times new roman,times,serif">sudo apt-get install -y boot-repair</span></pre>
<pre style="margin-top:0px; margin-bottom:10px; padding:0px; border:0px; outline:0px; font-size:16px; vertical-align:baseline; background-color:rgb(199,199,184); font-family:'Courier New',monospace; color:rgb(51,51,51); line-height:16px"><span style="font-size:12pt; font-family:times new roman,times,serif">boot-repair</span></pre>
</div>
<div><br clear="none">
</div>
<p><span style="font-size:12pt; font-family:times new roman,times,serif"><strong>2.ctrl + alt + cursor 切换工作区间</strong></span><br clear="none">
</p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">装了ubuntu13.04后第一个最大的感受就是。。我切换工作区间的快捷键怎么没有用了！！</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">当然先在设置中把workspace打开，还是不行</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">但在快捷键的列表中看到还是有这几个快捷键。。。最后在ubuntuask上看到了这么一个回答</span><br clear="none">
</p>
<p><span style="color:rgb(128,128,128); font-size:12pt; font-family:times new roman,times,serif">“I had this same issue. I enabled workspace from
<em>Appearance-&gt;Behavior</em>, and also tried using Ubuntu Tweak, but no go on the keyboard shortcuts, even though all the defaults were there.</span></p>
<p><span style="color:rgb(128,128,128); font-size:12pt; font-family:times new roman,times,serif">I then opened CCSM to make sure that the Desktop Wall was enabled. In my case it wasn't, and as soon as I enabled it, my keyboard shortcuts started working again.”</span></p>
<p><span style="color:rgb(128,128,128); font-size:12pt; font-family:times new roman,times,serif"><span style="color:rgb(51,51,51)">然后我就装了一下CCSM，把</span><span style="color:rgb(51,51,51)">Desktop Wall这个选项勾上。。结果真的完全恢复正常了。</span>
</span></p>
<p><br clear="none">
</p>
<span style="font-size:12pt; font-family:times new roman,times,serif"><strong>3.更新软件源&nbsp;</strong></span></div>
<div><span style="font-size:12pt; font-family:times new roman,times,serif">不知道是不是163的源里没有13.04，我直接从12.10升级的时候悲剧了。</span></div>
<div><span style="font-size:12pt; font-family:times new roman,times,serif">然后现在让它自动检测最快的源，现在就用china的第一个源，貌似也挺好用。</span></div>
<div><br clear="none">
<p><span style="font-size:12pt; font-family:times new roman,times,serif"><strong>4. 双显卡</strong></span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">一开机笔记本就轰轰轰的掉点&nbsp;&nbsp;&nbsp;&nbsp; 就按以前的方法把独显关了算了&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; intel的独显绝对够用了。</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">cat&nbsp; /sys/kernel/debug/vgaswitcheroo/switch</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">echo "OFF" &gt; /sys/kernel/debug/vgaswitcheroo/switch</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">可以前好像出现过在ubuntu中把nvidia禁用了&nbsp;&nbsp; 结果win7中也开不起来了。&nbsp;</span></p>
<p><br clear="none">
</p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif"><strong>5.输入法</strong></span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">以前还装了搜狗的输入法。感觉一般吧</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">这次在ubuntu中用了谷歌的输入法 真的给了我很大的惊喜</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">输入时光标终于能跟着拼音动&nbsp;&nbsp;&nbsp;&nbsp; 感觉和windows的体验也没什么区别了。</span></p>
<p><br clear="none">
</p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif"><strong>6.开机的亮度</strong></span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">这肯定都知道吧 <br clear="none">
</span></p>
<table>
<tbody>
<tr style="margin:0px; padding:0px; border:0px; font-size:12px; vertical-align:baseline; background-color:transparent">
<td colspan="1" rowspan="1" style="margin:0px; padding:0px; border:0px; vertical-align:top; background-color:transparent">
<div style="margin:0px 5px 5px 0px; padding:0px; border:0px; font-size:14px; vertical-align:baseline; background-color:transparent; width:660px; word-wrap:break-word; line-height:1.3">
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="color:rgb(128,128,128); font-size:12pt; font-family:times new roman,times,serif">The file /etc/rc.local should look like this:</span></p>
<pre style="margin-top:0px; margin-bottom:10px; padding:5px; border:0px; vertical-align:baseline; background-color:rgb(238,238,238); overflow:auto; width:auto; max-height:600px; font-family:'Ubuntu Mono','Ubuntu Beta Mono A',Consolas,'Bitstream Vera Sans Mono','Courier New',Courier,monospace; word-wrap:normal"><span style="color:rgb(128,128,128); font-size:12pt; font-family:times new roman,times,serif"><code style="margin:0px; padding:0px; border:0px; font-size:14px; vertical-align:baseline; font-family:'Ubuntu Mono','Ubuntu Beta Mono A',Consolas,'Bitstream Vera Sans Mono','Courier New',Courier,monospace; color:rgb(34,34,34)">#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.
echo 0 &gt; /sys/class/backlight/acpi_video0/brightness
exit 0
</code></span></pre>
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="color:rgb(128,128,128); font-size:12pt; font-family:times new roman,times,serif">Per @zerdo: In my dell studio 1558 the brightness setting is stored in<code style="margin:0px; padding:1px 5px; border:0px; font-size:14px; vertical-align:baseline; background-color:#eeeeee; font-family:'Ubuntu Mono','Ubuntu Beta Mono A',Consolas,'Bitstream Vera Sans Mono','Courier New',Courier,monospace; color:#222222">/sys/class/backlight/intel_backlight/brightness</code>.
 Just change the path if your computer doesn't use the acpi_video0 folder.</span></p>
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="color:rgb(128,128,128); font-size:12pt; font-family:times new roman,times,serif">Also, per @Nick : If this is the only answer you read, note that the 0 in&nbsp;<code style="margin:0px; padding:1px 5px; border:0px; font-size:14px; vertical-align:baseline; background-color:#eeeeee; font-family:'Ubuntu Mono','Ubuntu Beta Mono A',Consolas,'Bitstream Vera Sans Mono','Courier New',Courier,monospace; color:#222222">echo
 0</code>&nbsp;is going to be your default brightness setting. I had set this up and it was driving me crazy for a long time : every time I booted up, it would set it to the lowest brightness setting. I prefer mine to start at max brightness, so I used&nbsp;<code style="margin:0px; padding:1px 5px; border:0px; font-size:14px; vertical-align:baseline; background-color:#eeeeee; font-family:'Ubuntu Mono','Ubuntu Beta Mono A',Consolas,'Bitstream Vera Sans Mono','Courier New',Courier,monospace; color:#222222">echo
 10</code>instead. Your hardware might vary in brightness scale.</span></p>
<pre><span style="font-size:12pt; font-family:'times new roman',times,serif"><code>sudo gedit <span style="color:rgb(128,128,128)">/etc/rc.local<br clear="none">在exit 0 前加上</span><br clear="none">echo 2 &gt; /sys/class/backlight/acpi_video0/brightness</code></span></pre>
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="font-size:12pt; font-family:times new roman,times,serif">0～10代表不同的亮度。</span><br clear="none">
</p>
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="font-size:12pt; font-family:times new roman,times,serif"><span style="font-family:'times new roman',times,serif; font-size:14px">作者：daya0576 &nbsp;（天津工大）qq 746058508 &nbsp; &nbsp;欢迎有志同道合的朋友一起学习一起进步</span><br clear="none">
</span></p>
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="font-size:12pt; font-family:times new roman,times,serif">7.截图小工具&nbsp; <br clear="none">
</span></p>
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="font-size:12pt; font-family:times new roman,times,serif">&nbsp;&nbsp;&nbsp; <span style="color:rgb(51,51,51); font-family:tahoma,宋体; font-size:14px; line-height:22px; background-color:rgb(239,239,239)">
sudo apt-get install ksnapshot</span></span></p>
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="font-size:12pt; font-family:times new roman,times,serif"><span style="color:rgb(51,51,51); font-family:tahoma,宋体; font-size:14px; line-height:22px; background-color:rgb(239,239,239)">结果后来发现ubuntu有截图的快捷键 &nbsp;</span><br clear="none">
</span></p>
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="font-size:12pt; font-family:times new roman,times,serif"><span style="color:rgb(51,51,51); font-family:tahoma,宋体; font-size:14px; line-height:22px; background-color:rgb(239,239,239)"><img src="" alt="">
</span></span></p>
<p style="margin-top:0px; margin-bottom:1em; padding-top:0px; padding-bottom:0px; border:0px; vertical-align:baseline; background-color:transparent; clear:both">
<span style="font-size:12pt; font-family:times new roman,times,serif"><span style="color:rgb(51,51,51); font-family:tahoma,宋体; font-size:14px; line-height:22px; background-color:rgb(239,239,239)">
</span></span></p>
</div>
</td>
</tr>
</tbody>
</table>
<p><br clear="none">
</p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">总之ubuntu还是很棒的&nbsp;&nbsp; 和windows比起来&nbsp;&nbsp; 我更愿意留在ubuntu～</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">
</span></p>
<p><span style="font-size:12pt; font-family:times new roman,times,serif">（小菜一个 &nbsp;学习中 &nbsp; &nbsp; 欢迎大家指出错误 &nbsp;&nbsp;<span style="color:rgb(51,51,51); font-family:Tahoma,Verdana,STHeiTi,simsun,sans-serif; font-size:14px; line-height:19px">&gt;_&lt;|||</span> &nbsp;）</span></p>
</div>

</div>