# CLAUDE.md

## 项目概述

Hugo 静态博客，站点地址：https://changchen.me
主题：`nostyleplease`（**极简风格**），Hugo v0.154+


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

### 主题

`nostyleplease` 以 git submodule 形式挂载于 `themes/nostyleplease`，对主题的修改直接在 submodule 内进行。

- CSS：`themes/nostyleplease/assets/css/main.scss`
- Heading render hook：`layouts/_default/_markup/render-heading.html`
- 自定义 partials（覆盖主题）：`layouts/partials/`
- 自定义 shortcodes：`layouts/shortcodes/`
- 主题 partials：`themes/nostyleplease/layouts/partials/`


