---
title: r24_memory_leak_issue
tags:
---



![](../images/blog/2021-09-04-jvm-note/16490471027778.jpg)


![](../images/blog/2021-09-04-jvm-note/16490470838107.jpg)

### syslog 配置



dmesg
syslog

`/proc/sys/vm/oom_dump_tasks`

> Enables a system-wide task dump (excluding kernel threads) to be produced when the kernel performs an OOM-killing and includes such information as pid, uid, tgid, vm size, rss, nr_ptes, swapents, oom_score_adj score, and name. This is helpful to determine why the OOM killer was invoked, to identify the rogue task that caused it, and to determine why the OOM killer chose the task it did to kill.

### 日志持久化 

#### Rsyslog Client
Rsyslog 收集
```shell
# /etc/rsyslog.conf
/etc/init.d/rsyslog start 

# 调试：logger -p kern.warn MESSAGE
```

#### log
https://openwrt.org/docs/guide-user/base-system/log.essentials
```shell
# vim /etc/config/system

config system 
...
   option log_file '/var/log/mylog'
   option log_remote '0'
   
# /etc/init.d/log restart && /etc/init.d/system restart


```

#### syslog-ng
https://openwrt.org/docs/guide-user/perf_and_log/log.syslog-ng3

#### u 盘
持久化存储
```
cp -r /var/* /mnt/sda1/var/

```
### 模拟 OOM 

```python
var = []
for x in range(99999999999):
    var.append(str(x))
    
bash -c "for b in {0..10000000}; do a=$b$a; done"
```

![](../images/blog/2021-09-04-jvm-note/16490575843322.jpg)

几个参数（**加粗**代表系统当前值）：`sysctl xxx`
- [vm.panic_on_oom](https://sysctl-explorer.net/vm/panic_on_oom/): 控制内存不足的行为
    - **值为0**：启动 OOM killer，干掉“无赖”进程
    - 值为1：触发 kernel panics（系统重启），但特殊情况进程会通过 OOM killer 被杀死。
    - 值为2：强制 panic
- [vm.oom_dump_tasks](https://sysctl-explorer.net/vm/oom_dump_tasks/): 
    - 值为0：关闭线程 dump
    - **不为0**：OOM Killer 干掉一个进程时，开启 dump 并记录日志
- [vm.oom_kill_allocating_task](https://sysctl-explorer.net/vm/oom_kill_allocating_task/): 控制 OOM 时先杀掉哪种进程
    - **值为0**：优先干掉得分最高的进程
    - 不为0：简单粗暴干掉所有申请内存并导致 OOM 的进程
- vm.overcommit_memory
- vm.overcommit_ratio



### 配置 OOM killer
尝试1：
```shell
# 临时修改
echo 1 | tee /proc/sys/vm/oom_kill_allocating_task
# 永久修改


sysctl vm.overcommit_memory
```

尝试2:



## 参考
1. https://baheyeldin.com/technology/linux/using-rsyslog-and-usb-storage-openwrt-logging.html
2. https://www.vpsee.com/2013/10/how-to-configure-the-linux-oom-killer/
3. http://linuxperf.com/?p=102