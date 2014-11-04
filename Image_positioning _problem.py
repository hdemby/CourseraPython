# Image positioning problem

###################################################
# Student should enter code below

import simplegui

# global constants
WIDTH = 400
HEIGHT = 300

# load test image
# 95x93
asteroid="http://commondatastorage.googleapis.com/codeskulptor-assets/asteroid.png"

def init():
    global draw_cntr
    draw_cntr=[WIDTH/2, HEIGHT/2]

# mouseclick handler
def click(pos):
    global draw_cntr
    draw_cntr=pos
    
# draw handler
def draw(canvas):
    global draw_cntr
    roid_cntr=[95/2,93/2]
    canvas.draw_image(image,roid_cntr,[95,93],draw_cntr,[95,93])
    
# create frame and register draw handler    
frame = simplegui.create_frame("Test image", WIDTH, HEIGHT)
frame.set_canvas_background("Gray")
image=simplegui.load_image("%s"%asteroid)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)

# start frame
init()
frame.start()
        
