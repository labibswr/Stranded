# Importing Python
import pygame
from pygame.locals import *

import random
import math

from Bullet import *

# Class for the enemy
class Enemy():
    def __init__(self, x, y, e_type, e_img):
        self.x = x #x coord
        self.y = y #y coord

        self.xspeed = 0 # xspeed
        self.yspeed = 0 # yspeed

        self.in_air = False
        self.e_type = e_type #type of enemy, ranged / melee

        self.direction = round ( random.randint(0, 1) )

        self.img = e_img
        self.sprite_timer = 0  # timer for sprites
        self.img_type = 0  # initalises what image is displayed

        self.shoot_timer = 0
        self.angle = 0

    def get_type (self) :
        return self.e_type #returns type of enemy

    def m_display(self, py_screen): #melee display
        e_img = self.img[self.img_type]

        self.sprite_timer += 2
        if (self.sprite_timer < 100):
            self.img_type = 0  # walk 1
        elif (self.sprite_timer < 200):
            self.img_type = 1  # idle 1
        elif (self.sprite_timer < 300):
            self.img_type = 2  # walk 2
        else:
            self.sprite_timer = 0  # resets timer

        if ( self.direction == 0 ) : # flips left
            c_img = pygame.transform.flip(e_img, True, False) # current img
        elif ( self.direction == 1) : # flips right
            c_img = pygame.transform.flip(e_img, False, False)
        py_screen.blit(c_img, (self.x, self.y))

    def t_display ( self, py_screen) :
        py_screen.blit(self.img[1], (self.x, self.y))
        #self.angle += 4
        if ( self.direction == 0 ) : # flips left
            c_img = pygame.transform.flip(self.img[2], False, True) # current img
        elif ( self.direction == 1) : # flips right
            c_img = pygame.transform.flip(self.img[2], False, False)
        r_img = pygame.transform.rotate (c_img, self.angle)
        py_screen.blit(r_img, (self.x + 10 - ( r_img.get_width() / 2),
                               self.y + 10- ( r_img.get_height() / 2) ) )

    def physics(self):
        self.x += self.xspeed #
        self.y += self.yspeed

        self.yspeed += 0.01

        if (self.xspeed > 0):
            self.xspeed -= 0.075
        if (self.xspeed < 0):
            self.xspeed += 0.075
        if (self.xspeed > -0.25 and self.xspeed < 0.25):
            self.xspeed = 0

        if (self.yspeed > 0) :
            self.can_jump = False

        if (self.yspeed > 1.5):
            self.yspeed = 1.5

        if (self.y > 800):
            return True

    def movement (self) :
        if ( self.direction == 0) :
            self.xspeed = -0.2
        elif ( self.direction == 1) :
            self.xspeed = 0.2
        pass

    def collision(self, arr, health):
        # collisions
        for p in arr:  # calls object

            if (p.x > self.x - 20 and p.x < self.x - 19
                        and p.y > self.y - 19 and p.y < self.y + 19):
                p.x = self.x - 20  # left side
                self.direction = 1
                p.xspeed = -0.2
                if ( p.p_im < 0) :
                    p.p_im = 10
                    return health - 20

            if (p.x > self.x + 19 and p.x < self.x + 20
                        and p.y > self.y - 19 and p.y < self.y + 18):
                p.x = self.x + 20  # right side
                self.direction = 0
                p.xspeed = 0.2
                if (p.p_im < 0):
                    p.p_im = 10
                    return health - 20

            if (p.y > self.y - 20 and p.y < self.y - 18):
                if ( p.x > self.x - 20 and
                            p.x < self.x + 20 and p.yspeed >= 0):
                    p.y = self.y - 20  # top side
                    p.yspeed = -0.2
                    if (p.p_im < 0):
                        p.p_im = 10
                        return health - 20

            if (p.y > self.y + 18 and p.y < self.y + 20
                  and p.x > self.x - 20 and p.x < self.x + 20 and p.yspeed < 0):
                p.y = self.y + 20  # bottom side
                p.yspeed = 0
                if (p.p_im < 0):
                    p.p_im = 10
                    return health - 20

        return health

    def shoot_gun ( self, arr, b_arr, py_screen) :
        pass
        for p in arr :
            p_x_dist = ( ( p.x + 10 ) - (self.x + 10))
            p_y_dist = ( (p.y + 10 ) - (self.y + 10))
            self.angle = -math.atan2 ((self.x + 10) - (p.x + 10), (p.y + 10) - (self.y + 10)) * (180/3.14159265) + 90

        magn = math.sqrt ( (p_x_dist ** 2) + (p_y_dist ** 2) )
        x_dir = p_x_dist / magn
        y_dir = p_y_dist / magn
        self.shoot_timer += 1

        bul_speed = 0.25

        if ( p_x_dist < 0) :
            self.direction = 1
        else :
            self.direction = 0

        if ( self.shoot_timer > 600) :
            bul = Bullet(self.x + 10, self.y + 10, x_dir * bul_speed,
                             y_dir * bul_speed, self.img[0])
            b_arr.append (bul)
            self.shoot_timer = 0
