---
title: A Site Reliability Engineer's Simple Guide to Change Request
date: 2024-02-23 22:35:18
tags:
---

System will never go down without "changes", e.g. code release, traffic overloaded or external dependency down,...

In all kinds of changes above, human changes are responsible for over 80% of incidents, as humans are not machines and make mistakes all the time :)

So when planning a change request for production operation (without a perfect and automated pipeline), how can we leverage strategies to minimize the risk and impact on our customers? 

<!--more-->

---

Here are three tips for planning a change request: 
- **Change gradually**, for example, internal users -> 1% customers -> 5% customers -> ...
- **Verify** the change result through dashboards or logs 
- Ensure that the change can be swiftly **rolled back**

Change Request Risk-Minimization Model: 
![change request.drawio](../images/blog/2021-09-04-jvm-note/change%20request.drawio.svg)

p.s. For difference services, we can adjust the pace of change based on the level of risk acceptance.