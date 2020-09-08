import pygame
import random
from pygame.locals import *

from locals import *

class Particle (pygame.sprite.Sprite):
    def __init__(self, position, vect, colour, acceleration, size, life, opacity, underwater = True):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(position[0], position[1], size, size)
        self.vect = vect
        self.colour = colour
        self.acceleration = acceleration
        self.initial_life = life
        self.life = life
        self.opacity = opacity
        self.underwater = underwater

        self.image = pygame.Surface([int(size), int(size)])#, SRCALPHA, 32)
        self.image.fill((255,0,255))
        self.image.set_colorkey((255,0,255))

        pygame.draw.ellipse(self.image, self.colour, self.image.get_rect())

        if Variables.alpha:
            self.image.set_alpha(self.life * 255 * self.opacity / self.initial_life)

    def update(self):
        self.rect.left += self.vect[0]
        self.rect.top += self.vect[1]
        self.vect[0] += self.acceleration[0]
        self.vect[1] += self.acceleration[1]
        if self.life > 0:
            self.life -= 1

        if not self.underwater and self.vect[1] > 0.0:
            self.life = 0

        if Variables.alpha:
            self.image.set_alpha(self.life * 255 * self.opacity / self.initial_life)

class Particles (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.particles = []
        self.particle_sprites = pygame.sprite.Group()
        if Variables.alpha:
            self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), SRCALPHA, 32)
        else:
            self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()

    def update(self):
        self.image.fill((255,0,255,0))
        
        self.particle_sprites.draw(self.image)

        for p in self.particles:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)
                self.particle_sprites.remove(p)

    def add_blood_particle(self, position):
        particle = Particle(position, [random.random() * 5 - 2.5, random.random() * 5 - 2.5], [230, 30, 20], [0.0, 0.7], random.random() * 5.0 + 1.0, random.random() * 30, 1.0)
        self.particles.append(particle)
        self.particle_sprites.add(particle)

    def add_explosion_particle(self, position):
        particle = Particle(position, [random.random() * 5 - 2.5, random.random() * 5 - 2.5], [230, 30 + random.random() * 200, 20], [0.0, 0.2], random.random() * 7.0 + 1.0, random.random() * 30, 1.0)
        self.particles.append(particle)
        self.particle_sprites.add(particle)

    def add_water_particle(self, position):
        particle = Particle(position, [random.random() * 5 - 2.5, -random.random() * 2.5 - 2.0], (20,60,180), (0.0, 0.3), random.random() * 5.0 + 1.0, random.random() * 30, 0.5, underwater = False)
        self.particles.append(particle)
        self.particle_sprites.add(particle)

    def add_debris_particle(self, position):
        particle = Particle(position, [random.random() * 5 - 2.5, random.random() * 5 - 2.5], [90, 90, 90], [0.0, 0.2], random.random() * 7.0 + 1.0, random.random() * 30, 1.0)
        self.particles.append(particle)
        self.particle_sprites.add(particle)

    def add_wood_particle(self, position):
        particle = Particle(position, [random.random() * 5 - 2.5, random.random() * 5 - 2.5], [148, 69, 6], [0.0, 0.2], random.random() * 7.0 + 1.0, random.random() * 30, 1.0)
        self.particles.append(particle)
        self.particle_sprites.add(particle)

    def add_steam_particle(self, position):
        particle = Particle(position, [-random.random() * 0.3, -random.random() * 0.1], [240, 240, 240], [-0.1, -0.00002], random.random() * 10.0 + 1.0, random.random() * 30, 0.5)
        self.particles.append(particle)
        self.particle_sprites.add(particle)

    def add_fire_steam_particle(self, position):
        particle = Particle(position, [-random.random() * 0.3, -random.random() * 0.1], [255, 210, 170], [-0.1, -0.00002], random.random() * 11.0 + 1.0, random.random() * 30, 0.4, False)
        self.particles.append(particle)
        self.particle_sprites.add(particle)

    def add_trace_particle(self, position):
        particle = Particle(position, [0.0, 0.0], [170, 170, 170], [0.0, 0.0], 6.0, 5+random.random() * 5, 0.1+random.random()*0.1, False)
        self.particles.append(particle)
        self.particle_sprites.add(particle)
