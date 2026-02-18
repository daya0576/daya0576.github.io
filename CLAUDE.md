# CLAUDE.md

## 项目概述

Hugo 静态博客，站点地址：https://changchen.me
主题：`nostyleplease`（极简风格），Hugo v0.154+

## 常用命令

- `hugo server -D` — 本地预览（含草稿）
- `make` — 拉取、提交、推送（等同于 `make pull commit push`）
- `hugo new posts/<slug>.markdown` — 创建新文章

## 项目结构

```
content/posts/       # 博客文章（~195 篇）
content/about/       # 关于页面
layouts/partials/    # 自定义 partial（head.html, structured-data.html）
layouts/shortcodes/  # 自定义 shortcode（video.html）
layouts/footer.md    # 页脚
static/images/       # 图片资源
hugo.toml            # 站点配置
```

## 文章 Front Matter 格式

```yaml
---
title: "文章标题"
date: 2026-02-17T11:00:31+08:00
draft: true          # 发布时改为 false 或删除
categories:
- 分类名
series:
- 系列名
tags:
- 标签名
---
```

## 写作规范

- 文章文件名使用小写 + 下划线，扩展名 `.markdown`
- 文章语言以中文为主
- 图片放在 `static/images/blog/` 下，文章中用 `![](/images/blog/...)` 引用
- 永久链接格式：`/blog/:year:month:day/:slug/`
