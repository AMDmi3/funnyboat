import pygame
import pygame
import math
import random
import sys
import os

import PixelPerfect

from pygame.locals import *

from shark import Shark
from health import Health
from cannonball import Cannonball
from steamboat import Steamboat
from particles import Particles
from mine import Mine
from score import Score
from water import Water
from pirateboat import Pirateboat
from seagull import Seagull
from level import Level
from titanic import Titanic
from powerup import Powerup

import cloud

import util

from locals import *

rr=random.random

def rrr(left,right):
    return left+rr()*(right-left)
    
class Game:
    sky = None
    
    
    
        

    def __init__(self, screen, endless = False):
        self.screen = screen

        self.sharks = []
        self.shark_sprites = pygame.sprite.Group()

        self.player = Steamboat()
        self.player_sprite = pygame.sprite.Group()
        self.player_sprite.add(self.player)

        self.health = Health()
        self.health_sprite = pygame.sprite.Group()
        self.health_sprite.add(self.health)

        self.damage_count = 0

        self.t = 0

        self.water = Water.global_water
        #Water.global_water = self.water
        self.water_sprite = pygame.sprite.Group()
        self.water_sprite.add(self.water)

        if not Game.sky:
            Game.sky = util.load_image("taivas")
            Game.sky = pygame.transform.scale(self.sky, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.cannonballs = []
        self.cannonball_sprites = pygame.sprite.Group()

        self.pirates = []
        self.pirate_sprites = pygame.sprite.Group()

        self.titanic = None
        self.titanic_sprite = pygame.sprite.Group()

        self.seagulls = []
        self.seagull_sprites = pygame.sprite.Group()

        self.particles = Particles()
        self.particle_sprite = pygame.sprite.Group()
        self.particle_sprite.add(self.particles)

        self.mines = []
        self.mine_sprites = pygame.sprite.Group()

        self.score = Score()
        self.score_sprite = pygame.sprite.Group()
        self.score_sprite.add(self.score)

        self.powerups = []
        self.powerup_sprites = pygame.sprite.Group()

        self.level = Level(endless)

        self.lastshot = MIN_FIRE_DELAY + 1

        self.gameover = False
        self.gameover_image = None
        self.gameover_rect = None
        self.done = False

        self.pause = False
        self.pause_image = util.bigfont.render("Pause", Variables.alpha, (0,0,0))
        self.pause_rect = self.pause_image.get_rect()
        self.pause_rect.center = self.screen.get_rect().center

        self.spacepressed = None

    def run(self):
        while not self.done:
            if not self.pause:
                if not self.gameover:
                    self.spawn_enemies()

                self.update_enemies()
                self.player.update()
                self.health.update()
                cloud.update()
                for cb in self.cannonballs:
                    if not cb.underwater:
                        #~ particle_point=cb.rect.left, cb.rect.top
                        particle_point = cb.tail_point()
                        self.particles.add_trace_particle(particle_point)
                        particle_point = [particle_point[i] + cb.vect[i]/2 for i in (0,1)]
                        self.particles.add_trace_particle(particle_point)
                    if cb.special and (not cb.underwater or rr()>0.6) :
                        particle_point = cb.tail_point()
                        self.particles.add_explosion_particle(particle_point)
                    und_old=cb.underwater
                    cb.update()
                    if cb.underwater and not und_old:
                        for i in xrange(5):
                            particle_point=cb.rect.right-4.0+rr()*8.0, cb.rect.top+rr()*2.0
                            self.particles.add_water_particle(particle_point)
                    if (cb.rect.right < 0 and cb.vect[0] < 0) or (cb.rect.left > SCREEN_WIDTH and cb.vect[0] > 0) or (cb.rect.top > SCREEN_HEIGHT):
                        self.cannonballs.remove(cb)
                        self.cannonball_sprites.remove(cb)
                self.score.update()

                # Add steam particles
                if Variables.particles:
                    particle_point = self.player.get_point((5.0 + rr() * 9.0, 0))
                    particle_point[0] += self.player.rect.centerx
                    particle_point[1] += self.player.rect.centery
                    if self.spacepressed and self.t > self.spacepressed + FPS * 3:
                        pass
                        #~ self.particles.add_fire_steam_particle(particle_point)
                    else:
                        self.particles.add_steam_particle(particle_point)

                    particle_point = self.player.get_point((19.0 + rr() * 7.0, 5.0))
                    particle_point[0] += self.player.rect.centerx
                    particle_point[1] += self.player.rect.centery
                    if self.spacepressed and self.t > self.spacepressed + FPS * 3:
                        pass
                        #~ self.particles.add_fire_steam_particle(particle_point)
                    else:
                        self.particles.add_steam_particle(particle_point)

                    if self.titanic:
                        for j in xrange(4):
                            particle_point = self.titanic.get_point((49 + rr() * 9.0 + 28 * j, 25))
                            particle_point[0] += self.titanic.rect.centerx
                            particle_point[1] += self.titanic.rect.centery
                            self.particles.add_steam_particle(particle_point)

                    self.particles.update()

                self.water.update()

                if self.player.splash:
                    if Variables.particles:
                        for i in xrange(10):
                            r = rr()
                            x = int(r * self.player.rect.left + (1.0-r) * self.player.rect.right)
                            point = (x, self.water.get_water_level(x))
                            self.particles.add_water_particle(point)
    
                for powerup in self.powerups:
                    powerup.update()
                    if powerup.picked:
                        self.powerups.remove(powerup)
                        self.powerup_sprites.remove(powerup)

                if not self.gameover:
                    self.check_collisions()

                if self.health.hearts_left == 0 and not self.player.dying:
                    self.player.die()

                if self.player.dying and not self.player.dead:
                    if Variables.particles:
                        self.particles.add_explosion_particle((self.player.rect.centerx, self.player.rect.centery))
                        self.particles.add_debris_particle((self.player.rect.centerx, self.player.rect.centery))

                if self.player.dead:
                    #self.done = True
                    self.set_gameover()

                if self.damage_count > 0:
                    self.damage_count -= 1
                self.lastshot += 1
                self.t += 1

            self.draw()

            self.handle_events()

        return self.score.get_score()

    def damage_player(self):
        self.health.damage()
        for i in xrange(10):
            particle_point = self.player.get_point((rr() * 26.0, rr() * 10.0))
            particle_point[0] += self.player.rect.centerx
            particle_point[1] += self.player.rect.centery
            self.particles.add_debris_particle(particle_point)
        self.player.blinks+=12


    def set_gameover(self, message = "Game Over"):
        self.gameover = True
        images = []
        height = 0
        width = 0
        for text in message.split("\n"):
            images.append(util.bigfont.render(text, Variables.alpha, (0,0,0)))
            height += images[-1].get_height()
            if images[-1].get_width() > width:
                width = images[-1].get_width()
        self.gameover_image = pygame.Surface((width, height), SRCALPHA, 32)
        self.gameover_image.fill((0,0,0,0))
        for i in xrange(len(images)):
            rect = images[i].get_rect()
            rect.top = i * images[i].get_height()
            rect.centerx = width / 2
            self.gameover_image.blit(images[i], rect)

        self.gameover_rect = self.gameover_image.get_rect()
        self.gameover_rect.center = self.screen.get_rect().center

    def take_screenshot(self):
        i = 1
        filename = "sshot.tga"
        while os.path.exists(filename):
            i += 1
            filename = "sshot" + str(i) + ".tga"
        
        pygame.image.save(self.screen, filename)
        print "Screenshot saved as " + filename

    def handle_events(self):
        nextframe = False
        framecount = 0
        while not nextframe:
          # wait until there's at least one event in the queue
          #nextframe = True
          pygame.event.post(pygame.event.wait())
          for event in pygame.event.get():
            #event = pygame.event.wait()
            if event.type == QUIT or \
               event.type == KEYDOWN and event.key == K_ESCAPE:
                self.done = True
                nextframe = True
            elif event.type == NEXTFRAME:
                framecount += 1
                nextframe = True
            elif self.gameover:
                if event.type == JOYBUTTONDOWN:
                    self.done = True
                    nextframe = True
                elif event.type == KEYDOWN:
                    self.done = True
                    nextframe = True
                continue
            elif event.type == JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.5:
                        self.player.move_left(True)
                    elif event.value > 0.5:
                        self.player.move_right(True)
                    else:
                        self.player.move_left(False)
                        self.player.move_right(False)
            elif event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    if not self.pause:
                        self.player.jump()
                elif event.button == 1:
                    if not self.pause:
                        if self.lastshot > MIN_FIRE_DELAY and not self.player.dying:
                            cb = Cannonball(self.player.rect, self.player.angle)
                            self.cannonballs.append(cb)
                            self.cannonball_sprites.add(cb)
                            particle_point = self.player.get_point((42.0,10.0))
                            particle_point[0] += self.player.rect.centerx
                            particle_point[1] += self.player.rect.centery
                            for i in xrange(4):
                                self.particles.add_fire_steam_particle(particle_point)
                            self.lastshot = 0
                            self.spacepressed = self.t
                elif event.button == 5:
                    self.take_screenshot()
                elif event.button == 8:
                    self.set_pause()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.player.move_left(True)
                elif event.key == K_RIGHT:
                    self.player.move_right(True)
                elif event.key == K_SPACE:
                    if not self.pause:
                    # Only 3 cannonballs at once
                    # Maximum firing rate set at the top
                        if self.lastshot > MIN_FIRE_DELAY and not self.player.dying:
                            cb = Cannonball(self.player.rect, self.player.angle)
                            self.cannonballs.append(cb)
                            self.cannonball_sprites.add(cb)
                            particle_point = self.player.get_point((42.0,10.0))
                            particle_point[0] += self.player.rect.centerx
                            particle_point[1] += self.player.rect.centery
                            for i in xrange(4):
                                self.particles.add_fire_steam_particle(particle_point)
                            self.lastshot = 0
                            self.spacepressed = self.t
                elif event.key == K_UP:
                    if not self.pause:
                        self.player.jump()
                elif event.key == K_s:
                    self.take_screenshot()
                elif event.key == K_p:
                    self.set_pause()
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.player.move_left(False)
                elif event.key == K_RIGHT:
                    self.player.move_right(False)
                elif event.key == K_SPACE:
                    if not self.pause:
                        if self.spacepressed and self.t > self.spacepressed + FPS * 3 and not self.player.dying:
                            cb = Cannonball(self.player.rect, self.player.angle, special=True)
                            self.cannonballs.append(cb)
                            self.cannonball_sprites.add(cb)
                            particle_point = self.player.get_point((42.0,10.0))
                            particle_point[0] += self.player.rect.centerx
                            particle_point[1] += self.player.rect.centery
                            for i in xrange(30):
                                self.particles.add_fire_steam_particle((particle_point[0]+rrr(-4,4),particle_point[1]+rrr(-3,3)))
                            self.lastshot = 0
                        self.spacepressed = None
            elif event.type == JOYBUTTONUP:
                if event.button == 1:
                    if not self.pause:
                        if self.spacepressed and self.t > self.spacepressed + FPS * 3 and not self.player.dying:
                            cb = Cannonball(self.player.rect, self.player.angle, special=True)
                            self.cannonballs.append(cb)
                            self.cannonball_sprites.add(cb)
                            particle_point = self.player.get_point((42.0,10.0))
                            particle_point[0] += self.player.rect.centerx
                            particle_point[1] += self.player.rect.centery
                            for i in xrange(30):
                                self.particles.add_fire_steam_particle((particle_point[0]+rrr(-4,4),particle_point[1]+rrr(-3,3)))
                            self.lastshot = 0
                        self.spacepressed = None

        #if framecount > 1:
        #    print str(self.t) + ": missed " + str(framecount - 1) + " frames!"

    def set_pause(self):
        self.pause = not self.pause

        #if framecount > 1:
        #    print str(self.t) + ": missed " + str(framecount - 1) + " frames!"

    def set_pause(self):
        self.pause = not self.pause

    def draw(self):
        self.screen.blit(Game.sky, self.screen.get_rect())
        self.health_sprite.draw(self.screen)
        self.score_sprite.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.powerup_sprites.draw(self.screen)
        self.pirate_sprites.draw(self.screen)
        if self.titanic:
            self.titanic_sprite.draw(self.screen)
        self.seagull_sprites.draw(self.screen)
        cloud.draw(self.screen)
        self.shark_sprites.draw(self.screen)
        self.mine_sprites.draw(self.screen)
        self.cannonball_sprites.draw(self.screen)
        self.water_sprite.draw(self.screen)
        if Variables.particles:
            self.particle_sprite.draw(self.screen)

        if self.pause:
            self.screen.blit(self.pause_image, self.pause_rect)

        if self.gameover:
            self.screen.blit(self.gameover_image, self.gameover_rect)

        if self.level.t < 120:
            image = None
            i = 0
            if self.level.phase < len(self.level.phase_messages):
              for text in self.level.phase_messages[self.level.phase].split("\n"):
                image = util.smallfont.render(text, Variables.alpha, (0,0,0))
                rect = image.get_rect()
                rect.centerx = self.screen.get_rect().centerx
                rect.top = 100 + rect.height * i
                blit_image = pygame.Surface((image.get_width(), image.get_height()))
                blit_image.fill((166,183,250))
                blit_image.set_colorkey((166,183,250))
                blit_image.blit(image, image.get_rect())
                if self.level.t > 60:
                    blit_image.set_alpha(255 - (self.level.t - 60) * 255 / 60)
                self.screen.blit(blit_image, rect)
                i += 1

        pygame.display.flip()



    def check_collisions(self):
        collisions = PixelPerfect.spritecollide_pp(self.player, self.powerup_sprites, 0)
        for powerup in collisions:
            if not powerup.fading:
                if not self.player.dying:
                    self.health.add()
                    powerup.pickup()

        collisions = PixelPerfect.spritecollide_pp(self.player, self.mine_sprites, 0)

        for mine in collisions:
            if not mine.exploding:
                if not self.player.dying:
                    self.damage_player()
                    mine.explode()

        collisions = PixelPerfect.spritecollide_pp(self.player, self.shark_sprites, 0)

        for shark in collisions:
            if not shark.dying:
                if not self.player.dying:
                    self.damage_player()
                    shark.die()

        collisions = PixelPerfect.spritecollide_pp(self.player, self.cannonball_sprites, 0)

        for cb in collisions:
            if not self.player.dying:
                self.damage_player()
                self.cannonballs.remove(cb)
                self.cannonball_sprites.remove(cb)
                if (Variables.sound):
                   Mine.sound.play() # Umm... the mine has a nice explosion sound.

        collisions = PixelPerfect.groupcollide_pp(self.cannonball_sprites, self.shark_sprites, 0, 0)

        for cb in dict.keys(collisions):
            for shark in collisions[cb]:
                # The test on cb.vect is a rude hack preventing cannonballs from pirate ships from killing sharks.
                if not shark.dying and cb.vect[0] > 0:
                    self.score.add(15)
                    shark.die()
                    # give her a part of ball's momentum:
                    shark.dx+=cb.vect[0]*0.6
                    shark.dy+=cb.vect[1]*0.4
                    if not cb.special:
                        self.cannonballs.remove(cb)
                        self.cannonball_sprites.remove(cb)
                    break

        collisions = PixelPerfect.groupcollide_pp(self.cannonball_sprites, self.seagull_sprites, 0, 0)

        for cb in dict.keys(collisions):
            for seagull in collisions[cb]:
                # cb.vect test is a rude hack preventing pirates from killing seagulls
                if not seagull.dying and cb.vect[0] > 0:
                    self.score.add(75)
                    seagull.die()
                    # give her a part of ball's momentum:
                    seagull.vect[0]+=cb.vect[0]*0.4
                    seagull.vect[1]+=cb.vect[1]*0.4
                    if not cb.special:
                        self.cannonballs.remove(cb)
                        self.cannonball_sprites.remove(cb)
                    break

        collisions = PixelPerfect.groupcollide_pp(self.cannonball_sprites, self.pirate_sprites, 0, 0)

        for cb in dict.keys(collisions):
            for pirate in collisions[cb]:
                # cb.vect hack for preventing pirates from killing each other
                if not pirate.dying and cb.vect[0] > 0:
                    if (Variables.sound):
                       Mine.sound.play() # Umm... the mine has a nice sound.
                    self.score.add(25)
                    pirate.damage()
                    for i in range(6):
                        self.particles.add_wood_particle((pirate.rect.centerx+rrr(-0,15), pirate.rect.centery+rrr(-10,20)))
                    if not cb.special:
                        self.cannonballs.remove(cb)
                        self.cannonball_sprites.remove(cb)
                    break

        if self.titanic:
            collisions = PixelPerfect.spritecollide_pp(self.titanic, self.cannonball_sprites, 0)
            for cb in collisions:
                if not self.titanic.dying and cb.vect[0] > 0:
                    if (Variables.sound):
                       Mine.sound.play()
                    if cb.special: 
                        #special round is hard to fire, so lets reward our crafty player
                        self.titanic.damage(12)
                        self.score.add(100)
                    else:
                        self.score.add(7)
                        self.titanic.damage()
                    self.cannonballs.remove(cb)
                    self.cannonball_sprites.remove(cb)
                    break

    def update_enemies(self):
        self.mine_sprites.update()
        for mine in self.mines:
            if mine.exploding:
                if mine.explode_frames == 0:
                    self.mines.remove(mine)
                    self.mine_sprites.remove(mine)
                # this should really be done in the Mine class, but oh well, here's some explosion effects:
                if Variables.particles:
                    self.particles.add_explosion_particle((mine.rect.centerx, mine.rect.top + mine.image.get_rect().centerx))
                    self.particles.add_debris_particle((mine.rect.centerx, mine.rect.top + mine.image.get_rect().centerx))
            if mine.rect.right < self.screen.get_rect().left:
                self.mines.remove(mine)
                self.mine_sprites.remove(mine)

        self.shark_sprites.update()
        for shark in self.sharks:
            if shark.dying:
                if Variables.particles:
                    self.particles.add_blood_particle(shark.rect.center)
            if shark.rect.right < self.screen.get_rect().left or shark.dead:
                self.sharks.remove(shark)
                self.shark_sprites.remove(shark)

        self.pirate_sprites.update()
        for pirate in self.pirates:
            if pirate.t % 50 == 0 and not pirate.dying:
                # Pirate shoots, this should probably be handled by the Pirateboat class
                cb = Cannonball(pirate.rect, pirate.angle, left = True)
                self.cannonballs.append(cb)
                self.cannonball_sprites.add(cb)
                particle_point = pirate.get_point((0.0,10.0))
                particle_point[0] += pirate.rect.centerx
                particle_point[1] += pirate.rect.centery
                for i in xrange(4):
                    self.particles.add_fire_steam_particle(particle_point)
                
            if pirate.rect.right < self.screen.get_rect().left or pirate.dead:
                self.pirates.remove(pirate)
                self.pirate_sprites.remove(pirate)
            elif pirate.dying:
                if Variables.particles:
                    self.particles.add_explosion_particle((pirate.rect.centerx, pirate.rect.centery))
                    self.particles.add_wood_particle((pirate.rect.centerx, pirate.rect.centery))

        if self.titanic:
            self.titanic.update()
            if self.titanic.t % 100 == 0 and not self.titanic.dying:
                for i in xrange(3):
                    cb = Cannonball(self.titanic.rect, self.titanic.angle + (i-1)*10 - 50, left = True)
                    self.cannonballs.append(cb)
                    self.cannonball_sprites.add(cb)
            elif self.titanic.t % 100 == 50 and not self.titanic.dying:
                for i in xrange(3):
                    cb = Cannonball(self.titanic.rect, self.titanic.angle + (i-1)*10 - 52.5, left = True)
                    self.cannonballs.append(cb)
                    self.cannonball_sprites.add(cb)
            if self.titanic.dead:
                self.set_gameover("Congratulations!\nYou sunk Titanic!")
                self.titanic = None

        self.seagull_sprites.update()
        for seagull in self.seagulls:
            if seagull.rect.right < 0 or seagull.dead:
                self.seagulls.remove(seagull)
                self.seagull_sprites.remove(seagull)

    def spawn_enemies(self):
        spawns = self.level.get_spawns()
        if spawns[Level.SHARKS]:
            # Make a new shark
            self.sharks.append(Shark())
            self.shark_sprites.add(self.sharks[-1])

        if spawns[Level.PIRATES]:
            # Make a new pirate ship
            self.pirates.append(Pirateboat())
            self.pirate_sprites.add(self.pirates[-1])

        if spawns[Level.MINES]:
            self.mines.append(Mine())
            self.mine_sprites.add(self.mines[-1])

        if spawns[Level.SEAGULLS]:
            self.seagulls.append(Seagull())
            self.seagull_sprites.add(self.seagulls[-1])

        if spawns[Level.TITANIC]:
            self.titanic = Titanic()
            self.titanic_sprite.add(self.titanic)

        if spawns[Level.POWERUPS]:
            self.powerups.append(Powerup())
            self.powerup_sprites.add(self.powerups[-1])

