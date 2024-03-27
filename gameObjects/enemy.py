from . import Animated, Bullet, Heart, BigHeart
from utils import SoundManager, SpriteManager, SCALE, RESOLUTION, vec
import pygame
"""
The highest class in the enemy hierarchy.
A basic enemy that moves in a sqaure.
"""


class Enemy(Animated):
    def __init__(self, position = vec(0,0), fileName ="", direction=0):
        super().__init__(position, fileName, (0,direction))
        self.vel = vec(0,0)
        self.dead = False
        self.speed = 20
        self.hp = 10
        self.damage = 1
        self.flashTimer = 0

        self.initialPos = position
        self.row = direction
        self.framesPerSecond = 8
        self.nFrames = 6
        self.walkTimer = 0
        self.walking = False
        self.freezeTimer = 0
        self.frozen = False


    def getDamage(self):
        return self.damage

    def getDrop(self):
        return Heart((self.position[0]+3, self.position[1]+5))
    
    def getCollisionRect(self):
        newRect = pygame.Rect(0,0,14,23)
        newRect.left = int(self.position[0]+2)
        newRect.top = int(self.position[1]+2)
        return newRect
    
    def respawn(self):
        self.hp = 10
        self.position = self.initialPos
        self.dead = False
        self.vel = vec(0,0)
        self.row = 0
        self.flashTimer = 0
        self.walkTimer = 0
        self.walking = False
        self.freezeTimer = 0
        self.frozen = False

    def handleEvent(self, event):
        pass
    
    def handleCollision(self, other):
        if self.row < 4:
            self.row += 4
            self.flashTimer = 0
            self.hp -= other.damage
            if self.hp > 0:
                SoundManager.getInstance().playSFX("enemyhit.wav")
        if self.frozen:
            self.hp -= other.damage
            if self.hp > 0:
                SoundManager.getInstance().playSFX("enemyhit.wav")
        
        if self.hp <= 0:
            self.dead = True
    
    def freeze(self):
        SoundManager.getInstance().playSFX("freeze.wav")
        self.frozen = True
        self.nFrames = 1
    
    def move(self, seconds):
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

    def update(self, seconds):
        
        if self.frozen:
            self.freezeTimer += seconds
            if self.freezeTimer >= 5.0:
                self.frozen = False
                self.freezeTimer = 0
                self.nFrames = 6
        #Add death animation here if self.hp = 0
        #Moves depending on its direction
        super().update(seconds)

        if self.row >= 4:
            self.flashTimer += seconds
            if self.flashTimer >= 0.2:
                self.row -= 4
    
        if not self.frozen:
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
        
            self.move(seconds)
           
    

    
    
    
