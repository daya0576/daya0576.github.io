---
title: "Unraid_10g_smb_debugging"
date: 2025-05-15T10:34:46+08:00
draft: true
---


# 问题
通过 Mac 通过 SMB 写入文件时，虽然与 Unraid 服务器连接的是万兆网络，但文件传输速度只 ~400MB/s 

# 阶段一（400MB/s -> 700MB/s）

## 1、确认网络性能 ✅
```shell
iperf3 -c 10.200.1.159 -p 5201 -t 5
Connecting to host 10.200.1.159, port 5201
[  5] local 10.200.1.222 port 54941 connected to 10.200.1.159 port 5201
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-1.01   sec  1.16 GBytes  9.92 Gbits/sec
[  5]   1.01-2.01   sec  1.15 GBytes  9.90 Gbits/sec
[  5]   2.01-3.01   sec  1.15 GBytes  9.88 Gbits/sec
[  5]   3.01-4.01   sec  1.15 GBytes  9.90 Gbits/sec
[  5]   4.01-5.01   sec  1.15 GBytes  9.90 Gbits/sec
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-5.01   sec  5.77 GBytes  9.90 Gbits/sec                  sender
[  5]   0.00-5.01   sec  5.77 GBytes  9.89 Gbits/sec                  receiver
```

## 2、确认硬盘性能  ✅
```shell
# 写入速度 
root@Lisa:~# dd if=/dev/zero of=/mnt/user/speed/testfile bs=1G count=3 oflag=direct
3221225472 bytes (3.2 GB, 3.0 GiB) copied, 2.62346 s, 1.2 GB/s
root@Lisa:~# dd if=/dev/zero of=/mnt/cache/speed/testfile bs=1G count=3 oflag=direct
3221225472 bytes (3.2 GB, 3.0 GiB) copied, 2.1049 s, 1.5 GB/s

# 读取速度
root@Lisa:~# dd if=/mnt/user/speed/testfile of=/dev/null bs=1G count=3 iflag=direct
3221225472 bytes (3.2 GB, 3.0 GiB) copied, 1.09751 s, 2.9 GB/s
root@Lisa:~# dd if=/mnt/cache/speed/testfile of=/dev/null bs=1G count=3 iflag=direct
3221225472 bytes (3.2 GB, 3.0 GiB) copied, 1.12702 s, 2.9 GB/s
```

# 3、Exclusive shares ⚠️ 

