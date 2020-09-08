import pygame
import pygame
import math

from water import Water

import util

from locals import *

def init():
    Shark.image = util.load_image("hai")
    Shark.death_sound = util.load_sound("kraah")

class Shark (pygame.sprite.Sprite):
    image = None
    death_sound = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        if not Shark.image or not Shark.death_sound:
            shark.init()

        self.image = Shark.image

        self.rect = pygame.Rect(SCREEN_WIDTH, 0, Shark.image.get_width(), Shark.image.get_height())
        self.life = 0

        #self.hitmask = pygame.surfarray.array_alpha(self.image)

        self.dx, self.dy = -3, 0

        self.jumping = False
        self.dying = False
        self.dead = False
        self.angle = 0
        self.target_angle = 0

    def update(self):
        water_levels = [Water.global_water.get_water_level(self.rect.left),
                        Water.global_water.get_water_level(self.rect.centerx),
                        Water.global_water.get_water_level(self.rect.right)]
        if self.dying:
            angle = 0.4 * self.target_angle + 0.6 * self.angle

            self.update_angle(angle)
            self.rect.top += self.dy
            self.rect.left += self.dx
            self.dy += 1

            if self.rect.bottom > water_levels[1]:
                self.dy *= 0.8
                self.dx *= 0.8

            if self.rect.top >= SCREEN_HEIGHT:
                self.dead = True
            return
        if not self.jumping:
            self.rect.top = water_levels[1] - 8
            self.target_angle = math.atan((water_levels[0] - water_levels[2]) / 32.0) * 180.0 / math.pi
        else:
            self.dy = self.dy + 1
            if self.rect.top > water_levels[1] - 8:
                self.jumping = False
                self.dy = 0
                self.dx = -2

        if self.life % 40 == 0:
            self.jumping = True
            self.dy = -10
            self.dx = - 3

        self.rect.top = self.rect.top + self.dy
        self.rect.left = self.rect.left + self.dx

        self.life = self.life + 1

        angle = 0.2 * self.target_angle + 0.8 * self.angle

        self.update_angle(angle)


    def update_angle(self, angle):
        self.angle = angle

        self.image = util.rotate(Shark.image, angle)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        #self.hitmask = pygame.surfarray.array_alpha(self.image)

    def die(self):
        self.dying = True
        while not self.dying:
            pass
        if (Variables.sound):
           Shark.death_sound.play()
        self.dy = -5
        self.target_angle = 90
        #self.image = pygame.transform.rotate(Shark.image, 90)

