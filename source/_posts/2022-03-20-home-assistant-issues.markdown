---
title: 【智能家居】我的家庭网络拓扑
tags:
  - 智能家居
date: 2022-03-20 17:10:51
---

近期上海疫情😷日益严重，封锁在家着实无聊，淘宝购入一块 R2S 开始折腾软路由科学上网～

这篇文章简单分享一下我的家庭网络拓扑，以及回答软路由作为二级路由后：   
1⃣️ **电视设备如何科学上网（主路由模式）？**   
2⃣️ **树莓派 HA（Home Assistant）如何科学上网（旁路由模式）？**   
3⃣️ **HA 如何控制二级路由子设备？**   

<!--more-->

## 一、电视如何科学上网（主路由模式）

购买软路由后，首当其冲需解决电视科学上网的问题。

下图为商家推荐的模式，相当于“软路由”完全接管家庭的网络：
![R2S_taobao_solution](../images/blog/2021-09-04-jvm-note/R2S_taobao_solution.svg) 

但个人更期望一级路由网络尽可能的纯粹（不影响老婆大人上网秒杀），所以选择将软路由作为**二级路由器**。

在不改变原有网络架构的情况下，配置闲置路由器，实现**设备按需接入，即插即用**：
![openwrt_v1](../images/blog/2021-09-04-jvm-note/openwrt_v1.svg)

顺利完成目标，畅快享用好剧！
![netflix_1](../images/blog/2021-09-04-jvm-note/netflix_1.png)

![netflix_2](../images/blog/2021-09-04-jvm-note/netflix_2.png)

## 二、HA 如何科学上网（旁路由模式）

子设备一级路由，如果也有“科学上网”的需求，但迫于各种原因无法移动至二级路由网段，例如“HA（home assistant）” 若移动至二级路由后，将无法发现家庭智能设备。

这时软路由摇身一变，承担起旁路由的职责，也就是说修改子设备的「路由」配置，指向软路由即可：
*⚠️除此之外还需修改软路由防火墙与静态路由配置，请参考第三小节*

![](../images/blog/2021-09-04-jvm-note/16477658391223.jpg)

从此安装更新等操作，如丝般顺滑 🥰


## 三、HA 如何控制二级路由子设备

引入软路由作为二级路由器后，产生一个新的问题：由于 NAT 以及防火墙的存在，下图中的“树莓派”设备，无法找到二级设备“电视”（不在同一个网段）。

最终导致无法在 HA（Home Assistant）中，控制电视与游戏机等设备😭：
![r2s_3](../images/blog/2021-09-04-jvm-note/r2s_3.svg)


所以需要手动新增静态路由（添加在 Linksys 与 R2S 路由器中），告诉访问 `电视（192.168.2.170）`的请求，具体应该走哪一个网关。

但是在 TP-Link 路由中，可能因为 NAT 以及防火墙的存在，迟迟无法搞定，所以新引入了一个交换机：
![r2s_4](../images/blog/2021-09-04-jvm-note/r2s_4.svg)


以下为具体修改的配置：

### 1）新增静态路由
一级路由静态路由设置（帮助树莓派找到二级网段），以 Linksys 路由器为例：
![](../images/blog/2021-09-04-jvm-note/16476806894838.jpg)

二级路由（R2S 软路由）不知道为什么没有也没有子设备的路由，

```shell
$ route -n  
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.200.1.1      0.0.0.0         UG    0      0        0 eth0
10.200.1.0      0.0.0.0         255.255.255.0   U     0      0        0 eth0
```

http://192.168.2.1/cgi-bin/luci/admin/network/routes
![](../images/blog/2021-09-04-jvm-note/16477510448050.jpg)

### 2）修改防火墙配置
修改 `网络/防火墙/基本设置` 中“转发”配置，更新为“接受”：
![](../images/blog/2021-09-04-jvm-note/16477634717388.jpg)

### 3）实验测试成功

```shell
➜  /dev traceroute 192.168.2.170
traceroute to 192.168.2.170 (192.168.2.170), 64 hops max, 52 byte packets
 1  linksys01644 (10.200.1.1)  7.046 ms  5.507 ms  6.316 ms
 2  10.200.1.94 (10.200.1.94)  6.584 ms  7.058 ms  7.362 ms
 3  192.168.2.170 (192.168.2.170)  7.280 ms  7.356 ms  7.777 ms
```

顺利重新获取对电视的掌控权 🥰

![IMG_4495](../images/blog/2021-09-04-jvm-note/IMG_4495.png)

![](../images/blog/2021-09-04-jvm-note/16477647212258.jpg)



## 四、参考：
1. https://www.right.com.cn/FORUM/thread-5493924-1-1.html 
2. https://www.home-assistant.io/integrations/discovery/#mdns-forwarding
3. ..