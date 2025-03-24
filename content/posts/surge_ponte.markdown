---
title: "分享我的家庭自部署实践"
date: 2025-02-28T15:57:50+08:00
categories:
- 智能家居
---

通过自部署（Self-Hosted），你可以轻易地使用 [Bitwarden](https://bitwarden.com/) 取代 1Password 丝滑地管理所有密钥；使用 [Transmission](https://transmissionbt.com/) 随时随地通过游览器插件一键下载喜欢的 pt 电影；使用 [Home Assistant](https://www.home-assistant.io/) 管理家中所有智能设备并远程控制...

配合同城小于 5ms 的延迟，甚至可以在公司午休时，一键回家写会代码放松一下 ^^

---

# 网络（内网穿透）

## 选项一: Cloudflare Tunnel

下图为之前家中的网络拓扑：

- 绿色代表 Mesh 路由器，支持设备在多个路由器之间无缝切换
- 黄色代表 Surge 作为网关的设备（通过接管 DHCP 统一管理子网设备）

![20240228_homelab](/images/blog/global/20240228_homelab.svg)

可以看到虽然通过 cloudflare tunnel 暴露了内网的服务，但这种模式有两个缺点：
1. 网络延迟：由于恶劣的网络环境，每次“回家”需要跨越半个地球（100+ms 延迟）
2. 隐私问题：暴露公网后，所有用户可直接访问

### 题外话：云宽带

2022 年开始，电信未通知用户情况下默认开启。

对老婆解释：之前快递支持上门送件，结果有一天只配送至菜鸟驿站，但细思恐极的是菜鸟号称为了方便接收快递，直接配了你家的钥匙。

![cloud_gateway](/images/blog/global/cloud_gateway.svg)


## 选项二: Surge Ponte

幸运的是，Surge 支持开启私有 mesh 网络：[Ponte](https://kb.nssurge.com/surge-knowledge-base/zh/guidelines/ponte)。通过国内代理做转发，或直接使用公网 IP 做端口转发即可开启：

博主选择了后者，通过以下步骤 100% 掌控家庭的网络：

1. 联系电信客服关闭云宽带
2. 联系电信客服申请公网 IP
3. 联系电信客服或对应宽带师傅，将光猫修改为桥接后，通过路由器拨号
4. 通过 Surge 开启 Ponte 并在路由器中设置端口转发（如下图）
5. 通过域名 mini.sponte 无缝丝滑访问家庭自部署服务

### 通过 ssh 回家

个人的 ssh config 供参考：
```shell
# Optional
Host *
    ServerAliveInterval 15
    ServerAliveCountMax 10
    AddressFamily inet

# Target
Host surge_mini
    HostName mini.local
    User mini
    ProxyCommand nc -x 127.0.0.1:6153 %h %p 
```

# 服务管理

通过 docker compose 手动管理自部署的服务。唯一的缺点是无法统一管理各个物理设备上的容器。

目前运行非常稳定，每次秒开自部署服务的页面都会让人身心愉悦，一天的烦恼烟消云散☺️
