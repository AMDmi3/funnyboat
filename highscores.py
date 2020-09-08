import pygame
import os
import sys
import codecs

import util
from locals import *
from water import Water

import cloud

class Highscores:
    sky = None
    def __init__(self, screen, new_score = -1, endless = False, online = False):
        self.screen = screen

        if not endless:
            self.title = util.bigfont.render("Story Mode", True, (0,0,0))
        elif not online:
            self.title = util.bigfont.render("Endless Mode", True, (0,0,0))
        else:
            self.title = util.bigfont.render("Endless Online", True, (0,0,0))

        if not Highscores.sky:
            Highscores.sky = util.load_image("taivas")
            Highscores.sky = pygame.transform.scale(Highscores.sky, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.inputting = False
        self.input_score = -1 

        self.scores = []
        self.done = False

        self.endless = endless

        if online:
            if not self.online_init():
               self.done = True
               print "Could not get online highscores!"
            return

        self.pathname = util.get_config_path()
        if not endless:
            self.filename = self.pathname + "/scores"
        else:
            self.filename = self.pathname + "/endless_scores"

        try:
            if not os.path.exists(self.pathname):
                os.mkdir(self.pathname)
        except:
            print "Can't make directory " + self.pathname
            self.done = True
            return

        if not os.path.exists(self.filename):
            #print "Creating dummy high scores"
            self.dummy_scores()
        else:
            try:
                f = codecs.open(self.filename, "r", "utf_8")
                i = 0
                name, score = "", 0
                for line in f:
                    if i % 2 == 0:
                        name = line.strip()
                    else:
                        try:
                            score = int(line)
                        except:
                            print "Corrupt high score file."
                            self.dummy_scores()
                            break
                        self.scores.append((name, score))
                    i += 1
            except:
                self.dummy_scores()
                print "Can't open file " + self.filename + " or file corrupt"

        if len(self.scores) < 10:
            print "Corrupt high score file."
            self.dummy_scores()

        # The online highscore is always submitted
        if endless and new_score != -1:
            self.submit_score(Variables.name, new_score)

        if new_score > self.scores[9][1]:
            #print "It's a new high score!"
            #self.inputting = True
            for i in xrange(10):
                if self.scores[i][1] < new_score:
                    self.input_score = i
                    for j in xrange(9 - i):
                        self.scores[9 - j] = self.scores[8 - j]
                    self.scores[i] = [Variables.name, new_score]
                    break

            self.write_scores()

    def online_init(self):
        HIGHSCORE_URL = "http://funnyboat.sourceforge.net/cgi-bin/top10.py"
        try:
            import socket
            socket.setdefaulttimeout(20)
            import urllib2
            f = urllib2.urlopen(HIGHSCORE_URL)
            for line in f.readlines():
                name,score = line.split("\t")
                score = int(score)
                name = unicode(name, "utf-8")
                self.scores.append((name,score))
            f.close()
        except:
            # Getting highscores failed
            return False
        # Success
        return True

    def submit_score(self, name, score):
            SUBMIT_URL = "http://funnyboat.sourceforge.net/cgi-bin/submit.py"
            try:
                import socket
                socket.setdefaulttimeout(20)
                import urllib
                import urllib2
                #name,score = self.scores[self.input_score]
                data = urllib.urlencode({'name' : name.encode('utf-8'), 'score' : score})
                req = urllib2.Request(SUBMIT_URL, data)
                f = urllib2.urlopen(req)
                f.close()
            except:
                print "Failed to submit highscore"

    def run(self):
        water = Water.global_water
        water.set_amplitude(SCREEN_HEIGHT / 8.0)
        water_sprite = pygame.sprite.Group()
        water_sprite.add(water)
        while not self.done:
            self.screen.blit(Highscores.sky, self.screen.get_rect())
            water.update()
            cloud.update()
            cloud.draw(self.screen)
            water_sprite.draw(self.screen)

            rect = self.title.get_rect()
            rect.centerx = self.screen.get_rect().centerx
            rect.top = 10

            self.screen.blit(self.title, rect)

            for i in xrange(10):
                color = (0,0,0)
                #if self.inputting and self.input_score == i:
                if self.input_score == i:
                    color = (220, 120, 20)
                score = self.scores[i]
                image = 0
                try:
                    image = util.smallfont.render(str(i + 1) + ". " + score[0], True, color)
                except:
                    image = util.smallfont.render(str(i + 1) + ". Error", True, color)
                rect = image.get_rect()
                rect.top = 50 + i * 1.5 * rect.height
                rect.left = 10
                self.screen.blit(image, rect)

                image = util.smallfont.render(str(score[1]), True, color)
                rect = image.get_rect()
                rect.top = 50 + i * 1.5 * rect.height
                rect.right = self.screen.get_rect().right - 10
                self.screen.blit(image, rect)

            pygame.display.flip()

            nextframe = False
            while not nextframe:
                pygame.event.post(pygame.event.wait())
                for event in pygame.event.get():
                    if event.type == NEXTFRAME:
                        nextframe = True
                        continue
                    if self.inputting:
                        if event.type == QUIT:
                            self.inputting = False
                            self.write_scores()
                        if event.type == KEYDOWN:
                            if event.key == K_RETURN or event.key == K_ESCAPE:
                                self.inputting = False
                                if self.endless:
                                    self.submit_score()
                                self.write_scores()
                            elif event.key == K_BACKSPACE:
                                if len(self.scores[self.input_score][0]) != 0:
                                    self.scores[self.input_score][0] = self.scores[self.input_score][0][:-1]
                            elif event.key == K_SPACE or event.unicode != " ":
                                if len(self.scores[self.input_score][0]) < 32:
                                    self.scores[self.input_score][0] += event.unicode
                    else:
                        if event.type == KEYDOWN or event.type == QUIT or event.type == JOYBUTTONDOWN:
                            self.done = True
                            nextframe = True

    def dummy_scores(self):
        self.scores = []
        self.scores.append(("Funny Boat",     2000)) # 1
        self.scores.append(("Hectigo",        1500)) # 2
        self.scores.append(("JDruid",         1000)) # 3
        self.scores.append(("Pekuja",          750)) # 4
        self.scores.append(("Pirate",          500)) # 5
        self.scores.append(("Shark",           400)) # 6
        self.scores.append(("Seagull",         300)) # 7
        self.scores.append(("Naval mine",      200)) # 8
        self.scores.append(("Cannonball",      100)) # 9
        self.scores.append(("Puffy the Cloud",  50)) #10

        self.write_scores()

    def write_scores(self):
        try:
            f = codecs.open(self.filename, "w", "utf_8")
            for i in xrange(10):
                print >> f, self.scores[i][0]
                print >> f, self.scores[i][1]
        except:
            print "Failed to write high scores to file " + self.filename
            self.done = True
            return
