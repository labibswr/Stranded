# Import Pygame
import pygame
from pygame.locals import *


class Block():
    def __init__(self, x, y, b_type, b_img): # initialise variables
        self.x = x  # x coord
        self.y = y  # y coord
        self.type = b_type #type of block
        self.img = b_img

    def get_type (self) :
        return self.type #returns type of block

    def display(self, type, py_screen): # displays the block, spikes and
        # portal



        if (type == "block"):

            py_screen.blit(self.img, (self.x, self.y)) # img displayed

        elif (type == "portal"):

            py_screen.blit(self.img, (self.x, self.y)) #img displayed


        elif (type == "spikes"):

            py_screen.blit(self.img, (self.x, self.y)) #img displayed

    def portal_next_lvl (self, p_arr, track) :

            for p in p_arr : #calls player object
                #if player touches portal, next lvl.
                if (p.x > self.x - 20 and p.x < self.x + 20 and p.y >
                        self.y - 20 and p.y < self.y + 20):

                    return True, track + 1

                else :

                    return False, track

    def collision(self, arr):
        # collisions
        if (self.type == "block"):  # if block is solid

            for p in arr:  # calls object

                if (p.x > self.x - 20 and p.x < self.x - 19
                        and p.y > self.y - 19 and p.y < self.y + 19):
                    p.x = self.x - 20  # left side
                    p.direction = 0
                    p.xspeed = 0

                if (p.x > self.x + 19 and p.x < self.x + 20
                        and p.y > self.y - 19 and p.y < self.y + 18):
                    p.x = self.x + 20  # right side
                    p.direction = 1
                    p.xspeed = 0

                if (p.y > self.y - 20 and p.y < self.y - 18):
                    if ( p.x > self.x - 20 and
                            p.x < self.x + 20 and p.yspeed >= 0):
                        p.y = self.y - 20  # top side
                        p.yspeed = 0
                        p.can_jump = True
                    if (p.x > self.x and p.x < self.x + 20):
                        p.e_on_block = 5
                        p.e_switch = True

                if (p.y > self.y + 18 and p.y < self.y + 20
                  and p.x > self.x - 20 and p.x < self.x + 20 and p.yspeed < 0):
                    p.y = self.y + 20  # bottom side
                    p.yspeed = 0

    def p_coll(self, arr, health):
        # collisions
        for p in arr:  # calls object
            if (p.x > self.x - 20 and p.x < self.x - 19
                    and p.y > self.y - 19 and p.y < self.y + 19):
                p.x = self.x - 20  # left side
                p.direction = 0
                p.xspeed = -0.2
                return health - 20

            if (p.x > self.x + 19 and p.x < self.x + 20
                    and p.y > self.y - 19 and p.y < self.y + 18):
                p.x = self.x + 20  # right side
                p.direction = 1
                p.xspeed = 0.2
                return health - 20

            if (p.y > self.y - 20 and p.y < self.y - 18
                 and p.x > self.x - 20 and p.x < self.x + 20 and p.yspeed >= 0):
                p.y = self.y - 20  # top side
                p.yspeed = -0.2
                return health - 20

            if (p.y > self.y + 18 and p.y < self.y + 20
                 and p.x > self.x - 20 and p.x < self.x + 20 and p.yspeed < 0):
                p.y = self.y + 20  # bottom side
                p.yspeed = 0
                return health - 20

        return health