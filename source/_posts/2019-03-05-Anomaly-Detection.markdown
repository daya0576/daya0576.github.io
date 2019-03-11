---
title: 正态分布(Normal Distribution)学习小记
date: 2019-03-05 22:36:56
tags:
---


Coursera 上吴恩达的[《机器学习》](https://www。coursera。org/learn/machine-learning/home/welcome)终于学到了第九周的课程。这周上半部分讲述了 Anomaly Detection，因为和工作比较相关([监控报警的智能降噪](/blog/20190113/anomaly-detection/))，所以比较感兴趣也很期待! 然而看完视频后，说实话略有些失望，因为只介绍了正态分布这一种算法。但视频和课后作业带我从各种不同角度深度剖析了一遍正态分布，收获颇多~         

本文主要记录了完成**课后编程作业**的过程，并用python实现一遍(课程为matlab)，talk is cheap，show me the code。也希望自己也包括正在读这篇文章的你，可以对正态分布有更深的理解。

<!--more-->

# 课后编程作业:
> In this exercise，you will implement the anomaly detection algorithm and apply it to detect failing servers on a network。

检测服务器是否异常，兴奋🥰

## 1. 加载数据:
> You suspect that the vast majority of these examples are 'normal' (non-anomalous) examples of the servers operating normally，but there might also be some examples of servers acting anomalously within this dataset。

利用正态分布检测异常，其实是有一个前提的，就是数据集中大部分的数据都是"正常"的。将指定的数据集可视化后，可以明显的看到有几个点孤零零的分布在异常的位置。   
![](/images/blog/190302_cousera_anomaly_detection/15516041918813.jpg)

## 2.1 高斯分布模型介绍
有了数据，第二步就是用这些数据建立一个高斯分布的模型: 下图中的公式 `P(x;μ，σ^2)`，代表给定一个点(x)，返回它在整个分布中的具体概率:   
![](/images/blog/190302_cousera_anomaly_detection/model.jpg)


## 2.2 模型参数计算
计算高斯分布模型的两个关键参数: 

1. μ(mean): 平均值，读作mu
2. σ^2(variance): 方差

可视化之后，并可以看到大部分的点集中在最中心黄色的圆圈，并且刚刚计算的平均值和反差决定了圆圈的形状和大小。p。s。但看了半天没明白具体每个圈具体代表什么，求指点。  
![](/images/blog/190302_cousera_anomaly_detection/15516064266294.jpg)

## 2.3 选择阈值
完成高斯分布模型的参数之后，可以根据公式计算出每个点在数据集中的概率(越边缘的点概率越低，i.e. 概率越低，越可能是个异常)。在这一小节我们就是要找到一个特定的阈值(ε)，如果某个点的概率在这个阈值以下，`p(x) < ε`，即可判断为异常!   
![](/images/blog/190302_cousera_anomaly_detection/15516075882385.jpg)

很神奇，作业中是利用 f1 score 来找到最合适的阈值(之前写过[异常检测的precision，recall和f1 score的介绍](/blog/20190113/anomaly-detection/#2-回归测试)，感兴趣可以看一下)。

大致过程是根据最大和最小概率得到的间隔，不断地尝试一千个不同的阈值: `stepsize = (max(pval) - min(pval)) / 1000;`，最后计算得到 f1 score 最大的那个阈值就是最优解。   

但刚刚一直很疑惑🤔: 给定一个阈值，如何计算哪些点是tp(true positive: the number of true positives: the ground truth label says it's an anomaly and our algorithm correctly classified it as an anomaly。)，因为要依赖人工标记的 ground truth。好吧，和怀疑的一样，传入了人工标记好的 cross validation set。  

# Python实现
[要是上边有没看懂的地方，没关系，点我来直接看代码吧!](http://localhost:63343/normal_distribution_demo/normalization。html?_ijt=qjm1k3uhlise5vek8b664icc4r)   
但在计算出多个 feature 的"概率"之后就卡住了，因为一个点如果有两个 features，就会有两个概率，如何合并为一个呢?  
![](/images/blog/190302_cousera_anomaly_detection/15517965144087.jpg)

## 领悟到的:
Q: 为什么最大的概率不是100%？（上面说到概率的时候加了引号）
A: 因为正态分布的整体的**积分面积**为1，只不过宽窄高低不同罢了，所以y轴并不代表概率，最大值也就不是 100%


# 思考 & 收获
1. 在机器学习的课程中，大部分情况下，更多的是强调如何选取有效的特征，并同时使用多个特征去做预测。而现实中，我们常常只考虑了一维的特征，例如对于一个 spm 监控(请求量，成功量，成功率，耗时，错误数)，只对请求量做了计算，但其实可以同时对五个特征的数据集做异常检测。
2. 向量计算: 例如文中提示，在计算 f1 score 的过程中，尽可能使用向量计算，而不是 for 循化: `fp = sum((cvPredictions == 1) & (yval == 0))`。
3. 验证了异，常检测确实需要用 precision，recall & f1 score 来衡量，上  [Information Retrieval](/blog/20160731/comp6714-information-retrieval-and-web-search-2016s2/) 的时候学到的知识，并正确在工作中正确应用实践，给自己点个赞 👍 



