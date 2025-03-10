---
title: 精装全屋智能灯改造小记
categories:
- 智能家居
date: 2022-02-06 15:43:59
---


去年末交房后，虽是精装交付，但按耐不住爱折腾的心，将家中绝大部分的灯都换了一遍。在满足个人需求的过程中也踩了不少坑，趁着春季假期写一篇博客记录一下，如果刚好帮到你那就更好啦～

<!--more-->

![smart_home_lights](/images/blog/2021-09-04-jvm-note/smart_home_lights.svg)

# 一、名词解释

起初听到「单开双控」、「双开单控」等名词的时候，也是一脸懵逼，所以先明确几个概念：

| 名词 | 含义 |
|---|---|
| 墙壁开关 | 墙壁开关=面板+开关+暗盒底座。家用开关暗盒基本都是国家标准86型，所以升级智能开关一般无需更换底座。 |
| 单开 vs 双开 | 顾名思义双开指一个开关面板上有2个开关，同理存在3个开关即三开 |
| 单控 vs 双控 | 双控指两个开关面板可以同步控制一个灯，即在开关A关闭灯1，然后在开关B打开灯1 |

p.s. 单控与双控背后的实现非常巧妙！忍不住再简单补充一下：

例如下图中左边👈为关灯状态，此时博主无论单击开关1还是开关2，灯都会从关闭 -> 开启：

![double_control](/images/blog/2021-09-04-jvm-note/double_control.svg)


# 二、日常需求
精装交付后所有灯具如下图：
![original](/images/blog/original.svg)

首先简单罗列个人日常需求：
1. 普通级（自动场景）：
    - 出门/回家自动关开灯
    - 落日自动开灯，并调至暖色
    - 床头随手开关灯
    - 深夜自动熄灯 or 一键关闭所有灯
    - ...
2. 升级版（biantai 需求）：
    - 开门后自动开灯（门厅四个筒灯延迟逐个打开）
    - 夜晚射灯感应活动
    - ...

# 三、改造心路历程

简单分析上面的个人需求后，我们可以发现背后隐含的技术需求：**在一个生态中（HomeKit），通过改造传统灯与开关，实现自动控制家内的每个灯。**

<u>补充一下：为什么选择 HomeKit？</u>
一方面当然是相信苹果封闭生态把控的良好体验；另一方面因为家人用的苹果手机，并且暂时没有更换智能锁的计划，所以只有 HomeKit 可以实现如下前置条件：当最后一个人离家的时候 -> 触发 xxx 自动化场景。

![](/images/blog/2021-09-04-jvm-note/16441150164048.jpg)


## 心路历程

这时聪明的你可能发现 “改造传统灯与开关” 并没有那么简单，两者会衍生出多种组合：`传统灯+智能开关`、`智能灯+传统开关`、`智能灯+智能开关`。甚至会出现有**多对多**的情况：`智能灯+传统灯 vs 传统+智能开关`？？？

同时也是最容易踩坑的地方，下面将结合实际的场景，详细介绍博主的心路历程～


### 1) 单开单控 - 卧室/书房

先从最简单的卧室说起（单开单控），这时摆在我面前的有两个选择：1）仅更换传统开关 or 2）升级传统灯为智能灯🤔。前者成本更低，但缺点为丢失了智能灯的功能性，例如缓慢开启，色温调节，夜灯模式等。后者体验更佳，但墙壁开关沦为了摆设，甚至不小心关闭后，智能灯就完全“离线失联”了。。

正当纠结时，yeelight 的凌动开关映入我的眼帘，「凌动开关」本质上并非无线智能开关，而是通过触碰时物理的电流脉冲，i.e. 瞬间的断电，从而控制智能灯的状态（默认一直通电，所以原生支持双控）。

**最终卧室采购了 yeelight 光璨吸顶灯 + 凌动开关**，不仅颜值在线，功能也很齐备（HomeKit认证，凌动支持，夜光模式都不在话下）。使用一个月后，配合床边 aqara 无线按钮（单按开/关，双击切换至夜灯模式，摇一摇切换为日光模式），体验非常丝滑。
![](/images/blog/2021-09-04-jvm-note/16441141473647.jpg)

唯一不太让我满意的是凌动开关的手感，有点神似青轴键盘，**键程长噪音大**，个人更加偏爱鼠标点触。
![](/images/blog/2021-09-04-jvm-note/16441096015140.jpg)

书房由于用的四年前珍藏的一代 yeelight 彩光灯泡，不支持凌动模式（当前 1s 支持凌动），所以选择了新出的**米家屏显开关**（顺便省去一个温湿度计传感器）。按键手感非常喜欢，但美中不足的是，切换为无线开关控制灯泡后.. 延迟略高，粗略估计接近一秒，着实让人有些不爽..

p.s. 0106 补充：手动升级固件版本后，延迟减少到半秒以内，勉强可以接受。
![](/images/blog/2021-09-04-jvm-note/16441143892783.jpg)

细心的同学可能注意到，书房明明只有一个开关，为什么选择了双开的开关？   
这是因为预留控制其他智能设备的开关，例如窗帘、加湿器等，希望不是过度设计 ：）
![CD1916B3-B9D5-47F3-9BD0-9974F60F5F9B_1_105_c](/images/blog/2021-09-04-jvm-note/CD1916B3-B9D5-47F3-9BD0-9974F60F5F9B_1_105_c.jpeg)

卧室&书房单控开关改造就到此为止啦，整体变动见下图：
![bedroon_switch](/images/blog/2021-09-04-jvm-note/bedroon_switch.svg)

### 2) 三开三控 - 厨房

厨房不大但自带了一堆筒灯射灯与一个三开开关，由于这时博主对于智能家居的热情已经从 200% 降低至 50%，所以选择的方案为：**仅替换传统开关为 Aqara D1 智能墙壁开关**，从而达到手机端控制灯的目的。
![](/images/blog/2021-09-04-jvm-note/16441200256713.jpg)

个人认为，智能灯终极的体验：让用户忘记开关的存在。所以在厨房中配合使用人体传感器：1）光线暗+有人进入厨房，自动开灯 2）当传感器持续15分钟检测到无人，自动关灯。

真的很香，谁用谁知道😋 
![kitchen_switch](/images/blog/2021-09-04-jvm-note/kitchen_switch.svg)


### 3) 三开单控 - 厕所

上面罗列了两种最常见的改造方式（智能灯+凌动开关 / 传统灯+智能开关），但现实状况往往更加复杂..

比如我们的厕所，上个月师傅在安装浴霸时，无法找到电源，最终只能将浴霸与厕所的筒灯串联。也就是说如果关闭筒灯的开关，浴霸就断电进入离线状态无法再用遥控器控制 0.0
![](/images/blog/2021-09-04-jvm-note/16441202282954.jpg)

这时显然无法像厨房一样，简单采用“传统灯+智能开关”的解决方案，但 **aqara 墙壁开关支持转无线**，这样就可以保持物理开关通电保持浴霸在线的同时，按键手动无线控制智能灯。

⚠️⚠️⚠️但是注意！！**转成无线开关后，在 HomeKit 里面无法生效！！（点击开关后还是作为有线开关直接断电！！）**，只能是在米家或者 Aqara home app 中绑定后置动作。也就是说假如灯是米家生态，只能放弃 zigbee 协议！！将开关通过米家蓝牙网关接入！

![bathroom_switch](/images/blog/2021-09-04-jvm-note/bathroom_switch.svg)

*UPDATE: 2/14/22: 今晚哼着歌，打开浴霸，准备美美洗个热水澡时，突然断电了。。意料之外，情理之中，开关标识只能承载 200w，小米开关终于不堪重负罢工了。短暂出神后，选择将浴霸与小米灯串联火线（通过人体传感+无线开关控制）* 

### 4) 三开双控 - 客餐厅

终于到了最复杂的双控环节，但还不是最难的... 还记得开头博主的 biantai 需求吗：开门后四个筒灯依次延迟打开（回家的仪式感），所以重金购入四个 **yeelight 蓝牙 Mesh 智能筒灯**，但很遗憾客厅的灯已经替换为宜家的吸顶灯（非智能带遥控）：
![](/images/blog/2021-09-04-jvm-note/16441231420418.jpg)

面对 智能灯+传统灯+双控开关 的现实，逐步融化.. 
![](/images/blog/2021-09-04-jvm-note/16441110577026.jpg)

先来罗列双控的常见解决方案：
1. **凌动墙壁开关**：因为永远通电，不难理解原生支持双控。但因为有传统灯具的存在，pass..
2. **智能墙壁开关 + 无线开关**：假如有双控开关（A+B），设置开关 A1 打开时同步 B1 开灯，A1 关闭时同步 B1 灯关；B1 设置同理。理论上可行，但总觉得不够优雅，同时对无线开关的稳定性存疑，pass...
3. **小燕多联多控**：小燕智能家居提供的集成方案，但很可惜需要再购买一个昂贵的网关..暂时放弃。

最终做了一个妥协方案（牺牲部分双控功能）：
1. 入户开关A：替换为凌动开关 -> 控制智能筒灯
2. 右边开关B：替换为智能墙壁开关 -> 左键&中键 转无线开关控制筒灯+餐厅灯（不离线），又键物理控制客厅灯

![](/images/blog/2021-09-04-jvm-note/16441205201392.jpg)

所以客餐厅改造后整体布局如下：
![living_room](/images/blog/2021-09-04-jvm-note/living_room.svg)

## 小结

上面简单介绍了折腾智能灯的心路历程，全屋整体改动如下图： 
![smart_home_lights](/images/blog/2021-09-04-jvm-note/smart_home_lights.svg)

以下为个人主观视角的最佳组合排名：
1. 智能灯具 + 人体传感器（灯的最佳体验：忘记开关的存在）
2. 智能灯具 + 智能开关（灯缓慢亮起的那个感觉，配合物理转无线更多玩法）
3. 智能灯具 + 凌动开关（物理开关永远比无线稳定省心，如果凌动手感改进，可以上升一位排至第二）
4. 普通灯具 + 智能开关（保留传统灯具的轻度折腾，也不失为一种选择）


# 四 总结

最后分享一点个人感悟：
1. **专业的事让专业的人做**：虽然精装交付，但小小的改造却耗费个人大量精力，怪不得有一句话说如果没经历过装修不是完整的人生。在“装修”过程中，感悟出的一句话即“专业的事让专业的人做”。如果再给我一次机会进行全屋灯光改造，我可能更倾向于直接选择 aqara 或者 米家的全屋灯改造解决方案。
2. **不要过于迷信 HomeKit**：选用 HomeKit 还一个重要原因希望设备大一统，即直接使用米家开关控制 aqara 窗帘设备。但是后来购入米家的蓝牙 Mesh 网关后，发现它可以同时接入米家设备以及 aqara 的设备。如果对于延迟没有太高要求，可以完全只在米家生态折腾。
3. **有线永远比无线稳定**：无线开关不管走的本地还是远端，多多少少有一定延迟，恍惚间感叹要是有一种开关，单击后灯可以瞬间打开就好了 XD。还记得有一次，回家支持开关木有自动打开，还以为网络问题，原来是手机没有电了😂
4. **用户体验**：完全无感 > 物理开关 > 声音控制 > 手机操作，个人认为智能灯最佳体验是让用户完全忘记了开关的存在，尽可能配合使用人体感应、自适应灯光等辅助手段，来达到这个目的。
5. **历史包袱**：客厅双控的窘境，本质上更多的是因为自己选择了一款宜家的非智能吸顶灯，导致智能灯与传统灯“混搭”，徒增加了复杂度。

# 五 附录

## 设备列表

1. **网关：**
    - 绿米Aqara网关M1S（Zigbee 协议低延迟）
    - 米家智能多模网关（同时支持蓝牙+Zigbee）
    - 树莓派 HACS（无认证米家设备接入 HomeKit）
    - 苹果 HomePod（外网控制内部设备）
2. **灯具：**
    - 主卧 Yeelight易来 光璨LED吸顶灯（原生支持 HomeKit + 凌动 + 夜光模式）
    - 次卧 绿米Aqara 吸顶灯L1（支持 HomeKit 接入，不支持凌动）
    - 客厅 宜家泰尔比恩 + 飞利浦米家智能灯泡
    - 入户 Yeelight易来led智能蓝牙Mesh筒灯x4
    - 餐厅 宜家克尼斯胡特 + YeelightLED灯泡彩光版
3. **开关：**
    - 绿米Aqara 智能墙壁开关D1(ZigBee单火三键)
    - 小米米家屏显开关 双开单控（自带温湿度传感）
    - 易来Yeelight 凌动开关（自回弹不离线）