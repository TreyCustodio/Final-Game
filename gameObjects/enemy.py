from . import Animated
from utils import SpriteManager, SCALE, RESOLUTION, vec
import pygame
"""
The highest class in the enemy hierarchy.
A basic enemy that moves in a sqaure.
"""
class Enemy(Animated):
    def __init__(self, position = vec(0,0), fileName ="", direction=0):
        super().__init__(position, fileName, (0,direction))
        self.vel = vec(0,0)
        self.speed = 20
        self.hp = 200

        self.row = direction
        self.framesPerSecond = 8
        self.nFrames = 6
        self.walkTimer = 0
        self.walking = False
    
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
        
        super().update(seconds)
        if self.walking == False:
            self.walking = True
            if self.row == 0:
                self.vel[1] = self.speed
                
            elif self.row == 1:
                self.vel[0] = self.speed
                
            elif self.row == 2:
                self.vel[1] = -self.speed
            
            elif self.row == 3:
                self.vel[0] = -self.speed
                

        self.position += self.vel * seconds
        self.walkTimer += seconds

        if self.walkTimer >= 0.8:
            self.walkTimer = 0
            self.walking = False
            self.vel = vec(0,0)
            

            #Change direction
            #Square code: 0 (down), 3 (left), 2 (up), 1 (right)
            if self.row == 0:
                self.row = 3
                #self.set_sprite(0,self.direction)
            elif self.row == 3:
                self.row = 2
                #self.set_sprite(0,self.direction)
            elif self.row == 2:
                self.row = 1
                #self.set_sprite(0,self.direction)
            else:
                self.row = 0
                #self.set_sprite(0,self.direction)

    def handleCollision(self, other):
        pass
    
