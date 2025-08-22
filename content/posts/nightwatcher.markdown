---
title: "Nightwatcher - A Simple IP Camera Viewer 🦇"
date: 2025-08-11T19:45:19+08:00
categories:
- python
---

GitHub: https://github.com/daya0576/nightwatcher

## Background

As a first-time dad, to reduce anxiety, I set up two cameras for quick glances:
- A room overview camera (`Tplink IPC45AW`)
- A dedicated baby monitor (`Aqara G100`)

Both cameras have been integrated into HomeKit and shared with my family (through [Home Assistant ONVIF](https://www.home-assistant.io/integrations/onvif/))

![](/images/blog/global/17549158473402.jpg)

## Current Limitations & Challenges :(

Thanks to the camera replay, we manually record our newborn's [feeding and sleep patterns](https://changchen.me/blog/20250727/paipai_two_months_old/#full-time-parent), which helps us analyze his long-term routines. 

However, the user experience was frustrating for several reasons:

1. <u>**Performance Issues**</u>: High latency and frequent freezing, taking 2-3 seconds to load screenshots and stream video. And the stream quality is limited to low resolution.
2. <u>**Cross Platform Support**</u>: HomeKit only works within Apple ecosystem, so it's impossible to view all the cameras at the same time on my Android tablet.
3. <u>**Privacy & Extensibility**</u>: Both of the montors provide advanced AI detection features, but the streaming must be processed through the cloud with unknown algorithms.
4. <u>**Simplicity**</u>: Tried several existing open source solutions, but they are a bit too complex and put me off.


## The Solution: Night Watcher

> Nightwatchers? The name comes from the lateest DLC of my favorate game "[Against the Storm](https://store.steampowered.com/app/3725110/Against_the_Storm__Nightwatchers/)".

Due to these limitations, I decided to create a micro web-based IP camera viewer: [https://github.com/daya0576/nightwatcher](https://github.com/daya0576/nightwatcher)

1. <u>**Performance**</u>: Blazing fast without any delay.
2. <u>**Cross Platform Support**</u>: Works on any device with a browser.
3. <u>**Privacy & Extensibility**</u>: Local models and custom detection support.
4. <u>**Simplicity**</u>: Minimal navigations and css styles.


![2025-08-15 00.06.09](/images/blog/global/2025-08-15%2000.06.09.gif)


## Next...

- [x] PWA web app
- [ ] Dockerlization
- [ ] User friendly custom detection
- [ ] Refine camera configuration
- [ ] Train a YOLO11 model on my custom dataset 
- [ ] ...


## Final words

This project is made with love for families, tested by my wife :p 

Hoping you can enjoy this project and feel free to contribute!

![4DD287FD-24AB-4564-ADD5-1E4D1D0AD86D_1_102_o](/images/blog/global/4DD287FD-24AB-4564-ADD5-1E4D1D0AD86D_1_102_o.jpeg)
