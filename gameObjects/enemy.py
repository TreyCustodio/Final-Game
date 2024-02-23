from . import Drawable
from utils import SpriteManager, SCALE, RESOLUTION, vec
import pygame
"""
The highest class in the enemy hierarchy.
A basic enemy that moves in a sqaure.
"""
class Enemy(Drawable):
    def __init__(self, position = vec(0,0), fileName ="", offset=(0,0), direction=0):
        super().__init__(position, fileName, offset)
        self.vel = vec(0,0)
        self.speed = 20
        self.direction = direction # (0 down), (1 right), (2 up), (3 left)
        self.hp = 200
        self.walkTimer = 0
        self.walking = False
        self.set_sprite(0,self.direction)
    
    def set_sprite(self, value, direction):
        self.image = SpriteManager.getInstance().getSprite(self.imageName, (value,direction))

    def getCollisionRect(self):
        newRect = pygame.Rect(0,0,14,23)
        newRect.left = int(self.position[0]+2)
        newRect.top = int(self.position[1]+2)
        return newRect
    
    def handleEvent(self, event):
        pass

    def update(self, seconds):
        #Moves depending on its direction
        
        if self.walking == False:
            self.walking = True
            if self.direction == 0:
                self.vel[1] = self.speed
                
            elif self.direction == 1:
                self.vel[0] = self.speed
                
            elif self.direction == 2:
                self.vel[1] = -self.speed
            
            elif self.direction == 3:
                self.vel[0] = -self.speed
                

        self.set_sprite(1,self.direction)
        self.position += self.vel * seconds
        self.walkTimer += seconds

        if self.walkTimer >= 0.8:
            self.walkTimer = 0
            self.walking = False
            self.set_sprite(0,self.direction)
            self.vel = vec(0,0)
            

            #Change direction
            #Square code: 0 (down), 3 (left), 2 (up), 1 (right)
            if self.direction == 0:
                self.direction = 3
                self.set_sprite(0,self.direction)
            elif self.direction == 3:
                self.direction = 2
                self.set_sprite(0,self.direction)
            elif self.direction == 2:
                self.direction = 1
                self.set_sprite(0,self.direction)
            else:
                self.direction = 0
                self.set_sprite(0,self.direction)

    def handleCollision(self, other):
        pass
    
