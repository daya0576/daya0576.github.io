---
title: "终端搬家小记（iTerm → Alacritty）"
date: 2024-12-08T14:49:56+08:00
categories:
- SRE
- 编程
---

工欲善其事，必先利其器，作为一名程序员，有一款趁手的终端工具，就像厨子拥有一把锋利的菜刀一样重要。

虽然 iTerm 开箱即用，但强大丰富的功能却让它显得略显臃肿，例如添加 tab 或分屏等功能，由于使用 tmux 所以完全用不上。以及配置选项眼花缭乱，甚至有些混乱，令人头痛。

偶遇 Alacritty 便被它的设计哲学所吸引：尽可能的做减法。选择它并不是因为拥有某个 killer feature 或独一无二的地方，只是因为 Alacritty 拥有你所需要的所有功能，而且没有你暂时不需要的功能。

除此之外，在 Alacritty 中，配置文件也非常符合直觉，保存后便实时自动生效（On The Fly），令人身心愉悦，神清气爽。

# Troubleshoot
上手的过程并非一帆风顺，可以看到初次开启后，右边的 Alacritty 在配色和字体渲染方面明显劣于左边的 iTerm（或许是因为习惯）：

![](/images/blog/2021-09-04-jvm-note/17337046376248.jpg)

## 配色自定义
即使在 Alacritty 中使用 [同款配色](https://github.com/mbadolato/iTerm2-Color-Schemes/blob/master/alacritty/iTerm2%2520Dark%2520Background.toml)

在 iTerm 中，颜色明显更“亮”一些，排查后是由于 "Brighten bold text" 导致：

![](/images/blog/2021-09-04-jvm-note/17337051077592.jpg)

不难找到 Alacritty 中相应配置，以达到一致的显示效果：
```toml
[colors]
draw_bold_text_with_bright_colors = true
```

## 字体自定义
即使已设置相同字体，iTerm 中的字符却看上去明显更“细”一些。

排查后是由下图配置导致：

![](/images/blog/2021-09-04-jvm-note/17337067023858.jpg)

进而不难发现是与 Apple Font Smoothing 相关，更新配置并重新开启 app 即可：
```shell
defaults write org.alacritty AppleFontSmoothing -int 0
```

详情参考 [issue #7333](https://github.com/alacritty/alacritty/issues/7333)

# 题外话
在当今短视频和 AI 盛行的时代，快乐与知识的获取变得日益便捷，但人们的耐心似乎逐渐减弱。。

尝试通过传统搜索，并在 issues 中仔细阅读游览每条讨论，最终解决问题过程竟令人怀念并感到快乐。

# 参考

<link href="https://cdn.rawgit.com/Killercodes/281792c423a4fe5544d9a8d36a4430f2/raw/36c2eb3e0c44133880485a143717bda9d180f2c1/GistDarkCode.css" rel="stylesheet" type="text/css">

<script src="https://gist.github.com/daya0576/3527263bc9f47e769171e9569e225ced.js"></script>