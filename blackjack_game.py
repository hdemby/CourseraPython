# Mini-project #6 - Blackjack
# coursera link: http://www.codeskulptor.org/#user38_Vxlgdrltci4G7LJ_5.py


import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

def card_to_tuple(card):
    return tuple(card)

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
        self.cards = []	# the cards held : list of [(rank,suit),...]
        self.state = ""	# what the player is doing
        self.value = 0	# current numeric value of the hand
#
    def __str__(self):
        return "cards: "+str(self.cards)+" state: "+str(self.state)+"value: "+str(self.value)
#
    def add_card(self,card):
        self.cards.append(card)	# add a card object to a hand
#
    def set_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for card in self.cards:
            card = card_to_tuple(card)
            value += VALUES[card[0]]
            if card[0]=="A" and value+10 < 21:
                 value += 10
        self.value = value
#
    def get_value(self):
        "return the current value of the hand"
        return self.value
#   
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards

test="""
myhand = Hand(); myhand.cards=[('7C'),('2S'),('5D')]; myhand.set_value(myhand.cards); assert(myhand.get_value() == 14)
myhand = Hand(); myhand.cards=[('AH'),('2H'),('5S')]; myhand.set_value(myhand.cards); assert(myhand.get_value()  == 18)
myhand = Hand(); myhand.cards=[('AH'),('JD')]; myhand.set_value(myhand.cards); assert(myhand.get_value() == 21)
myhand = Hand(); myhand.cards=[('AH'),('AD')]; myhand.set_value(myhand.cards); assert(myhand.get_value() == 12)
print myhand
""" 

  
# define deck class 
class Deck:
    def __init__(self):
        self.state = 0
        self.cards = []
        self.gen_deck()
#
    def gen_deck(self):
        "create a desk of cards"
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(rank+suit)
        self.state = len(self.cards)        
#
    def shuffle(self):
        "shuffle the deck" 
        import random
        random.shuffle(self.cards)
#
    def deal_card(self):
        "deal a card object from the deck"
        return self.deck.pop()
#    
    def __str__(self):
        "return a string representing the deck"
        return str(self.cards)

test="""
mydeck=Deck(); assert(mydeck.state==52)
mydeck.shuffle(); assert(mydeck.state==52)
assert("7C" in mydeck.cards)
print mydeck
"""

# 
def new_game():
    global deck, hand, outcome, in_play
    deck=Deck()
    hand=Hand()
    deck.shuffle()
    in_play = True
    print "Game on" 
    
# define event handlers for buttons
def deal():
    global deck, hand
    hand.add_card(deck.cards.pop())
    
test="""
deck=Deck(); deck.shuffle(); print deal()
hand=Hand()
hand.add_card(deal())
hand.set_value()
while True:
    print hand
    if raw_input("Hit or stand?[H,s] ") in ('s','S'):
        print "Standing with hand >",hand
        break
    else:
        deal()
        hand.set_value()
        if hand.get_value() > 21:
            print "BUST: ",
            print "ended with hand : ",hand
            break
        elif hand.get_value() == 21:
            print "WINNER!! ",
            print "ended with hand > ",hand
            break
"""

def hit():  # player button handler?
    "if the hand is in play, hit the player"
    global outcome, hand, in_play, score
    deal()
    hand.set_value()
    score=hand.get_value()
    # if busted, assign a message to outcome, update 'in_play', score, and start new game
    if score > 21:
        outcome = "!!! BUST !!! "
    # if hand value = '21', assign a message to outcome, start new game
    elif score == 21:
        outcome = "*** PLAYER WINS ***! "
        print outcome
    else:
        print score
    
def stand():  # player button handler?
    global hand, in_play, score   
    score = hand.get_value(hand.set_value())
    in_play = True
    # if hand is in play, dealer plays:
    # repeatedly hit dealer until his hand has value 17 or more:
    hand=Hand()
    deal()
    hand.set_value()
    while in_play:
        score = hand.get_value()
        # No '21' so calculate the winner:
        if score == 21:
            outcome = "*** DEALER WINS ***! "
            print outcome
            in_play = False
        elif score > 17:
            in_play = False
        else:
            deal()
            hand.set_value()
        in_play = True
          
    # if hand value = '21', assign a message to outcome, start new game 
    else:
        in_play = False
        
    # assign a message to outcome, update in_play and score
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
new_game()
#deal()
frame.start()


# remember to review the gradic rubricdef new_game():

    







