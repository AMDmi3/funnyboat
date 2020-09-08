import pygame
import math

from water import Water

import util

from locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos = [0.0, 0.0], health = 1):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.velocity [0.0, 0.0]

        self.health = health

        #self.hitmask = pygame.surfarray.array_alpha(self.image)

        self.angle = 0
        self.targetangle = 0
        self.dying = False
        self.dead = False

        self.t = 0

    def damage(self):
        self.health -= 1

        if self.health == 0:
            self.die()

    def update(self):
        self.t += 1

        self.velocity[1] += 1.0 # Gravity

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def die(self):
        self.dying = True
