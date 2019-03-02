---
title: github_not_responding.
date: 2019-02-17 20:19:01
tags:
---

![](/images/blog/190217_github_not_responding/15504060008860.jpg)


![](/images/blog/190217_github_not_responding/15504099678333.jpg)


开启 [Surge 的 Enhanced Mode](https://manual.nssurge.com/others/enhanced-mode.html) 就可以了???
![](/images/blog/190217_github_not_responding/15504100846494.jpg)



# debug 的两种方式: 
虽然这次解决问题了, 但下次还是要找下根因.   
## debug git
```bash
➜  zblog git:(master) ✗ GIT_TRACE=1 gp
21:41:18.099749 git.c:344               trace: built-in: git push
21:41:18.103318 run-command.c:640       trace: run_command: unset GIT_PREFIX; ssh git@github.com 'git-receive-pack '\''daya0576/zblog.git'\'''
Everything up-to-date
```

## debug ssh
```bash
# Debug level 1
GIT_SSH_COMMAND="ssh -v" git clone <repositoryurl>

# Debug level 2
GIT_SSH_COMMAND="ssh -vv" git clone <repositoryurl>

# Debug level 3
GIT_SSH_COMMAND="ssh -vvv" git clone <repositoryurl>
```

