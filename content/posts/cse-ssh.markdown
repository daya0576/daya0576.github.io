---
layout: post
title: "SSH to UNSW CSE Server Without Password"
date: 2016-08-19 21:56:56
comments: true
tags: [cse, unsw]
---

It's so painful to input password every time login to cse server, so this article will show u how to ssh cse server without password.    

<!--more-->


The CSE login servers doc: [http://taggi.cse.unsw.edu.au/FAQ/Accessing_CSE_login_servers/](http://taggi.cse.unsw.edu.au/FAQ/Accessing_CSE_login_servers/)     


##My solution:    
- **Step1:** generate your ssh public key in your own laptop, my favorite tutotial about this step:     
[https://confluence.atlassian.com/bitbucket/set-up-ssh-for-git-728138079.html](https://confluence.atlassian.com/bitbucket/set-up-ssh-for-git-728138079.html)     
- **Step2:** put the public key into `~/.ssh/authorized_keys` in the remote server.     
- **Step3:** Done!!!     
<img style="max-height:300px" class="lazy" data-original="/images/blog/160819_ssh/ssh.png">    

##Another tips: 
- Use sshfs to mount the whole disk to ur own maschine
``` bash
mkdir /tmp/ssh
alias zsshfs='sshfs z5082423@login.cse.unsw.edu.au:/import/adams/2/z5082423 /tmp/ssh'
```

