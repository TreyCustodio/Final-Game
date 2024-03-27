import pygame
from utils import SpriteManager, SCALE, RESOLUTION, vec
from . import Drawable, Animated
"""
This class includes everything relevant to the weapons
"""
class Bullet(Drawable):
    SOUND = None
    def __init__(self, position = vec(0,0), direction = 0, hp = 5, max_hp = 5):
        

        if hp == max_hp:
            self.speed = 600
            self.damage = 2
            column = 1
        elif hp <= max_hp/5 or hp == 1:
            self.speed = 300
            self.damage = 6
            column = 2
        
        else:
            self.damage = 2
            self.speed = 300
            column = 0
        super().__init__(position, "Bullet.png", (column, direction))

        self.direction = direction
        if direction == 0:
            self.vel = vec(0,self.speed)
        elif direction == 1:
            self.vel = vec(self.speed,0)
        elif direction == 2:
            self.vel = vec(0,-self.speed)
        elif direction == 3:
            self.vel = vec(-self.speed,0)
        
    def getCollisionRect(self):
        if self.direction == 0:
            return pygame.Rect((self.position[0]+5,self.position[1]+1), (5,15))
        elif self.direction == 1:
            return pygame.Rect((self.position[0]+1,self.position[1]+5), (15,5))
        elif self.direction == 2:
            return pygame.Rect((self.position[0]+5,self.position[1]), (5,15))
        elif self.direction == 3:
            return pygame.Rect((self.position[0],self.position[1]+5), (15,5))
        
    def collides(self, blocks):
        if self.doesCollideList(blocks) != -1:
            return True
        else:
            return False

    def update(self, seconds):
        self.position += self.vel * seconds

class Cleats(object):
    def __init__(self):
        self.damage = 0

    def collides(self, blocks):
        pass

    def getCollisionRect(self):
        return pygame.Rect(((self.position[0]-7),self.position[1]-2), (32,32))
    

class Slash(Animated):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "gale.png", (0,direction))
        
class Sword(Animated):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "fire.png", (0,direction))
        self.direction = direction
        self.nframes = 5
        self.damage = 5
        self.lifetime = 0.2#Seconds the swing lasts
        self.timer = 0
        self.soundCounter = 1#Rotates between 3 sounds
        self.position = position
    
    def collides(self, blocks):
        pass
    
    def getCollisionRect(self):
       if self.direction == 0:
           return pygame.Rect((self.position[0], self.position[1] + 20), (18,14))
       elif self.direction == 1:
           return pygame.Rect((self.position[0]+14, self.position[1]+4), (14,18))
       elif self.direction == 2:
        return pygame.Rect((self.position[0], self.position[1]-4), (18,14))
       elif self.direction == 3:
            return pygame.Rect((self.position[0]-10, self.position[1]+4), (14,18))
       
    def update(self,seconds):
        self.timer += seconds
        

class Clap(Animated):
    SOUND = "lightning.wav"
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "Objects.png", (0,0))
        self.damage = 20
        self.lifetime = 0.2#Seconds the clap lasts
        self.timer = 0
        

    def collides(self, object):
        pass

    def getCollisionRect(self):

        return pygame.Rect(((self.position[0]-7),self.position[1]-2), (32,32))
    
    def update(self,seconds):
        self.timer += seconds

    
