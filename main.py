 #!/usr/bin/python

import pygame
import math
import random
import sys

import PixelPerfect

from pygame.locals import *

from water import Water
from menu import Menu
from game import Game
from highscores import Highscores
from options import Options

import util

from locals import *

import health
import cloud
import mine
import steamboat
import pirateboat
import shark
import seagull

def init():
    health.init()
    steamboat.init()
    shark.init()
    pirateboat.init()
    cloud.init()
    mine.init()
    seagull.init()

def main():
    global SCREEN_FULLSCREEN
    pygame.init()

    util.load_config()

    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == "-np":
                Variables.particles = False
            elif arg == "-na":
                Variables.alpha = False
            elif arg == "-nm":
                Variables.music = False
            elif arg == "-ns":
                Variables.sound = False
            elif arg == "-f":
                SCREEN_FULLSCREEN = True

    scr_options = 0
    if SCREEN_FULLSCREEN: scr_options += FULLSCREEN
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),scr_options ,32)

    pygame.display.set_icon(util.load_image("kuvake"))
    pygame.display.set_caption("Trip on the Funny Boat")

    init()

    joy = None
    if pygame.joystick.get_count() > 0:
        joy = pygame.joystick.Joystick(0)
        joy.init()

    try:
        util.load_music("JDruid-Trip_on_the_Funny_Boat")
        if Variables.music:
            pygame.mixer.music.play(-1)
    except:
        # It's not a critical problem if there's no music
        pass

    pygame.time.set_timer(NEXTFRAME, 1000 / FPS) # 30 fps

    Water.global_water = Water()

    main_selection = 0

    while True:
        main_selection = Menu(screen, ("New Game", "High Scores", "Options", "Quit"), main_selection).run()
        if main_selection == 0:
            # New Game
            selection = Menu(screen, ("Story Mode", "Endless Mode")).run()
            if selection == 0:
                # Story
                score = Game(screen).run()
                Highscores(screen, score).run()
            elif selection == 1:
                # Endless
                score = Game(screen, True).run()
                Highscores(screen, score, True).run()
        elif main_selection == 1:
            # High Scores
            selection = 0
            while True:
                selection = Menu(screen, ("Story Mode", "Endless Mode", "Endless Online"), selection).run()
                if selection == 0:
                    # Story
                    Highscores(screen).run()
                elif selection == 1:
                    # Endless
                    Highscores(screen, endless = True).run()
                elif selection == 2:
                    # Online
                    Highscores(screen, endless = True, online = True).run()
                else:
                    break
        elif main_selection == 2:
            # Options
            selection = Options(screen).run()
        else: #if main_selection == 3:
            # Quit
            return


if __name__ == '__main__':
    main()
