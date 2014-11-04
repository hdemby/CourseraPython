DEBUG=0

##==========================================
## Test Module
##==========================================

def do_test(tests):
    for test in tests.split("\n"):
        if DEBUG: print test
        parts=test.split(";")
        try:
            for part in parts:
                exec(part.strip())
        except AssertionError:
            print "*** Test failed:\n", test,

##==========================================
## Application code
##==========================================

## modeling ship drive and rotation math
##  

class Ship:
    def __init__(self,image,pos,vel,angle,thrust):
        self.image=image
	self.pos=pos		# point  ; += velocity
	self.vel=vel    	# vector ; += accel
	self.accel=accel	# vector ; +=[cos(angle),sin(angle)* const
	self.angle		# scalar
#
    def __str__(self):
        return self.image
#
    def draw(self):
        ## implements 'canvas.draw_image(image,img_cntr,img_siz,frm_cntr,frm_siz,angle)'

	pass

tests="""
myship=Ship("viper.png",[100,100],[1,1],[.1,.1],45); assert(myship.image=="viper.png")

""" 

