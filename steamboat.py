import pygame
import math

from water import Water

import util

from locals import *

def init():
    Steamboat.image = util.load_image("laiva")
    Steamboat.death_sound = util.load_sound("blub")

class Steamboat(pygame.sprite.Sprite):
    image = None
    death_sound = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not Steamboat.image or not Steamboat.death_sound:
            init()

        self.image = Steamboat.image
        self.rect = pygame.Rect(50, 20, self.image.get_width(), self.image.get_height())
        self.area = pygame.Rect(100, 100, 100, 100)

        #self.hitmask = pygame.surfarray.array_alpha(self.image)

        self.health = 5
        self.jumping = False
        self.taking_damage = False
        self.moving_right = False
        self.moving_left = False
        self.shooting = False
        self.angle = 0
        self.target_angle = 0
        self.dying = False
        self.dead = False
        self.splash = False
        self.blinks=0

        self.steam = []

        self.dx, self.dy = 0,0
        self.t = 0

    def update(self):
        water_levels = [Water.global_water.get_water_level(self.rect.left),
                        Water.global_water.get_water_level(self.rect.centerx),
                        Water.global_water.get_water_level(self.rect.right)]
        self.splash = False

        if self.dying:
            angle = 0.1 * self.target_angle + 0.9 * self.angle

            self.update_angle(angle)
            self.rect.top += self.dy
            self.dy += 1

            if self.rect.bottom > water_levels[1]:
                self.dy *= 0.8

            if self.rect.top >= SCREEN_HEIGHT:
                self.dead = True
            return

        if self.moving_left and not self.moving_right:
            self.dx = -2
        elif self.moving_right:
            self.dx = 2
        else:
            self.dx = 0

        if self.rect.bottom > water_levels[1]:
            if self.jumping:
                self.splash = True
            self.jumping = False
            plap = self.rect.bottom - water_levels[1]
            self.dy *= 0.8
            if self.rect.top > water_levels[1]:
                self.dy -= 2
            else:
                self.dy -= (self.rect.bottom - water_levels[1]) * 0.25

            self.target_angle = 180.0 / math.pi * math.atan((water_levels[0] - water_levels[2]) / 32.0) + math.sin(self.t * 0.05) * 5
        else:
            self.jumping = True

        self.dy += 1

        self.rect.left += self.dx
        self.rect.top += self.dy #move((self.dx, self.dy))

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        self.t += 1
        self.update_angle(self.angle * 0.8 + self.target_angle * 0.2)
        
        if self.blinks:
            if self.blinks&1:
                self.image.fill((255,255,255,0))
            self.blinks-=1

    def update_angle(self, angle):
        self.angle = angle
        self.image = util.rotate(Steamboat.image, angle)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        #self.hitmask = pygame.surfarray.array_alpha(self.image)

    def jump(self):
        if not self.dying:
            if not self.jumping:
                self.jumping = True
                self.dy = -10
                #self.target_angle += 45
                #self.update_angle(-25)

    def move_left(self, bool):
        if not self.dying:
            if bool:
                self.moving_left = True
            else:
                self.moving_left = False

    def move_right(self, bool):
        if not self.dying:
            if bool:
                self.moving_right = True
            else:
                self.moving_right = False

    def get_point(self, point):
        dx = point[0] - self.image.get_rect().centerx
        dy = point[1] - self.image.get_rect().centery

        new_point = [-dy * math.sin(-math.pi / 180.0 * self.angle) + dx * math.cos(-math.pi / 180.0 * self.angle),
                      dy * math.cos(-math.pi / 180.0 * self.angle) + dx * math.sin(-math.pi / 180.0 * self.angle)]
        
        return new_point

    def die(self):
        if not self.dying:
            if (Variables.sound):
               Steamboat.death_sound.play(3, 0)
            self.dying = True
            self.dy = -5
            self.target_angle = -90
