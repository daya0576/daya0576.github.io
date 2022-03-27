---
title: 我的家庭监控大盘 categories:

- 智能家居 date: 2022-03-27 17:03:38 tags:
---

周末突然想起许久前与朋友聊天，谈到他的家庭网络虽然是电信接入，但是质量堪忧总是时不时的“抽风”，最终却也不知是路由器还是宽带在捣鬼。

作为一名 SRE 每日在解决线上业务可观测的问题，突发奇想有没有可能针对自家的状况，也配置一个监控大盘？🤔

<!--more-->

花了一天时间踩坑后初版如下，包含局域网设备负载、网络流量、湿温度趋势等信息。本篇文章将分享家庭大盘搭建的思路，希望读者可以少踩几个坑 XD
![](../images/blog/2021-09-04-jvm-note/16483716356989.jpg)

# TOC
- [TOC](#toc)
- [一、名词解释](#一、名词解释)
- [二、监控需求](#二、监控需求)
- [三、整体方案](#三、整体方案)
- [四、技术细节](#四、技术细节)
  - [4.1 数据收集](#4-1数据收集)
    - [4.1.1 Openwrt 软路由系统指标](#4-1-1-openwrt软路由系统指标)
    - [4.1.2 HA 树莓派系统指标](#4-1-2-ha树莓派系统指标)
    - [4.1.3 智能家居设备数据](#4-1-3智能家居设备数据)
    - [4.1.4 家庭外网/内网可用性数据](#4-1-4家庭外网内网可用性数据)
  - [4.2 数据存储](#4-2数据存储)
    - [4.2.1 安装 InfluxDB Add-on](#4-2-1安装-influxdb-add-on)
    - [4.2.2 安装 Prometheus Add-on](#4-2-2安装-prometheus-add-on)
  - [4.3 数据展示](#4-3数据展示)
    - [4.3.1 安装 Grafana](#4-3-1安装-grafana)


# 一、名词解释

| 名词 | 解释 |
|---|---|
| HA | Home Assistant 系统，基于树莓派硬件搭建。负责家庭智能设备的管理。 |
| HA Integration | Home Assistant 系统集成，本篇文章主要用于收集数据 |
| HA Addons | Home Assistant 系统加载项，简单理解为由 HA OS 动态新增&管理的容器 |
| R2S 软路由 | OpenWrt 系统，基于 R2S 硬件设备搭建。负责二级网络的路由 |
| Linksys | Linksys 路由器，家庭网路中的主路由。 |

整体家庭网络拓扑以及关键设备如下（详情参考上一篇文章）：
![network_status](../images/blog/2021-09-04-jvm-note/network_status.svg)


# 二、监控需求

基于下图家庭网络拓扑（参考上一篇文章），期望最终绘制的大盘满足以下几个需求：
1. **设备负载情况**：`树莓派（Home Assistant）`、`R2S 软路由` 等局域网设备的系统指标，例如 load、内存等..
2. **宽带流量使用趋势**：Linksys 主路由、子网二级路由，对应的上传下载实时速率，以及历史趋势。
3. **智能家居传感器**：室内室外湿温度、设备开关状态等..
4. ...


# 三、整体方案

最终将整体系统分为三部分：

1. **数据收集 & 数据存储**：
    1. `树莓派` 相关数据（智能家居信息+系统指标），直接保存至本地 InfluxDB
    2. `R2S 软路由` 系统指标，通过 expert 的形式暴露，并保存至 Prometheus 中
2. **数据展示**：通过主流的 grafana 可视化平台，配置大盘展示数据 

![home_monitoring_system_design](../images/blog/2021-09-04-jvm-note/home_monitoring_system_design.svg)

p.s. 针对数据存储多说两句，因为博主的 HA 直接以 Home Assistant Operating System 的形式安装在树莓派中，所以可访问 Add-ons（例如直接安装 grafana 等）。如果读者是以 container 的形式安装，针对下文提到的 Add-ons 应用，在宿主机中直接用 docker 一键快速拉起即可。

# 四、技术细节
这一小章简单说下我踩过的那些坑～

## 4.1 数据收集
### 4.1.1 Openwrt 软路由系统指标
安装 prometheus node exporter 后，Openwrt 的实时系统数据就会通过 http 接口透出，方便下一章 prometheus 进行采集与持久化：
![](../images/blog/2021-09-04-jvm-note/16483684440919.jpg)

具体脚本如下：
```shell
# openwrt prometheus exporter
opkg install prometheus-node-exporter-lua \
prometheus-node-exporter-lua-nat_traffic \
prometheus-node-exporter-lua-netstat \
prometheus-node-exporter-lua-openwrt \
prometheus-node-exporter-lua-wifi \
prometheus-node-exporter-lua-wifi_stations

# 启动：
/etc/init.d/prometheus-node-exporter-lua restart
# 打开开机启动
/etc/init.d/prometheus-node-exporter-lua enable
```

### 4.1.2 HA 树莓派系统指标
安装 [System Monitor](https://www.home-assistant.io/integrations/systemmonitor/) 集成：修改 `/config/configuration.yaml` 后重启。

配置参考：
```yaml
sensor:
  - platform: systemmonitor
    resources:
      - type: disk_use_percent
      - type: memory_free
      - type: memory_use
      - type: memory_use_percent
      - type: load_1m
      - type: load_5m
      - type: load_15m
      - type: processor_temperature
      - type: processor_use
```

### 4.1.3 智能家居设备数据
HA 安装 [InfluxDB](https://www.home-assistant.io/integrations/influxdb/) 集成，配置参考（注意 host地址/数据库名称/用户名密码等信息，需根据实际情况更新）：
```yaml
influxdb:
  host: 10.200.1.*
  port: 8086
  database: homeassistant
  username: grafana
  password: ***
  ssl: false
  verify_ssl: false
  max_retries: 3
  default_measurement: state
```

### 4.1.4 家庭外网/内网可用性数据
HA 安装 [Binary Sensor](https://www.home-assistant.io/integrations/binary_sensor/) 集成，配置需要的网络探测（后续用于判定家庭网络的可用性）：

```yaml
binary_sensor:
  - platform: ping
    host: 192.168.2.170
    name: "Sony TV"
    count: 2
    scan_interval: 10
  - platform: ping
    host: 47.52.*.*
    name: "HK SS"
    count: 2
    scan_interval: 10
  - platform: ping
    host: 223.5.5.5
    name: "ALIBABA DNS"
    count: 2
    scan_interval: 10
```


## 4.2 数据存储

### 4.2.1 安装 InfluxDB Add-on
HA Add-ons 中找到 InfluxDB 安装即可：https://github.com/hassio-addons/addon-influxdb

⚠️注意
1. 关闭配置中 ssl 选项后启动
2. 创建用户
3. 创建数据库

### 4.2.2 安装 Prometheus Add-on

这一步坑较多，有条件的朋友推荐 docker 一键拉起。

步骤：
1）因为该 prometheus addon 为测试版本（未正式发行），需更新repo后才能在ha中找到：https://github.com/hassio-addons/repository-beta
![](../images/blog/2021-09-04-jvm-note/16483714471537.jpg)

2）安装并启动
3）参考文档配置 targets 时，文件一定要以 `yaml` 后缀：
```shell
[core-ssh targets]$ cat /share/prometheus/targets/openwrt.yaml
---
job_name: "openwrt"
scrape_interval: 15s
metrics_path: "/metrics"
static_configs:
  - targets: ["10.200.1.94:9100"]
[core-ssh targets]$
```
4）web 界面查看 target 是否生效
![](../images/blog/2021-09-04-jvm-note/16483715464467.jpg)


## 4.3 数据展示

### 4.3.1 安装 Grafana
安装 grafana 后，根据上一步 InfluxDB + Prometheus 两个数据源，自由配置大盘即可。

如下为我初步配置的大盘，设备负载情况，室内室外温差湿度，以及关心的网络可用性，历史趋势等信息一目了然 ✨

![](../images/blog/2021-09-04-jvm-note/16483716356989.jpg)


# 参考：
- https://bbs.iobroker.cn/t/topic/7944
- https://grafana.com/blog/2021/02/09/how-i-monitor-my-openwrt-router-with-grafana-cloud-and-prometheus/

