from . import NonPlayer
from utils import vec, SpriteManager
import pygame

class Switch(NonPlayer):
    def __init__(self, position = vec(0,0), weighted = False):
        super().__init__(position, "Objects.png", (2,0))
        self.pressed = False
        self.weighted = weighted
    
    def getCollisionRect(self):
        newRect = pygame.Rect(0,0,12,12)
        newRect.left = int(self.position[0]+2)
        newRect.top = int(self.position[1]+2)
        return newRect
    
    def set_sprite(self):
        if self.pressed:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (3,0))
        else:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (2,0))

    def press(self, block=None):
        if self.weighted:
            if block:
                self.pressed = True
                self.set_sprite()
        else:
            self.pressed = True
            self.set_sprite()

    def update(self, block):
        if self.weighted:
            if self.doesCollide(block) == False:
                self.pressed = False
                self.set_sprite()