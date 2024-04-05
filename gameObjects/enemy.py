from . import Animated, Bullet, Element, Blizzard, Heart, BigHeart
from utils import SoundManager, SpriteManager, SCALE, RESOLUTION, vec
import pygame
"""
The highest class in the enemy hierarchy.
A basic enemy that moves in a sqaure.
"""






class Enemy(Animated):
    """
    Abstract Enemy Class
    """
    def __init__(self, position = vec(0,0), fileName ="", direction=0):
        if fileName != "":
            self.image = SpriteManager.getInstance().getEnemy(fileName, direction)
        
        #Animation properties
        self.fileName = fileName
        self.row = direction
        self.frame = 0
        self.nFrames = 6
        self.totalFrames = self.nFrames
        self.animate = True
        self.framesPerSecond = 8
        self.animationTimer = 0
        self.FSManimated = None

        self.hurtRow = 4
        self.freezeShield = False
        self.position = vec(*position)
        self.vel = vec(0,0)
        self.dead = False
        self.flashTimer = 0
        self.initialPos = position
        self.initialDir = direction
        self.walkTimer = 0
        self.walking = False
        self.freezeTimer = 4.5
        self.frozen = False
        self.freeze(playSound=False)
        self.maxHp = 0
        ##Strengths and Weaknesses
        #0 -> Neutral
        #1 -> Fire
        #2 -> Ice
        #3 -> Thunder
        #4 -> Wind
        self.shield = 0
        self.type = Element(0)
        

    def setSpeed(self, row):
        if row == 0 or row == 4:
            self.vel[1] = self.speed
            self.vel[0] = 0
            
        elif row == 1 or row == 5:
            self.vel[0] = self.speed
            self.vel[1] = 0
            
        elif row == 2 or row == 6:
            self.vel[1] = -self.speed
            self.vel[0] = 0
        
        elif row == 3 or row == 7:
            self.vel[0] = -self.speed
            self.vel[1] = 0

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
        self.vel = vec(0,0)
        self.dead = False
        self.frozen = False
        self.walking = False
        self.row = self.initialDir
        self.hp = self.maxHp
        #self.position = self.initialPos
        self.flashTimer = 0
        self.walkTimer = 0
        self.freezeTimer = 4.5
        self.freeze(playSound=False)
        
    def handleEvent(self, event):
        pass
    
    def heal(self, integer):
        diff = self.maxHp - self.hp
        if integer < diff:
            self.hp += integer
        else:
            self.hp = self.maxHp

    def handleCollision(self, other):
        if self.type != 2 and type(other) == Blizzard and not self.frozen:
            self.freeze()

        if self.row < self.hurtRow:
            self.row += self.hurtRow
            self.flashTimer = 0
            if other.type == self.type:
                self.heal(other.damage)
            elif self.shield > 0:
                if other.type.beats(self.type):
                    self.hp -= other.damage
            else:
                self.hp -= other.damage

            if self.hp > 0:
                SoundManager.getInstance().playSFX("enemyhit.wav")
            else:
                self.dead = True
        
    def freeze(self, playSound = True):
        self.frozen = True
        self.nFrames = 1
        if playSound:
            SoundManager.getInstance().playSFX("freeze.wav")
        
    
    #intended to be modified but could be used as is
    def move(self, seconds):
        if not self.frozen:
            self.position += self.vel * seconds
            
    
    def bounce(self, other):
        if not self.frozen:
            side = self.calculateSide(other)
            #print(other.position)
            if side == "right":
                self.vel[0] = -self.speed
                if self.row >= 4:
                    self.row = 7
                else:
                    self.row = 3
                #self.vel[1] = 0
            elif side == "top":
                self.vel[1] = self.speed
                if self.row >= 4:
                    self.row = 4
                else:
                    self.row = 0
                #self.vel[0] = 0
            elif side == "left":
                self.vel[0] = self.speed
                if self.row >= 4:
                    self.row = 5
                else:
                    self.row = 1
                #self.vel[1] = 0
            elif side == "bottom":
                self.vel[1] = -self.speed
                if self.row >= 4:
                    self.row = 6
                else:
                    self.row = 2

    def changeDirection(self):
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
        
    def calculateSide(self, object):
        ##  Colliding with Block    ##
        collision1 = self.getCollisionRect()
        collision2 = object.getCollisionRect()
        clipRect = collision1.clip(collision2)
        #print("clip",rect)
        #print(collision1)
        #print(collision2)
        ##Calculate the side
        side = ""
        if clipRect.width < clipRect.height:
            #print("x")
            #X direction
            if collision2.collidepoint(collision1.right,collision1.top) or collision2.collidepoint(collision1.right, collision1.bottom):
                #print("RIGHT")
                side = "right"
            else:
                #print("Left")
                side = "left"
        else:
            #print("Y")
            #Y direction
            if collision2.collidepoint(collision1.right, collision1.top) or collision2.collidepoint(collision1.left,collision1.top):
                #print("Up")
                side = "top"
            else:
                #print("Bottom")
                side = "bottom"
        return side
    
    def unfreeze(self, seconds):
        if self.frozen:
            self.freezeTimer += seconds
            if self.freezeTimer >= 5.0:
                self.frozen = False
                self.freezeTimer = 0
                self.nFrames = self.totalFrames
                self.setSpeed(self.row)

    def updateFlash(self, seconds):
        pass

    def update(self, seconds):
        if self.dead:
        #Add death animation here if self.hp = 0
            pass

        
        
        self.unfreeze(seconds)

        super().update(seconds)
        self.updateFlash(seconds)

        ##Move
        self.move(seconds)
        
       


class Mofos(Enemy):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "mofos.png", direction)
        self.speed = 20
        self.maxHp = 10
        self.hp = self.maxHp
        self.damage = 1

    def bounce(self, other):
        return
                #self.vel[0] = 0

    #override
    def move(self, seconds):
        if self.frame == 5:
            self.changeDirection()
            self.setSpeed(self.row)
            self.frame = 0
        
        if not self.frozen:
            self.position += self.vel * seconds

    def updateFlash(self, seconds):
        if self.row >= 4:
            self.flashTimer += seconds
            if self.flashTimer >= 0.2:
                self.row -= 4

    def update(self, seconds):
        super().update(seconds)
    

class Flapper(Enemy):
    """
    The direction refers to the direction it moves in,
    not to be confused with the direction it faces,
    which is how direction is used for Mofos.
    Flappers always face down. 
    """
    def __init__(self, position = vec(0,0), typeRow = 0, direction = 0):
        super().__init__(position, "flapper.png", typeRow)
        self.typeRow = typeRow
        self.row = self.typeRow
        self.speed = 70
        self.maxHp = 5
        self.hp = self.maxHp
        self.damage = 1
        self.direction = direction
        self.hurtRow = 1
        ##Set velocity based on direction
        self.setSpeed(direction)


    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+3), (16,12))
    

    def move(self, seconds):
        if not self.frozen:
            self.position += self.vel * seconds


    def setSpeed(self, direction):
        if direction == 0:
            self.vel[0] = self.speed
            self.vel[1] = self.speed
        elif direction == 1:
            self.vel[0] = self.speed
            self.vel[1] = -self.speed
        elif direction == 2:
            self.vel[0] = -self.speed
            self.vel[1] = -self.speed
        elif direction == 3:
            self.vel[0] = -self.speed
            self.vel[1] = self.speed
        else:
            return

    def bounce(self, other):
        if not self.frozen:
            side = self.calculateSide(other)
            #print(other.position)
            if side == "right":
                self.vel[0] = -self.speed
                #self.vel[1] = 0
            elif side == "top":
                self.vel[1] = self.speed
                #self.vel[0] = 0
            elif side == "left":
                self.vel[0] = self.speed
                #self.vel[1] = 0
            elif side == "bottom":
                self.vel[1] = -self.speed
                #self.vel[0] = 0

    #override
    def handleCollision(self, other):
        """
        self.row is set to self.hurtRow
        for Flappers
        """
        if self.type != 2 and type(other) == Blizzard and not self.frozen:
            self.freeze()
        if self.row < self.hurtRow:
            self.row = self.hurtRow
            self.flashTimer = 0
            self.hp -= other.damage
            if self.hp > 0:
                SoundManager.getInstance().playSFX("enemyhit.wav")
            else:
                self.dead = True
    
    def updateFlash(self, seconds):
        if self.row == self.hurtRow:
            self.flashTimer += seconds
            if self.flashTimer >= 0.2:
                self.row = self.typeRow

    def update(self, seconds):
        super().update(seconds)



class Puffer(Enemy):
    """
    Must be damaged via ranged attacks.
    Will puff up and damage you if you get to close.
    Play a sound when it puffs
    """
    def __init__(self, position):
        pass
    
    def puff(self):
        pass

class Violater(Enemy):
    """
    Runs across the screen if you enter its line of sight.
    Plays a funny sound when it runs.
    """
    def __init__(self, position):
        pass

    def run(self):
        pass

class Gremlin(Enemy):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "gremlin.png", direction)
        self.speed = 50
        self.maxHp = 20
        self.hp = self.maxHp
        self.damage = 1
        

    def bounce(self, other):
        if not self.frozen:
            side = self.calculateSide(other)
            #print(other.position)
            if side == "right":
                self.vel[0] = -self.speed
                if self.row >= 4:
                    self.row = 7
                else:
                    self.row = 3
                #self.vel[1] = 0
            elif side == "top":
                self.vel[1] = self.speed
                if self.row >= 4:
                    self.row = 4
                else:
                    self.row = 0
                #self.vel[0] = 0
            elif side == "left":
                self.vel[0] = self.speed
                if self.row >= 4:
                    self.row = 5
                else:
                    self.row = 1
                #self.vel[1] = 0
            elif side == "bottom":
                self.vel[1] = -self.speed
                if self.row >= 4:
                    self.row = 6
                else:
                    self.row = 2
    
    
    def updateFlash(self, seconds):
        if self.row >= 4:
            self.flashTimer += seconds
            if self.flashTimer >= 0.2:
                self.row -= 4

        



class Dummy(Enemy):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "dummy.png", 0)
        self.freezeShield = True
        self.nFrames = 1
        self.totalFrames = 1
        self.speed = 0
        self.maxHp = 6
        self.hp = self.maxHp
        self.damage = 0
    
    def getCollisionRect(self):
        return pygame.Rect(self.position, (16,16))
    
    def handleCollision(self, other):
        if issubclass(type(other), Bullet):
            if self.row < 1:
                self.row = 1
                self.flashTimer = 0
                self.hp -= other.damage
                if self.hp > 0:
                    SoundManager.getInstance().playSFX("enemyhit.wav")
                else:
                    self.dead = True


    def updateFlash(self, seconds):
        if self.row > 0:
           
            self.flashTimer += seconds
            if self.flashTimer >= 1.0:
                self.row = 0


class FireEnemy(Enemy):
    pass

class IceEnemy(Enemy):
    pass

class ThunderEnemy(Enemy):
    pass

class WindEnemy(Enemy):
    pass

class FireFlapper(Flapper):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, 2, direction)
        



class IceFlapper(Flapper):
    pass

class ThunderFlapper(Flapper):
    pass

class WindFlapper(Flapper):
    pass

class FireMofos(Mofos):
    pass
class IceMofos(Mofos):
    pass
class ThunderMofos(Mofos):
    pass
class WindMofos(Mofos):
    pass

class MovementPatterns(object):
    def changeDirectionSquare(enemy):
        if enemy.row == 0:
            enemy.row = 3
        elif enemy.row == 4:
            enemy.row = 7
        elif enemy.row == 3:
            enemy.row = 2
        elif enemy.row == 7:
            enemy.row = 6
        elif enemy.row == 2:
            enemy.row = 1
        elif enemy.row == 6:
            enemy.row = 5
        elif enemy.row == 1:
            enemy.row = 0
        elif enemy.row == 5:
           enemy.row = 4


    def diamond(enemy, seconds):
        """
        adjust enemy.frame == condition to lengthen or shrink the range
        """
        if enemy.frame == 5:
            MovementPatterns.changeDirectionSquare(enemy)
            
            if enemy.row == 0 or enemy.row == 4:
                enemy.vel[1] = enemy.speed
                
            elif enemy.row == 1 or enemy.row == 5:
                enemy.vel[0] = enemy.speed
                
            elif enemy.row == 2 or enemy.row == 6:
                enemy.vel[1] = -enemy.speed
            
            elif enemy.row == 3 or enemy.row == 7:
                enemy.vel[0] = -enemy.speed

            enemy.frame = 0
        if not enemy.frozen:
            enemy.position += enemy.vel * seconds
           
    

    
    
    
