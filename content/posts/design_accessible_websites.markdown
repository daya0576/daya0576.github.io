---
title: "[开源] 无障碍网页设计（Design Accessible Websites）"
date: 2025-03-23T09:46:36+08:00
categories:
- PYTHON
---

# 背景
> I've also been looking for a habit tracker that just does habits. Closest I've found is Beaver Habit Tracker but its accessibility issues made it impossible for me to use

偶然刷到一条 [reddit](https://www.reddit.com/r/selfhosted/comments/1jaosfe/sharing_my_setup/) 的帖子，介绍日常使用的 selfhosted 软件。文中提到他对 [Beaver Habit Tracker](https://github.com/daya0576/beaverhabits) 的极简长草，但很遗憾由于 accessibility 的问题导致无法使用。

第一时间没有明白 accessibility 的含义，以为是交互不够友好。后来才注意到作者是一名盲人，由于网站从来没有考虑到无障碍的设计，导致他无法使用。内心小小的受震撼，这篇文章将介绍 Udemy 课程 [Web Accessibility Training Course WCAG 2.1 & 2.2 Compliance](https://www.udemy.com/course/web-accessibility-training-course-wcag-21-compliance/?couponCode=KEEPLEARNING) 的学习笔记与心得。

# 更新（2025/03/28）
在实际的网页优化改造中，Quasar 提供的大部分前端组件自身已支持无障碍设计。而我们需要做的：
1. 通过 ARIA 主动隐藏无关的组件（让屏幕阅读器跳过）
2. 通过 ARIA 主动添加描述信息，例如在移动至 checkbox 时，分别添加描述：今天，昨天，两天前。
3. ...

# 正文
## 重新认识无障碍（Accessibility）
### 定义残疾人
残疾人的定义可从不同视角来看待：

#### 1. 医学模式
认为残疾是个体与外界互动的障碍，也就说只要能够治疗个体当前的医疗状况，他们就不再会有残障。例如给盲人做了一次手术修复视力，他就不再残障。

#### 2. 社会模式
强调关注个人的环境而非个体自身。也就是说只要改变社会运行方式并消除障碍后，这个人就不再是“残疾人”了（They are disabled by the way the environment is organized，Remove barriers and the person is not longer 'disabled'）。

P.S. 当然所谓的「社会模式」的定义也有一些批评声音：如果完全将问题归结于社会环境，会导致忽视个体的残障，而主动关注个人和缺陷才能使他们的生活更美好。

### 实现无障碍设计的基本思路

无障碍的网页设计，更多从上面提到的「社会模式」出发并实现：首先确保内容对大部分的受众是可以正常访问的。进而不断扩大受众，但注意不是针对每个群体硬编码，而是**通过灵活与结构化的网页设计，确保用户可以根据自己的需求自行更改网站呈现方式**。例如当盲人访问网站时，可以使用屏幕阅读器（screen reader），将网页内容朗读给他们听。

另一个问题：在不清楚各个用户需求的情况下，应该如何实现无障碍？从 1990 年开始，设计了许多标准，只要我们按照这些标准设计网站，就可以默认支持不同用户的需求。

总而言之确保网页设计具有足够的灵活性，通过改变内容的呈现方式来消除“障碍”，从而让所谓的特殊人群不再特殊。

## 残障人士如何游览网页

### 盲人或视力受损
通过屏幕阅读器获取信息是盲人浏览网页的常见方式，市场上常见的软件：NVDA 72.4% JAWS 61.7% VoiceOver 47.1%。这些工具依赖于清晰且结构良好的网页标题（例如`<h1>`, `<h2>`, `<h3>`等），以帮助用户高效导航和获取信息。并且尽可能使用文字而不是图片，同时针对非文字的内容例如图标等需要都提供适当的替代文本（alt text）。

此外视力受损的用户，会使用放大和高对比度模式工具来更容易地阅读网页内容。所以使用左对齐文本有助于使用屏幕放大镜的用户，因为它使每行的起始位置保持一致，从而更容易找到每行的开头。

有个细节，课程发布者采访了一名视力受损者，她表示页面中自动播放的视频会造成巨大困扰，因为她需要放大页面才能看清，导致会找很久。

### 听力障碍群体
数据显示，听力损失问题在老年人中相当普遍，超过 70% 的人在 70 岁后听力会有所下降或丧失。虽然网页游览的交互中大部分是文字和图片，但当涉及音频或视频内容时，提供了可替代的访问方式尤为重要，比如字幕与手语翻译。且由于无法通过电话交流，不要忘了提供基于文本的服务。

### 认知障碍者（learning difficulties）
复杂和杂乱的网页可能会极大地影响这里群体使用体验（每次需要重新学习）。特别是导航的设计：提供始终一致的导航有助于用户在不同页面间切换时，不用重新学习导航的方式。

### 身体障碍
想到了一部电影：[伊贝林的非凡人生 / The Remarkable Life of Ibelin](https://movie.douban.com/subject/36219875/)。 

除了依赖语音识别技术进行操作，也要确保网站能够完全通过键盘导航。


## 如何提升可访问性
下文将针对不同元素，给出提升可访问性的策略和途径。

### 非文本内容
确保 icons 和 charts 等内容，需要提供可替换并等价的文字，因为文字是可访问性程度最高的媒介。同时添加 alt text 对网页的 SEO 有一定好处。
```html
// Guideline
// 尽可能保持简短：最多 7 or 8 words，不要包含累赘的信息：“这是一个图片”
// 如果是复杂的图片，可以靠谱单独添加一段描述，或设置链接到完整描述。也可以使用 `longdesc` 属性，但可能有兼容性问题，可能只在 JAWS 上工作
// 描述应该与图片的*目的*保持一致，例如表单的提交按钮，alt text 就应该被设置为提交
// 如果图片仅是装饰作用或与标题重复，记得将 alt 属性设置为空
// 确保背景图片仅用于装饰，因为无法对背景图片添加 alt 描述
<img src="" alt="description"> 
```

### Accessible video
注意点⚠️：
  - 确保播放器支持字幕，并可以通过键盘访问所有交互元素
  - 确保不要自动播放视频 
  - 确保视频不包含 flashing or strongcontent；which can cause seizuies
  - 确保提供的手语与视频同步

奇怪的知识：原来 YouTube 上的 CC 代表 closed capture

### Contrast & Colours
为什么好的对比度设计很重要？
- 超过 50 岁的司机，相比于 30 岁，在夜晚需要几乎两倍的灯光才能保证安全驾驶。
- 8% 的男性与 0.5% 的女性有一定程度色盲

以个人博客为例，可以使用 WAVE 软件来改善网页的对比度（对比度的范围：1 - 21）。可以看到正文的对比度符合要求，但链接的对比度有待提升（注意不同字体大小的对比度要求不同）：
![](/images/blog/global/17427813192153.jpg)

通过手动调节颜色，使得对比度符合要求：
![](/images/blog/global/17427814143805.jpg)

⚠️其他注意点：
- 确保不要仅以颜色作为传递信息的手段，例如使用颜色标识表单中的字段是必填的
- 需要避免的颜色组合: 红色/绿色、蓝色/黄色、。。。

### Accessible links
当盲人使用 screen reader 游览网页时，常常会一次性获取所有的链接方便进一步阅读自己感兴趣的信息。下图为在 macOS 中使用 VoiceOver 时，`ctrl+option+u` 获取链接菜单：
![](/images/blog/global/17427843523053.jpg)

⚠️如何让链接更有意义？
1. 确保链接使用描述性文字，而不是 点击这里 或 阅读更多
2. 使用下划线突出链接，并在 fucos 时高亮
3. 不要使用完整的 URL 作为链接的文本
4. 链接到 PDF 或其他文本：建议添加图标、文件大小、以及打开需要的软件链接。
5. 考虑插入“skip link”，方便依赖键盘导航或使用屏幕阅读器的用户，可以直接跳过重复的导航菜单而访问页面的主要内容

[Skip Navigation Links](https://webaim.org/techniques/skipnav/) 的一个例子：
```html
<!--
1. 确保链接是 body 中的第一个元素
2. 确保链接通过 css 隐藏
-->
<body>
<a href="#maincontent">Skip to main content</a>
...
<main id="maincontent">
<h1>Heading</h1>
<p>This is the first paragraph</p>
```

### Accessible Tables 表格
⚠️注意点：
- 表格尽可能仅表达数据，而不是用来布局（个人理解丢失了层级信息）
- 表格格式化的技巧：**标题加粗向左对齐，内容向右对齐**
- 鼠标聚焦的时候高亮辅助提示

扩展阅读：[Tables Tutorial](https://www.w3.org/WAI/tutorials/tables/#:~:text=Accessible%20tables%20need%20HTML%20markup,td%3E%20to%20make%20tables%20accessible)

### Accessible Form 表单
⚠️注意点：屏幕阅读器自带表单模式，除了确保针对每个字段添加并关联明确的 label，还需要对字段进行分组（因为盲人范围表单或跳转时往往缺少上下文）：
```html
<fieldset>
  <legend>Personal Details</legend>
  <label for="name">Name<lable>
  <input name="Name" type="text id="name">
  ...
</fieldset>

<fieldset>
  ...
</fieldset>
```

表单校验以及错误提示的处理：
- 不同校验方式的策略：
    - 服务器端校验：错误显示在页面顶部，并 id 聚焦在错误信息上（通过`url#myerrormessages`）。
    - 客户端校验：在填写单个字段后或提交时触发，并确保用户能迅速定位到问题字段
- 关于弹框：
    - javascript 弹框虽然大部分情况下令人讨厌，但这个场景下是屏幕阅读器友好并推荐使用。可以考虑使用 `aria-invalid="true"` 字段帮助屏幕阅读器识别无效字段


### Accessible javascript
⚠️注意点：
- 即使 JavaScript 被禁用，确保所有的功能可以正常使用
- 事件处理：除了 `mouseover`，`mouseout` 等，也要支持使用键盘对应的事件 `onfocus`，`onblur` 等


### ARIA（Accessible Rich Internet Applications Suite）
对网页元素添加额外的属性，方便 screen reader 直接定位，举个例子（注意 `role` 属性）：
```html
<!--the main navigation-->
<div id="mainnav" role="navigaton" aria-labelledby="mainnavigation">
<h2  id="mainnavigation">Main Navigation</h2>
...main navigation links here ...
</div>

<!--the right-hand column navigation-->
<div id="rightcolunnnav" role="navigation" aria-labelledby="rightnavigation">
<h2  id="rightnavigation">Right-Hand Column Navigation</h2>
...right-hand column navigation goes here ...
</div>
```

更多参考：https://www.w3.org/TR/wai-aria-practices-1.1/

## 总结

虽然课程中针对各个组件罗列了详细的 checklist，但也可以安装游览器插件 [WAVE web accessibility evaluation tool](https://wave.webaim.org/extension/) 帮助你快速评估网页内容的可访问性。

待博主将网页优化一版后，再更新用户的反馈。
