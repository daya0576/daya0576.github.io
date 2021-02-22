---
title: 如何零成本制作一个 Python Telegram 机器人
date: 2021-02-21 15:42:05
tags:
---


春节放假在家，写了一个基于 Telegram 的天气预报机器人🤖️ 本篇文章为不完全教程，主要分享该小玩具的实现路径，以及零散的思路～

<!--more-->

# 一、机器人介绍

基于 [和风 API](https://dev.qweather.com) 的天气预报小棉袄 - 根据用户定位查询实时天气，并支持每日定时自动播报天气预报。    
源码: https://github.com/daya0576/he_weather_bot

👉戳链接调戏我：https://t.me/he_weather_bot  

![](https://raw.githubusercontent.com/daya0576/he_weather_bot/master/img/2021-02-21%2015-49-06.gifcask.2021-02-21%2017_20_45.gif)

# 二、技术栈汇总

和风机器人使用的编程语言以及第三方依赖如下：

1. 开发：`Python3.9` ｜ webserver: `fastapi`
2. 存储
    - 持久型数据：`Heroku Postgres`
    - 缓存数据：`Heroku Redis`
2. 定时任务：`Heroku Scheduler`
2. 部署
    - CICD: `heroku`
3. 监控
    - 运行态：`sentry`
    - 请求量：TODO

尝鲜使用了异步的 fastapi web 框架，所以 telegram 的 sdk 也需要异步：[aiogram](https://github.com/aiogram/aiogram)。但有一句说一句，同步与异步的分别对应了两个完全不同的 telergam sdk 仓库，感觉还是挺别扭的。

最后不得不感叹一句，heroku 的自动部署对于我这种手残党真的很方便：推送 master 即可触发。还有环境变量的界面配置，https域名自动生成，日志在线查看，等等... 唯一的缺点是只在在美国与欧洲提供服务，访问国内 api 会存在一定延迟。

当然丰富并且开箱即用的插件。让我想起 cloudflare 的 add-on(app)，例如无感一键开启 [Google Analytics 插件](https://www.cloudflare.com/apps/google-analytics)，不需要对代码做任何侵入，就能达到流量的统计。
![](/images/blog/200104_japan_travel/16138585335863.jpg)


# 三、原理 & 实现

Bot Father -> Bot Token <-> Your Web Server

## 机器人申请 - token

第一步先找到 [@BotFather](https://t.me/BotFather)，创建你的机器人，并获取对应 `token` 唯一标识。

## 本地调试 - webhook
telegram python SDK 中提供两种消费机器人动态的方式：
1. server 本地主动轮训拉取最新动态 
2. server 被动接受 http 请求的推送。类似消息队列的 pull & push，本文主要基于第二种模式。

所以不管是 fastapi/flask/django，需要开启一个 `/hook` 的接口，参考项目中的这档逻辑： `telegram_bot.routers.webhook.webhook_handler`

p.s. 本地调试推荐 ngrok 这个小工具，一键针对内网 IP 创建一个对外可访问的 https 地址。
![](/images/blog/200104_japan_travel/16138553359280.jpg)

## 绑定 Bot Token & Server Webhook

用户与机器人的每次交互，甚至在群组中的每次对话及交互，都会以 http 的形式，请求到机器人对应的 `webhook`，所以需要将 `webhook` 与 `token` 进行绑定。

两种方式：

1. 手动请求 `https://api.telegram.org/bot{{token}}/setWebhook?url={{webhook}}`
2. sdk 设置：`aiogram.bot.bot.Bot.set_webhook` 一个小技巧：在 fastapi app 每次启动的时候，检查如果与当前机器人绑定的 webhook 不同，则进行更新。需要注意调用的频率，参考 `telegram_bot.routers.webhook.set_webhook`

## 线上部署 

heroku 一键部署：参考[《Getting Started on Heroku with Python》](https://devcenter.heroku.com/articles/getting-started-with-python)

heroku 原生不支持 poetry，只认识 requrements.txt，可以通过第三方 buildpack 解决：https://github.com/moneymeets/python-poetry-buildpack


# 四、时序交互 & 系统架构

用户与 telegram 机器人的交互，大致可以分为三个场景：

1. **用户位置更新：**和风 很贴心提供了地址相关的 API，不管用户是输入关键字还是发送定位，统一转化为坐标经纬度，在数据库中进行保存。 这部分的代码实现也挺有趣：使用了框架的状态机，当前用户「输入阶段」的状态会保存在缓存之中，e.g. 只有当前状态为等待用户输入地址时，才会对下一次输入的定位或文本进行解析，并更新用户位置。参考 `telegram_bot.telegram.finite_state_machine.update_location`
2. **实时天气获取**：单个用户触发 `/weather` 命令，请求外部 API，返回实时天气
3. **定时天气发送**：遍历开启的用户，发送对应城市的天气预报。     定时任务通常由消息驱动实现，通过三层分发(Splitter->Loader->Executor)等手段避免单点热点。因为是单点部署，所以简单通过定时 curl http 请求实现，需要考虑扫描误触发&恶意攻击，但最好是通过内部的幂等机制支持。

## 时序交互
三个场景对应的时序交互如下：

![](/images/blog/200104_japan_travel/16138563037292.jpg)

## 系统架构

虽然是个小玩具，但也需要一定的分层与抽象，减少整体代码的「复杂度」：

1. Web 层代表 fastapi app 暴露给外部的两个接口
2. Telegram 层将收到的 webhook 请求，根据内容分发至对应的 command 处理
3. Integration 层为对外的依赖封装，例如 `weather_client` 是一个天气预报获取的接口，定义标准的行为后，底层可以由任意获取外部数据逻辑构成，实现解耦与未来快速替换
4. DAL 则是 DB 层的包装

![](/images/blog/200104_japan_travel/16138614119002.jpg)

但 cron 触发定时任务后，web 层会直接与 integration 与 dal 层交互，纠结是否需要新增一层 🤔

**###TODO**


# 其他问题
1. async/await 看到最好的一个解释：https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work



