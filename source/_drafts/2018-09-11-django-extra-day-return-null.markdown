---
title: django_extra_day_return_null
date: 2018-09-11 11:48:49
tags:
---


```sql
SELECT EXTRACT(DAY FROM CONVERT_TZ(`alarm_list`.`created_gmt`, 'UTC', 'Asia/Shanghai')) AS `day`, COUNT(`alarm_list`.`id`) AS `count` FROM `alarm_list` INNER JOIN `monitor_config` ON (`alarm_list`.`monitor_config_id` = `monitor_config`.`id`) WHERE (`alarm_list`.`created_gmt` >= '2018-08-08 16:00:00' AND `alarm_list`.`created_gmt` < '2018-09-09 16:00:00' AND `monitor_config`.`need_check_alarm` = 1) GROUP BY EXTRACT(DAY FROM CONVERT_TZ(`alarm_list`.`created_gmt`, 'UTC', 'Asia/Shanghai')) ORDER BY NULL LIMIT 21;
```

```sql
SELECT EXTRACT(DAY FROM CONVERT_TZ(`alarm_list`.`created_gmt`, 'UTC', 'Asia/Shanghai')) AS `day` FROM `alarm_list`;
```

```sql
SELECT EXTRACT(DAY FROM `alarm_list`.`created_gmt`) AS `day` FROM `alarm_list`;
```

https://www.google.com/search?q=convert_tz+returns+null&oq=CONVERT_TZ+&aqs=chrome.2.69i57j0l5.2352j0j7&sourceid=chrome&ie=UTF-8

`mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql`
![](/images/blog/180911_django_extra_day_return_null/15366456266149.jpg)

`mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -h mysql.takachiho.inc.alipay.net -u root -p -D mysql`


