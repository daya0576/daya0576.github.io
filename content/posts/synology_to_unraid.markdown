---
title: "万兆 nas diy 搭建小记（Synology -> Unraid）"
date: 2024-12-28T06:13:48+08:00
categories:
- 智能家居
---

自从购买了 Mac Mini M4 PRO, 博主便寝食难安 :(

原因竟是选配了「万兆」网口，却无奈家中预铺的网线与群晖 DS220+ 都受限**千兆**，白白浪费着实令人焦虑。

近日更是被群晖硬盘“炒豆子”声音困扰，于是便着手打造一台心目中理想的万兆 nas 🤩
1. 拒绝噪音：全固态阵列 or 机械硬盘休眠
2. 高速连接：万兆 or 雷电连接
3. 可扩展性：横向无限扩展
4. ...

# TOC

- [改造计划](#改造计划)
- [硬件改造](#硬件改造)
  - [HDD](#hdd)
  - [万兆网卡](#万兆网卡)
- [软件搭建](#软件搭建)
  - [Unraid](#unraid)
- [最终效果](#最终效果)
  - [硬件交互](#硬件交互)
  - [软件交互](#软件交互)
- [总结](#总结)


# 改造计划
基于上述需求，市场上有不少优秀的全闪存 nas 产品，例如新推出的 [LincPlus N1](https://www.lincplustech.com/products/lincstation-n1-network-attached-storage)，[TERRA MASTER F8 SSD](https://www.terra-master.com/us/f8-ssd.html), 都性感的令人心动。但一体化的设计，在扩展性上隐隐令人犹豫与担忧。

转念一想，最终将魔爪竟伸向了一年前搭建的 PC（[FormD T1 V2.0 装机小记](/blog/20230806/build-pc-formd-t1/)）与 Unraid 系统：
1. 拒绝噪音：
    - 机械硬盘无访问超时自动休眠（spin down delay）-> 解决炒豆子噪音问题
    - 定期或根据自定义策略，深夜自动将 ssd 缓存池数据，写入 hdd 冷备（*美妙的是对于外部共享访问无感*）
2. 高速连接
    - 新增万兆网卡，配合 ssd 缓存池（Unraid Pool），与 Mac 高速连接
    - 未来官方支持雷电后，进一步提升传输速率
3. 可扩展性
    - Unraid 支持不同容量硬盘组阵列，灵活新增硬盘（*校验盘的容量必须最大*）
4. ...

# 硬件改造
当初购买了 formd t1，第一眼就被它性感的外观吸引，以及享受动手 diy 的过程。不同的自定义组件相互拼凑，就如同编程中的“组合”，令人心旷神怡。

如今有了新的用户需求，不妨对它做一次“重构” :)

## HDD
幸运的是，主板 z690i 上提供了前面板 SATA 扩展卡(包含 4 个 SATA 端口)。

淘宝定制电源线与数据线后，便顺利将群晖中的硬盘拆卸并接入。

![](/images/blog/2021-09-04-jvm-note/17353418708512.jpg)

## 万兆网卡
不幸的是，主板自带的网卡只有 2.5Gb，虽然可以轻松跑满机械硬盘，但在固态硬盘前显得有一丝乏力。

更不幸的是，唯一的 PCIe x16 卡槽已被显卡占用。万幸的是在淘宝中，找到了 *M2 转 PCIe x4 的延长线*，可以兼容大部分消费级的万兆网卡。

令人又爱又恨的 itx 机箱：

![IMG_2228](/images/blog/2021-09-04-jvm-note/IMG_2228.jpeg)

# 软件搭建

## Unraid

根据官方 [Getting Started](https://unraid.net/getting-started) 文档，制作启动盘并进入系统即可。

Un-raid 顾名思义，即“非-RAID”：不同于 raid5 甚至 raid1，仅利用一个或多个校验盘实现的数据冗余（[官方文档](https://docs.unraid.net/unraid-os/overview/nas/#parity-protected-array)）。

![](/images/blog/2021-09-04-jvm-note/17353543537707.jpg)

总而言之，越是简单容易理解的方案，个人越是更加喜欢～

> Simple is better than complex.

## 缘分

更为奇妙的是，安装完 Unraid 并打开应用商店的一刻。首页最新加入的应用竟然是我开发 [Beaver Habit Tracker](https://github.com/daya0576/beaverhabits)（感谢好心人☺️）：

![](/images/blog/2021-09-04-jvm-note/17353556762017.jpg)

缘分妙不可言～

# 最终效果
## 硬件交互

万兆链路：
```
// FormD T1
- ROG STRIX Z690-I 
- M.2 NVMe to PCIe x4 Extension Cable (ADT-Link M42UF)
- 10G PCIe NIC (TL-NT521 - AQC107)

// Switch
- 10G DAC Cable (XikeStor)
- 10G Switch (XikeStor)
- 10G SFP+ to RJ45 Module (XikeStor)

// Mac Mini
- 10 Gigabit Ethernet Port
```

简单收纳后效果似乎还不错哟：

![37D5AA00-87F9-42FC-9705-E31F21A585A2](/images/blog/2021-09-04-jvm-note/37D5AA00-87F9-42FC-9705-E31F21A585A2.jpeg)

![BA2D1CB7-FE36-4151-8C90-8123C4533ABC](/images/blog/2021-09-04-jvm-note/BA2D1CB7-FE36-4151-8C90-8123C4533ABC.jpeg)


## 软件交互

![unraid](/images/blog/2021-09-04-jvm-note/unraid.png)

待填满的 Pool & Array 池：

![](/images/blog/2021-09-04-jvm-note/17353574826432.jpg)


搭配 Infuse 管理电影与个人视频：

![](/images/blog/2021-09-04-jvm-note/17353453778902.jpg)

# 总结
Unraid 系统几乎每个特性，都击中在博主的心趴上。期待未来几天继续探索更多功能：

- [ ] 雷电4 直连（官方暂不支持 thunderbolt bridge，但理论上可行）
- [x] 搭配 Mover Tuning 自定义缓存池移动逻辑（例如根据日期文件大小等）
- [x] 虚拟化游戏体验
- [x] 网外连接：简单通过 cloudflare tunnel 即可实现
- ...


# 其他
## Mover Tuning 设置
以大疆拍摄的乒乓球视频工作流为例：

1. 将当日乒乓球录制视频导入 Cache，进行回顾与视频剪辑
2. 每日凌晨两点定制扫描，若满足下面的条件，则移动至冷备 Array
    - 视频距上次超过 15 天
    - 文件大于 10M

![](/images/blog/global/17356894814590.jpg)


## 虚拟化游戏体验
step by step tutorial to enable GPU passthrough: 
<iframe width="560" height="315" src="https://www.youtube.com/embed/nTZ1Whx3cZo?si=Xa0M5en81hF6pwL6" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

虽然遇到了显卡无法 passthrough 显示器无法点亮的问题，但万幸最终通过升级 bois 版本解决了。

成功启动后，体验非常丝滑（舒服😌）

## "cache" file and directory information
尽可能的希望 Array 处于休眠的状态，可以通过 NFS 的 `Tunable (fuse_remember)` 配置，可以缓存文件/目录名称：

![](/images/blog/2021-09-04-jvm-note/17355275285679.jpg)

## macOS 自动挂载 NFS
```
# fstab 编辑的入口: /etc/fstab
sudo vifs

# device-spec     mount-point     fs-type      options     
lena.local:/mnt/user/movies /System/Volumes/Data/Lena/movies nfs rw,nolockd,resvport,hard,bg,intr,rw,tcp,nfc,rsize=65536,wsize=65536
lena.local:/mnt/user/tt /System/Volumes/Data/Lena/tt nfs rw,nolockd,resvport,hard,bg,intr,rw,tcp,nfc,rsize=65536,wsize=65536

sudo automount -cv
```

不清楚为什么这种方式，导致传输速率极慢。排查无果，暂时切换为原生的 finder 挂载，并加入 login items

## 避免必须要键盘连接才能启动

尝试了很多 bois 设置无果，最终够买了键盘长期直连。

1. https://www.truenas.com/community/threads/motherboards-that-boot-automatically-from-usb-without-pressing-f8-or-so-solved.11672/

## GPU 休眠/关闭

安装插件后，虽然观察到 GPU 使用率为 0，但依然在耗电并产生电流声噪音：

![](/images/blog/global/17356900667932.jpg)

