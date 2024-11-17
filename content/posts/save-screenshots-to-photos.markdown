---
title: macOS 如何将截图自动保存至相册(Photos)
categories:
- 奇技淫巧
date: 2019-07-30 10:58:01
---


今天突然有个小需求，希望在 macOS 上截图后，自动保存至应用 Photos. 搜索了一下，发现系统原生不支持这种骚操作，但有个自带的应用叫 Automator, 可以完美的实现这个需求✌️


<!--more-->

# 整体流程
## 第一步: 创建相册
在 Photos 应用中，新建一个相册，随便取一个名字，e.g. Mac Screenshots

## 第二步: 打开 & 配置 Automator
Automator 是个系统自带的软件：
![](/images/blog/190729_save_screenshot_tutorial/15643694506733.jpg)

打开后选择 "New Document":
![](/images/blog/190729_save_screenshot_tutorial/15643696947239.jpg)

选择 "Folder Action":
![](/images/blog/190729_save_screenshot_tutorial/15643697575204.jpg)

右上角的 "Folder Action receives files and folders added to", 选择桌面:
![](/images/blog/190729_save_screenshot_tutorial/15643698567086.jpg)

添加第一个 Action! 在左侧(Action Library) 选择 "Filter Finder Items" 并双击添加。然后编辑添加过滤 "Screen Shot" 开头的文件（如果是中文系统这里可能有点不同）:
![](/images/blog/190729_save_screenshot_tutorial/15643703266478.jpg)

再新建一个 Action(Import Files into Photos)，把截图导入至对应的相册：
![](/images/blog/190729_save_screenshot_tutorial/15643705737083.jpg)

保存 automator workflow

## 第三步：使用
像平时一样截图，稍微等个三四秒喝口咖啡，done~
![](/images/blog/190729_save_screenshot_tutorial/15643707665517.jpg)


# 其他
其实很早之前就知道 macOS 上有 automator 这个应用，并且看上无比强大，估计做这个团队也挺 high 的。但就像 iPhone 上新推出的 Workflow, 实则总有一种鸡肋的感觉，看上去吊炸天，但配置的成本过高，导致很难去广泛推广和使用。

突然想到了「少数派」🐶

# 参考
1. https://www.quora.com/Can-I-make-my-macOS-screenshots-automatically-save-to-the-Photos-app-instead-of-the-desktop

