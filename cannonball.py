import pygame
import math

from water import Water
from locals import *

import util

class Cannonball (pygame.sprite.Sprite):
    image = None
    spec_image = None
    sound = None
    def __init__(self, ship_rect, ship_angle, left = False, special = False):
        pygame.sprite.Sprite.__init__(self)

        if not Cannonball.image:
            Cannonball.image = util.load_image("kuti")
        if not Cannonball.spec_image:
            Cannonball.spec_image = pygame.transform.flip(util.load_image("lokki2"),1,0)
            
        if not Cannonball.sound:
            Cannonball.sound = util.load_sound("pam")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        if special:
            self.image= Cannonball.spec_image
        else:
            self.image = Cannonball.image
        self.special=special
        self.underwater=0
        
        #self.hitmask = pygame.surfarray.array_alpha(self.image)
        if (Variables.sound):
            Cannonball.sound.play()
        #self.dy = -5
        #self.dx = 10
        # Shoot at an angle of 25 relative to the ship

        self.angle=0
        
        if not left:
            if special:
                velocity = 14.0
                self.rect = pygame.Rect(ship_rect.right, ship_rect.top, self.image.get_width(), self.image.get_height())
                self.vect = [math.cos((-ship_angle - 15.0) / 180.0 * math.pi) * velocity,
                         math.sin((-ship_angle - 15.0) / 180.0 * math.pi) * velocity]
            else:
                velocity = 11.0
                self.rect = pygame.Rect(ship_rect.right, ship_rect.centery, self.image.get_width(), self.image.get_height())
            self.vect = [math.cos((-ship_angle - 25.0) / 180.0 * math.pi) * velocity,
                         math.sin((-ship_angle - 25.0) / 180.0 * math.pi) * velocity]
        else:
            self.rect = pygame.Rect(ship_rect.left, ship_rect.centery, self.image.get_width(), self.image.get_height())
            self.vect = [math.cos((-ship_angle + 180.0 + 25.0) / 180.0 * math.pi) * 11.0,
                         math.sin((-ship_angle + 180.0 + 25.0) / 180.0 * math.pi) * 11.0]
        # Will have to think this through later
        #self.vect = [10, -2] #vect

    def update_angle(self, angle):
        self.angle = angle
        self.image = util.rotate(Cannonball.spec_image, angle)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        #self.hitmask = pygame.surfarray.array_alpha(self.image)

    def tail_point(self):
        return self.rect.left, self.rect.centery-3+self.rect.width*math.sin(self.angle/180.0*math.pi)

    def update(self):
        self.rect.left += self.vect[0] #self.dx
        self.rect.top += self.vect[1] #self.dy



        self.vect[1] += 0.4
        #self.dy += 1
        if self.rect.bottom > Water.global_water.get_water_level(self.rect.centerx):
            
            self.vect[0] *= 0.9
            self.vect[1] *= 0.9
            self.underwater=1

        if 1 and self.special:
            try: 
                self.update_angle(-180/math.pi*math.atan(self.vect[1]/self.vect[0]))
            except ZeroDivisionError:
                self.update_angle(-90)

