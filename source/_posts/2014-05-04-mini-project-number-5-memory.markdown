---
layout: post
title: "Mini-project#5-Memory"
date: 2014-05-04 14:03:07
comments: true
tags: [cousera, study, python]
---

 《An Introduction to Interactive Programming in Python》

差点来不及了   心都碎了    
deadline是一点钟。。 还没写完就交了个半成品 心都碎了    
但是偷偷把本地的时间改早了40分钟，竟然成功地把deadlin延迟了   
好开心  哈哈哈哈哈哈![哈哈](http://i3.dpfile.com/s/img/editor/Emoticon68.gif)

一个翻牌的游戏 考记忆力 直戳我的软肋呀 哈哈    
我做的：   
（一看以为是女生做的一定会多给分吧 直戳程序员的软肋![阴笑](http://ctc.qzonestyle.gtimg.cn/qzone/em/e151.gif?max_age=2592000)）
![ico_topitme](\images\blog\140504_cousera\1.png)

TT吃饭去了   饿的手指都颤抖了![饿](http://i3.dpfile.com/s/img/editor/Emoticon89.gif)
<!--more-->

code：http://www.codeskulptor.org/#user31_5R1CHSudUHFWeJg.py
```python
# implementation of card game - Memory

import simplegui
import random

state = 0
tures = 0
before1 = -1
before2 = -1
list_word = range(8)
list_word = list_word + list_word


list_word_exposed = []
for i in range(16):
    list_word_exposed.append(False)

def clear_exposion():
    global list_word_exposed
    for i in range(16):
        list_word_exposed[i] = False

def win():
    win = 0
    for i in range(16):
        if list_word_exposed[i] == True:
            win += 1
    if win >= 16:
        return True
    else:
        return False
    
        
# helper function to initialize globals
def new_game():
    global state, list_word
    random.shuffle(list_word)
    clear_exposion()
    state = 0
    before = None
    tures = 0
     
# define event handlers
def mouseclick(pos):
    global state, tures, list_word_exposed, before
    click = pos[0] // 50
    global state
    
    if list_word_exposed[click] == False:
        global before1, before2
        if state == 0:
            before1 = click
            print "before1", before1
            state = 1
        elif state == 1:
            before2 = click
            print "before2", before2
            state = 2
        else:
            tures += 1
            if not list_word[before1] == list_word[before2]:
                list_word_exposed[before2] = False
                list_word_exposed[before1] = False
                
            before1 = click
            print "before1", before1
            label.set_text("Tures = " + str(tures))
            state = 1
        list_word_exposed[click] = True
                                
# cards are logically 50x100 pixels in size    
def draw(canvas):
    if win() and not state == 0:
        canvas.draw_text("YOU WIN!!!! haha :)", (5, 80), 80, 'white', 'serif')
    else:  
        for index, word in enumerate(list_word):
            canvas.draw_text(str(word), (index * 50 + 5, 80), 80, 'white', 'serif')
        for index, exposed in enumerate(list_word_exposed):
            if(not exposed and index % 2 == 0):
                canvas.draw_polygon([[index * 50 + 30, 3], [index * 50 + 20, 95]], 50, 'pink')
            elif(not exposed and index % 2 == 1):
                canvas.draw_polygon([[index * 50 + 30, 3], [index * 50 + 20, 95]], 50, 'white')
            

def button_handler():
    new_game()
    
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
```