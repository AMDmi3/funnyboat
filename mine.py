import pygame
import random

from water import Water
from locals import *

import util

def init():
    Mine.image = util.load_image("miina")
    Mine.sound = util.load_sound("poks")

class Mine(pygame.sprite.Sprite):
    image = None
    sound = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # This is an easy way to get a random number that is a water level.
        height = int(SCREEN_HEIGHT -  Water.global_water.get_water_level(random.random() * 320)) - 4

        if not Mine.image or not Mine.sound:
            mine.init()

        self.image = pygame.Surface((Mine.image.get_width(), Mine.image.get_height() + height), SRCALPHA, 32)
        self.image.fill((0,0,0,0))

        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT
        self.rect.left = SCREEN_WIDTH

        self.image.blit(Mine.image, Mine.image.get_rect())
        pygame.draw.line(self.image, (25, 25, 25), (self.image.get_rect().centerx, Mine.image.get_height()),
                                                   (self.image.get_rect().centerx, self.image.get_height()))

        #self.hitmask = pygame.surfarray.array_alpha(self.image)

        self.dx = -1

        self.exploding = False
        self.explode_frames = 0

    def update(self):
        water_level = Water.global_water.get_water_level(self.rect.centerx)

        self.rect.left += self.dx

        if SCREEN_HEIGHT - water_level < self.rect.height - 4:
            self.rect.top = water_level - 4
        else:
            self.rect.bottom = SCREEN_HEIGHT

        if self.exploding:
            if self.explode_frames > 0:
                self.explode_frames -= 1
            # animate

    def explode(self):
        if (Variables.sound):
           Mine.sound.play()

        self.exploding = True
        self.explode_frames = 10

