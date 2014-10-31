# Mini-project #6 - Blackjack
# coursera link: http://www.codeskulptor.org/#user38_Vxlgdrltci4G7LJ_8.py

# almost working but withou proper 'Card' object:
# http://www.codeskulptor.org/#user38_WaqPe0IJoc_0.py
# http://www.codeskulptor.org/#user38_hJfKtRWpcnuhJzT_1.py
# http://www.codeskulptor.org/#user38_hJfKtRWpcnuhJzT_6.py : mostly working
# http://www.codeskulptor.org/#user38_hJfKtRWpcnuhJzT_8.py : basic card display working
# http://www.codeskulptor.org/#user38_hJfKtRWpcnuhJzT_15.py : See below
# http://www.codeskulptor.org/#user38_hJfKtRWpcnuhJzT_48.py : Final! (See below)

# Mini-project #6 - Blackjack

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
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

DEBUG=0

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
        #print str(self.suit) + str(self.rank)
        suit=str(self.get_suit())
        rank=str(self.get_rank())
        return  suit+rank

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
            #card = card_to_tuple(card.rank,card.suit) # (card)
            value += VALUES[card.get_rank()]
            #value += VALUES[card[0]]
        for card in self.cards:
            if card.get_rank()=='A' and (value+10) <= 21:
                 value+=10
        self.value = value
#
    def get_value(self):
        "return the current value of the hand"
        return self.value
#   
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards
#
    def __str__(self):
        return str(" ".join("%s"%s for s in self.cards)+" | %s"%self.value)

# define deck class 
class Deck:
    def __init__(self):
        self.state = 0
        self.cards = []
        self.gen_deck()
        if DEBUG: print "new deck"
#
    def gen_deck(self):
        "create a desk of cards"
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank)) #(rank+suit)
        self.state = len(self.cards)        
#
    def shuffle(self):
        "shuffle the deck" 
        import random
        if DEBUG: print "shuffled..."
        random.shuffle(self.cards)
#
    def deal_card(self):
        "deal a card object from the deck"
        return self.deck.pop()
#    
    def __str__(self):
        "return a string representing the deck"
        return str(self.cards)

def new_game():
    global deck, in_play, outcome, player_points, dealer_points    # player_hand, dealer_hand
    if DEBUG: print "\n\n*** New Game - click 'Deal' to start *** "
    ## generate a new deck"
    deck=Deck()
    deck.shuffle()
    ## set idle condition
    in_play = True		# use to expose/hide dealer card
    if DEBUG: print "in_play in 'new_game': ", in_play

## define helper functions:
def eval_hand(hand):
    #hand.set_value()
    value=int(hand.get_value())
    if value == 21:
        output = "21"
    elif value > 21:
        output = "bust"
    else:
        output = ""
    return value,output   

# define event handlers for buttons
def deal():
    """Issue first two cards to player and dealer with dealers 2nd unexposed"""
    global deck, player_hand, dealer_hand, outcome, in_play, player_points, dealer_points
    ## clear screen output
    outcome=""
    in_play = False		# use to expose/hide dealer card
    if DEBUG: print "in_play in 'deal': ", in_play
    ## clear the hands for the player and dealer
    player_hand=Hand()  # reset player hand
    dealer_hand=Hand()	# reset dealer hand
    if DEBUG: print "dealing.. "
    givecards = 2
    for givecards in [0,1]:
        player_hand.add_card(deck.cards.pop())
        dealer_hand.add_card(deck.cards.pop())
        givecards-=1
    if DEBUG: print "Dealer hand\: "
    if DEBUG: print dealer_hand.cards[0],"??"
    if DEBUG: print "Player hand\: "
    if DEBUG: print player_hand.cards[0],player_hand.cards[1],
    ## start player turn:
    player_hand.set_value()
    result,output = eval_hand(player_hand)
    if output == "21":
        outcome = " ** Player has '21'! Player Wins! ** "
        player_points+=1
        if DEBUG: print " ** Player has '21'! Player Wins! ** "
        get_winner() #new_game()
    elif output == "bust":
        outcome = " ** Player Bust! Dealer Wins! ** "
        if DEBUG: print " ** Player Bust! Dealer Wins! ** "
        dealer_points+=1    
        get_winner() #new_game()
    else:
        pass        

def hit():  # player 'hit' button handler?
    "if the hand is in play, hit the player"
    global player_hand, in_play, outcome, player_points, dealer_points
    player_hand.add_card(deck.cards.pop())
    if DEBUG: print player_hand.cards[-1],
    player_hand.set_value()
    result,output = eval_hand(player_hand)
    if output == "21":
        outcome = " ** Player has '21'! Player Wins! ** "
        player_points+=1
        if DEBUG: print " ** Player has '21'! Player Wins! ** "
        get_winner() #new_game()
    elif output == "bust":
        outcome = " ** Player Bust! Dealer Wins! ** "
        dealer_points+=1
        if DEBUG: print " ** Player Bust! Dealer Wins! ** "
        get_winner() #new_game()
    else:
        pass        
        
def stand():  # player 'stand' button handler?
    global dealer_hand, player_hand, in_play, outcome, player_points, dealer_points
    
    in_play = True		# flip the dealer card
    if DEBUG: print "in_play in 'stand' :", in_play
    if DEBUG: print "\nPlayer Stands..."
    if DEBUG: print player_hand
    ## player is finished. 
    ## start 'Dealer play':
    ## repeatedly hit dealer until his hand has value 17 or more:
    if DEBUG: print "\nDealer:"
    if DEBUG: print dealer_hand.cards[0],dealer_hand.cards[1],
    dealer_hand.set_value()
    result,outcome = eval_hand(dealer_hand)
    while result < 17:    
        dealer_hand.add_card(deck.cards.pop())
        if DEBUG: print dealer_hand.cards[-1],
        dealer_hand.set_value()
        result,output = eval_hand(dealer_hand)
        if output=="21":
            if DEBUG: print " \n** Dealer has '21'! Dealer Wins! ** "
            outcome = " ** Dealer has \'21\'! Dealer Wins! ** "
            dealer_points+=1
            get_winner() #new_game()
        elif output=="bust":
            if DEBUG: print " \n** Dealer Bust! Player Wins! ** "
            outcome = " ** Dealer Bust! Player Wins! ** "
            player_points+=1
            get_winner() #new_game()
        else:
            pass
    ## dealer has 17 or more so must stop    
    if DEBUG: print "\nDealer Stands... "
    if DEBUG: print dealer_hand            
    get_winner()

def get_winner():
    global player_hand, dealer_hand, outcome, player, dealer, in_play
    global player_points, dealer_points
    # Nobody has '21' so calculate the winner:
    if DEBUG: print "in_play in 'winner': ", in_play
    player = player_hand.get_value()
    dealer = dealer_hand.get_value()
    # assign a message to outcome, update in_play and score
    if outcome=="":
        if player > dealer:
           outcome = " *** PLAYER WINS *** "
           player_points+=1
        elif player < dealer:
           outcome = " *** DEALER WINS *** "
           dealer_points+=1
        else:
           outcome = " *** Tie: DEALER WINS *** "
           dealer_points+=1 
    if DEBUG: print outcome
    new_game()

# draw handler    
def draw(canvas):
    global player_hand, dealer_hand, outcome, in_play
    global player_points, dealer_points
    # test to make sure that card.draw works, replace with your code below

    dealer_score = str(dealer_hand.get_value())
    player_score = str(player_hand.get_value())
    player_pos = [200,300]
    shft = 25
    try:
        pos = [100-shft,400]  ## player tray
        for card in player_hand.cards:
            place = player_hand.cards.index(card)
            card.draw(canvas, [pos[0]+place*CARD_SIZE[0], pos[1]])
        pos = [100-shft,200]  ## dealer tray
        for card in dealer_hand.cards:
            place = dealer_hand.cards.index(card)
            card.draw(canvas, [pos[0]+place*CARD_SIZE[0], pos[1]])
        if in_play == False :
            crdcntr=[144/4,96/2]  # 144x96 - two cards
            canvas.draw_image(card_back,crdcntr,[144/2,96],[208-shft,248],[144/2,96])
  
        ## screen static decorations  
        canvas.draw_text("BlackJack",[200,100],48,"yellow")
        canvas.draw_text("Dealer",[75,180],24,"yellow")
        canvas.draw_text("Player",[75,380],24,"yellow")
        canvas.draw_text("Hand Score",[425,185],20,"black")
        canvas.draw_text("Hand Score",[425,385],20,"black")
        canvas.draw_text("Wins",[5,225],24,"black")
        canvas.draw_text("Wins",[5,425],24,"black")
        
        ## dynamic messages  
        canvas.draw_text(outcome,[125,340],24,"white")
        
        canvas.draw_text(dealer_score,[470,250],28,"yellow")
        canvas.draw_text(player_score,[470,450],28,"yellow")
        canvas.draw_text(str(dealer_points),[20,250],22,"black")
        canvas.draw_text(str(player_points),[20,450],22,"black")
    except: 
        pass
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
in_play=False
player_hand=Hand()
dealer_hand=Hand()
player_points = 0
dealer_points = 0

new_game()
deal()
frame.start()


# remember to review the gradic rubricdef new_game():



