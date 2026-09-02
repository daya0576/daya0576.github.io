---
title: "[2h] Get Started with Databricks for Data Engineering"
date: 2026-08-16T15:59:41+08:00
draft: true
tags:
  - study
  - coursera
  - iceberg
categories:
- SRE
---


<!--more-->

## [2h] Get Started with Databricks for Data Engineering

- Engines
    - **Lakehouse**: Data warehousing (Queries, dashboard)
    - **Lakebase**: Serverless Postgres (Agent state)
    - **Lakeflow**: Ingest, ETL, streaming
- Unified Catalog: permissions, lineage, discovering and auditing
- Open Formats：Postgres / Delta Lake / ICEBERG

![](/images/blog/global/17880959318122.jpg)



### databricks walkthrough
结构：
`<catalog>.<schema>.<table|volumn>`

```sql
SELECT current_catalog(), current_schema()
SHOW tables;
SHOW volumns;

CREATE TABLE IF NOT EXISTS as
SELECT * FROM read_files('/Volumes/' || my_catalog || '/' || my_schema || 'xxx.csv')

```

### version history & time travel

```sql
DESCRIBE HISTORY employs;
operation + operationParameters

SELECT * FROM employs VERSION AS OF 1;

# compare versions
SELECT 'Current', COUNT(*) FROM emplyees
UNION ALL
SELECT 'Version 0', COUNT(*) FROM emplyees VERSION AS OF 0;
```

### Load Data incrementally with COPY INTO

```sql
COPY INTO XXX
FROM <VOLUMN>
FILEFORMAT = CSV
FORMAT_OPTIONS('header'='true')
```

### Medallion Architecture Pipeline

1. Bronze - Raw Ingestion
2. Silver - Cleaned & Enriched 
3. Gold - Business-Ready: aggregated, filtered, or joined.

```sql
List '/Volumes/{my_catalog}/{my_schema}/myfiles/'
```

## Pipeline

==types==:
1. Job
2. ETL pipeline
3. Ingestion pipeline

trigger:
1. scheduled
2. file arrival
3. table update
4. continuous 


