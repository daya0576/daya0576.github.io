---
title: test
tags:
---


代码是我们最好的朋友，通过源码尝试简单理解 rate/increase & irate 计算的基本逻辑：

## rate/increase

首先计算首尾两个 sample 的差值

例如下图 `1 1 1 2 3`，则 `resultFloat = 3 - 1 = 2`
![rate-1.drawio](images/rate-1.drawio.svg)
```go
numSamplesMinusOne = len(samples.Floats) - 1
firstT = samples.Floats[0].T
lastT = samples.Floats[numSamplesMinusOne].T
resultFloat = samples.Floats[numSamplesMinusOne].F - samples.Floats[0].F
if !isCounter {
    break
}
```

<mark>边界情况1</mark> -> 处理计数器重置（e.g. exporter 重启等情况）
例如 `1 2 3 1 2`，则 `resultFloat = 2 - 1 + 3 = 4`，个人理解等同于 `(3 - 1) + (2 - 0)`
![rate-2.drawio](images/rate-2.drawio.svg)
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

由于现实世界中，首尾 samples（`firstT` & `lastT`）并不会刚好落在 range 的开始/结束位置（`rangeStart`/`rangeEnd`），所以需要进一步推断（extrapolate）`rangeStart` 位置，从而估计更加准确的数值变化率。

<mark>边界情况2</mark> -> 推断范围限制（起始时间估计的计数不得为负数）
简而言之，下图黄线向左延伸时，不得低于 x 轴
![rate-3.drawio](images/rate-3.drawio.svg)

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

以下图为例，sample 只有两个（A & B），所以`平均间隔 = (75s - 45s) / (2 - 1) = 30s`，`阈值 = 30s * 1.1 = 33s`

由于 `durationToStart = 45s - 30s = 15s < 33s`，所以黄线可以扩展至 `rangeStart`

若超出阈值，则最多延伸样本平均间隔的一半（注意首尾相加刚好凑齐一个整的间隔）

![rate-4.drawio](images/rate-4.drawio.svg)

假如不做推断，`increase = 3 - 1 = 2`，推断扩展后 `increase = 4 - 0 = 4`

显然后置更加准确，同时不难理解：
- 为什么 rate 函数计算的结果会出现小数点
- 为什么 推荐针对平稳性数据使用 rate 计算变化率

```go
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

不难理解 `rate` 等同于 `increase / range seconds`
```go
if isRate {
    factor /= ms.Range.Seconds()
}
```

## irate