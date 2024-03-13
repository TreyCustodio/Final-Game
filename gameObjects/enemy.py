from . import Animated, Bullet
from utils import SpriteManager, SCALE, RESOLUTION, vec
import pygame
"""
The highest class in the enemy hierarchy.
A basic enemy that moves in a sqaure.
"""
class Timer(object):
    def __init__(self, max):
        self.seconds = 0
        self.max = max

class Enemy(Animated):
    def __init__(self, position = vec(0,0), fileName ="", direction=0):
        super().__init__(position, fileName, (0,direction))
        self.vel = vec(0,0)
        self.speed = 20
        self.hp = 10
        self.flashTimer = 0

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
        
        
        #Add death animation here if self.hp = 0
        #Moves depending on its direction
        super().update(seconds)
        if self.row >= 4:
            self.flashTimer += seconds
            if self.flashTimer >= 0.2:
                self.row -= 4
        if self.walking == False:
            self.walking = True
            if self.row == 0 or self.row == 4:
                self.vel[1] = self.speed
                
            elif self.row == 1 or self.row == 5:
                self.vel[0] = self.speed
                
            elif self.row == 2 or self.row == 6:
                self.vel[1] = -self.speed
            
            elif self.row == 3 or self.row == 7:
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
            elif self.row == 4:
                self.row = 7
            elif self.row == 3:
                self.row = 2
            elif self.row == 7:
                self.row = 6
            elif self.row == 2:
                self.row = 1
            elif self.row == 6:
                self.row = 5
            elif self.row == 1:
                self.row = 0
            elif self.row == 5:
                self.row = 4
           
    

    def handleCollision(self, other):
        if self.row < 4:
            self.row += 4
            self.flashTimer = 0
            self.hp -= other.damage
    
    
