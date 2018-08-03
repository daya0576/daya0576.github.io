---
layout: post
title: "Mini-project # 6 - Blackjack"
date: 2014-05-16 10:11:18
comments: true
tags: [cousera, study]
---

 《An Introduction to Interactive Programming in Python》

眼泪都要调出来了~~      
图片没加载出来。。
T ^ T   
<!--more-->
![ico_topitme](\images\blog\140516_cousera\2014-05-16_212319.jpg)   
刚看到的时候还是很郁闷的，毕竟付出了好多的心血，结果因为一个不是自身的原因毁掉了。。     
现在还是看开了吧 :) 过去就过去了  无所谓了。

我做的~   
![ico_topitme](\images\blog\140516_cousera\2014-05-16_211654.jpg)

code:   
``` python
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://g.hiphotos.baidu.com/album/pic/item/8b82b9014a90f6039500b4ce3b12b31bb151ed83.jpg?psign=9500b4ce3b12b31bb051f8198618367adbb44aed2f73c9bb")
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://f.hiphotos.baidu.com/album/pic/item/d833c895d143ad4b1c4e6e4980025aafa50f06d2.jpg?psign=1c4e6e4980025aafa40f4bfbfbedab64024f78f0f63622ea")
# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck_cards = None
player_hands = None
deck_hands = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_cards = []
        self.value_card = 0

    def __str__(self):
        hand_str = "Hand contains "
        for card in self.hand_cards:
            hand_str = hand_str + str(card) + " "
        return hand_str

    def add_card(self, card):
        self.hand_cards.append(card)

    def get_value(self):
        value_sum = 0
        Ace_in = False
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        for card in self.hand_cards:
            self.value_card = VALUES[card.get_rank()] 
            value_sum += self.value_card
            if self.value_card == 1:
                Ace_in = True
        
        if Ace_in == False:
            return value_sum
        else:
            if value_sum + 10 < 21:
                return value_sum + 10
            else:
                return value_sum
   
    def draw(self, canvas, pos):
        for card in self.hand_cards:  
            index = self.hand_cards.index(card)
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 10
     
# define deck class 
class Deck:
    def __init__(self):
        self.deck_cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck_cards)

    def deal_card(self):
        card = self.deck_cards[-1]
        self.deck_cards.remove(card)
        return card
    
    def __str__(self):
        deck_str = "Deck contains"
        for card in self.deck_cards:
            deck_str += str(card) + " "       
        return deck_str

#define event handlers for buttons
def deal():
    global outcome, in_play, deck_cards, player_hands, deck_hands, score
    if in_play == True:
        score -= 1
    
    deck_cards = Deck()
    deck_cards.shuffle()
    
    player_hands = Hand()
    player_hands.add_card(deck_cards.deal_card())
    player_hands.add_card(deck_cards.deal_card())
    print str(player_hands)
    
    deck_hands = Hand()
    deck_hands.add_card(deck_cards.deal_card())
    deck_hands.add_card(deck_cards.deal_card())
    print str(deck_hands)
    in_play = True

def hit():
    global outcome, in_play, score, player_hands
    # if the hand is in play, hit the player
    if in_play == True:
        player_hands.add_card(deck_cards.deal_card())
        print "deck_hands.get_value()", deck_hands.get_value()
        if(player_hands.get_value() > 21):
            print  "You have busted"
            outcome = "Busted, you lose~~"
            in_play = False
            score -= 1
            
    print  str(player_hands)
       
def stand():
    global outcome, in_play, score, deck_hands
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while deck_hands.get_value() < 17:
            deck_hands.add_card(deck_cards.deal_card())
            if(deck_hands.get_value() > 21):
                outcome = "Dealer busted, you wine~~"
                in_play = False
                score += 1
        print "deck_hands.get_value()", deck_hands.get_value()
        
        if in_play == True:
            if player_hands.get_value() > deck_hands.get_value():
                outcome = "bigger You win!!!"
                score += 1
            else:
                outcome = "smaller lose~~"
                score -= 1
            in_play = False
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global outcome
    canvas.draw_text('Blackjack', (40, 80), 50, 'Gray', 'serif')
    
    canvas.draw_text("Dealer", (50, 140), 30, 'black', 'serif')
    canvas.draw_text("Player", (50, 290), 30, 'black', 'serif')
    
    canvas.draw_text("score: " + str(score), (450, 90), 30, 'Gray', 'serif')
    
    player_hands.draw(canvas, [50, 300])
    deck_hands.draw(canvas, [50, 150])
    if in_play == True:
        canvas.draw_text("Hit or stand?", (200, 290), 30, 'Gray', 'serif')
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (50+CARD_BACK_CENTER[0], 150+CARD_BACK_CENTER[1]), CARD_BACK_SIZE)
    else:
        canvas.draw_text(outcome, (200, 140), 30, 'Gray', 'serif')
        canvas.draw_text("New deal?", (200, 290), 30, 'Gray', 'serif')
        
    
# initialization frame
frame = simplegui.create_frame("Blackjack~", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric


```