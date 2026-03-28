---
title: "Reading DDIA as an SRE"
date: 2026-03-22T12:55:56+08:00
categories:
- SRE
- TECH
---

## Henry's DDIA Notes

Over the past few weeks, to prepare for the system design interview, I read a book called DDIA (Designing Data-Intensive Applications). Not sure how much it will help my interview performance, but I truly enjoy it and have a brand new understanding of two past incidents.

This note shares my takeaways and initial thoughts of a real incident from SRE's perspective.

## Problem

It was a Friday morning and I was paged by a P1 alert showing that a key merchant's payment request had dropped by 20%. Fortunately, as soon as I opened the dashboard, the service recovered automatically within one minute.

The incident was caused by an internal bug in OceanBase: the database hung for about 30 seconds while merging data from memory to disk.

## Root cause
During the postmortem meeting, everyone focused on this bug and discussed the fix.

However, as a professional SRE, I noticed a deeper issue. The bug occurred in a customer-profile-related service's database, which means even if the database were totally down, it should not significantly impact payments because 99% of traffic was expected to be served from cache.


```
Client      Service        Cache           DB
  |            |             |             |
  |----------->|             |             |  request
  |            |-----------> |             |  get user profile
  |            |<----------- |             |  cache hit (99%)
  |            |             |             |
  |            |------x------------------->|  DB unavailable
  |            |   (optional / skipped)    |
  |            |             |             |
  |<-----------|             |             |  payment continues
```


After reading the application's Java code for several days, I finally found out that although the `get_or_create_user` service had a proper cache strategy, the implementation queried database time at the beginning when preparing thread-local context. This unnecessary hard dependency was the true root cause of the incident.

## Solution
Then I created a pull request, using a "lazy load" strategy to fix this issue, preventing similar incidents from happening again across all related services in the application.

However, at that time, I still had a small question: <u>why didn't we simply use `now()` in the database when creating new users?</u>

<br>

## What I learned

After reading DDIA, I realized the answer is related to the complexity of distributed databases and data replication.

In DDIA, distributed databases are divided into three types:

1. Single leader, such as traditional MySQL database, one leader with multiple followers. 
2. Multi leader, personally I think it's similar to the Apple Notes app: every device is a leader; when a write conflict occurs, simply use the last write version or let the user handle it themselves.
3. Leaderless, e.g. AWS DynamoDB.

For most single-leader databases, multiple followers can significantly improve global read performance, but they also introduce data-consistency challenges because of replications.

Coming back to my original question, `now()` is a **nondeterministic function**. If a database uses statement-based replication, executing `INSERT ... now()` on the leader and followers will result in different timestamps and breaks data consistency.

Although modern databases already use binlog replication to avoid this inconsistency, **explicit is better than implicit**, managing time in application layer ensures overall consistency and less coupled to underlaying infrastructure.
