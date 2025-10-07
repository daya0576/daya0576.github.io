---
title: "Postmortem of My Journey at Autodesk"
date: 2025-10-05T20:00:00+08:00
categories:
- SRE
- 编程
---

As an SRE (Site Reliability Engineer), switching jobs is extremely risky - comparing it to a production change without any canary strategy and rollback option!😱 However, YOLO (you only live once), just embrace and enjoy the risks.

After joining Autodesk for 1y5m, the whole team was unfortunately impacted by layoff. Currently I have already left the company and became a fulltime parent.

Nonetheless, Autodesk is an incredible company with excellent benefits and professional colleagues. This post is a little retrospective in the form of a [postmortem](/blog/20180403/impressions-of-google-sre/#chapter-15---postmortem-culture-learning-from-failure).


# Timeline
I started my career as a Python developer in a startup in Shanghai, the engineering experience became a solid cornerstone for my SRE transition.

- 2017.03 ~ 2018.04: Python Software Engineer (Hypers)
- 2018.04 ~ 2023.10: Site Reliability Engineer (Ant Group) 
- 2023.10 ~ 2025.04: Site Reliability Engineer (Autodesk)


# Why did I join Autodesk? 

> Don’t Be The Best, Be The Only.

To enhance my competitiveness in the job market, I set three professional development goals upon joining the company:
- Site Reliability: Explore popular tech stacks
- Engineering: Launched an open source project in part time
- Communication Skills: Enhance English speaking proficiency

P.S. Fun fact - at Autodesk, in addition to ORK, everyone is also encouraged to set up an Individual Development Plan (IDP), and the goals aren't necessarily closely related to their daily job.

# So, how was it?

It turned out that I successfully achieved most of my goals:

- ✅ Site Reliability: Achieved AWS SysOps Administrator certification
- ✅ Engineering: Launched an open-source project with user from more than 100 countries
- ☑️ Communication Skills: Enhanced ability to effectively collaborate in English-speaking environments

*However, this did not completely reduce my anxiety :( I eventually realized that, as an "average" person, the easiest way of being competitive isn't about being resilient in the job market, but about being unique—like being the only person who can understand and modify a piece of core code in the company.*

![IMG_1659](/images/blog/global/IMG_1659.jpeg)


# Lessons learned
The definition of SRE varies significantly across companies, including platform engineer, technical support, server reboot engineer, emotional support SRE...

I'v experienced two distinct SRE models: At Ant Group, I was part of a centralized SRE team (~80 people) responsible for the SLOs of global payment services (~3000 people). In contrast, at Autodesk, I work as a dedicated SRE embedded within a specific product team (~15 people).

The two experiences have helped me gain a **deep and broad understanding** of achieving Service Level Object (SLO).

<img width="450" src="/images/blog/global/17596656935359.jpg">

In Autodesk, as a dedicated SRE being directly responsible for the SLO target with limited resources, I'm facing more challenges. So I had to think globally and prioritize my time smartly. 

Personally I invested 70% of my time on incident prevention, and 30% on incident detection and recovery.

## Incident Prevention (70%)

### 1. Changes
Simply focus on changes:

#### 1.1 Code Changes (Application/Config/Infra/...)
A key distinction between SRE and Platform Engineer is the requirement of deep domain knowledge. After spending several months documenting business workflows through sequence diagrams, I began actively participate in code reviews to identify and mitigate potential production risks at an early stage.

Here are two examples:
1. During an application code review, I found a defect that the cache TTL (Time to Live) will be incorrectly reset every time on value update, which may causing the rate limiting not working as expected.
2. In an terraform code change (traffic cutover), I recommended implementing AWS Route53 weighted routing to enable gradual traffic shifting (starting with 1% of traffic), significantly reducing the risk of service disruption during the cutover.

#### 1.2 Dependency Changes (Resiliency Test)

Service dependency failures are one of the leading causes of incidents. For example, when the database is hanging, most of the traffic of the service should be handled by the cache. However, due to unnecessary hard dependency on the database, the service is completely down.

To address this, I developed an HTTP(S) proxy tool that enables the team to perform resiliency tests and fire drills (chaos), helping identify and eliminate unnecessary hard dependencies.

[Read more..](/blog/20231118/https-hijack/)

#### 1.3 Other Changes

- Upstream traffic surge: using bi-week service reviews to monitor upstream traffic trend and ensure our rate-limiting and scaling policies are working as expected.
- ...

### 2. Incident & Issues Management

I have the habit of tracking all incidents and issues. Interestingly, after collecting and analyzing 40+ cases, it magically helped me identify *key patterns* in service reliability problems and shaped my next year's OKRs. This also significantly impressed my manager during the yearly performance review.

## Incident Detection & Recovery (30%)

### End-to-End Monitoring
While our monitoring system (SLO alerts and health checks) can detect incidents within one minute, identifying root causes remains challenging even for experienced engineers, resulting in high Mean Time To Recovery (MTTR).

To address this challenge, I implemented **end-to-end Synthetic Monitoring** with [AWS CloudWatch Canaries](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html). The synthetic monitoring simulates real user transactions and validates key steps throughout the service workflow. For instance, it even verifies the design file visualization process by checking cache loading status in DynamoDB.

This solution automatically output the failing step when an alert triggers, significantly improving our root cause analysis efficiency.


# Action items
Incidents are inevitable and not always negative; they provide opportunities to review and enhance our services.

Even though I was affected by layoffs, on the other side, this change has offered me the precious opportunity to become a full-time parent 😊

The next thing for me is taking care of my newborn at least 12 months, I will be writing more on the topic so stay tuned!

![](/images/blog/global/17596686979017.jpg)

# References
- https://www.tinystruggles.com/posts/google_postmortem/