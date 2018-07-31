---
layout: post
title: "dell inspiron7420 ubuntu13.04触摸板设置"
date: 2014-09-24 21:50:55 +0800
comments: true
categories: [ubuntu, study]
---

CSDN以前写的博客   
原地址： [http://blog.csdn.net/dayadaya/article/details/20141673](http://blog.csdn.net/dayadaya/article/details/20141673 "http://blog.csdn.net/dayadaya/article/details/20141673")   

<!--more-->
  
<div id="article_content" class="article_content">

<h3><a name="t0"></a>废话不多说 &nbsp; &nbsp;
<img src="" alt="">
就是为了调出 touchpad两只手指滚动的设置
讽刺的是google了一个晚上还是在一个中文页面上找到了解决的方法</h3>
<h3><a name="t1"></a>原因：</h3>
<div>
<h3 style="margin:0px 0px 0.3em; padding:0.5em 0px 0.17em; border-width:0px; border-bottom-style:none; line-height:19.046875px; font-family:sans-serif; font-size:17px; color:rgb(34,34,34); overflow:hidden"><a name="t2"></a>
<span style="line-height:1.428571em"><span class="highlight" style="line-height:1.428571em; border:1px solid rgb(212,205,126); background-color:rgb(246,238,150)">Touchpad</span>&nbsp;detected as "PS/2 Generic Mouse" or "Logitech PS/2 mouse"</span></h3>
<p style="margin-top:0.4em; margin-bottom:0.5em; padding-top:0px; padding-bottom:0px; border:0px; line-height:19.046875px; font-family:sans-serif; font-size:13px">
This is caused by a<span style="line-height:1.428571em">&nbsp;</span><a target="_blank" href="https://bugzilla.kernel.org/show_bug.cgi?id=27442" rel="nofollow" shape="rect" style="margin:0px; padding:0px; border:0px; line-height:1.428571em; color:rgb(102,102,102); text-decoration:none; outline:none; font-weight:bold">kernel
 bug</a><span style="line-height:1.428571em">&nbsp;</span>which was fixed in kernel version 3.3. Wrongly detected touchpads cannot be configured with the Synaptic input driver. To fix this, simply install the<span style="line-height:1.428571em">&nbsp;</span><a target="_blank" title="AUR" href="https://wiki.archlinux.org/index.php/AUR" shape="rect" style="margin:0px; padding:0px; border:0px; line-height:1.428571em; color:rgb(102,102,102); text-decoration:none; outline:none; font-weight:bold">AUR</a><span style="line-height:1.428571em">&nbsp;</span>package<span style="line-height:1.428571em">&nbsp;</span><span style="line-height:1.428571em; font-family:monospace"><a target="_blank" href="https://aur.archlinux.org/packages/psmouse-alps-driver/" rel="nofollow" shape="rect" style="margin:0px; padding:0px; border:0px; line-height:1.428571em; color:rgb(102,102,102); text-decoration:none; outline:none; font-weight:bold">psmouse-alps-driver</a></span>.</p>
<p style="margin-top:0.4em; margin-bottom:0.5em; padding-top:0px; padding-bottom:0px; border:0px; line-height:19.046875px; font-family:sans-serif; font-size:13px">
Among the affected notebooks are the following models:</p>
<ul style="margin:0.3em 0px 0px 1.6em; padding:0px; border:0px; line-height:19.046875px; list-style:square outside none; font-family:sans-serif; font-size:13px">
<li style="margin:0px 0px 0.1em; padding:0px; border:0px; line-height:1.428571em">
Acer Aspire 7750G</li><li style="margin:0px 0px 0.1em; padding:0px; border:0px; line-height:1.428571em">
Dell Latitude E6230, E6520, E6430 and E6530 (ALPS DualPoint&nbsp;<span class="highlight" style="line-height:1.428571em; border:1px solid rgb(212,205,126); background-color:rgb(246,238,150)">TouchPad</span>),<span style="line-height:1.428571em"><span style="line-height:1.428571em; color:rgb(0,0,255)">&nbsp;Inspiron
 N5110 (ALPS GlidePoint), Inspiron 14R 5420/Turbo SE7420/SE7520 (ALPS GlidePoint)</span></span></li><li style="margin:0px 0px 0.1em; padding:0px; border:0px; line-height:1.428571em">
Samsung NC110/NF210/QX310/QX410/QX510/SF310/SF410/SF510/RF410/RF510/RF710/RV515</li></ul>
<p style="margin-top:0.4em; margin-bottom:0.5em; padding-top:0px; padding-bottom:0px; border:0px; line-height:19.046875px; font-family:sans-serif; font-size:13px">
You can check whether your&nbsp;<span class="highlight" style="line-height:1.428571em; border:1px solid rgb(212,205,126); background-color:rgb(246,238,150)">touchpad</span>&nbsp;is correctly detected by running:</p>
<pre style="margin-top:0px; margin-bottom:0px; padding:1em; border:1px solid rgb(187,204,221); line-height:1.1em; font-size:14px; color:rgb(34,34,34); background-color:rgb(235,241,245); overflow:auto">$ xinput list
</pre>
<p style="margin-top:0.4em; margin-bottom:0.5em; padding-top:0px; padding-bottom:0px; border:0px; line-height:19.046875px; font-family:sans-serif; font-size:13px">
More information can be found in<span style="line-height:1.428571em">&nbsp;</span><a target="_blank" href="https://bbs.archlinux.org/viewtopic.php?id=117109" rel="nofollow" shape="rect" style="margin:0px; padding:0px; border:0px; line-height:1.428571em; color:rgb(102,102,102); text-decoration:none; outline:none; font-weight:bold">this
 thread</a>.</p>

</div>
<div>
</div>
<div>
</div>
<div>
</div>
<h3><a name="t3"></a>google找到这个包 下载</h3>
<h4><a name="t4"></a><span style="font-family:Consolas,'Bitstream Vera Sans Mono','Courier New',Courier,monospace; font-size:14px; line-height:15.390625px; background-color:rgb(250,250,250)">（psmouse-alps-1.3-alt.tbz）</span></h4>
<p></p>
<p>
</p><table border="0" cellspacing="0" cellpadding="0" style="line-height:21px; font-size:14px; border-collapse:collapse; border-spacing:0px; color:rgb(69,69,69); font-family:Tahoma,Helvetica,Arial,STHeiti">
<tbody style="line-height:1.428571em">
</tbody>
</table>
<p></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; border:0px; line-height:21px; font-size:14px; color:rgb(69,69,69); font-family:Tahoma,Helvetica,Arial,STHeiti">
解压：</p>
<table border="0" cellspacing="0" cellpadding="0" style="line-height:21px; font-size:14px; border-collapse:collapse; border-spacing:0px; color:rgb(69,69,69); font-family:Tahoma,Helvetica,Arial,STHeiti">
<tbody style="line-height:1.428571em">
<tr style="line-height:1.428571em">
<td rowspan="1" colspan="1" style="line-height:1.428571em; padding:0px; margin:0px">
<div style="margin:0px; padding:0px; border:0px; line-height:1.428571em; font-family:Helvetica,Arial,'Droid Sans',sans-serif; font-size:14px">
<div style="padding:0px; border:0px; line-height:1.428571em; width:516.46875px; margin:1em 0px!important; font-size:1em!important; position:relative!important">
<table border="0" cellspacing="0" cellpadding="0" style="">
<tbody style="line-height:1.428571em">
<tr style="">
<td rowspan="1" colspan="1" style="">
<div style="">1</div>
</td>
<td rowspan="1" colspan="1" style="">
<div style="">
<div style=""><code style="">tar</code><span style="line-height:1.428571em">&nbsp;</span><code style="">xvf psmouse-alps-1.3-alt.tbz</code></div>
</div>
</td>
</tr>
</tbody>
</table>
</div>
</div>
</td>
<td rowspan="1" colspan="1" style="line-height:1.428571em; padding:0px; margin:0px">
&nbsp;</td>
</tr>
</tbody>
</table>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; border:0px; line-height:21px; font-size:14px; color:rgb(69,69,69); font-family:Tahoma,Helvetica,Arial,STHeiti">
复制到 /usr/src 目录下：</p>
<table border="0" cellspacing="0" cellpadding="0" style="line-height:21px; font-size:14px; border-collapse:collapse; border-spacing:0px; color:rgb(69,69,69); font-family:Tahoma,Helvetica,Arial,STHeiti">
<tbody style="line-height:1.428571em">
<tr style="line-height:1.428571em">
<td rowspan="1" colspan="1" style="line-height:1.428571em; padding:0px; margin:0px">
&nbsp;</td>
<td rowspan="1" colspan="1" style="line-height:1.428571em; padding:0px; margin:0px">
<div style="margin:0px; padding:0px; border:0px; line-height:1.428571em; font-family:Helvetica,Arial,'Droid Sans',sans-serif; font-size:14px">
<div style="padding:0px; border:0px; line-height:1.428571em; width:516.46875px; margin:1em 0px!important; font-size:1em!important; position:relative!important">
<table border="0" cellspacing="0" cellpadding="0" style="">
<tbody style="line-height:1.428571em">
<tr style="">
<td rowspan="1" colspan="1" style="">
<div style="">1</div>
</td>
<td rowspan="1" colspan="1" style="">
<div style="">
<div style=""><code style="">sudo</code><span style="line-height:1.428571em">&nbsp;</span><code style="">cp</code><span style="line-height:1.428571em">&nbsp;</span><code style="">-afr usr</code><code style="">/src/psmouse-alps-1</code><code style="">.3/<span style="line-height:1.428571em">&nbsp;</span></code><code style="">/usr/src/</code></div>
</div>
</td>
</tr>
</tbody>
</table>
</div>
</div>
</td>
</tr>
</tbody>
</table>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; border:0px; line-height:21px; font-size:14px; color:rgb(69,69,69); font-family:Tahoma,Helvetica,Arial,STHeiti">
安装：</p>
<div style="margin:0px; padding:0px; border:0px; line-height:21px; font-family:Tahoma,Helvetica,Arial,STHeiti; font-size:14px; color:rgb(69,69,69)">
<div style="padding:0px; border:0px; line-height:1.428571em; font-family:Helvetica,Arial,'Droid Sans',sans-serif; width:727.671875px; margin:1em 0px!important; font-size:1em!important; position:relative!important">
<table border="0" cellspacing="0" cellpadding="0" style="">
<tbody style="line-height:1.428571em">
<tr style="">
<td rowspan="1" colspan="1" style="">
<div style="">1</div>
<div style="">2</div>
<div style="">3</div>
</td>
<td rowspan="1" colspan="1" style="">
<div style="">
<div style=""><code style="">sudo</code><span style="line-height:1.428571em">&nbsp;</span><code style="">cd</code><span style="line-height:1.428571em">&nbsp;</span><code style="">/usr/src/ppsmouse-alps-1</code><code style="">.3</code></div>
<div style=""><code style="">sudo</code><span style="line-height:1.428571em">&nbsp;</span><code style="">dkms add .</code></div>
<div style=""><code style="">.</code><code style="">/alps</code><code style="">.sh dkms_build_alps</code></div>
</div>
</td>
</tr>
</tbody>
</table>
</div>
</div>
<h4><a name="t5"></a>安装完驱动之后，synclient就能识别出触摸板了。</h4>
<div>但是发现触摸板变得非常不灵敏，有种想删驱动的感觉。。。</div>
<div>
</div>
<div>但是man synclient一下，发现syclient的功能真的是强大的可怕，</div>
<div>
</div>
<p>之后把</p>
<p>FingerLow &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; = 12
FingerHigh &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;= 15
</p>
<p>都调低后 &nbsp; 终于可以正常使用了</p>
<p>
</p>
<p>哈哈哈哈哈哈！</p>
<p>
</p>
<p>
</p>

</div>