# Rain Effect - About Page

## Overview
About 页面的雨天氛围效果：视觉雨滴、水波纹动画、环境雨声。

## Components

### 1. Rain (Top)
- **File:** `layouts/partials/rain.html`
- Canvas 绘制的静态雨滴，带 shimmer 闪烁效果
- 支持明/暗模式自适应颜色
- 移动端减少雨滴数量（40 vs 120）

### 2. Ripple (Bottom)
- **File:** `layouts/partials/ripple.html`
- 雨滴落地水波纹效果

### 3. Rain Sound
- **File:** `layouts/partials/rain-sound.html`
- **Audio:** `static/rain-long.m4a`（原 `rain.m4a` 重复 11 次拼接，320kbps 立体声 48kHz，30 分钟，~70MB，streaming 加载）
- **Usage:** `{{ partial "rain-sound.html" . }}` in `layouts/about/single.html`
- **CSS:** `themes/nostyleplease/assets/css/main.scss`（`#rain-toggle`）

#### 播放控制
- 圆形按钮固定在屏幕右下角，`▶`（暂停）/ `⏸`（播放中）
- 3rem 圆形，满足 mobile 最小 48px 触摸目标
- `-webkit-tap-highlight-color: transparent` + `touch-action: manipulation` 消除移动端点击延迟和高亮
- Dark mode: 半透明黑底白字；Light mode: 半透明浅底深字
- 点击切换播放/暂停

#### 播放策略
1. **首次访问（无 cookie）** — 自动播放，autoplay 被阻止时等待首次交互后播放
2. **用户点暂停** — 停止播放，cookie `rain-sound-pref=0`，记住 1 天
3. **用户点播放** — 开始播放，cookie `rain-sound-pref=1`，记住 1 天
4. **cookie=0** — 不自动播放
5. **cookie=1** — 尝试自动播放

> **设计原则：** cookie 只在用户主动点击时写入，自动播放不写入 cookie，避免状态不一致。

#### 渐入渐出（Fade In/Out）
- 播放和暂停均有 **1 秒** 音量过渡
- 切换时按钮文字**立即变化**，不等待 fade 结束
- 使用 Web Audio API `GainNode` + `linearRampToValueAtTime` 实现平滑过渡
- fadeIn: `0 → 1`，fadeOut: `当前音量 → 0` 后 `pause()`

## Integration
- About 页面模板：`layouts/about/single.html`
- Rain visual：`{{ partial "rain.html" . }}` 在 `baseof.html` 中引入
- Rain sound：`{{ partial "rain-sound.html" . }}` 在 `layouts/about/single.html` 中引入

## Known Issues & Fixes

### Rain drops 积攒后消失（已修复）
- **现象：** 开始下雨 → 离开页面 → 回来后雨滴积攒在画面中然后消失
- **原因：** `requestAnimationFrame` 在后台被浏览器暂停，回到前台时 `dt`（帧间隔）变得巨大，导致一帧内所有雨滴飞出画布被删除，同时 `SPAWN_RATE * W * dt` 一次性生成几千个新雨滴
- **修复：**
  1. `dt` cap 上限 `Math.min(dt, 0.1)`，单帧最多模拟 100ms
  2. 监听 `visibilitychange`：页面隐藏时暂停动画循环（`paused = true`），恢复时重置 `lastTs = 0` 并重新启动 `requestAnimationFrame`
- **参考：** `ripple.html` 已有相同的 `visibilitychange` 处理

### 滚动后点击误触发下雨（已修复）
- **现象：** 页面滚动到中间 → 刷新（浏览器恢复滚动位置）→ 点击页面上半部分会触发下雨/音乐播放，即使 canvas 已不在视口内
- **原因：** `inRainZone()` 使用 `e.clientY < canvas.clientHeight` 判断，`clientY` 是视口坐标，`clientHeight` 是 canvas 高度（33.4vh）。页面滚动后 canvas 在视口上方不可见，但视口内上半部分点击的 `clientY` 仍小于 canvas 高度，导致误判
- **修复：** 改用 `canvas.getBoundingClientRect()` 获取 canvas 在视口中的实际矩形位置，判断点击坐标是否真正落在 canvas 范围内

### 循环播放卡顿（已修复）
- **现象：** 雨声在浏览器中循环播放时，每次循环衔接处有可感知的卡顿/间隙；本地播放器无此问题
- **原因：** `<audio loop>` 的循环方式是 seek 回开头重新播放，浏览器不处理 M4A/MP3 的 encoder padding（头尾的静音填充帧），导致循环处有间隙。本地播放器会读取元数据跳过这些 padding
- **修复：** 将原始 `rain.m4a`（2.75 分钟）重复拼接 11 次生成 `rain-long.m4a`（30 分钟），保持原始码率 320kbps 立体声 48kHz（~70MB，streaming 加载无影响）。循环间隙 30 分钟才出现一次，用户几乎不会感知

### Safari 音频播放延迟（待调查）
- **现象：** Safari 中点击播放后，雨声有明显延迟才开始
- **可能原因：** `preload="metadata"` 导致音频数据未预加载；Safari 的 AudioContext resume 策略更严格
- **Status:** investigating

## Status
- [x] Rain partial
- [x] Ripple partial
- [x] Rain audio with Web Audio API fade in/out
- [x] 1-day cookie preference (user-click only)
- [x] ASCII fixed toggle `[♪ on/off]` at bottom-right
- [x] Integrate into About page
- [x] CSS in `themes/nostyleplease/assets/css/main.scss`
- [x] Visibility change handling for rain canvas (prevent frame accumulation)
