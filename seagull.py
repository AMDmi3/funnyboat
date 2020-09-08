import pygame

from locals import *

import util
import random

def init():
    Seagull.animation = []
    Seagull.animation.append(util.load_image("lokki1"))
    Seagull.animation.append(util.load_image("lokki2"))
    Seagull.animation.append(util.load_image("lokki3"))
    Seagull.death_sound = util.load_sound("kraah")

class Seagull (pygame.sprite.Sprite):
    animation = None
    death_sound = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not Seagull.animation or not Seagull.death_sound:
            seagull.init()

        self.image = Seagull.animation[0]
        #self.hitmask = pygame.surfarray.array_alpha(self.image)

        self.rect = self.image.get_rect()

        self.rect.top = SCREEN_HEIGHT / 10.0 + random.random() * SCREEN_HEIGHT / 10.0
        self.rect.left = SCREEN_WIDTH
        self.area = pygame.display.get_surface().get_rect()

        self.vect = [-2.0, 0.0]

        self.angle = 0
        self.target_angle = 0

        self.t = 0

        self.dying = False
        self.dead = False

        self.frame = 0

    def update(self):
        self.t += 1

        if not self.dying:
            if self.t % 3 == 0:
                self.frame += 1
                if self.frame >= len(Seagull.animation):
                    self.frame = 0

        self.rect.left += self.vect[0]
        self.rect.top += self.vect[1]

        #if (self.t / 3) % len(Seagull.animation) == 2:
        #self.vect[1] -= 5.0

        #if self.angle != self.target_angle:
        self.update_angle(self.angle * 0.8 + self.target_angle * 0.2)

        if self.dying:
            self.vect[1] += 1.0
            if not self.rect.colliderect(self.area):
                self.dead = True

    def update_angle(self, angle):
        self.angle = angle
        # seagulls look best when they are sharp
        #~ self.image = util.rotate(Seagull.animation[self.frame], self.angle)
        self.image = pygame.transform.rotate(Seagull.animation[self.frame], self.angle)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        #self.hitmask = pygame.surfarray.array_alpha(self.image)

    def die(self):
        if (Variables.sound):
           Seagull.death_sound.play()
        self.target_angle = 90
        self.dying = True
        self.vect = [0.0, -3.0]
