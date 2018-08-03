---
layout: post
title: "cousera作业_Guess the number"
date: 2014-04-14 21:03:09 +0800
comments: true
tags: [study, python, cousera]
---


>  《An Introduction to Interactive Programming in Python》

**哎   半夜把第三周的大作业写完了     差点来不及  ** 
   
<!--more-->

一个二分法猜数字的小游戏       都给出提示了    照着写就行了   
可是用的是codeskullptor，还要翻个墙    心酸。

```python
# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code
secret_number = 0
remain = 0


# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    
    print "New game. Range is from 0 to 100"
    print "Number of remaining guesses is 7"
    
    global secret_number, remain
    secret_number = random.randrange(0, 100)
    remain = 7
    print 


def range1000():
    # button that changes range to range [0,1000) and restarts
    
    print "New game. Range is from 0 to 1000"
    print "Number of remaining guesses is 10"
    
    global secret_number, remain
    secret_number = random.randrange(0, 1000)
    remain = 10
    print
    
# helper function to start and restart the game
def new_game():
     range100()
    
    
def input_guess(guess):
    # main game logic goes here	
    global remain
    print "Guess was " + guess
    
    
    guess = int(guess)
    if guess > secret_number:
        print "Lower!"
    elif guess < secret_number:
        print "Higher!"
    else:
        print "Correct!\n"
        new_game()
    remain = remain - 1
    print "Number of remaining guesses is %d"%(remain) 
    
    if remain == 0:
        print "sorry u run out of range, the num is %d"%secret_number
        new_game()
        
    print
        

# Handler to draw on canvas
def draw(canvas):
    canvas.draw_text(message, [50,112], 48, "Red")
    
    
# create frame
f = simplegui.create_frame("Home", 300, 200)


# register event handlers for control elements
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game and start frame
f.start()
new_game()


# always remember to check your completed program against the grading rubric

```