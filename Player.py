# player
import pygame
from pygame.locals import *

# loading and creating a surface for the players image
player_surface = pygame.Surface((20,20))
player_image = pygame.image.load("graphics/player.png")

class Player():
    def __init__(self, x, y, p_img):
        self.x = x #x coord
        self.y = y #y coord

        self.xspeed = 0 # xspeed
        self.yspeed = 0 # yspeed

        self.can_jump = False #if player can jump
        self.in_air = False #if player is in air
        self.key_pressed = False

        self.direction = 0 #direction of player
        self.img = p_img # list of images

        self.sprite_timer = 0 #timer for sprites
        self.img_type = 0 #initalises what image is displayed
        self.on_g = 0 #determines whether player is on ground

        self.p_im = 0

    def display(self, py_screen): #displays player
        # Uses the previously created/loaded images to display the
        # player as those images

        p_img = self.img[self.img_type]
        self.on_g -= 1 # timer lowers when player is in the air

        #a timer for sprites

        if (self.on_g > 0): # if player is on the ground
            self.sprite_timer += 2
            if ( self.sprite_timer < 100 ) :
                if ( self.key_pressed > 0) :
                    self.img_type = 2  # walk 1
                else :
                    self.img_type = 0 #idle 1

            elif ( self.sprite_timer < 200) :
                    self.img_type = 0  # idle 1
            elif ( self.sprite_timer < 300) :
                if (self.key_pressed > 0):
                    self.img_type = 3  # walk 2
                else:
                    self.img_type = 1  # idle 2
            elif ( self.sprite_timer < 400) :
                if (self.key_pressed > 0):
                    self.img_type = 0  # idle 1
                else:
                    self.img_type = 1  # idle 2
            else :
                self.sprite_timer = 0 # resets timer
        else :
            self.sprite_timer = 0 # keeps timer at 0
            self.img_type = 2 #jump

        if ( self.direction == 0 ) : # flips left
            c_img = pygame.transform.flip(p_img, True, False) # current img
        elif ( self.direction == 1) : # flips right
            c_img = pygame.transform.flip(p_img, False, False)
        py_screen.blit(c_img, (self.x, self.y))

    def key_inputs(self): #keys input
        keys = pygame.key.get_pressed() #allows key input

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]): #if player types 'a'
            self.xspeed -= 0.0025 #accelerate left
            self.key_pressed = 10


        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]): #if player types 'd'
            self.xspeed += 0.0025 #accelerate right
            self.key_pressed = 10

        if (keys[pygame.K_w] or keys[pygame.K_UP]): #if player types 'w'

            if (self.can_jump): #if the player can jump,

                self.yspeed = -0.4 #y speed goes up
                self.can_jump = False #prevents player from jumping

    def physics(self): #physics
        self.x += self.xspeed #connects x coord with xspeed
        self.y += self.yspeed #connects y coord with yspeed

        self.yspeed += 0.00125 #gravity acceleration

        self.key_pressed -= 1 #to determine if player is moving sideways

        self.p_im -= 1 #to make sure player does not instantly die

        if ( self.can_jump is True) :
            self.on_g = 5 #if player is on ground, on_g is above 0.

        #direction
        if (self.xspeed > 0):
            self.direction = 1  # facing right
        if ( self.xspeed < 0) :
            self.direction = 0  # facing left

        if ( self.yspeed < 0 or self.yspeed > 0.1) : #if player is not still,

            self.in_air = True #player is in the air
            can_jump = False #prevents the player from jumping in the air

        else :
            if (self.can_jump == False) : #if yspeed is 0 but cannot jump,

                self.in_air = True #player is still in the air

            else :

                self.in_air = False #otherwise, player is not in air.

        #if player is on ground,
        if ( self.key_pressed < 0) :

            if (self.xspeed > 0): #player experiences friction
                self.direction = 1  # facing right
                self.xspeed -= 0.00125

            if (self.xspeed < 0):

                self.xspeed += 0.00125

            if (self.xspeed > -0.0025 and self.xspeed < 0.0025):

                self.xspeed = 0

        if (self.yspeed > 0) :
            self.can_jump = False



        if (self.xspeed > 0.2) : #maximum speeds of player
            self.xspeed = 0.2
        if (self.xspeed < -0.2) :
            self.xspeed = -0.2

        if (self.yspeed > 1.5):
            self.yspeed = 1.5

        if (self.y > 800): #if player jumps off screen, player dies
            return True
