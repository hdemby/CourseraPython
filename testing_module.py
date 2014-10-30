DEBUG=0

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
        for card in self.cards:
            if card[0]=='A' and (value+10) <= 21:
                 value+=10
        self.value = value
#
    def get_value(self):
        "return the current value of the hand"
        return self.value
#   
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards

def do_test(tests):
    for test in tests.split("\n"):
        if DEBUG: print test
        parts=test.split(";")
        try:
            for part in parts:
                exec(part.strip())
        except AssertionError:
            print "*** Test failed:\n", test,
            print " : got -",myhand.get_value()

tests="""
myhand = Hand(); myhand.cards=[('7C')]; myhand.set_value(); assert(myhand.get_value() == 7)
print myhand
myhand = Hand(); myhand.cards=[('7C'),('2S')]; myhand.set_value(); assert(myhand.get_value() == 9)
print myhand
myhand = Hand(); myhand.cards=[('AH'),('JD')]; myhand.set_value(); assert(myhand.get_value() == 21)
print myhand
myhand = Hand(); myhand.cards=[('AH'),('AD')]; myhand.set_value(); assert(myhand.get_value() == 12)
print myhand
myhand = Hand(); myhand.cards=[('AH'),('AD'),('9D')]; myhand.set_value(); assert(myhand.get_value() == 11) # is wrong
print myhand
myhand = Hand(); myhand.cards=[('7C'),('2S'),('5D')]; myhand.set_value(); assert(myhand.get_value() == 14)
print myhand
myhand = Hand(); myhand.cards=[('AH'),('2H'),('5S')]; myhand.set_value(); assert(myhand.get_value()  == 18)
print myhand
myhand = Hand(); myhand.cards=[('AH'),('AD'),('AC'),('AS')]; myhand.set_value(); assert(myhand.get_value() == 14)
print myhand
myhand = Hand(); myhand.cards=[('AH'),('AD'),('AC'),('AS'),('JD')]; myhand.set_value(); assert(myhand.get_value() == 14)
print myhand
myhand = Hand(); myhand.cards=[('AH'),('AD'),('AC'),('AS'),('JD'),('7S')]; myhand.set_value(); assert(myhand.get_value() == 21)
print myhand
myhand = Hand(); myhand.cards=[('JH'),('AD'),('AC'),('AS'),('AD')]; myhand.set_value(); assert(myhand.get_value() == 14)
print myhand

""" 

