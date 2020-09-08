import pygame

from locals import *

import util

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.score = 0
        self.target_score = 0

        self.image = util.smallfont.render("Score: 0", Variables.alpha, (10,10,10))

        self.rect = self.image.get_rect()
        self.rect.left = 100
        self.rect.top = 5

    def update(self):
        if self.target_score > self.score:
            self.score += 1
            self.image = util.smallfont.render("Score: " + str(self.score), Variables.alpha, (10,10,10))
            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()

    def add(self, points):    
        self.target_score += points
        self.update()

    def get_score(self):
        return self.target_score
