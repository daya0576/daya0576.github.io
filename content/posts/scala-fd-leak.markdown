---
title: Troubleshooting Scala File Descriptor Leaks
date: 2024-02-24 15:49:27
categories:
- SRE
tags:
---

Recently, we discovered some unexpected autoscaling EC2_INSTANCE_TERMINATE events in our Scala system: "instance was taken out of service in response to an ELB system health check failure".

After checking the error logs, the issue was caused by `Too many open files`, which leaded to unsuccessful DNS resolution, consequently resulting in errors when accessing the AWS endpoint, finally causing the server to hang.

<!--more-->

# Troubleshooting
Luckily, we can still log in to the instance. From the following command, you can see that the system's maximum file descriptor (fd) limit is 65534, while soft and hard limits applying to the process are both 4096.
```
[root@ecsxxx ~]# ulimit -n
65534

[root@ecsxxx ~]# cat /proc/1485/limits
Limit                     Soft Limit           Hard Limit           Units
Max open files            4096                 4096                 files
```

Apart from system libraries and JAR files, there are fd leaks where even after deleting a directory, the process still maintains **read access to that directory**.

For example:
```
[root@ecsxxx ~]# lsof -p 1485 -a -d 1589
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF     NODE NAME
java    1485 root 1589r   DIR  259,1        6 23511394 /mnt/f303d707-24e0-434e-a7e1-93a2612e3240 (deleted)
```

As it is related to the `/mnt` folder, it may be suspected that the issue lies in the Foo code. However, the code only list/read/delete files of the directory, <u>how can it lead to an fd leak???</u>

---

Wait a minute, let's seek help from chatGPT: "In Scala, file descriptor leak of reading directory".

```scala
One way to cause a file descriptor leak in Scala involving a read directory is to not properly close the Stream after reading the directory content. Here’s an example code that illustrates this issue:

import java.nio.file.{Files, Paths}

object FileDescriptorLeakExample {

  def readDirectory(path: String): Unit = {
    val files = Files.list(Paths.get(path))
    
    files.forEach(file => {
      // Reading the file content
      println(s"Reading file: ${file.getFileName}")
    })
    
    // Not closing the stream
  }

  def main(args: Array[String]): Unit = {
    val directoryPath = "/path/to/directory"
    readDirectory(directoryPath)
    
    // Deleting the directory after reading it
    val directory = Paths.get(directoryPath)
    Files.delete(directory)
  }
}

In this code snippet, the readDirectory function reads the content of a directory using the Files.list method but does not close the Stream returned by this method. As a result, the file descriptor associated with the directory remains open even after the directory has been deleted in the main method. This can cause a file descriptor leak because the process still maintains read access to the directory.

To prevent this type of file descriptor leak, it is essential to close the Stream returned by Files.list method after using it. Adding a files.close() call at the end of the readDirectory function can help release the file descriptor and avoid the leak.
```

The answer above is 100% correct. `java.nio.file.Files#list` is a Java code referenced in our Scala code. This method returns a "lazy" stream, which I guess is holding the file descriptor all the time. 

The fd will only be closed with:
- Internal exception
- try-with-resources construct
- Manually call `stream.close()`

Unfortunately, our code did not use any of them, causing a file descriptor leak. 

A simple reproducible scala code:
```scala
val path = Paths.get("/tmp/test_fd")
val stream = Files.list(path)
Thread.sleep(1.hour.toMillis);
// stream.close();
```

![C95E36ED-116F-4BDF-8133-1652B0E2721C_1_201_a](../images/blog/2021-09-04-jvm-note/C95E36ED-116F-4BDF-8133-1652B0E2721C_1_201_a.jpeg)


# What happens inside `Files#list`?

Java Source code: [java/nio/file/Files.java#L3450](https://github.com/JetBrains/jdk8u_jdk/blob/94318f9185757cc33d2b8d527d36be26ac6b7582/src/share/classes/java/nio/file/Files.java#L3450)
```java
public static Stream<Path> list(Path dir) throws IOException {
    DirectoryStream<Path> ds = Files.newDirectoryStream(dir);
    ...

// sun.nio.fs.UnixFileSystemProvider#newDirectoryStream
long ptr = opendir(dir);

// sun.nio.fs.UnixNativeDispatcher#opendir0
return opendir0(buffer.address());

// native method
private static native long opendir0(long pathAddress) throws UnixException;
```

JVM Source code: [src/solaris/native/sun/nio/fs/UnixNativeDispatcher.c#L654](https://github.com/JetBrains/jdk8u_jdk/blob/94318f9185757cc33d2b8d527d36be26ac6b7582/src/solaris/native/sun/nio/fs/UnixNativeDispatcher.c#L654)
```c
/* src/solaris/native/sun/nio/fs/UnixNativeDispatcher.c */
JNIEXPORT jlong JNICALL
Java_sun_nio_fs_UnixNativeDispatcher_opendir0(JNIEnv* env, jclass this,
    jlong pathAddress)
{
    DIR* dir;
    const char* path = (const char*)jlong_to_ptr(pathAddress);

    /* EINTR not listed as a possible error */
    dir = opendir(path);
    if (dir == NULL) {
        throwUnixException(env, errno);
    }
    return ptr_to_jlong(dir);
}
```

C Standard Library: eventually `opendir` trigger system call `openat`
![](../images/blog/2021-09-04-jvm-note/17087608145598.jpg)
