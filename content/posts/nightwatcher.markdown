---
title: "Nightwatcher - A Simple IP Camera Viewer 🦇"
date: 2025-08-11T19:45:19+08:00
categories:
- python
- 开源
- 编程
---

GitHub: https://github.com/daya0576/nightwatcher

<img src="/images/blog/global/2025-08-27%2019-19-26.2025-08-27%2019_24_27.gif"></img>


## Background

As a first-time parent, to reduce anxiety, I set up two cameras for quick glances:
- A room overview camera (`Tplink IPC45AW`)
- A dedicated baby monitor (`Aqara G100`)

Both cameras have been integrated into HomeKit and shared with my family (through [Home Assistant ONVIF](https://www.home-assistant.io/integrations/onvif/))

![](/images/blog/global/17549158473402.jpg)


## Constraints

The user experience of HomeKit was *frustrating* for several reasons:

1. <u>**Performance Issues**</u>: High latency and frequent freezing, taking 2-3 seconds to load screenshots and stream video. And the image quality is limited to low resolution.
2. <u>**Cross Platform Support**</u>: HomeKit only works within Apple ecosystem, so it's impossible to view all the cameras at the same time on my Android tablet.
3. <u>**Privacy & Extensibility**</u>: Both of the montors provide advanced AI detection features, but the streaming must be processed through the cloud with unknown algorithms.
4. <u>**Simplicity**</u>: Tried several existing open source solutions, but they are a bit too complex and put me off.

Fortunately, both cameras support RTSP (Real Time Streaming Protocol) for video stream consuming.


## The Solution: Night Watcher

> Nightwatchers? The name comes from the lateest DLC of my favorate game "[Against the Storm](https://store.steampowered.com/app/3725110/Against_the_Storm__Nightwatchers/)".

Due to these limitations, I decided to create a micro web-based IP camera viewer: [https://github.com/daya0576/nightwatcher](https://github.com/daya0576/nightwatcher)

1. <u>**Performance**</u>: Blazing fast without any delay.
2. <u>**Cross Platform Support**</u>: Works on any device with a browser.
3. <u>**Privacy & Extensibility**</u>: Local models and custom detection support.
4. <u>**Simplicity**</u>: Minimal navigations and css styles.


### Demo

![2025-08-27 19-19-26.2025-08-27 19_24_27](/images/blog/global/2025-08-27%2019-19-26.2025-08-27%2019_24_27.gif)


## Interesting story

My sweet got recognized as an apple by YOLO 🤣🤣🤣: 

<img width="150" src="/images/blog/global/IMG_2810.png"></img>


## Next...

- [x] PWA web app
- [ ] Dockerlization
- [ ] User friendly custom detection pipeline
- [ ] Refine camera configuration
- [ ] Train a YOLO11 model on my custom dataset 
- [ ] ...


## Final words

As a full-time parent, I created this small project as a toy during my baby's nap times. It works wonderfully, and my wife quickly took to it :p 

I hope you enjoy it and feel free to contribute.

![4DD287FD-24AB-4564-ADD5-1E4D1D0AD86D_1_102_o](/images/blog/global/4DD287FD-24AB-4564-ADD5-1E4D1D0AD86D_1_102_o.jpeg)
