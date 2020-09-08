import pygame
import math

from locals import *

import util

class Water(pygame.sprite.Sprite):
    global_water = None
    raster_image = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()

        if not Water.raster_image:
            Water.raster_image = util.load_image("rasteri")

        self.water_levels = []
        for i in xrange(self.rect.width):
            self.water_levels.append(0.0)
        self.t = 0


        self.target_amplitude = self.amplitude = SCREEN_HEIGHT / 8.0
        self.target_wavelength = self.wavelength = 0.02 * SCREEN_WIDTH / 2.0 / math.pi
        self.target_speed = self.speed = 0.06 / math.pi / 2.0 * FPS
        self.target_baseheight = self.baseheight = SCREEN_HEIGHT / 24.0 * 8.0

        self.xmul = 2.0 * math.pi / self.wavelength / float(SCREEN_WIDTH)
        self.tmul = math.pi * 2.0 / float(FPS) * self.speed

        self.image=self.image.convert_alpha()
        #~ if Variables.alpha:
            #~ self.image.set_alpha(110)

        self.update()
    
    def update(self):
        self.image.fill((200,210,255,0))
        for x in xrange(self.rect.width):
            h = SCREEN_HEIGHT - (math.sin(x * self.xmul + self.t * self.tmul) * self.amplitude + self.baseheight)
            self.water_levels[x] = h
            h_float,h_int=math.modf(h)
            pygame.draw.line(self.image, (20, 60, 180,110), (x, h_int+1), (x, SCREEN_HEIGHT))
            if Variables.aa:
                self.image.set_at((x,int(h_int)),(20, 60, 180,int(110*(1.0-h_float))))

        if self.target_amplitude != self.amplitude:
            self.amplitude = 0.99 * self.amplitude + 0.01 * self.target_amplitude
        if self.target_wavelength != self.wavelength:
            self.wavelength = 0.99 * self.wavelength + 0.01 * self.target_wavelength
            self.xmul = 2.0 * math.pi / self.wavelength / float(SCREEN_WIDTH)
        if self.target_speed != self.speed:
            self.speed = 0.99 * self.speed + 0.01 * self.target_speed
            self.tmul = math.pi * 2.0 / float(FPS) * self.speed
        if self.target_baseheight != self.baseheight:
            self.baseheight = 0.99 * self.baseheight + 0.01 * self.target_baseheight

        self.t += 1

        if not Variables.alpha:
            self.image.blit(Water.raster_image, self.image.get_rect())
            self.image.set_colorkey((255,0,255))
            

    def get_water_level(self, x):
        if x >= len(self.water_levels):
            return self.water_levels[len(self.water_levels) - 1]
        elif x < 0:
            return self.water_levels[0]
        return self.water_levels[int(x)]
        
    def set_amplitude(self, amplitude):
        self.target_amplitude = amplitude

    def set_wavelength(self, wavelength):
        self.target_wavelength = wavelength

    def set_speed(self, speed):
        self.target_speed = speed

    def set_baseheight(self, baseheight):
        self.target_baseheight = baseheight
