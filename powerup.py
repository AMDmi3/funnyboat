import pygame

from locals import *

import util
import health
from water import Water

class Powerup (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not health.Health.heart:
            health.init()

        self.image = health.Health.heart
        #self.hitmask = pygame.surfarray.array_alpha(self.image)

        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_WIDTH
        self.rect.bottom = Water.global_water.get_water_level(SCREEN_WIDTH)

        self.dx, self.dy = -1, 0
        self.t = 0
        self.picked = False
        self.fading = False

    def update(self):
        water_level = Water.global_water.get_water_level(self.rect.centerx)
        if self.fading:
            if self.fadecount > 0:
                self.image.set_alpha(self.fadecount * 255 / 15)
                self.fadecount -= 1
            else:
                self.picked = True
        if self.rect.bottom > water_level:
            self.dy *= 0.8
            if self.rect.top > water_level:
                self.dy -= 2
            else:
                self.dy -= 0.25 * (self.rect.bottom - water_level)

        self.dy += 1

        self.rect.left += self.dx
        self.rect.top += self.dy

        self.t += 1

    def pickup(self):
        self.fading = True
        self.fadecount = 15
        image = pygame.Surface((self.image.get_width(), self.image.get_height()))
        image.fill((255,0,255))
        image.set_colorkey((255,0,255))
        image.blit(self.image, self.image.get_rect())
        self.image = image
