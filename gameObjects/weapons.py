import pygame
from utils import SpriteManager, SCALE, RESOLUTION, vec
from . import Drawable, Animated
"""
This class includes everything relevant to the weapons
"""

class Element(object):
    """
    Elemental types:
    0 -> None
    1 -> Fire
    2 -> Ice
    3 -> Thunder
    4 -> Wind
    """
    def __init__(self, integer = 0):
        self.type = integer
    
    def beats(self, otherInt = 0):
        return (otherInt == 1 and self.type == 2) or (otherInt == 2 and self.type == 1) or (otherInt == 3 and self.type == 4) or (otherInt == 4 and self.type == 3)
    
class Bullet(Drawable):
    SOUND = None
    def __init__(self, position = vec(0,0), direction = 0, hp = 5, max_hp = 5):
        

        if hp == max_hp:
            self.speed = 900
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
        
        
        self.type = 0


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
    """
    Only check collision for enemies. If it goes out of bounds, pop it
    """
    def __init__(self, position = vec(0,0), direction = 0, chargeMultiplier = 0):
        super().__init__(position, "gale.png", (0, direction))
        self.vel = vec(0,0)
        if chargeMultiplier == 1:
            self.damage = 10
        elif chargeMultiplier == 2:
            self.damage = 15
        else:
            self.damage = 5
        
        self.animate = False
        self.row = direction
        speed = 200
        if direction == 0:
            self.vel[1] = speed
        elif direction == 1:
            self.vel[0] = speed
        elif direction == 2:
            self.vel[1] = -speed
        elif direction == 3:
            self.vel[0] = -speed
        
        self.type = 4
        

    def getCollisionRect(self):
        return pygame.Rect((self.position), (18,14))
    
    def draw(self, drawSurface):
        super().draw(drawSurface, True)

    def update(self, seconds):
        self.position += self.vel * seconds
        
class Sword(Animated):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "fire.png", (0,direction))
        self.direction = direction
        self.nFrames = 5
        self.row = direction
        self.damage = 5
        self.lifetime = 0.2#Seconds the swing lasts
        self.timer = 0
        self.soundCounter = 1#Rotates between 3 sounds
        if self.direction == 0:
            self.position[1] += 22
        elif self.direction == 1:
            self.position[0] += 14
            self.position[1] += 4
        elif self.direction == 2:
            self.position[1] -= 10
        elif self.direction == 3:
            self.position[0] -= 14
            self.position[1] += 5

        self.type = 1
        
        
    
    def collides(self, blocks):
        pass
    
    def getCollisionRect(self):
       if self.direction == 0:
           return pygame.Rect((self.position[0], self.position[1]), (18,14))
       elif self.direction == 1:
           return pygame.Rect((self.position[0], self.position[1]), (14,18))
       elif self.direction == 2:
        return pygame.Rect((self.position[0], self.position[1]), (18,14))
       elif self.direction == 3:
            return pygame.Rect((self.position[0], self.position[1]), (14,18))
       
    def update(self, seconds):
        #print(self.frame)
        super().updateWeapon(seconds)
        self.timer += seconds
        
class Blizzard(Animated):
    def __init__(self, position = vec(0,0), direction=0):
        super().__init__(position, "Objects.png", (0,0))
        self.animate = False
        self.damage = 1
        self.nFrames = 5
        if direction == 0:
            self.position[0] += 1
            self.position[1] += 24
        elif direction == 1:
            self.position[0] += 14
            self.position[1] += 6
        elif direction == 2:
            self.position[0] += 1
            self.position[1] -= 10
        elif direction == 3:
            self.position[0] -= 12
            self.position[1] += 7

        self.type = 2
    
    def draw(self, drawSurface):
        super().draw(drawSurface, True)

    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]), (16,16))
    
class Clap(Animated):
    SOUND = "lightning.wav"
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "thunder.png", (0,0))
        self.damage = 20
        self.lifetime = 0.2#Seconds the clap lasts
        self.timer = 0
        self.nFrames = 5
        self.position[0] -= 28
        self.position[1] -= 16
    
        self.type = 3

    def collides(self, object):
        pass

    def getCollisionRect(self):

        return pygame.Rect(((self.position[0]),self.position[1]), (64,64))
    
    def update(self,seconds):
        super().update(seconds)
        self.timer += seconds


