"""
Parent class for drawable objects.

"""
from spriteManager import SpriteManager
from vector import vec, rectAdd
import pygame
from constants import RESOLUTION, UPSCALED


class Drawable(object):
    OFFSET = vec(0,0)
        
    def __init__(self, fileName, position, offset=None):
        self.fileName = fileName
        self.position = position
        #Object's instance of the sprite manager
        self.SM = SpriteManager.getInstance()
        self.image = self.SM.getSprite(self.fileName, offset)
    
    def draw(self, drawSurface, drawHitbox = False):
        drawPosition = self.position
        drawSurface.blit(self.image, list(map(int, drawPosition)))

        collision = self.getCollisionRect()
        collision = rectAdd(-Drawable.OFFSET, collision)
        if drawHitbox:
            pygame.draw.rect(drawSurface, (255,255,255), collision, 1)
    
    def getRect(self):
        return self.image.get_rect()
    
    def getCollisionRect(self):
        return rectAdd(self.position, self.image.get_rect())
    