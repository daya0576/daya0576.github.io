---
title: 你真的会使用 ChatGPT 吗？ | 第一章：Guidelines for Prompting
tags:
date: 2023-05-03 21:05:49
categories:
- 个人相关
---

作为吴教主 Andrew Ng 的头号粉丝，怎能错过最新公开课《ChatGPT Prompt Engineering for Developers》。希望学完该课程后可以更好的“调教”大模型，避免其胡编乱造🤣

本篇文章整理了第一章 [Guidelines](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/2/guidelines) 的重点，主要阐述了与大模型更好人机交互的两个指导原则：
1. Principle 1: Write clear and specific instructions
2. Principle 2: Give the model time to "think"

<!--more-->

# 两个原则

## Principle 1: Write clear and specific instructions

### 策略1：划重点
使用 ```` ``` ```` 等分隔符，高亮待分析的独立内容，避免其误导意图。
![](../images/blog/2021-09-04-jvm-note/16830723690948.jpg)

### 策略2：明确输出格式
不难理解，如下图指定生成的内容通过 json 等格式结构化输出：
![](../images/blog/2021-09-04-jvm-note/16830192018694.jpg)

### 策略3：让模型学会说“不”
简单的 if..else 判断
![](../images/blog/2021-09-04-jvm-note/16830196562591.jpg)

![](../images/blog/2021-09-04-jvm-note/16830195655015.jpg)

### 策略4：不要吝啬你的提示
简单给出若干案例，供模型高效的效仿：
![](../images/blog/2021-09-04-jvm-note/16830200654353.jpg)


## Principle 2: Give the model time to “think”

### 策略1：手把手指导
提供完成任务所需的所有步骤：
![](../images/blog/2021-09-04-jvm-note/16830282120339.jpg)

### 策略2：循循善誘
当模型给出错误结论时，用户可引导模型将任务分解成若干步骤，**优先给出自身的回答**，再进一步对比判断结论是否正确。

直接以课程中的例子，学生回答其实是错误的：因为**维护成本是 10元/平方，而不是 100元/平方**
![](../images/blog/2021-09-04-jvm-note/16830310966012.jpg)

换一种提问的方式，迫使模型先独立计算后再判断学生的回答是否正确，最终获取更加准确的回答。
![](../images/blog/2021-09-04-jvm-note/16830316216662.jpg)

# 模型的局限性：幻觉（Hallucinations）
虽然模型被喂食了海量的数据，但它无法完美的记住所有看到的信息，所以并不太了解自己知识的边界。最终导致正确的废话甚至层出不穷的“谎言”。

模型竟然会为自己辩解，着实有一点可怕。个人觉得 AI 终有一天会作为人类的进化体，物竞天择替代我们成为这个世界的“主人”。
![](../images/blog/2021-09-04-jvm-note/16830318949352.jpg)
    
---

BTW，本篇文章使用的工具：
- 模型：GPT-4
- 客户端：OpenCat
