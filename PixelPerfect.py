import pygame
from pygame.locals import *

def _pixelPerfectCollisionDetection(sp1,sp2):
    """
    Internal method used for pixel perfect collision detection.
    """
    rect1 = sp1.rect;     
    rect2 = sp2.rect;                            
    rect  = rect1.clip(rect2)
                    
    #hm1 = sp1.hitmask
    #hm2 = sp2.hitmask
            
    x1 = rect.x-rect1.x
    y1 = rect.y-rect1.y
    x2 = rect.x-rect2.x
    y2 = rect.y-rect2.y

    for r in xrange(0,rect.height):      
        for c in xrange(0,rect.width):
            # I changed this for the 1.5 release of Funny Boat,
            # because generating hitmasks is a bit problematic
            # now that Numeric is outdated and surfarrays don't work.
            # It's not an optimal solution, but is good enough for
            # this game.

            #if hm1[c+x1][r+y1] & hm2[c+x2][r+y2]:
            if sp1.image.get_at((c+x1, r+y1))[3] & sp2.image.get_at((c+x2, r+y2))[3]:
                return 1        

    return 0

def spritecollide_pp(sprite, group, dokill):
    """pygame.sprite.spritecollide_pp(sprite, group, dokill) -&gt; list
       pixel perfect collision detection between sprite and group

       given a sprite and a group of sprites, this will
       return a list of all the sprites that intersect
       the given sprite.
       all sprites must have a "hitmap" value, which is a 2d array 
       that contains a value larger than zero for all pixels that 
       can collide. the "hitmap" 2d array can be set by using 
       pygame.surfarray.array_colorkey() or pygame.surfarray.array_alpha(). 
       all sprites must have a "rect" value, which is a
       rectangle of the sprite area.if the dokill argument
       is true, the sprites that do collide will be
       automatically removed from all groups."""
    crashed = []
    spritecollide = sprite.rect.colliderect
    ppcollide = _pixelPerfectCollisionDetection
    if dokill:
        for s in group.sprites():
            if spritecollide(s.rect):
                if ppcollide(sprite,s):
                    s.kill()
                    crashed.append(s)
    else:
        for s in group.sprites():
            if spritecollide(s.rect):
                if ppcollide(sprite,s):
                    crashed.append(s)
    return crashed


def groupcollide_pp(groupa, groupb, dokilla, dokillb):
    """pygame.sprite.groupcollide_pp(groupa, groupb, dokilla, dokillb) -&gt; dict
       collision detection between group and group by using pixel perfect 
       collision detection

       given two groups, this will find the intersections
       between all sprites in each group. it returns a
       dictionary of all sprites in the first group that
       collide. the value for each item in the dictionary
       is a list of the sprites in the second group it
       collides with. the two dokill arguments control if
       the sprites from either group will be automatically
       removed from all groups."""
    crashed = {}
    SC = spritecollide_pp
    if dokilla:
        for s in groupa.sprites():
            c = SC(s, groupb, dokillb)
            if c:
                crashed[s] = c
                s.kill()
    else:
        for s in groupa.sprites():
            c = SC(s, groupb, dokillb)
            if c:
                crashed[s] = c
    return crashed

def spritecollideany_pp(sprite, group):
    """pygame.sprite.spritecollideany_pp(sprite, group) -&gt; sprite
       finds any sprites that collide by using pixel perfect 
       collision detection

       given a sprite and a group of sprites, this will
       return return any single sprite that collides with
       with the given sprite. If there are no collisions
       this returns None.

       if you don't need all the features of the
       spritecollide function, this function will be a
       bit quicker.

       all sprites must have a "hitmap" value, which is a 2d array 
       that contains a value larger than zero for all pixels that 
       can collide. the "hitmap" 2d array can be set by using 
       pygame.surfarray.array_colorkey() or pygame.surfarray.array_alpha(). 

       all sprites must have a "rect" value, which is a
       rectangle of the sprite area.       
       """
    spritecollide = sprite.rect.colliderect
    ppcollide = _pixelPerfectCollisionDetection    
    for s in group.sprites():
        if spritecollide(s.rect):
            if ppcollide(sprite,s):
                return s
    return None
