---
title: Apache Iceberg 数据湖仓(Coursera)个人笔记
date: 2026-08-16T15:59:41+08:00
draft: true
tags:
  - study
  - coursera
  - iceberg
categories:
- SRE
comments: true
---


<!--more-->



## 名词解释

## [2h] Get Started with Databricks for Data Engineering

- Engines
    - Lakehouse: Data warehousing (Queries, dashboard)
    - Lakebase: Serverless Postgres (Agent state)
    - Lakeflow: Ingest, ETL, streaming
- Unified Catalog: permissions, lineage, discovering and auditing
- Open Formats：Postgres / Delta Lake / ICEBERG

### databricks walkthrough
结构：
<catalog>.<schema>.<table> (volumn)

```
SELECT current_catalog(), current_schema()
SHOW tables;
SHOW volumns;

CREATE TABLE IF NOT EXISTS as
SELECT * FROM read_files('/Volumes/' || my_catalog || '/' || my_schema || 'xxx.csv')


```

### version history & time travel

```
DESCRIBE HISTORY employs;
operation + operationParameters

SELECT * FROM employs VERSION AS OF 1;

# compare versions
SELECT 'Current', COUNT(*) FROM emplyees
UNION ALL
SELECT 'Version 0', COUNT(*) FROM emplyees VERSION AS OF 0;
```



