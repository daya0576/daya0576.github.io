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
- **Usage:** `{{ partial "rain-sound.html" . }}` in `layouts/about/single.html`
- **CSS:** `themes/nostyleplease/assets/css/main.scss`（`#rain-prompt`, `.rain-toggle-wrap`）

#### 播放策略
1. **自动播放** — 页面加载时直接 fadeIn 播放（About 页通常从主页导航进入，浏览器允许同站交互后的自动播放）
2. **记住偏好 7 天** — 通过 cookie `rain-sound-pref` 存储（`1`=开启，`0`=关闭），7 天过期
3. **用户曾关闭** — cookie 为 `0` 时不自动播放，需手动点击开启

#### 渐入渐出（Fade In/Out）
- 播放和暂停均有 **1 秒** 音量过渡
- 使用 `setInterval`（30ms）线性插值 `audio.volume`
- fadeIn: `0 → 1`，fadeOut: `当前音量 → 0` 后 `pause()`

#### 静音开关
- 固定在页面右下角（`position: fixed`）
- 🌧️ = 播放中，🔇 = 已静音
- 点击触发 fadeIn/fadeOut 切换

## Integration
- About 页面模板：`layouts/about/single.html`
- Rain partial 通过 `{{ partial "rain.html" . }}` 引入（在 `baseof.html` 或 about 模板中）

## Status
- [x] Rain partial
- [x] Ripple partial
- [x] Rain audio with fade in/out
- [x] 7-day cookie preference
- [x] Mute toggle button
- [x] Integrate into About page
- [x] CSS in `themes/nostyleplease/assets/css/main.scss`
