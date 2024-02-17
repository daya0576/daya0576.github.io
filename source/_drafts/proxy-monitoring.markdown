---
title: Monitoring HTTP Proxy
tags:
---

家庭网络质量，如同水电燃气一般，对生活幸福感至关重要。而作为一名 SRE，突发奇想为家中 proxy 编写 exporter 并配置可观测大盘。

本文主要介绍 1）如何编写一个自定义的 exporter 2）PromQL 中 `rate`/`irate` 函数的实现原理

<!--more-->

![](../images/blog/2021-09-04-jvm-note/17081545533064.jpg)

# Workflow
```
Exporter (0.0.0.0:8000) ---pull--> Prometheus -> Grafana
```

## Step1: 编写 HTTP proxy exporter
Prometheus 中共存在四种 metrics 类型：
1. `Counter`: 累计计数的指标，随着时间的推移递增，例如请求数量、错误次数等。
2. `Gauge`: 适用于需要实时测量的指标，例如CPU 使用率、内存占用、网络延迟等。
3. `Histogram`: 用于度量和统计数据分布的指标类型，例如默认的 bucket 使用的 Web/RPC 请求耗时范围，从毫秒到秒：`DEFAULT_BUCKETS = (.005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0, 2.5, 5.0, 7.5, 10.0, INF)`。
4. `Summary`: 在不同百分位数上对观测值进行摘要统计的指标类型。

最终决定使用 `Counter` 统计请求总数与失败数，`Histogram` 统计请求耗时：[proxy_monitor/exporter.py](https://github.com/daya0576/proxy-monitor/blob/master/proxy_monitor/exporter.py)

## Step2: 接入 Prometheus
修改 yaml 配置文件，重启后稍等片刻即可生效。

## Step3: 配置 Grafana 大盘
针对 `Counter` 指标，通常使用 `rate`/`increase` 函数查询每分钟的请求量。但该函数背后的实现原理是？以及 `rate` 与 `irate` 函数的区别？

代码是我们最好的朋友，尝试通过源码一探究竟 :)

### rate & increase
Source code: [promql/functions.go](https://github.com/prometheus/prometheus/blob/6feffeb92e36b064a53d2283e50d6db355c95cb0/promql/functions.go#L70)

#### 1）计算增长率
首先计算首尾两个 sample 的差值，例如下图 `1 1 1 2 3`，则 `resultFloat = 3 - 1 = 2`
![rate-1.drawio](../images/blog/2021-09-04-jvm-note/rate-1.drawio.svg)

关键代码如下：
```go
numSamplesMinusOne = len(samples.Floats) - 1
firstT = samples.Floats[0].T
lastT = samples.Floats[numSamplesMinusOne].T
resultFloat = samples.Floats[numSamplesMinusOne].F - samples.Floats[0].F
if !isCounter {
	break
}
```

#### 2）推测增长率
但现实世界中，虽然样本间隔时间大概率接近，但首尾样本（`firstT` & `lastT`）并不会刚好落在 range 的开始/结束位置（`rangeStart` & `rangeEnd`）

所以需要进一步<mark>推断（extrapolate）</mark> `rangeStart` 的位置（i.e. 黄色虚线延伸），从而尝试估算更加真实准确的 rate 变化率。

![rate-4.drawio](../images/blog/2021-09-04-jvm-note/rate-4.drawio.svg)

如上图，假如不做推断，`increase = 3 - 1 = 2`，尝试推断后 `increase = 4 - 0 = 4`

显然后置更加准确，同时也不难理解：
- 为什么 rate 函数计算的结果会出现小数点
- 为什么 推荐针对平稳型数据使用 rate 计算变化率

```go
// p.s. extrapolate 推测的源码逻辑，请参考下文 “边界情况3”
```

#### 3）边界情况处理
<mark>边界情况1</mark> -> 处理计数器重置（e.g. exporter 重启等情况）

例如 `1 2 3 1 2`，则 `resultFloat = 2 - 1 + 3 = 4`，个人理解等同于 `(3 - 1) + (2 - 0)`
![rate-2.drawio](../images/blog/2021-09-04-jvm-note/rate-2.drawio.svg)

关键代码如下：
```go
// Handle counter resets:
prevValue := samples.Floats[0].F
for _, currPoint := range samples.Floats[1:] {
	if currPoint.F < prevValue {
		resultFloat += prevValue
	}
	prevValue = currPoint.F
}
```

<mark>边界情况2</mark> -> 推断范围限制（估计的起始时间，对应计数不得为负数）。

简而言之，下图黄线向左持续延伸时，不得低于 x 轴
![rate-3.drawio](../images/blog/2021-09-04-jvm-note/rate-3.drawio.svg)

关键代码如下：
```go
// Duration between first/last samples and boundary of range.
durationToStart := float64(firstT-rangeStart) / 1000
durationToEnd := float64(rangeEnd-lastT) / 1000

sampledInterval := float64(lastT-firstT) / 1000
averageDurationBetweenSamples := sampledInterval / float64(numSamplesMinusOne)

// TODO(beorn7): Do this for histograms, too.
if isCounter && resultFloat > 0 && len(samples.Floats) > 0 && samples.Floats[0].F >= 0 {
	// Counters cannot be negative. If we have any slope at all
	// (i.e. resultFloat went up), we can extrapolate the zero point
	// of the counter. If the duration to the zero point is shorter
	// than the durationToStart, we take the zero point as the start
	// of the series, thereby avoiding extrapolation to negative
	// counter values.
	durationToZero := sampledInterval * (samples.Floats[0].F / resultFloat)
	if durationToZero < durationToStart {
		durationToStart = durationToZero
	}
}
```

<mark>边界情况3</mark> -> 推断范围限制（根据样本平均间隔）

以下图为例，sample 只有两个（A & B），所以平均间隔 `averageDurationBetweenSamples = (75s - 45s) / (2 - 1) = 30s`，阈值`extrapolationThreshold = 30s * 1.1 = 33s`
- 由于 `durationToStart = 45s - 30s = 15s < 33s`，未超过阈值，所以黄线可以扩展至 `rangeStart`
- 反之若超出阈值，则最多延伸样本平均间隔的一半（首尾相加刚好凑齐一个整的间隔）

![rate-4.drawio](../images/blog/2021-09-04-jvm-note/rate-4.drawio.svg)

关键代码如下：
```go
// If the first/last samples are close to the boundaries of the range,
// extrapolate the result. This is as we expect that another sample
// will exist given the spacing between samples we've seen thus far,
// with an allowance for noise.
extrapolationThreshold := averageDurationBetweenSamples * 1.1
extrapolateToInterval := sampledInterval

if durationToStart < extrapolationThreshold {
	extrapolateToInterval += durationToStart
} else {
	extrapolateToInterval += averageDurationBetweenSamples / 2
}
if durationToEnd < extrapolationThreshold {
	extrapolateToInterval += durationToEnd
} else {
	extrapolateToInterval += averageDurationBetweenSamples / 2
}
factor := extrapolateToInterval / sampledInterval
```

#### 4）`increase` vs `rate`
参考如下代码，不难理解 `rate` 每秒增长率，等同于 `increase / range seconds`
```go
if isRate {
	factor /= ms.Range.Seconds()
}
```

### irate



--- 

大功告成，大盘使用的配置如下：
```

```

# 参考：
- https://zhangguanzhang.github.io/2020/07/30/prometheus-rate-and-irate/#/rate
- https://promlabs.com/blog/2021/01/29/how-exactly-does-promql-calculate-rates/
