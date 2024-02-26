import pygame

from . import Drawable,  GameEngine, NonPlayer, Block

from utils import  vec, RESOLUTION

from pygame.locals import *


class PauseEngine(object):


    def __init__(self):
        """
        Initialize item icons.
        Screen is 304 x 200
        [               ]  
        

        [               ]
        128 x 96 space
        16 x 16 squares
        beggining at (3,1)
        """
        self.menu = Drawable((0,0), "Pause.png")
        self.timer = 0
        self.highlight = Drawable((48,16), "Objects.png", (0,0))
        self.highlighted = vec(0,0)
    
    def draw(self, drawSurf):

        self.menu.draw(drawSurf)

        if self.timer >= .3:
            self.highlight.draw(drawSurf)
        else:
            self.highlight.draw(drawSurf, True)

    def handleEvent(self, event):
        """
           0    1    2   3   4   5   6   7
        0
        1
        2
        3
        4
        5

        min offset[0] = 0
        max offset[0] = 7
        min offset[1] = 0
        max offset[1] = 5
        """
        if event.type == KEYDOWN and event.key == K_UP:
            if self.highlighted[1] != 0:
                self.highlighted[1] -= 1
                self.highlight.position[1] -= 16
        elif event.type == KEYDOWN and event.key == K_DOWN:
            if self.highlighted[1] != 5:
                self.highlighted[1] += 1
                self.highlight.position[1] += 16
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if self.highlighted[0] != 7:
                self.highlighted[0] += 1
                self.highlight.position[0] += 16
        elif event.type == KEYDOWN and event.key == K_LEFT:
            if self.highlighted[0] != 0:
                self.highlighted[0] -= 1
                self.highlight.position[0] -= 16

    def update(self, seconds):
        self.timer += seconds
        if self.timer >= .5:
            self.timer = 0
        