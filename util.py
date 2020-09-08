import pygame
import codecs
import os
from locals import *

# Some general utility functions here

pygame.font.init()

# The Cosmetica font seemed to be broken... had trouble rendering small text
# with underscores (_) ... it's weird.
smallfont = pygame.font.Font("data/Vera.ttf", 14)
bigfont = pygame.font.Font("data/Vera.ttf", 24)

def get_config_path():
    pathname = ""
    try:
        pathname = os.environ["HOME"] + "/.funnyboat"
    except:
        try:
            pathname = os.environ["APPDATA"] + "/Funny Boat"
        except:
            print "Couldn't get environment variable for home directory"
            pathname = "."
    if not os.path.exists(pathname):
        os.mkdir(pathname)
    return pathname

def str_to_bool(text):
    ltext = text.lower().strip()
    if ltext in ("on", "true", "yes"):
        return True
    else:
        return False

def load_config():
    filename = get_config_path() + "/config"
    if not os.path.exists(filename):
        return
    f = codecs.open(filename, "r", "utf_8")

    for line in f.readlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        variable,value = parts
        variable = variable.lower()
        if variable == "alpha":
            pass        
            # This is disabled because it's no longer in the in-game options
            # and it seems to be acting up in weird ways, so it's better
            # to just ditch it. The code is littered with it still, so I'm
            # not completely removing the variable yet.
            #Variables.alpha = str_to_bool(value)
        elif variable == "particles":
            Variables.particles = str_to_bool(value)
        elif variable == "music":
            Variables.music = str_to_bool(value)
        elif variable == "name":
            Variables.name = value.strip()[:32]
        elif variable == "sound":
            Variables.sound = str_to_bool(value)
        elif variable == "aa":
            Variables.aa = str_to_bool(value)

    f.close()

def save_config():
    filename = get_config_path() + "/config"
    if not os.path.exists(get_config_path()):
        os.mkdir(get_config_path())
    f = codecs.open(filename, "w", "utf_8")

    print >> f, "alpha\t%s" % Variables.alpha
    print >> f, "particles\t%s" % Variables.particles
    print >> f, "music\t%s" % Variables.music
    print >> f, "name\t%s" % Variables.name
    print >> f, "sound\t%s" % Variables.sound
    print >> f, "aa\t%s" % Variables.aa

    f.close()

def load_image(name):
    image = pygame.image.load("data/" + name + ".png").convert_alpha()
    if not Variables.alpha:
        # this is kinda not useful. you can't even get Variables.alpha set
        # without modifying the config file by hand
        # in case someone does, at least it won't crash the game if they don't
        # have Numeric installed
        w,h = image.get_size()
        for i in xrange(w):
            for j in xrange(h):
                pixel = image.get_at((i,j))
                if pixel[3] > 127:
                    image.set_at((i,j), (pixel[0], pixel[1], pixel[2], 255))
                else:
                    image.set_at((i,j), (pixel[0], pixel[1], pixel[2], 0))
        #surfarray = pygame.surfarray.pixels_alpha(image)
        #for i in xrange(len(surfarray)):
        #    for j in xrange(len(surfarray[i])):
        #        if surfarray[i][j] > 127:
        #            surfarray[i][j] = 255
        #        else:
        #            surfarray[i][j] = 0

    return image

def load_sound(name):
    return pygame.mixer.Sound("data/" + name + ".ogg")

def load_music(name):
    # The all-caps ogg is because the original file just happened to be that way
    pygame.mixer.music.load("data/" + name + ".ogg")

def rotate(surf, angle):
    if Variables.aa:
        return pygame.transform.rotozoom(surf, angle, 1.0)
    else:
        return pygame.transform.rotate(surf, angle)

