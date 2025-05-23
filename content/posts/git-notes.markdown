---
layout: post
title: "Notes of Atlassian git tutorial"
date: 2016-07-05 14:18:24
comments: true
tags: [git, study]
---

Although we have powerful tools such as sourcetree,    
learning the details of git is still very necessary.    
I found a fantastic tutorial:[https://www.atlassian.com/git/tutorials](https://www.atlassian.com/git/tutorials), this is my learning notes.   

<!--more-->
  

###git log vs git status###
`git log`: showing all the comments in this branch    
`git status`: showing the overview of this branch   


###Show commits in graph###
draw a graph of all comments:    
``` 
git log --graph --decorate --oneline    
```
<img style="max-height:400px" src="/images/blog/160705_git/graph.png">    
 

###git diff###
- Using "git diff" to compare two commits.   
<img style="max-height:330px" src="/images/blog/160705_git/diff.png">   


###Undoing Changes###
- **"git add <file>..."** to update what will be committed(stage changes)       
**"git reset <file>"** to remove the specified file from the staging area, but **leave the working directory unchanged**.)     

- "git revert <commit>" to generate a new commit that undoes all of the changes introduced in <commit>, then apply it to the current branch.    

"Whereas reverting is designed to safely undo a public commit, git reset is designed to undo local changes."     
<img style="max-height:430px" src="/images/blog/160705_git/redo.svg">   


"The `git reset --hard` and `git clean -f` commands are your best friends after you’ve made some embarrassing developments in your local repository and want to burn the evidence."    
Example:    
``` python
# Edit some existing files
# Add some new files
# Realise you have no idea what you're doing

# Undo changes in tracked files
git reset --hard

# Remove untracked files
git clean -df
```



###Rewriting history###
git commit --amend:   
``` python
# Edit hello.py and main.py
git add hello.py
git commit

# Realise you forgot to add the changes from main.py
git add main.py
git commit --amend --no-edit
```


###Difference of git fetch and git pull###
`git pull` = `git fetch` followed by a `git merge`(remote branch).    
Still a little confused.    
这篇文章解释的很清楚：[http://www.ruanyifeng.com/blog/2014/06/git_remote.html?20160711102657](http://www.ruanyifeng.com/blog/2014/06/git_remote.html?20160711102657)    
'fetch' is updating the remote branch info, then local branch merge to remote branch !!    



###git set defaul remote to push ###
Edit your .git/config    
```
[branch "master"]
  remote = origin
  merge = refs/heads/master
```



### merge conflict ###
Automatic merge failed; fix conflicts and then commit the result.     
`Try: git mergetool`
