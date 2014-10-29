import random
import simplegui

CANVAS_WIDTH = 800
CANVAS_HEIGHT= 100
CARD_VALUES = range(8)

DEBUG=0
 
picked = []
turns = 0

def gen_print_cards():
    global boxes
    #[[w/2+(n*w),0], [w/2+(n*w),h]]
    w=CANVAS_WIDTH/(len(CARD_VALUES*2))
    h=CANVAS_HEIGHT
    boxes=[]
    #print CARD_VALUES
    for n in range(len(CARD_VALUES)*2):
        boxes.append([[w/2+(n*w)-2,0], [w/2+(n*w)-2,h-1]])
    for s in boxes:
        if DEBUG: print s
        
def gen_card_ranges():
    global ranges
    #[1+(n*20),1+(n*20)+w-2],  y:[0,h]
    w=CANVAS_WIDTH/(len(CARD_VALUES*2))
    h=CANVAS_HEIGHT
    ranges=[]
    for n in range(len(CARD_VALUES*2)):
        ranges.append([[1+(n*w),1+(n*w)+w-2],[0,h-1]])
    for s in ranges:
        if DEBUG: print s
    
def gen_deck_values():
    global deck
    deck=CARD_VALUES+CARD_VALUES
    random.shuffle(deck)
    if DEBUG: print deck

##============
## game setup:
##============
def new_game():
    gen_print_cards()
    gen_card_ranges()
    gen_deck_values()
    reset()

def reset():
    global turns, picked, states, points, gameis
    turns = 0
    points = 0
    picked = []
    gameis = ""
    states=[int(s) for s in "0"*len(CARD_VALUES)*2]

##===========
## game play:
##===========
## determine the card picked by mouse pointer location:
def get_card_clicked(pos):
    global card,ranges
    w=CANVAS_WIDTH/(len(CARD_VALUES*2))
    h=CANVAS_HEIGHT
    for n in range(len(boxes)):
        if pos[1] in range(h):
            if DEBUG: print ranges[n][0],ranges[n][1]
            start=ranges[n][0][0]
            stop=ranges[n][0][1]
            if pos[0] in range(start,stop):
                if DEBUG: print "ranges(n):",ranges[n]                             
                if DEBUG: print "card:",n," range: ",start,stop
                return n
    return    

## respond to the mouse click; evaluate result:
def click(pos):
    global card, deck, states, picked, turns, points, gameis
    
    card = get_card_clicked(pos)
    if DEBUG: print "mouse position: ",pos
    if card >= 0:
        states[card]=1
        if DEBUG: print "card: ",card,": value: ",deck[card]
        picked.append(card)
        if DEBUG: print "picked: ",picked
        states[card]=1
        if DEBUG: print 'state',states
        if len(picked)==2:
            turns+=1
            if DEBUG: print "c1,v1:c2,v2",picked[0],deck[picked[0]],":",picked[1],deck[picked[1]]
            if deck[picked[0]]==deck[picked[1]]:
                points += 1
                if DEBUG: print "match!!"
                if DEBUG: print picked[0],picked[1]
                states[picked[0]] = 2
                states[picked[1]] = 2
                if DEBUG: print "new state: ",states
                if points==len(CARD_VALUES):
                    gameis = " !! Game Over !!"
            else:
                if DEBUG: print "no match"
        elif len(picked)==3:
            picked = picked[-1:]
            reset=[]
            for each in states:
                if each==2:
                    reset.append(each)
                else:
                    reset.append(0)
            turns += 1
            if DEBUG: print "reset state:",reset
            states=list(reset)
            states[card]=1
        else:
            pass
             
##=================
## game graphics:
##=================      
def draw(canvas):
    global boxes, deck, state, turns, gameis
    for n in range(len(boxes)):
        box_x,box_y = boxes[n]
        #if DEBUG: print deck[n]
        #if DEBUG: print box_x, box_y
        width=CANVAS_WIDTH/(len(CARD_VALUES)*2)
        #if DEBUG: print n
        #if DEBUG: print states[n]
        if states[n] > 0:
            d=n*width+width/4
            #canvas.draw_text('A', (20, 20), 12, 'Red')
            canvas.draw_text(str(deck[n]),(d+box_x[1]/2,box_y[1]/1.75),42,"white")
        else:
            canvas.draw_line(box_x,box_y, width-2, 'green')
        turns_taken.set_text("Turns: " + str(turns) + gameis)

    
frame=simplegui.create_frame("card pick test",CANVAS_WIDTH,CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
frame.add_button("reset",new_game)
frame.add_button("Retry",reset)
turns_taken = frame.add_label("Turns: ")
new_game()
frame.start()


