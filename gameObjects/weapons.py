import pygame
from utils import SpriteManager, SCALE, RESOLUTION, vec
from . import Drawable
"""
This class includes everything relevant to the weapons
"""
class Bullet(Drawable):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "Bullet.png", (0, direction))
        self.damage = 1
        self.speed = 300
        if direction == 0:
            self.vel = vec(0,self.speed)
        elif direction == 1:
            self.vel = vec(self.speed,0)
        elif direction == 2:
            self.vel = vec(0,-self.speed)
        elif direction == 3:
            self.vel = vec(-self.speed,0)
        
        
    def collides(self, blocks):
        if self.doesCollideList(blocks) != -1:
            return True
        else:
            return False

    def update(self, seconds):
        self.position += self.vel * seconds

class Sword(Drawable):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "Objects.png", (0, 0))
        self.direction = direction
        self.damage = 5
        self.lifetime = 0.2#Seconds the swing lasts
        self.timer = 0
    
    def collides(self, blocks):
        pass
    
    def getCollisionRect(self):
       if self.direction == 0:
           return pygame.Rect((self.position[0],self.position[1]+20), (18,12))
       elif self.direction == 1:
           return pygame.Rect((self.position[0]+12,self.position[1]), (12,18))
       elif self.direction == 2:
        return pygame.Rect((self.position[0],self.position[1]), (18,12))
       elif self.direction == 3:
            return pygame.Rect((self.position[0]-6,self.position[1]), (12,18))
       
    def update(self,seconds):
        self.timer += seconds
    
