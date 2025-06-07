---
title: "[硬件] 大逆不道 - 组装一台仅通过 WiFi 连接的 NAS"
date: 2025-04-28T11:00:38+08:00
categories:
- 智能家居
---

### 更新（20250515）：
最近将主机搬回了书房，硬盘休眠后轻微的风扇声，倒如同白噪音一般帮助我更好地集中注意力。

<blockquote class="reddit-embed-bq" data-embed-showtitle="true" data-embed-theme="dark" data-embed-created="2025-05-15T01:58:47Z">
<a href="https://www.reddit.com/r/homelab/comments/1glafbg/comment/lvstz6d/">Comment</a><br> by
<a href="https://www.reddit.com/user/tamay-idk/">u/tamay-idk</a> from discussion
<a href="https://www.reddit.com/r/homelab/comments/1glafbg/does_the_noise_of_your_servers_not_bother_you/"></a><br> in
<a href="https://www.reddit.com/r/homelab/">homelab</a>
</blockquote>
<script async src="https://embed.reddit.com/widgets.js" charset="UTF-8"></script>


---

在生活与工作中，我们总是一味地追求“快”，这个 feature 必须要在这周上线，那个 bug 必须在明天天亮前解决。但殊不知解决 bug 最好的办法是慢下来，take a break，甚至说不定睡一觉它自己就消失了。

上一次咱们讨论了如何[组装一台万兆 NAS](/blog/20241228/synology_to_unraid/)，这次俺打算组装一台可以通过 WiFi 接入家庭网络的 NAS，然后把它放在阳台上，彻底不去想它的存在 :p

![61E224F2-5A91-4416-8570-FCCB66CA1E04_1_201_a](/images/blog/global/61E224F2-5A91-4416-8570-FCCB66CA1E04_1_201_a.jpeg)

# 目录
- [软件](#软件)
- [硬件](#硬件)
  - [主板 & CPU](#主板cpu)
  - [机箱](#机箱)
- [价格（除去 HDD 存储）](#价格（除去hdd存储）)
- [功率统计](#功率统计)
- [网络性能](#网络性能)


# 软件
相比于通过 AP 路由接入，Unraid 在刚刚发布的 [7.1.0-beta.1](https://docs.unraid.net/unraid-os/release-notes/7.1.0/) 中原生支持了无线连接。

实际的接入体验相当丝滑。从下图可以看到，虽然设备被放置在阳台上，但它与客厅的主路由器相距不到十米，信号强度仍处于可接受的范围内。
![](/images/blog/global/17458026356328.jpg)


# 硬件

## 主板 & CPU 
考虑未来的可扩展性，俺选择了一张 ATX 主板：[华硕 PRIME Z370M-PLUS II](https://www.asus.com.cn/motherboards-components/motherboards/prime/prime-z370m-plus-ii/)，配合八代 CPU：8100 (65 W TDP)

- 6 x PCIe 3.0 // 其中一个 PCIex16 支持拆分 (x16, x8/x4+x4)
- 4 x SATA 接口
- 2 x M.2 (PCIe 3.0 x4)
- 4 x DDR4 双通道

![BC81CE8F-9E16-4734-9906-268340C4C60F_1_105_c](/images/blog/global/BC81CE8F-9E16-4734-9906-268340C4C60F_1_105_c.jpeg)

配合一款十元购入的原装二手散热，完美：
![06004328-E25B-466F-BA9F-5454CA28D8B2_1_105_c](/images/blog/global/06004328-E25B-466F-BA9F-5454CA28D8B2_1_105_c.jpeg)
![7ABCF5E8-2728-4051-AC6E-8D4A8B9F3E0C_1_105_c](/images/blog/global/7ABCF5E8-2728-4051-AC6E-8D4A8B9F3E0C_1_105_c.jpeg)

## 机箱
起初选择的是价格在一百元左右的动力火车机箱。收到货后，向客服咨询装机的一个细节。客服回复时给我发了一个链接：“主板安装教程：https://www.bilibili.com/video/BV17Z4y1T7qM?p=15” 🤡
![](/images/blog/global/17458126396122.jpg)

后来之所以选择机械大师 [C34PLUS](https://caseend.com/data/mechanic-master/mechanic-master-c34plus)，是因为它配备了一个提手，增加了便携性 :p。不过，如果更注重性价比，也可以考虑见方 L8 或 宝藏盒，同样都是不错的选择。

P.S. 推荐一个网站：[https://caseend.com/](https://caseend.com/)（收录了市面上大多数机箱的详细参数，并提供筛选和排序功能）。

利用 SFX 电源 & 官方可拆卸的快装硬盘支架，可以灵活地调整机箱内部布局，从而在机箱的右上方放入四块机械硬盘：
![unraid_hdd_case1](/images/blog/global/unraid_hdd_case1.png)

最终巧妙地使用装饰板固定 HDD 硬盘，十分优雅：
![05C94DB9-CB25-45E8-B586-FD1902CC7075_1_105_c](/images/blog/global/05C94DB9-CB25-45E8-B586-FD1902CC7075_1_105_c.jpeg)

## 无线网卡
![5102C7A2-2A5E-4C08-B1D4-8B1FA26B1BB8_1_105_c](/images/blog/global/5102C7A2-2A5E-4C08-B1D4-8B1FA26B1BB8_1_105_c.jpeg)

# 价格（除去 HDD 存储）
```
CPU：i3-8100                // 130 + 10 散热
主板：z370m plus2            // 225
内存：金士顿 2666x2           // 140
网卡：AX210 PCIe             // 98
电源：TT 钢影 350W           // 163
机箱：机械大师 C34PLUS        // 869
配件：SFX 转 ATX 电源支架      // 10
```

# 功率统计
下图分别统计了机器在不同状态的功耗：
- 硬盘休眠：~27W
- 硬盘活动：~35W
- CPU 满负载：~77W

![](/images/blog/global/17458046221843.jpg)

# 网络性能

- `Mac Mini` -> 千兆有线 -> `Linksys 路由器` -> wifi6 无线 -> `NAS`
```
mini@Mac-mini.local ➜  ~  iperf3 -c 10.200.1.194 -p 5201 -t 5
Connecting to host 10.200.1.194, port 5201
[  5] local 10.200.1.222 port 58349 connected to 10.200.1.194 port 5201
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-1.00   sec  52.5 MBytes   439 Mbits/sec
[  5]   1.00-2.00   sec  60.0 MBytes   505 Mbits/sec
[  5]   2.00-3.00   sec  65.8 MBytes   549 Mbits/sec
[  5]   3.00-4.01   sec  67.0 MBytes   561 Mbits/sec
[  5]   4.01-5.00   sec  67.1 MBytes   563 Mbits/sec
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-5.00   sec   312 MBytes   524 Mbits/sec                  sender
[  5]   0.00-5.01   sec   312 MBytes   522 Mbits/sec                  receiver
```

- `MBP` -> wifi6 无线 -> `Linksys 路由器` -> wifi6 无线 -> `NAS`
```
➜  zblog git:(main) ✗ iperf3 -c 10.200.1.194 -p 5201 -t 5
Connecting to host 10.200.1.194, port 5201
[  5] local 10.200.1.152 port 59994 connected to 10.200.1.194 port 5201
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-1.00   sec  53.4 MBytes   447 Mbits/sec
[  5]   1.00-2.01   sec  61.8 MBytes   516 Mbits/sec
[  5]   2.01-3.00   sec  61.4 MBytes   517 Mbits/sec
[  5]   3.00-4.00   sec  63.8 MBytes   535 Mbits/sec
[  5]   4.00-5.00   sec  64.0 MBytes   536 Mbits/sec
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-5.00   sec   304 MBytes   511 Mbits/sec                  sender
[  5]   0.00-5.02   sec   303 MBytes   506 Mbits/sec                  receiver
```

看起来极限大约在 500 Mb/s 左右，不确定是否能进一步提升，但对于冷备和日常使用，尤其是移动设备，这个速度已足够满足需求。
