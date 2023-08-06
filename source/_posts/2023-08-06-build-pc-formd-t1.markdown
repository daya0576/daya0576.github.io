---
title: FormD T1 V2.0 装机小记
date: 2023-08-06 22:12:09
tags:
---


清晰记得学生时代，烈阳高照的一个午后，偷偷购入 mp4，路中便迫不及待的撕开包装，一股迷人的数码产品“香气”至今令人难忘。

多年过去了，我决定自己动手组装一台 PC 小玩具，重新体验开箱的快乐，并与你分享 :)

<!--more-->

![1](../images/blog/2021-09-04-jvm-note/1.png)
![2](../images/blog/2021-09-04-jvm-note/2.png)
![5](../images/blog/2021-09-04-jvm-note/5.png)
![6](../images/blog/2021-09-04-jvm-note/6.png)
![7](../images/blog/2021-09-04-jvm-note/7.png)
![8](../images/blog/2021-09-04-jvm-note/8.png)


# 整体配置：
```
机箱：FormD T1 Sandwich
主板：华硕 Z690-I GAMING 
CPU：Intel Core i5 12400K
内存：海盗船 复仇者 16gx2
SSD：三星980pro 1T
散热：猫头鹰 NH-L9I 17xx
风扇：猫头鹰 NF-A12x25 两个
显卡：RTX 4070 FE
电源：海盗船 SF750 platinum
```

## 必选
### 机箱 ★★★★★
机箱的选择花了最多的时间，在 ATX、MATX 以及 ITX 中选择了最为小巧的 ITX 机箱（对应主板的尺寸为 17cm x 17cm）

经过几周的筛选，最终对 FormD T1 一见钟情（我选择的是 SANDWICH KIT + TITANIUM COLOR）。

一是颜值即正义，配合官网提供了大量 DLC 套件，在组装的过程中，由衷的感叹 t1 机箱就像一份精心设计的代码，不管是可维护性和扩展性都优雅的令人陶醉。

除了价格略贵，几乎没有任何缺点。
![1EDAD6DE-FC0C-4A95-9251-7A448D00B796_1_105_c](../images/blog/2021-09-04-jvm-note/1EDAD6DE-FC0C-4A95-9251-7A448D00B796_1_105_c.jpeg)


### 主板 ★★☆☆☆
在主板的选择上踩了个小坑，由于习惯了苹果设备雷电口一根 typec 的解决方案，寻思着从 mac mini 切换至 pc 也只需插拔线即可，所以特地选择了附带雷电口的主板。

理想很丰满：
![理想](../images/blog/2021-09-04-jvm-note/%E7%90%86%E6%83%B3.svg)

现实却给人无情一击，虽然雷电口可以输出 4k 视频信号，但主板没有 DP In 接口，只能单独显卡接线至显示器，着实不是很优雅：
![现实](../images/blog/2021-09-04-jvm-note/%E7%8E%B0%E5%AE%9E.svg)

如果 cpu 具备核心显卡，虽然咨询了客服反馈无法输出独显信号，但网上反馈目前普遍支持混合输出（一定性能损耗？），等下一代 cpu 换代时可不能省这个 50 元了 XD

### 散热 ★★★★★
猫头鹰的风扇给人很大的惊喜，用一个词形容就是精致：
![7488B0C5-4AED-4327-97DE-0318409A167E_1_102_a](../images/blog/2021-09-04-jvm-note/7488B0C5-4AED-4327-97DE-0318409A167E_1_102_a.jpeg)

关于进出风方向：Always intake on the sides (GPU, CPU cooler, PSU), and exhaust out the top

### CPU ★★★☆☆
中规中矩，性价比之王，真实游戏体验中还未遇到瓶颈。
![IMG_7616](../images/blog/2021-09-04-jvm-note/IMG_7616.jpeg)

### 显卡 ★★★★☆
4070fe 两槽的苗条身材，配合200w 的高能效，搭配 itx 机箱简直就是绝配
![1](../images/blog/2021-09-04-jvm-note/1-2.png)

除了一定的性价比问题。。
![1](../images/blog/2021-09-04-jvm-note/1-1.png)


## 可选
### 定制线 
装机最为挑战的是如何更加优雅的理线，有更高追求的朋友可以重点提前规划设计。

> 充满激情的工艺，就是要确保即使是隐藏的部分也要做得很漂亮。

### 风扇罩
第一次开机后出现异响，排查后虚惊一场，原来是风扇 k 到了电源线导致。购买两个风扇铁网后，轻松解决。

### 蓝牙接收器
开机后，蓝牙出现连接不上 + 声音信号卡顿的问题，折腾到凌晨也没有解决。第二天 pdd 购买蓝牙接收器 fix 该问题。

### 前面板 typec 扩展 
官网不清楚什么原因一直缺货，在万能的咸鱼购入。

# 总结
装机的难度比想象小一些，跟着视频或官网的电子说明书，多少花点时间即可圆满完成任务。

😚为10月25日发售的天际线2做好充足的准备～
![Pasted Graphic](../images/blog/2021-09-04-jvm-note/Pasted%20Graphic.png)


# 参考

1. 机箱官方说明书：https://cdn.shopify.com/s/files/1/0375/5973/0308/files/Manual_T1V2_V1.0.pdf
2. 第三方 build guide：https://youtu.be/ivMawWusdZI
3. 猫头鹰 CPU 散热指南：https://noctua.at/en/products/cpu-cooler-retail
4. 国内装机论坛：https://www.chiphell.com/
5. 装机分享网站：https://pcpartpicker.com/builds/