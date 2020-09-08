import pygame
import math
import random

from locals import *

import util

def init():
    Cloud.images = []
    Cloud.images.append(util.load_image("cloud1"))
    Cloud.images.append(util.load_image("cloud2"))
    Cloud.images.append(util.load_image("cloud3"))
    Cloud.images.append(util.load_image("cloud4"))

def update():
    if Cloud.t % 150 == 0:
        Cloud.global_clouds.append(Cloud())
        Cloud.cloud_sprites.add(Cloud.global_clouds[-1])
    for cloud in Cloud.global_clouds:
        cloud.update()
        if cloud.rect.right < 0:
            Cloud.global_clouds.remove(cloud)
            Cloud.cloud_sprites.remove(cloud)

    Cloud.t += 1

def draw(screen):
    Cloud.cloud_sprites.draw(screen)

class Cloud (pygame.sprite.Sprite):
    images = None
    global_clouds = []
    cloud_sprites = pygame.sprite.Group()
    t = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not Cloud.images:
            cloud.init()

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.cloudtype = int(random.random() * len(Cloud.images))

        self.image = Cloud.images[self.cloudtype]

        self.rect = pygame.Rect(SCREEN_WIDTH, random.random()*70, self.image.get_width(), self.image.get_height())
        self.life = 0

        self.dx, self.dy = -1, 0

    def update(self):
        self.rect.top = self.rect.top + self.dy
        self.rect.left = self.rect.left + self.dx
