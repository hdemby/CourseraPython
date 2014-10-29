import random

# current: http://www.codeskulptor.org/#user38_Vxlgdrltci4G7LJ_2.py

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

## helper functions:
def card_to_tuple(card):
    "return card string as a tuple"
    return len(list(card))==2 and tuple(card) or None
 
test="""
card='7C'; assert(card_to_tuple(card)==('7','C'))
"""     

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
#
    def __str__(self):
        return self.suit + self.rank
#
    def get_suit(self):
        return self.suit
#
    def get_rank(self):
        return self.rank
        
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
    def add_card(self, card):
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

Hand_test="""
myhand = Hand(); myhand.cards=[('7C'),('2S'),('5D')]; myhand.set_value(); assert(myhand.get_value() == 14)
myhand = Hand(); myhand.cards=[('AH'),('2H'),('5S')]; myhand.set_value(); assert(myhand.get_value()  == 18)
myhand = Hand(); myhand.cards=[('AH'),('JD')]; myhand.set_value(); assert(myhand.get_value() == 21)
myhand = Hand(); myhand.cards=[('AH'),('AD')]; myhand.set_value(); assert(myhand.get_value() == 12)
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

Deck_test="""
mydeck=Deck(); assert(mydeck.state==52)
mydeck.shuffle(); assert(mydeck.state==52)
assert("7C" in mydeck.cards)
print mydeck
"""

#define event handlers for buttons
def deal():
    global deck
    return deck.cards.pop()

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
        hand.add_card(deal())
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
    global outcome, hand, inplay, score
    pass	# replace with your code below
 
    # if the hand is in play, hit the player
    if not in_play:
       deal()
    # if busted, assign a message to outcome, update in_play and score
       
def stand():  # player button handler?
    global hand, in_play
    
    player_hand = hand
    in_play = True
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    in_play = False

def new_game():
    global deck, player_hand, dealer_hand, outcome, in_play
    deck=Deck()
    deck.shuffle()
    in_play = True
    





    







