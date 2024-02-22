from . import Drawable
from utils import SpriteManager, SCALE, RESOLUTION, vec
import pygame

class Enemy(Drawable):
    def __init__(self, position = vec(0,0), fileName ="", direction=0):
        super().__init__(position, fileName, (0, direction))
        self.vel = vec(0,0)
        self.speed = 250
        self.direction = direction # (0 down), (1 right), (2 up), (3 left)
        self.hp = 200
    
    def getCollisionRect(self):
        newRect = pygame.Rect(0,0,14,23)
        newRect.left = int(self.position[0]+2)
        newRect.top = int(self.position[1]+2)
        return newRect
    
    def handleEvent(self, event):
        pass

    def update(self, seconds):
        self.position += self.vel * seconds

    def handleCollision(self, other):
        pass
    
