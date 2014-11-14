# implementation of Spaceship - program template for RiceRocks
# with info for aminated rocks:
#   http://www.codeskulptor.org/#user38_ZC8iGRQhOy_0.py
#
import simplegui
import math
import random

# global constants for user interface
WIDTH = 800
HEIGHT = 600

# global constants for object parameters
ROCK_LIMIT = 20
MISSILE_LIMIT = 50
MISSILE_LIFE = 50
BOOM_FRAMES = 24

# dynamic references for game play
score = 0
lives = 3
time = 0
started = False
life_tick = 1


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, MISSILE_LIFE)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
# change this to the animation image and dimensions:
#
#
#

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, BOOM_FRAMES, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on: # and started:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global missile_set #a_missile
        if len(missile_set) <= MISSILE_LIMIT:
            forward = angle_to_vector(self.angle)
            missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
            missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
            #a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
            missile_set.add(Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound))    

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound: #and started:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update life: if image is missile, lifespan -= life_tick; set if expired (>0)
        if self.lifespan:
            self.lifespan -= life_tick
            
        # explosion is 3072x128 or 24 images; age = 24    
        if self.animated:
            #self.image_center[0]= 12*self.image_size[0] + 64
            self.age += 1
            self.age = self.age % BOOM_FRAMES
            self.image_center[0] = self.age*self.image_size[0]+64
            
"""
# load 64 frame sprite sheer for asteroid - image source is opengameart, artist is warspawn 
ROCK_CENTER = [64, 64]
ROCK_SIZE = [128, 128]
ROCK_DIM = 64
rock_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/asteroid1.opengameart.warspawn.png")

def draw(canvas):
    global time
    current_rock_index = (time % ROCK_DIM) // 1
    print time, current_rock_index, current_rock_index * ROCK_SIZE[0]
    current_rock_center = [ROCK_CENTER[0] +  current_rock_index * ROCK_SIZE[0], ROCK_CENTER[1]]
    canvas.draw_image(rock_image, current_rock_center, ROCK_SIZE, ROCK_CENTER, ROCK_SIZE) 
    time += 0.9  < this should be the ramdom value
"""
        

        
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        reset()
         
        
def reset():
    global score, lives, time
    score = 0
    lives = 3
    time = 0
    soundtrack.rewind()
    soundtrack.play()
    

def draw(canvas):
    global time, started, rock_set, missile_set, boom_set, lives, score  #, a_missile
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    # a_rock.draw(canvas)
    for rock in rock_set:
        rock.draw(canvas)
    # a_missile.draw(canvas)
    for missile in missile_set:
        missile.draw(canvas)
    
    # draw each explosion        
    for boom in boom_set:
        explosion_sound.play()
        boom.draw(canvas)
        
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
    for rock in rock_set:
        rock.update()
    #print rock.lifespan 
    #a_missile.update()
    for missile in missile_set:
        missile.update()
    #print a_missile.lifespan 
    for boom in boom_set:
        boom.update()

    # update collision status: remove if collide == True
    # if image is missile, check collision with rocks in list
    if started:
        for rock in rock_set:
            for missile in missile_set:
            # if collided == True:  set lifespan = -1 for both; score += 1
                if collided(missile,rock):
                    rock.lifespan=0
                    missile.lifespan=0
                    boom_spawn(rock)
                    score +=1
        #for rock in rock_set:
            if collided(my_ship,rock):
                rock.lifespan=0
                # add explosion_sprite at {rock_center} to explosion_list;
                boom_spawn(rock)
                lives -=1
                if lives == 0:
                    started = False
                
    # remove cancelled sprites
    missile_set = trim_set(missile_set)
    rock_set = trim_set(rock_set)
    boom_set = trim_set(boom_set)
    #explosion_set = trim_set(rock_set)
    
    # draw UI last to keep it uncovered
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        rock_set = set([])
        soundtrack.pause()

def collided(sprite1,sprite2):
    #return collision result:  distance <= r1+r2
    collided = dist(sprite1.pos,sprite2.pos) <= sprite1.radius + sprite2.radius
    return collided
        
def trim_set(sprite_set):
    # remove cancelled sprites: (lifespan < 0)
    trim_set=set([])
    for each in sprite_set:
        if each.lifespan == 0:
            trim_set.add(each)
    sprite_set.difference_update(trim_set)     
    return sprite_set    
        
# timer handler that spawns a set of rock    
def rock_spawner():
    global rock_set, started#a_rock
    if len(rock_set) < ROCK_LIMIT and started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
        rock_set.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))
    #a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)        
            
def boom_spawn(rock):
    global boom_set
    boom = Sprite(rock.pos,[0,0],0,0,explosion_image, explosion_info, explosion_sound)
    boom_set.add(boom)
                 
    # place an explosion at the item location
        
# initialize stuff:
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprite sets:
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#rock_set = set([Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)])
rock_set = set([])
#missile_set = set([Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)])
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_set = set([])
#boom_set = set([Sprite([10,10],[0,0],0,0,explosion_image, explosion_info, explosion_sound)])
#explosion = Sprite([10,10],[0,0],0,0,explosion_image, explosion_info, explosion_sound)
boom_set= set([])

# register handlers:
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

