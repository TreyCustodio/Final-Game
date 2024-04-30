import pygame
from utils import SpriteManager, SCALE, RESOLUTION, vec, INV
from . import Drawable, Animated, ShotParticle
"""
This file contains everything pertenent to dealing
damage to enemies. Each weapon is instantiated
in the Player Class and stored in the engine's self.projectiles list.
"""

class Element(object):
    """
    Elemental types:
    0 -> None,
    1 -> Fire,
    2 -> Ice,
    3 -> Thunder,
    4 -> Wind
    """
    def __init__(self, integer = 0):
        self.type = integer
    
    def beats(self, otherInt = 0):
        """
        Compares the instantiated Element to an integer that corresponds
        to another element's value. Returns True if the instantiated Element
        beats the other element.
        Fire (1) beats Ice (2)
        Ice (2) beats Fire (1)
        Thunder (3) beats Wind(4)
        Wind (4) beats Thunder (3)
        """
        return (otherInt == 1 and self.type == 2) or (otherInt == 2 and self.type == 1) or (otherInt == 3 and self.type == 4) or (otherInt == 4 and self.type == 3)
    
class AbstractWeapon(Animated):
    def __init__(self, position = vec(0,0), fileName = "", column = 0, direction = 0):
        super().__init__(position, fileName, (column, direction))
        self.hit = False
        self.direction = direction
        self.vel = vec(0,0)


    def setVelocity(self, direction, speed):
        if direction == 0:
            self.vel = vec(0,speed)
        elif direction == 1:
            self.vel = vec(speed,0)
        elif direction == 2:
            self.vel = vec(0,-speed)
        elif direction == 3:
            self.vel = vec(-speed,0)

    def vanish(self, seconds, engine, width):
        """
        vanishes once out of bounds, updates position otherwise
        """
        if self.direction == 0:
            if (self.position[1]) >= RESOLUTION[1]:
                engine.disappear(self)
                return
        elif self.direction == 1:
            if (self.position[0]) >= RESOLUTION[0]:
                engine.disappear(self)
                return
        elif self.direction == 2:
            if (self.position[1] + width) <= 0:
                engine.disappear(self)
                return
        elif self.direction == 3:
            if (self.position[0] + width) <= 0:
                engine.disappear(self)
                return
        
        self.position += self.vel * seconds
    


    #Most likely to be overriden
    def handleCollision(self, engine):
        if not self.hit:
            self.hit = True


    #abstract
    def getCollisionRect(self):
        pass

    def update(self, seconds, engine):
        super().updateWeapon(seconds)
        self.vanish(seconds, engine)





class Bullet(AbstractWeapon):
    """
    Arrows. Speed boost at full health. Damage boost at low health.
    """
    
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
        super().__init__(position, "Bullet.png", column, direction)
        self.setVelocity(self.direction, self.speed)
        self.type = 0
        self.frame = 0

    def setVelocity(self, direction, speed):
        if direction == 0:
            self.vel = vec(0,speed)
        elif direction == 1:
            self.position[1] = self.position[1] + 4
            self.vel = vec(speed,0)
        elif direction == 2:
            self.vel = vec(0,-speed)
        elif direction == 3:
            self.position[1] = self.position[1] + 4
            self.vel = vec(-speed,0)


    def getCollisionRect(self):
        if self.direction == 0:
            return pygame.Rect((self.position[0]+5,self.position[1]+1), (5,15))
        elif self.direction == 1:
            return pygame.Rect((self.position[0]+1,self.position[1]+5), (15,5))
        elif self.direction == 2:
            return pygame.Rect((self.position[0]+5,self.position[1]), (5,15))
        elif self.direction == 3:
            return pygame.Rect((self.position[0],self.position[1]+5), (15,5))
        

    
    def handleCollision(self, engine):
        self.hit = True
        engine.playSound("SM_missile.wav")
        #engine.playSound("OOT_DekuSeed_Hit.wav")
        #engine.disappear(self)
        engine.player.arrowCount += 1
        engine.player.shooting = False


    def handleOtherCollision(self, engine):
        if not self.hit:
            self.hit = True
            engine.playSound("SM_missile.wav")
            #engine.playSound("OOT_DekuSeed_Hit.wav")
            
            
            #engine.disappear(self)
            engine.player.arrowCount += 1
            engine.player.shooting = False


    def update(self, seconds, engine):
        if self.hit:
            super().updateShotParticle(seconds)
            if self.frame == 6:
                engine.disappear(self)
        else:
            self.vanish(seconds, engine, 16)

    
class Hook(AbstractWeapon):
    """
    This attack mimics the hookshot as implemented in
    ALTTP and Link's Awakening
    """
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "Objects.png", 0, direction)
        self.direction = direction
        self.nFrames = 1
        self.setVelocity(direction, 200)
        self.type = 2



    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+4), (8,8))
    

    def draw(self, drawSurface):
        super().draw(drawSurface, True)
    
    def movePlayer(self, player):
        if self.direction == 1:
            player.position = vec(self.position[0]-8, self.position[1])
        elif self.direction == 3:
            player.position = vec(self.position[0]+8, self.position[1])
        elif self.direction == 2:
            player.position = vec(self.position[0], self.position[1]+8)
        elif self.direction == 0:
            player.position = vec(self.position[0], self.position[1]-8)
        player.keyUnlock()


    def update(self, seconds, engine):
        super().updateWeapon(seconds)
        self.position += self.vel * seconds
        if self.hit:
            self.movePlayer(engine.player)
            engine.disappear(self)

class Slash(AbstractWeapon):
    """
    Only check collision for enemies. If it goes out of bounds, pop it
    """
    def __init__(self, position = vec(0,0), direction = 0, chargeMultiplier = 0):
        super().__init__(position, "slash.png", 0, 0)
        if chargeMultiplier == 1:
            self.damage = 10
        elif chargeMultiplier == 2:
            self.damage = 15
        else:
            self.damage = 5
        
        self.animating = False
        self.row = 0
        self.nFrames = 14
        self.framesPerSecond = 30
        self.setVelocity(direction, 200)
        
        self.direction = direction
        self.type = 4
        

    def handleCollision(self, engine):
        pass

    def getCollisionRect(self):
        return pygame.Rect((self.position), (32,32))
    
    def draw(self, drawSurface):
        super().draw(drawSurface)



    def update(self, seconds, engine):
        if self.animating and self.frame == 0:
            self.frame = 6
        super().updateWeapon(seconds, gale = True)
        self.vanish(seconds, engine, 32)
        

        
class Sword(AbstractWeapon):
    """
    Flame C attack
    """
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "fire.png", 0,direction)
        
        
        self.lifetime = 0.2#Seconds the swing lasts
        self.timer = 0
        self.soundCounter = 1#Rotates between 3 sounds
        ##Set the position
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

        ##Set damage based on upgrades
        if INV["flameCost"] == 5:
            self.damage = 10
            self.row = 4+direction
        else:
            self.damage = 5
            self.row = direction


        self.nFrames = 5
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

 
    def update(self, seconds, engine):
        super().updateWeapon(seconds)
        if self.frame == 4:
            engine.disappear(self)
        else:
            self.timer += seconds
        

class Blizzard(AbstractWeapon):
    def __init__(self, position = vec(0,0), direction=0):
        print(direction)
        super().__init__(position, "blizz.png", 0, direction)
        
        self.row = direction
        self.nFrames = 19
        self.damage = 1
        
        ##Set the position
        if direction == 0:
            self.position[0] -= 7
            self.position[1] += 24
        elif direction == 1:
            self.position[0] += 16
            #self.position[1]
        elif direction == 2:
            self.position[0] -= 7
            self.position[1] -= 26
        elif direction == 3:
            self.position[0] -= 30

        self.type = 2
    

    def handleCollision(self, engine):
        pass

    def draw(self, drawSurface):
        super().draw(drawSurface)

    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]), (32,32))
    

    def update(self, seconds, engine):
        super().updateWeapon(seconds)
        if not engine.player.freezing:
            engine.disappear(self)


class Clap(AbstractWeapon):
    SOUND = "lightning.wav"
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "thunder.png")
        self.damage = 20
        self.lifetime = 0.2#Seconds the clap lasts
        self.timer = 0
        self.nFrames = 5
        self.position[0] -= 28
        self.position[1] -= 16
    
        self.type = 3

    def handleCollision(self, engine):
        pass

    def getCollisionRect(self):
        return pygame.Rect(((self.position[0]),self.position[1]), (64,64))
    
    def update(self,seconds, engine):
        super().update(seconds)
        if self.frame == 4:
            engine.disappear(self)
        else:
            self.timer += seconds


