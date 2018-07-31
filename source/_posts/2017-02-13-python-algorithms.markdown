---
layout: post
title: "那些年 用python刷过的面试算法题"
date: 2017-02-13 15:32:09 +1100
comments: true
categories: [python, interview]
---

准备面试的过程中用Python写了一些的算法题, 用这篇日志记录一下.       

<!--more-->
  

##fibonacci数组:    
[/blog/20160915/dynamic-programming/](/blog/20160915/dynamic-programming/)    


##Generating all possible permutations of a list
生成一个列表的所有组合.    
1.The feeling of completing an algorithm with only one error, awesome.         
```python
def permutation(ABC, len_fix):
    if len_fix == len(ABC)-1:
        print(ABC)
    else:
        for i in range(len(ABC)-len_fix):
            part1, part2 = ABC[:len_fix], ABC[len_fix:]
            part2[i], part2[0] = part2[0], part2[i]
            permutation(part1+part2, len_fix+1)

ABC = [0, 1, 2, 3]
permutation(ABC, 0)
```
2.Python buildin method:
``` python
>>> horses = [1, 2, 3, 4]
>>> races = itertools.permutations(horses)
>>> print(races)
<itertools.permutations object at 0xb754f1dc>
>>> print(list(itertools.permutations(horses)))
[(1, 2, 3, 4),
 (1, 2, 4, 3),
...
 (4, 3, 1, 2),
 (4, 3, 2, 1)]
```





> 本来是想刷一遍leecode, 但算法题有四百多题..刷了三四题就放弃了    
接下来的一些算法题是剑指offer里的:
[https://www.nowcoder.com/ta/coding-interviews?query=&asc=false&order=submissionCount&page=1](https://www.nowcoder.com/ta/coding-interviews?query=&asc=false&order=submissionCount&page=1  )    


## 输入一个链表，从尾到头打印链表每个节点的值.
```python
# -*- coding:utf-8 -*-
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    # 返回从尾部到头部的列表值序列，例如[1,2,3]
    def printListFromTailToHead(self, listNode):
        # write code here

        if listNode is None:
            return []
        else:
            result = [listNode.val]

        while listNode.next:
            result.append(listNode.next.val)
            listNode = listNode.next

    	return result[::-1]
```

## 反转链表
```python
# -*- coding:utf-8 -*-
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None
class Solution:
    def ReverseList(self, pHead):
        if pHead is None or pHead.next is None:
            return pHead

        h = self.ReverseList(pHead.next)

        # reverse the linked list, except last one(because of return).
        pHead.next.next = pHead
        # head set null
        pHead.next = None

        return h
```

## 合并两个有序的链表
```python
class Solution:
    def Merge(self, pHead1, pHead2):
        if pHead1 is None: return pHead2
        if pHead2 is None: return pHead1

        if pHead1.val < pHead2.val:
            pHead1.next = self.Merge(pHead1.next, pHead2)
            head = pHead1
        else:
            pHead2.next = self.Merge(pHead1, pHead2.next)
            head = pHead2

        return head
```

## 生成二叉树的镜像
```python
# -*- coding:utf-8 -*-
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Solution:
    # 返回镜像树的根节点
    def Mirror(self, root):

        if root:
            root.left, root.right = self.Mirror(root.right), self.Mirror(root.left)

        return root
```

## 输入两棵二叉树A，B，判断B是不是A的子结构。
```python
# -*- coding:utf-8 -*-
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Solution:
    def HasSubtree(self, pRoot1, pRoot2):
        if pRoot1 is None or pRoot2 is None:
            return False
        elif self.is_subtree(pRoot1, pRoot2):
            return True
        else:
            return self.HasSubtree(pRoot1.left, pRoot2) or self.HasSubtree(pRoot1.right, pRoot2)

    def is_subtree(self, pRoot1, pRoot2):
        if pRoot2 is None:
            return True

        elif pRoot1 and pRoot2 and pRoot1.val == pRoot2.val:
            return self.is_subtree(pRoot1.left, pRoot2.left) and self.is_subtree(pRoot1.right, pRoot2.right)
        else:
            return False


# t1 = TreeNode(1)
# t1.left = TreeNode(1)
# t1.left.right = TreeNode(3)
# t1.left.left = TreeNode(2)
#
#
# t2 = TreeNode(1)
# t2.left = TreeNode(2)
# t2.right = TreeNode(3)
# # t2.left.left = TreeNode(4)
#
#
# print(Solution().is_sametree(t1, t2))
# print(Solution().HasSubtree(t1, t2))
```

## 一层一层打印二叉树
```python
# -*- coding:utf-8 -*-
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Solution:
    # 返回从上到下每个节点值列表，例：[1,2,3]
    def PrintFromTopToBottom(self, root):
        result = []

        nodes_in_level = [root] if root else []
        while nodes_in_level:
            nodes_in_next_level = []
            for node in nodes_in_level:
                result.append(node.val)
                nodes_in_next_level.append(node.left)
                nodes_in_next_level.append(node.right)

            nodes_in_level = [node for node in nodes_in_next_level if node]

        return result



# t1 = TreeNode(1)
# t1.left = TreeNode(1)
# t1.left.right = TreeNode(3)
# t1.left.left = TreeNode(2)
#
# print(Solution().PrintFromTopToBottom(t1))
```

## 栈的压入弹出序列  
```python
# -*- coding:utf-8 -*-

# 输入两个整数序列，第一个序列表示栈的压入顺序, 请判断第二个序列是否为该栈的弹出顺序。
# 假设压入栈的所有数字均不相等。
# 例如序列1,2,3,4,5是某栈的压入顺序，序列4，5,3,2,1是该压栈序列对应的一个弹出序列，但4,3,5,1,2就不可能是该压栈序列的弹出序列。（注意：这两个序列的长度是相等的）

class Solution:
    def IsPopOrder(self, pushV, popV):
        if pushV and popV and set(pushV) == set(popV):
            l = [pushV.pop(0)]

            while popV:
                # False
                if popV[0] in l[:-1]:
                    return False

                # 1. push
                elif pushV and l[-1] != popV[0]:
                    l.append(pushV.pop(0))

                # 2. pull
                else:
                    l.pop()
                    popV.pop(0)

            return True
        else:
            return False
```
