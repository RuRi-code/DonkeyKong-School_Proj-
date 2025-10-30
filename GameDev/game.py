import os #screen
import pygame #game dev module
import random # time for barrel

os.environ['SDL_VIDEO_CENTERED'] = '1' # call before pygame.init 

pygame.init()

pygame.display.set_caption('Donkey Kong')

# initializing game screen on pc
info_screen = pygame.display.Info()

screen_width, screen_height = info_screen.current_w, info_screen.current_h

window_width, window_height = screen_width - 800 , screen_height - 150

#Fps of the game
timer = pygame.time.Clock()
fps = 60

from pygame.locals import * # for resizing
screen = pygame.display.set_mode([window_width ,window_height  ]) # screen display

#Graphics import png
#Barrel
Barrel_image = pygame.transform.scale(pygame.image.load('Platform/Barrel_1.png'),(25,25))
#bg
Bg_image = "Platform/SchoolBg.png"
Bg_load = pygame.image.load(Bg_image)
Bg_load = pygame.transform.smoothscale(Bg_load,(500 ,
                                         screen_height ))

#Bridge
Bridge_image = "Platform/concrete_3.png"
Bridge_load = pygame.image.load(Bridge_image)
Bridge_load = pygame.transform.scale(Bridge_load,(Bridge_load.get_width() * 1.3,
                                     Bridge_load.get_height() * 1.3))
#Ladder
Ladder_image = "Platform/ladder_1.png"
Ladder_load = pygame.image.load(Ladder_image)
Ladder_load = pygame.transform.scale(Ladder_load,(Ladder_load.get_width()* 0.5 ,
                                          Ladder_load.get_height() * 0.9))
#fireball
fireball_trigger = False
#Initializing blocks per screen or sections on the game
section_width = window_width // 32
section_height = window_height // 32
slope = section_height // 8
#Level variables
start_y = window_height - 2 * section_height
row2_y = start_y - 4 * section_height
row3_y = row2_y - 7 * slope - 3 * section_height
row4_y = row3_y - 4 * section_height
row5_y = row4_y - 7 * slope - 3 * section_height
row6_y = row5_y - 4 * section_height
row6_top = row6_y - 4 * slope
row5_top = row5_y - 8 * slope
row4_top = row4_y - 8 * slope
row3_top = row3_y - 8 * slope
row2_top = row2_y - 8 * slope
row1_top = start_y - 5 * slope
#levels 
active_level = 0
levels = [{'bridges': [(1, start_y, 15), (16, start_y - slope, 3),
                       (19, start_y - 2 * slope, 3), (22, start_y - 3 * slope, 3),
                       (25, start_y - 4 * slope, 3), (28, start_y - 5 * slope, 3),
                       (25, row2_y, 3), (22, row2_y - slope, 3),
                       (19, row2_y - 2 * slope, 3), (16, row2_y - 3 * slope, 3),
                       (13, row2_y - 4 * slope, 3), (10, row2_y - 5 * slope, 3),
                       (7, row2_y - 6 * slope, 3), (4, row2_y - 7 * slope, 3),
                       (2, row2_y - 8 * slope, 2), (4, row3_y, 3),
                       (7, row3_y - slope, 3), (10, row3_y - 2 * slope, 3),
                       (13, row3_y - 3 * slope, 3), (16, row3_y - 4 * slope, 3),
                       (19, row3_y - 5 * slope, 3), (22, row3_y - 6 * slope, 3),
                       (25, row3_y - 7 * slope, 3), (28, row3_y - 8 * slope, 2),
                       (25, row4_y, 3), (22, row4_y - slope, 3),
                       (19, row4_y - 2 * slope, 3), (16, row4_y - 3 * slope, 3),
                       (13, row4_y - 4 * slope, 3), (10, row4_y - 5 * slope, 3),
                       (7, row4_y - 6 * slope, 3), (4, row4_y - 7 * slope, 3),
                       (2, row4_y - 8 * slope, 2), (4, row5_y, 3),
                       (7, row5_y - slope, 3), (10, row5_y - 2 * slope, 3),
                       (13, row5_y - 3 * slope, 3), (16, row5_y - 4 * slope, 3),
                       (19, row5_y - 5 * slope, 3), (22, row5_y - 6 * slope, 3),
                       (25, row5_y - 7 * slope, 3), (28, row5_y - 8 * slope, 2),
                       (25, row6_y, 3), (22, row6_y - slope, 3),
                       (19, row6_y - 2 * slope, 3), (16, row6_y - 3 * slope, 3),
                       (2, row6_y - 4 * slope, 14), (13, row6_y - 4 * section_height, 6),
                       (10, row6_y - 3 * section_height, 3)],
                'ladders': [(12, row2_y + 6 * slope, 2), (12, row2_y + 26 * slope, 2),
                       (25, row2_y + 11 * slope, 4), (6, row3_y + 11 * slope, 3),
                       (14, row3_y + 8 * slope, 4), (10, row4_y + 6 * slope, 1),
                       (10, row4_y + 24 * slope, 2), (16, row4_y + 6 * slope, 5),
                       (25, row4_y + 9 * slope, 4), (6, row5_y + 11 * slope, 3),
                       (11, row5_y + 8 * slope, 4), (23, row5_y + 4 * slope, 1),
                       (23, row5_y + 24 * slope, 2), (25, row6_y + 9 * slope, 4),
                       (13, row6_y + 5 * slope, 2), (13, row6_y + 25 * slope, 2),
                       (18, row6_y - 27 * slope, 4), (12, row6_y - 17 * slope, 2),
                       (10, row6_y - 17 * slope, 2), (12, -5, 13), (10, -5, 13)] }]
#slope = section_height // 8  # sections of the slope is by 8 every slopes goes up or down

dimension_width = 32
dimension_height = 32

# defs, classes
class Barrel(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.y_change = 0
        self.x_change = 1
        self.pos = 0
        self.count = 0
        self.oil_collision = False
        self.falling = False
        self.check_lad = False
        self.bottom = self.rect

    def update(self, fire_trig):
        if self.y_change < 8 and not self.falling:
            barrel.y_change +=2
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.y_change = 0
                self.falling = False
        if self.rect.colliderect(oil_drum):
            if not self.oil_collision:
                self.oil_collision = True
                if random.randint(0, 4) == 4:
                    fire_trig = True
        if not self.falling:
            if row5_top >= self.rect.bottom or row3_top >= self.rect.bottom >= row4_top or row1_top > self.rect.bottom >= row2_top:
                self.x_change = 2
            else:
                self.x_change = -2
        else:
            self.x_change = 0
        self.rect.move_ip(self.x_change, self.y_change)
        if self.rect.top > screen_height:
            self.kill()
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            if self.x_change > 0:
                if self.pos < 3:
                    self.pos += 1
                else:
                    self.pos = 0
            else:
                if self.pos > 0:
                    self.pos -= 1
                else:
                    self.pos = 3
        self.bottom = pygame.rect.Rect((self.rect[0], self.rect.bottom ), (self.rect[3], 1.5))
        pygame.draw.rect(screen,'red',self.bottom)
        return fire_trig
                    
    def check_fall(self):
        already_collided= False
        # Create a small area below the barrel
        below = pygame.rect.Rect((self.rect[0], self.rect[1] + section_height), (self.rect[2], section_height))
       

        # Check if barrel is directly above a ladder
        for lad in lads:
            if below.colliderect(lad) and not self.falling and not self.check_lad:
                self.check_lad = True
                already_collided = True
                
                # Random small chance to fall down the ladder
                if random.randint(1,2) == 2:  # about 1 in 40 frames
                    pygame.draw.rect(screen,'red',below) # checks the hitbox
                    self.falling = True
                    self.y_change =4

        # Reset check flag if no ladder below
        if not already_collided:
         self.check_lad = False

    def draw(self):
        screen.blit(pygame.transform.rotate(Barrel_image, 90 * self.pos), self.rect.topleft)
                     

class Bridge:
    def __init__(self,x_pos,y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.top = self.draw() # constructin

    def draw(self):
        line_width = 7 
        for i in range(self.length):
           left_coord = self.x_pos + (section_width * i)
           top_coord = self.y_pos
           screen.blit(Bridge_load,(left_coord  ,self.y_pos))

        top_line = pygame.rect.Rect((self.x_pos, self.y_pos),(self.length *section_width + 6,2))
        pygame.draw.rect(screen, 'blue',top_line)
        return top_line
    
class Ladder:
    def __init__(self,x_pos,y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.body = self.draw()

    def draw(self):
        lad_height = 0.6
        for i in range(self.length):
            left_coord = self.x_pos 
            top_coord = self.y_pos + lad_height * section_height * i
            screen.blit(Ladder_load,(left_coord  ,top_coord ))

        body = pygame.rect.Rect((self.x_pos, (self.y_pos - section_height)- 2),(section_width,(lad_height*self.length + section_height)))
        pygame.draw.rect(screen, 'blue',body)
        return body


def draw_screen():
    platforms = []
    climbers = []
    bridge_objs= []
    ladder_objs = []

    ladders = levels[active_level]['ladders']
    bridges = levels[active_level]['bridges']

    for bridge in bridges:
     bridge_objs.append(Bridge(*bridge))
     platforms.append(bridge_objs[-1].top)

    for ladder in ladders:
        ladder_objs.append(Ladder(*ladder))
        if ladder[2] >=  3:
             climbers.append(ladder_objs[-1].body)
    return platforms,climbers





    

    
#Barrel spawn time
barrel_spawn_time = 360
barrel_count = barrel_spawn_time/2
barrel_time = 360
#Barrel sprite
barrels = pygame.sprite.Group()
#oil drum
oil_drum = pygame.rect.Rect((1,1),(1,1))

running = True # Run the games if false then exit

while running:
    screen.fill ('black') # background
    screen.blit(Bg_load,(25,0))
    timer.tick (fps) # fps of the game
    #Bridge_level()
    #Ladder_level()
    plats,lads = draw_screen()


    if barrel_count < barrel_spawn_time: # barrel spawn mechanics
        barrel_count += 1
    
    else:
        barrel_count = random.randint(0,220)
        barrel_time = barrel_count - barrel_spawn_time
        barrel = Barrel(170,190)
        barrels.add(barrel)

    for barrel in barrels:
        barrel.draw()
        barrel.check_fall()
        fireball_trigger = barrel.update(fireball_trigger)



    for event in pygame.event.get(): # Exit button on window
        if event.type == pygame.QUIT:
            running = False
    

    pygame.display.flip()

pygame.quit()

