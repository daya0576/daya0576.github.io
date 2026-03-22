---
title: "Reading DDIA as an SRE"
date: 2026-03-22T12:55:56+08:00
TOC: true
categories:
- SRE
- TECH
---

Over the past few weeks, to prepare for a system design interview, I read a book called DDIA (Designing Data-Intensive Applications), which had sat on my shelf for years. Not sure how much it would help my interview performance, but I truly enjoy it and have a brand new understanding of two past incidents.

This post shares my takeaways and initial thoughts of two incidents from an SRE's perspective.


## Incident1

### Problem
During a regular code deployment, I received an alert that the payment error rate had become abnormal, and the error count kept going up. After inspecting the timeline, I highly suspected that the rising error rate was caused by this release, so I rolled back the change immediately. Fortunately, the errors disappeared.

### Root cause
After further investigation, I noticed `serialization error` in the RPC logs and eventually found out that the root cause was a newly added enum value with inappropriate release order.

```
Service A (Old)          Service B (New)
          │                        │
          │─────── RPC Request ───>│
          │                        │
          │<─── Response: [Enum X]─┤
          │                        │
   [ Serialization ]               │
   [   Exception   ]               │
          X                        │
```

### What I learned

After reading DDIA, I gained a better understanding of RPC encoding and its trade-offs compared with approaches such as JSON and pickle. More importantly, when versioning is involved, we must carefully consider *backward and forward compatibility*.

Although this incident could have been avoided by releasing `Service A` first, a more robust solution is to fall back to an `UNKNOWN` value instead of letting middleware raise a critical system error and fail the payment. Another option is to use strings in RPC payloads and convert them to internal enums inside each service.


## Incident2

### Problem

It was a Friday morning and I was paged by a P1 alert showing that a key merchant's payment success request count had dropped by 20%. Fortunately, as soon as I opened the dashboard, the service recovered automatically within one minute.

The incident was caused by an internal bug in OceanBase: the database hung for about 30 seconds while merging data from memory to disk.

### Root cause
During the postmortem meeting, everyone focused on this bug and discussed the fix.

However, as a professional SRE, I noticed a deeper issue. The bug occurred in a customer-profile-related service's database, which means even if the database were totally down, it should not significantly impact payments because 99% of traffic was expected to be served from cache.

After reading the application's Java code for several days, I finally found out that although the `get_or_create_user` service had a proper cache strategy, the implementation queried database time at the beginning when preparing thread-local context. This unnecessary hard dependency was the true root cause of the incident.

### Solution
Then I created a pull request, using a "lazy load" strategy to fix this issue, preventing similar incidents from happening again for all related services in the application.

However, at that time, I still had a small question: __why didn't we simply use `now()` in the database when creating new users?__

### What I learned

After reading DDIA, I realized the answer is related to the complexity of distributed databases and data replication.

In DDIA, distributed databases are divided into three types:

1. Single leader, such as traditional MySQL database, one leader with multiple followers. 
2. Multi leader, personally I think it's similar to the Apple Notes app: every device is a leader; when a syncing conflict happens, simply use the latest version or let the user handle it themselves.
3. Leaderless, e.g. AWS DynamoDB.

For most single-leader databases, multiple followers can significantly improve global read performance, but they also introduce data-consistency challenges because of replications.

Coming back to my original question, `now()` is a **nondeterministic function**. If a database uses statement-based replication executing `INSERT ... now()` on the leader and followers will result in different timestamps and breaks data consistency.

Although modern databases have already use binlog replication to avoid this inconsistency, **explicit is better than implicit**, managing time in application layer ensures overall consistency and less coupled to underlaying infratructure.
