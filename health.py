import pygame
from pygame.locals import *

from locals import *

import util

def init():
    Health.heart = util.load_image("sydan")
    Health.heart_empty = util.load_image("sydan-tyhja")
    Health.heart_broken = util.load_image("sydan-rikki")
    heart_broken = pygame.Surface((Health.heart_broken.get_rect().width, Health.heart_broken.get_rect().height))
    heart_broken.fill((255,0,255))
    heart_broken.set_colorkey((255,0,255))
    heart_broken.blit(Health.heart_broken, heart_broken.get_rect())
    Health.heart_broken = heart_broken

class Health (pygame.sprite.Sprite):
    heart = None
    heart_empty = None
    heart_broken = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not Health.heart or not Health.heart_empty or not Health.heart_broken:
            init()

        self.rect = pygame.Rect(10, 0, Health.heart.get_width() * 5 + 4, Health.heart.get_height() * 2)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.set_colorkey((255,255,255))

        self.hearts_left = 5
        self.hearts_dying = 0
        self.hearts_deathcounters = [0,0,0,0,0]


        self.update()

    def update(self):
        # clear the surface
        self.image.fill((255,255,255))

        for i in xrange(5):
            rect = pygame.Rect(i * (Health.heart.get_width() + 1), Health.heart.get_height(), Health.heart.get_width(), Health.heart.get_height())
            if i < self.hearts_left:
                self.image.blit(Health.heart, rect)
            else:
                self.image.blit(Health.heart_empty, rect)
                if i < (self.hearts_left + self.hearts_dying):
                    rect.top -= self.hearts_deathcounters[i]
                    if Variables.alpha:
                        Health.heart_broken.set_alpha(255 - self.hearts_deathcounters[i]*10)
                    self.image.blit(Health.heart_broken, rect)
                    self.hearts_deathcounters[i] += 1
                    if self.hearts_deathcounters[i] == 25:
                        self.hearts_dying -= 1


    def damage(self):
        if self.hearts_left > 0:
            self.hearts_left -= 1
            self.hearts_dying += 1
        self.update()

    def add(self):
        if self.hearts_left < 5:
            self.hearts_left += 1

