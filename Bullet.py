import pygame
from pygame.locals import *

class Bullet () :
    def __init__ ( self, x, y, x_speed, y_speed, b_img ) :
        self.x = x
        self.y = y

        self.x_speed = x_speed
        self.y_speed = y_speed

        self.img = b_img
        self.shot = False

    def display ( self, py_screen ) :
        if ( self.shot is False) :
            py_screen.blit(self.img, (self.x - 4, self.y - 4))  # img displayed

    def physics ( self, arr, hp) :
        pass
        self.x += self.x_speed
        self.y += self.y_speed

        for p in arr:
            if ( self.shot is False) :

                if ( self.x + 4 > p.x and self.x - 4 < p.x + 20 and
                        self.y + 4 > p.y and self.y - 4 < p.y + 20) :
                    p.xspeed = self.x_speed / 2
                    p.yspeed = self.y_speed / 2
                    self.shot = True
                    return hp - 10
        return hp
