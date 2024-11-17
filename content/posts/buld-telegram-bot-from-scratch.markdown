---
title: 零成本打造 Telegram 机器人指北
date: 2021-02-21 15:42:05
categories:
- PYTHON
---

春节放假在家，写了一个 [和风天气 API](https://dev.qweather.com) 的 [Telegram 天气预报机器人](https://github.com/daya0576/he-weather-bot)🤖️ - 根据用户精准定位查询实时天气，并支持每日的定时自动播报。    

本篇文章为该机器人实现的不完全教程～

<!--more-->

# 1 机器人介绍

源码: [https://github.com/daya0576/he-weather-bot](https://github.com/daya0576/he-weather-bot)

👉戳链接调戏我：https://t.me/he_weather_bot  

![](https://github.com/daya0576/he-weather-bot/blob/fdd4d924943ab6036646cc6d7b7888fc71b9d3e2/img/2021-02-21%2015-49-06.gifcask.2021-02-21%2017_20_45.gif?raw=true)

# 2 技术栈汇总

1. 开发
    - 语言：`Python3.9`
    - WEB框架: `fastapi`
    - telegram sdk: `aiogram`
2. 线上部署
    - CICD: `heroku`
    - 持久型数据：`Heroku Postgres`
    - 缓存数据：`Heroku Redis`
    - 定时任务：`Heroku Scheduler`
3. 监控
    - 运行态：`sentry`
    - 请求量：TODO

尝鲜使用了 python3.9，以及异步的 fastapi web 框架，所以 telegram 的 sdk 也需要使用异步：[aiogram](https://github.com/aiogram/aiogram)。

线上部署白嫖了 Heroku 全家桶：推送 master 即可触发部署(gitops)。同时支持数据库/缓存/定时任务的一键申请（最重要的都是免费的），以及 环境变量配置，域名https卸载，日志在线查看，等傻瓜操作... 唯一的缺点：Heroku 只在在美国与欧洲提供服务，访问国内 api 会存在一定延迟。

![image-20210314172708269](/images/blog/2021-02-21-buld-telegram-bot-from-scratch/image-20210314172708269.png)


# 3 原理 & 实现

分为以下四个步骤：

1. 申请机器人 - token
2. 搭建 server - webhook
3. 绑定 token & webhook
4. 线上部署

## 3.1 机器人申请 - token

第一步先找到 [@BotFather](https://t.me/BotFather)，创建你的机器人，并获取对应 `token` 唯一标识。

## 3.2 本地调试 - webhook
telegram python SDK 中提供两种消费机器人动态的方式：
1. server 本地主动轮训拉取最新动态 
2. server 被动接受 http 请求的推送。类似消息队列的 pull & push，**本文主要基于第二种模式**。

所以不管是 fastapi/flask/django，都需要开启一个 `/hook` 的接口，参考项目中的这档逻辑： `telegram_bot.routers.webhook.webhook_handler`

p.s. 本地调试推荐 ngrok 这个小工具，一键针对内网 IP 创建一个对外可访问的 https 地址。

![image-20210314172807664](/images/blog/2021-02-21-buld-telegram-bot-from-scratch/image-20210314172807664.png)

## 3.3 绑定 Bot Token & Server Webhook

用户与机器人的每次交互，甚至在群组中的每次对话及交互，都会以 http 请求的形式，分发至机器人对应的 `webhook`，所以需要提前将 `webhook` 与 `token` 进行绑定。两种方式：

1. 手动请求 `https://api.telegram.org/bot{token}/setWebhook?url={webhook}`
2. sdk 设置：`aiogram.bot.bot.Bot.set_webhook`。一个小技巧：在 fastapi app 每次启动的时候，检查如果与当前机器人绑定的 webhook 不同，则进行更新。需要注意调用的频率，参考 `telegram_bot.routers.webhook.set_webhook`

## 3.4 线上部署 

heroku 一键部署：参考[《Getting Started on Heroku with Python》](https://devcenter.heroku.com/articles/getting-started-with-python)

p.s. heroku 原生不支持 poetry，只认识 requrements.txt，可以通过第三方 buildpack 解决：https://github.com/moneymeets/python-poetry-buildpack

## 3.5 网络问题

利用 proxy 解决本地连接服务端报错的问题：

```python
# ClientConnectorError: Cannot connect to host api.telegram.org:443 ssl:default [Connection reset by peer]

bot = Bot(
    token=settings.TELEGRAM_BOT_API_KEY.get_secret_value(),
    proxy=settings.PROXY
)
```

# 4 时序交互 & 系统设计

用户与 telegram 机器人的交互，大致可以分为三个场景：

1. **用户位置更新：** 和风 SDK 很贴心提供了地址相关的 API，不管用户是输入关键字还是发送定位，统一转化为坐标经纬度，在数据库中进行保存。 这部分的代码实现也挺有趣：使用了框架的状态机，当前用户「输入阶段」的状态会保存在缓存之中，e.g. 只有当前状态为等待用户输入地址时，才会对下一次输入的定位或文本进行解析，并更新用户位置。参考 `telegram_bot.telegram.finite_state_machine.update_location`
2. **实时天气获取**：单个用户触发 `/weather` 命令，请求外部 API，返回实时天气
3. **定时天气发送**：遍历开启的用户，发送对应城市的天气预报。     定时任务通常由消息驱动实现，通过三层分发(Splitter->Loader->Executor)等手段避免单点热点。因为是单点部署... 所以简单通过定时 curl http 请求实现，需要考虑扫描误触发&恶意攻击，但最好是通过内部的幂等机制支持。

## 时序交互
三个场景对应的时序交互如下：

![](/images/blog/2021-02-21-buld-telegram-bot-from-scratch/16138563037292.jpg)

## 系统架构

虽然是个小玩具，但也需要一定的分层与抽象，减少整体代码的「复杂度」：

1. Web 层代表 fastapi app 暴露给外部的两个接口
2. Telegram 层将收到的 webhook 请求，根据内容分发至对应的 command 处理
3. Integration 层为对外的依赖封装，例如 `weather_client` 是一个天气预报获取的接口，定义标准的行为后，底层可以由任意获取外部数据逻辑构成，实现解耦与未来快速替换
4. DAL 则是 DB 层的包装

![](/images/blog/2021-02-21-buld-telegram-bot-from-scratch/16138614119002.jpg)

问题：cron 触发定时任务后，web 层会直接与 integration 与 dal 层交互，当然可以考虑新加一层 Service（同时统一做异常处理，日志打印等等）




# 性能问题

感兴趣可以阅读这两段代码，在遇到 IO 操作时，如何提升性能：

1. 使用 asycio 并行执行定时任务的分发：`telegram_bot.routers.cron.cron_handler`
2. 利用线程池，并行请求外部 sdk http 服务：  `telegram_bot.intergration.http.HttpClient.get_responses`



# THE END

本文介绍的天气预报小玩具，仅供个人练手使用。如果你有一些好的想法，欢迎欢迎私信我([@daya0576](https://t.me/daya0576))一起结对编程～～ 2021 希望去认识一些新朋友 XD



