import pygame

from water import Water
from locals import *
import cloud
import util

class Options:
    logo = None
    sky = None

    PARTICLES = 0
    AA = 1
    SOUND = 2
    MUSIC = 3
    NAME = 4

    def __init__(self, screen):
        self.screen = screen

        if not Options.sky:
            Options.sky = util.load_image("taivas")
            Options.sky = pygame.transform.scale(Options.sky, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.water = Water.global_water
        self.water_sprite = pygame.sprite.Group()
        self.water_sprite.add(self.water)

        if not Options.logo:
            Options.logo = util.load_image("logo")

        self.menu = ()
        self.refresh() # sets self.menu
        self.selection = 0
        self.t = 0

    def refresh(self):
        self.menu = ("Particle effects: " + (Variables.particles and "on" or "off"),
                     "Antialiasing: " + (Variables.aa and "on" or "off"),
                     "Sound effects: " + (Variables.sound and "on" or "off"),
                     "Music: " + (Variables.music and "on" or "off"),
                     "Player Name: " + Variables.name)

    def run(self):
        done = False

        while not done:
            self.screen.blit(Options.sky, self.screen.get_rect())
            self.water.update()
            self.water_sprite.draw(self.screen)

            for i in xrange(len(self.menu)):
                self.render(i)

            cloud.update()

            cloud.draw(self.screen)

            rect = Options.logo.get_rect()
            rect.centerx = self.screen.get_rect().centerx
            rect.top = 0
            self.screen.blit(Options.logo, rect)

            image = util.smallfont.render("http://funnyboat.sourceforge.net/", True, (0,0,0))
            rect = image.get_rect()
            rect.midbottom = self.screen.get_rect().midbottom
            self.screen.blit(image, rect)

            pygame.display.flip()

            self.t += 1

            nextframe = False
            while not nextframe:
                pygame.event.post(pygame.event.wait())
                for event in pygame.event.get():
                    if event.type == QUIT or \
                        event.type == KEYDOWN and event.key == K_ESCAPE:
                        self.selection = -1
                        done = True
                        nextframe = True
                    elif event.type == NEXTFRAME:
                        nextframe = True
                    elif event.type == JOYAXISMOTION:
                        if event.axis == 1:
                            if event.value < -0.5:
                                self.move_up()
                            if event.value > 0.5:
                                self.move_down()
                        elif event.axis == 0:
                            if event.value < -0.5:
                                self.change_left()
                            if event.value > 0.5:
                                self.change_right()
                    elif event.type == JOYBUTTONDOWN:
                        if event.button == 0:
                            #done = True
                            self.change_right()
                        elif event.button == 1:
                            done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_UP:
                            self.move_up()
                        elif event.key == K_DOWN:
                            self.move_down()
                        elif event.key == K_LEFT:
                            self.change_left()
                        elif event.key == K_RIGHT:
                            self.change_right()
                        elif self.selection == Options.NAME:
                            if event.key == K_BACKSPACE:
                                if len(Variables.name) != 0:
                                    Variables.name = Variables.name[:-1]
                            elif event.key == K_SPACE or event.unicode != " " and event.unicode>=u' ':
                                if len(Variables.name) < 32:
                                    Variables.name += event.unicode
                            self.refresh()
                        elif event.key == K_SPACE or event.key == K_RETURN:
                            #done = True
                            self.change_right()

        util.save_config()
        return self.selection

    def change_left(self):
        if self.selection == Options.PARTICLES:
            Variables.particles = not Variables.particles
        if self.selection == Options.AA:
            Variables.aa = not Variables.aa
        elif self.selection == Options.SOUND:
            Variables.sound = not Variables.sound
        elif self.selection == Options.MUSIC:
            Variables.music = not Variables.music
            try:
                if Variables.music:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
            except:
                pass
        self.refresh()

    def change_right(self):
        # They're all bools right now, so...
        self.change_left()

    def move_down(self):
        self.selection += 1
        if self.selection >= len(self.menu):
            self.selection = len(self.menu) - 1

    def move_up(self):
        self.selection -= 1
        if self.selection < 0:
            self.selection = 0

    def render(self, id):
        color = (0,0,0)
        if self.selection == id:
            color = (220, 120, 20)

        title = self.menu[id]
        image = util.smallfont.render(title, Variables.alpha, color)
        rect = image.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.top = Options.logo.get_height() + id * rect.height * 1.1

        self.screen.blit(image, rect)
