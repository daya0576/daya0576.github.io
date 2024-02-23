---
title: A Site Reliability Engineer's Guide to Change Request
tags:
---

System never goes down without making changes, e.g. code release, traffic change or dependency down, ....

In all kind of changes above, human changes are responsible for over 80% of incidents, as humans are not machines and make mistakes all the time :)

So when planning a change request for production operation (without perfect and automated pipeline), how can we leverage strategies to minimize the risk and impact to our customers? 

<!--more-->

Here is my guides for a Change Request: 

https://app.diagrams.net/#G17R5If_e5jOOraVfbaTrkZUvc640hp4zy#%7B%22pageId%22%3A%226a731a19-8d31-9384-78a2-239565b7b9f0%22%7D

- Change gradually, e.g. ca
- Rollback plan: 
- Verify the result after change

Finally, 

