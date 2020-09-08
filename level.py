import pygame
import random

from pygame.locals import *

import util
import random
from water import Water

class Level:
    SHARKS = 0
    PIRATES = 1
    MINES = 2
    SEAGULLS = 3
    TITANIC = 4
    POWERUPS = 5
    def __init__(self, endless = False):
      self.endless = endless
      if not endless:
        self.phase_lengths = [900, 900, 900, 1800, 1300, -1]
        self.phase_messages = [
                               "Watch out for those\nangry sharks, captain!",
                               "Minefield ahead, captain!",
                               "Oh no! It's the infamous fleet\n of pirate Captain Colorbeard!",
                               "",
                               "Uh, oh. Looks like some busy\nwaters ahead, captain!",
                               "Holy cow! It's the\nlegendary Titanic!"]

        colors = ["Brown", "Red", "Yellow", "Magenta", "Pink", "Cyan", "Blue", "Black", "Green", "Violet", "Beige", "White", "Grey", "Blonde", "Orange", "Brunette", "Ginger", "Turquoise"]
        self.phase_weather = [
                                30.0,
                                40.0,
                                20.0,
                                30.0,
                                60.0,
                                5.0]
        self.phase_messages[2] = "Oh no! It's the infamous fleet\nof pirate Captain " + colors[random.randint(0, len(colors) - 1)] + "beard!"
        # This is the big table describing the phases
        # The subtables are different phases, and they have two-celled tables describing
        # how often different enemies appear in the phase. The first number is the offset
        # from the beginning of the phase to when the enemy first appears, and the second
        # one is the delay between new enemies spawning. Both units are in frames, so 30
        # units equals one second in real time
        self.phases = [[[10, 80], # Shark frequency in first phase.
                        [230, 0], # Pirate frequency in first phase.
                        [120, 0], # Mine frequency in first phase.
                        [0, 3000], # Seagull frequency in first phase.
                        [1, 0], # Titanic
                        [450, 1000]
                        ],
                       [[100, 300], # Second phase
                        [257, 0],
                        [70, 137], # Mines this time around
                        [0, 3000],
                        [1, 0],
                        [0, 1000]
                        ],
                       [[257, 500], # Fewer sharks in the third phase
                        [30, 300], # Yarr, tharr be pirates aboot
                        [470, 500], # A few mines too
                        [0, 1500], # Two seagulls
                        [1, 0],
                        [0, 1000]
                        ],
                       [[0, 183], # Middle phase
                        [230, 319],
                        [40, 217],
                        [0, 700],
                        [1, 0],
                        [0, 1000]
                        ],
                       [[0, 233], # Big Kahuna phase
                        [230, 519],
                        [40, 317],
                        [0, 700],
                        [1, 0],
                        [0, 1000]
                        ],
                       [[70, 200], # The boss level, some sharks, a single powerup and Teh Titanic
                        [300, 0],
                        [0, 200],
                        [0, 0],
                        [10, -1], # -1 means that there will only be one Titanic
                        [0, 0]
                        ]
                        ]
      else:
          self.phase_lengths = [450]
          self.phase_messages = ["This is the endless mode.\nGood luck!"]
          self.phase_weather = [30,10,50]
          self.phases = [
                        [
                        [0, 255], # Balanced phase
                        [150, 257],
                        [50, 253],
                        [0, 507],
                        [0, 0], # No Titanic in the endless mode
                        [100, 0]
                        ],
                        [
                        [0, 150], # Lots of sharks
                        [400, 700],
                        [50, 700],
                        [0, 507],
                        [0, 0],
                        [500, 0]
                        ],
                        [
                        [150, 400], # Lots of pirates
                        [0, 150],
                        [350, 500],
                        [0, 507],
                        [0,0],
                        [500, 0]
                        ],
                        [
                        [350, 500], # Lots of mines
                        [150, 400],
                        [20, 150],
                        [0, 507],
                        [0, 0],
                        [100, -1]
                        ]
                       ]
        
      self.phase = 0
      self.t = 0
      self.modifier = 0

    def get_spawns(self):
        phase_length = self.phase_lengths[self.phase % len(self.phase_lengths)]

        if self.endless:
            phase_length -= self.modifier
            if phase_length < 30:
                phase_length = 30

        if phase_length != -1 and self.t > phase_length:
            self.t = 0
            self.phase += 1

        spawns = []

        for enemy in self.phases[self.phase % len(self.phases)]:
            offset, delay = enemy
            if self.endless and delay > 0:
                delay -= self.phase / 4 * 5
                offset -= self.phase / 4 * 5
                if delay <= 30:
                    delay = 30
                if offset < 0:
                    offset = 0
            if (delay == -1 and self.t == offset) or (delay != 0 and self.t % delay == offset):
                spawns.append(True)
            else:
                spawns.append(False)

        if not self.endless:
            Water.global_water.set_amplitude(self.phase_weather[self.phase % len(self.phase_weather)])
        else:
            Water.global_water.set_amplitude(self.phase_weather[(self.phase / 4) % len(self.phase_weather)])


        self.t += 1

        return spawns
