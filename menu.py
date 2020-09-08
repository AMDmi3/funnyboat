import pygame

from water import Water
from locals import *
import cloud
import util

class Menu:
    logo = None
    sky = None

    def __init__(self, screen, menu, selection = 0):
        self.screen = screen

        if not Menu.sky:
            Menu.sky = util.load_image("taivas")

        self.water = Water.global_water
        self.water_sprite = pygame.sprite.Group()
        self.water_sprite.add(self.water)

        if not Menu.logo:
            Menu.logo = util.load_image("logo")

        self.menu = menu
        self.selection = selection
        self.t = 0

    def run(self):
        done = False

        while not done:
            self.screen.blit(Menu.sky, self.screen.get_rect())
            self.water.update()
            self.water_sprite.draw(self.screen)

            for i in xrange(len(self.menu)):
                self.render(i)

            cloud.update()

            cloud.draw(self.screen)

            rect = Menu.logo.get_rect()
            rect.centerx = self.screen.get_rect().centerx
            rect.top = 0
            self.screen.blit(Menu.logo, rect)

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
                    elif event.type == JOYBUTTONDOWN:
                        if event.button == 0:
                            done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_UP:
                            self.move_up()
                        elif event.key == K_DOWN:
                            self.move_down()
                        elif event.key == K_SPACE or event.key == K_RETURN:
                            done = True

        return self.selection

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
        image = util.bigfont.render(title, Variables.alpha, color)
        rect = image.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.top = Menu.logo.get_height() + id * rect.height * 1.1

        self.screen.blit(image, rect)
