---
layout: post
title: "cousera_Mini-project # 4 - Pong"
date: 2014-04-29 16:27:47
comments: true
tags: [cousera, study, python]
---

《An Introduction to Interactive Programming in Python》

**小游戏~"Pong"   
这次时间还是挺充裕的，但是看英文看的头大，就没按步骤写了   
结果花了更多的时间   还写错了一些    
下次还是认真按步骤写好了

我做的：   
![ico_topitme](\images\blog\140430_cousera\1.png)

改作业改到一个做的好有创意： 评语评了一句碉堡了   
不知道看懂看不懂 哈哈   
![ico_topitme](\images\blog\140430_cousera\2.png)


<!--more-->

可以在[codeskullptor](http://www.codeskulptor.org/)上运行   
code:   
```python
# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [random.randrange(1, 2)*2, random.randrange(-2, 2)+0.5]
    if(direction == "LEFT"):	ball_vel[0] = -ball_vel[0]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle2_vel = 0
    paddle1_vel = 0
    spawn_ball(random.choice(["LEFT", "RIGHT"]))

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle2_vel, paddle1_vel
     
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]      
      
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if(ball_pos[1] + BALL_RADIUS >= HEIGHT or ball_pos[1] - BALL_RADIUS <= 0):
        ball_vel[1] = -ball_vel[1]
        
    # draw paddles
    canvas.draw_polyline([[HALF_PAD_WIDTH, paddle1_pos[1]-HALF_PAD_HEIGHT], 
                          [HALF_PAD_WIDTH, paddle1_pos[1]+HALF_PAD_HEIGHT]], 
                         PAD_WIDTH, 'Red')
    paddle1_pos[1] += paddle1_vel
    
    canvas.draw_polyline([[WIDTH - HALF_PAD_WIDTH, paddle2_pos[1]-HALF_PAD_HEIGHT], 
                          [WIDTH - HALF_PAD_WIDTH, paddle2_pos[1]+HALF_PAD_HEIGHT]], 
                         PAD_WIDTH, 'Red')
    paddle2_pos[1] += paddle2_vel
    
    if paddle1_pos[1] + HALF_PAD_HEIGHT >= HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        paddle1_vel = 0
    if paddle1_pos[1] - HALF_PAD_HEIGHT <= 0:
        paddle1_pos[1] = HALF_PAD_HEIGHT
        paddle1_vel = 0
        
    if paddle2_pos[1] + HALF_PAD_HEIGHT >= HEIGHT:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        paddle2_vel = 0
    if paddle2_pos[1] - HALF_PAD_HEIGHT <= 0:
        paddle2_pos[1] = HALF_PAD_HEIGHT
        paddle2_vel = 0
    
    if(ball_pos[1] < paddle1_pos[1] + HALF_PAD_HEIGHT and
       ball_pos[1] > paddle1_pos[1] - HALF_PAD_HEIGHT and
       ball_pos[0] <=  BALL_RADIUS + PAD_WIDTH):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.2
        ball_vel[1] *= 1.2
    elif(ball_pos[0] <  -1*BALL_RADIUS):
        score2 += 1
        spawn_ball(random.choice(["LEFT", "RIGHT"]))
    
    if(ball_pos[1] < paddle2_pos[1] + HALF_PAD_HEIGHT and
       ball_pos[1] > paddle2_pos[1] - HALF_PAD_HEIGHT and
       ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH):
         
        ball_vel[0] = -ball_vel[0] 
        ball_vel[0] *= 1.2
        ball_vel[1] *= 1.2
    elif(ball_pos[0] >= WIDTH + BALL_RADIUS):
        score1 += 1
        spawn_ball(random.choice(["LEFT", "RIGHT"]))
    # draw scores
    canvas.draw_text(str(score1), [50, 50], 50, 'Blue', 'serif')
    canvas.draw_text(str(score2), [500, 50], 50, 'Blue', 'serif')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 1
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel

def button_handler():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', button_handler, 60)

# start frame
new_game()
frame.start()
```