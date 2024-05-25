from . import Drawable, Animated, Bullet, Element, Blizzard, Heart, BigHeart, Buck, FireShard, GreenHeart, Buck_B, Buck_R
from utils import SoundManager, SpriteManager, SCALE, RESOLUTION, vec
from random import randint
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
        
        self.ignoreCollision = False
        self.top = False #Boolean that controls what layer the enemy is drawn on
        self.hit = False
        #Animation properties
        self.indicatorRow = 0
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
    
    
    def doesCollideBlock(self, block):
        return self.doesCollide(block)

    def doesCollideProjectile(self, projectile):
        return self.doesCollide(projectile)
    
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
        integer = randint(0,2)
        if integer == 0:
            return Heart((self.position[0]+3, self.position[1]+5))
        elif integer == 1:
            return Buck((self.position[0]+3, self.position[1]+5))
    
    def getMoney(self):
        integer = randint(0,1)
        if integer == 1:
            return Buck((self.position[0]+3, self.position[1]+5))
    
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

    def hurt(self, damage, setHit = True):
        self.hit = setHit
        self.hp -= damage
        if self.hp > 0: 
            SoundManager.getInstance().playSFX("enemyhit.wav")
        else:
            self.dead = True

    def handlePlayerCollision(self, player):
        """
        Expects a player
        Returns True if the Enemy hurts the Player

        Will be overriden by Enemies with multiple
        collision Rects
        """
        return True



    def handleCollision(self, other = None):
        """
        Enemy gets hurt, frozen, and healed.
        Damage = other.damage
        """
        
        if self.type != 2 and other.type == 2 and not self.frozen:
            self.freeze()

        if self.row < self.hurtRow:
            self.row += self.hurtRow
            self.flashTimer = 0
            if other.type == self.type:
                self.heal(other.damage)
            elif self.shield > 0:
                if other.type.beats(self.type):
                    self.hurt(other.damage)
            else:
                self.hurt(other.damage)

            if self.hp > 0:
                SoundManager.getInstance().playSFX("enemyhit.wav")
            else:
                self.dead = True
            
        elif other.type == 0:
            self.hurt(other.damage)
            if self.hp > 0: 
                SoundManager.getInstance().playSFX("enemyhit.wav")
            else:
                self.dead = True
        #print(self.hp)
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
        if self.row >= self.hurtRow:
            self.flashTimer += seconds
            if self.flashTimer >= 0.2:
                self.row -= self.hurtRow

    def update(self, seconds, position = None):
        if self.dead:
        #Add death animation here if self.hp = 0
            pass
        
        self.unfreeze(seconds)

        super().updateEnemy(seconds)
        self.updateFlash(seconds)

        ##Move
        self.move(seconds)
        

class LavaKnight(Enemy):
    def __init__(self, position=vec(0,0), fall = False, boss = True):
        """
        Position of shadow does not move unless
        the knight moves its position.
        Moving its position is not the same as
        jumping up or down.
        """
        super().__init__(position, "knight.png", 0)
        self.boss = boss
        ##Startup animation
        self.vibrationTick = 0
        self.startupTimer = 0.0
        self.fallTimer = 0.0 #timer for off screen
        self.shaking = False #vibrating bool
        self.moving = False #done with animation
        self.respawning = False
        self.falling = False
        self.targetPos = vec(0,0)

        self.desperate = False #True if final phase is active
        self.damage = 3
        self.nFrames = 1
        self.maxHp = 1
        self.freezeShield = True
        self.hp = self.maxHp
        self.jumpingUp = False
        self.jumpingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.frozen = False
        self.jumpTimer = 0.0
        self.pause = True
        self.speed = 30
        self.freezeCounter = 1 #Once this gets to zero, it becomes vulnerable to Bombofauns
        self.maxCount = 10 #The maximum integer the freezeCount can be
        self.cold = False #Able to be blown up
        self.vulnerable = False #Able to be frozen
        self.iframeTimer = 0.0
        self.shadow = Animated(vec(self.position[0], self.position[1]), "knight.png", (1,0))
        self.xVals = [] #list of possible positions in the collisionRect
        self.yVals = []

    def getDrop(self):
        return GreenHeart((self.position[0]+16, self.position[1]+16))
    
    def hurt(self, damage, setHit = True):
        self.hit = setHit
        self.hp -= damage
        if self.desperate:
            if self.hp <= 0:
                self.dead = True
            else:
                SoundManager.getInstance().playSFX("enemyhit.wav")

        elif self.hp <= 0:
            self.desperate = True
            self.hp = 2
        else:
            SoundManager.getInstance().playSFX("enemyhit.wav")

    def bounce(self, other):
        if not self.cold and not self.falling and not self.respawning:
            self.fullStop()
            self.respawning = True
    
    def startRespawn(self):
        SoundManager.getInstance().playSFX("big_jump.wav")
        self.fullStop()
        self.respawning = True
        self.top = True

    def fullStop(self):
        self.stop()
        self.jumpingUp = False
        self.jumpingDown = False
        self.jumpTimer = 0.0

    def stop(self):
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

    def setCold(self):
        self.cold = True
        self.movingDown = False
        self.movingUp = False
        self.movingLeft = False
        self.movingRight = False
        self.row = 1
    
    def unsetCold(self):
        self.cold = False
        self.vulnerable = False
        self.freezeCounter = self.maxCount
        self.fullStop()
        self.respawning = True
        self.top = True
        self.row = 0
    
    def stopMotion(self, position):
        self.setCollisionRange()
        if int(position[1]) in self.yVals:
            print("pos in x vals")
            self.movingUp = False
            self.movingDown = False
        if int(position[0]) in self.xVals:
            print("pos in x vals")
            self.movingRight = False
            self.movingLeft = False

    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+8), (32,24))
    
    def setImage(self):
        self.image = SpriteManager.getInstance().getSprite("knight.png", (self.frame, self.row))
    
    def draw(self, drawSurface):
        super().draw(drawSurface)
    
    def drawTop(self, drawSurface):
        self.shadow.draw(drawSurface)
        super().draw(drawSurface)

    """
    Only damage player when on the ground
    """

    def handlePlayerCollision(self, player):
        if self.ignoreCollision:
            return False
        else:
            return True
        
    def handleCollision(self, other=None):
        if self.cold:
            if other.id == "arrow":
                self.hurt(other.damage)
                self.unsetCold()
            return

        if not self.ignoreCollision:
            if self.vulnerable and other.id == "blizz":
                self.freezeCounter -= 1
                if self.freezeCounter <= 0:
                    self.setCold()
                    SoundManager.getInstance().playSFX("freeze.wav")
                else:
                    SoundManager.getInstance().playSFX("enemyhit.wav")
                    self.vulnerable = False
                    self.row = 2                
    
    def setTargetPos(self, position):
        self.targetPos = vec(position[0]-16, position[1]-16)

    def setCollisionRange(self):
        self.xVals = []
        self.yVals = []
        pos = self.getCollisionRect().topleft
        for i in range(16):
            for j in range(16):
                self.xVals.append(pos[0] + i)
                self.yVals.append(pos[1] + i)
        
        
    """
    Sets the position of the shadow and the knight
    """
    def setActualPos(self, axis = 0, add = True, value = 1):
        if add:
            self.position[axis] += value
            self.shadow.position[axis] += value
        else:
            self.position[axis] -= value
            self.shadow.position[axis] -= value

    """
    The knight chooses which direction 
    to move based on the player's position.

    position -> player's current position
    """
    def setDirection(self, position):
        if self.cold:
            return
        
        if int(position[0]) < int(self.position[0] + 16):
            self.movingLeft = True
            self.movingRight = False
        
        elif int(position [0]) > int(self.position[0] + 16):
            self.movingRight = True
            self.movingLeft = False

        if int(position[1]) < int(self.position[1] + 32):
            self.movingUp = True
            self.movingDown = False
        
        elif int(position [1]) > int(self.position[1] + 32):
            self.movingDown = True
            self.movingUp = False
        
        

    def update(self, seconds, position = None):
        ##I-frame update
        if not self.vulnerable:
            self.iframeTimer += seconds
            if self.iframeTimer >= 0.4:
                self.row = 0
                self.vulnerable = True
                self.iframeTimer = 0.0
                self.setImage()

        ##Jumping off screen and reappearing
        if self.respawning and not self.pause:
            if self.falling:
                ##Shadow reappears
                if self.top:
                    if self.shadow.frame == 1:
                        self.fallTimer += seconds
                        ##Falling down
                        if self.fallTimer >= 0.2:
                            self.position[1] += 12
                            ##Crashed
                            if self.position[1] >= self.targetPos[1]:
                                SoundManager.getInstance().stopAllSFX()                            
                                SoundManager.getInstance().playSFX("crash.wav")
                                self.position[1] = self.targetPos[1]
                                self.falling = False
                                self.top = False
                                self.fallTimer = 0.0
                                self.respawning = False
                                self.pause = True
                    ##Decrement shadow frame
                    else:
                        self.shadow.frame -= 1
                        self.shadow.image = SpriteManager.getInstance().getSprite("knight.png", (self.shadow.frame, 0))

                ##Off screen, ready to set target
                else:
                    self.fallTimer += seconds
                    if self.fallTimer >= 1.0:
                        self.fallTimer = 0.0
                        self.setTargetPos(position)
                        self.shadow.position = self.targetPos
                        self.position[0] = self.targetPos[0]
                        self.shadow.position[0] = self.targetPos[0]
                        self.top = True
            
            ##Jumping up  
            else:
                self.position[1] -= 4
                if self.position[1] + 32 <= -64:
                    self.shadow.frame += 1
                    self.shadow.frame %= 3
                    if self.shadow.frame == 0:
                        self.shadow.frame = 3
                        self.top = False
                        self.falling = True
                    self.shadow.image = SpriteManager.getInstance().getSprite("knight.png", (self.shadow.frame, 0))
            self.setImage()
            return
        
        ##Startup Animation
        if not self.moving:
            if not self.shaking:
                self.startupTimer += seconds
                if self.startupTimer >= 2:
                    self.startupTimer = 0.0
                    self.shaking = True
            else:
                self.startupTimer += seconds
                if self.startupTimer >= 2:
                    SoundManager.getInstance().stopSFX("LA_Rock_Push.wav")
                    self.moving = True
                else:
                    SoundManager.getInstance().playSFX("LA_Rock_Push.wav")
                    if self.vibrationTick == 0:
                        self.setActualPos(0, True)
                        self.vibrationTick += 1
                    elif self.vibrationTick == 1:
                        self.setActualPos(0, False)
                        self.vibrationTick += 1
                    elif self.vibrationTick == 2:
                        self.setActualPos(0, False)
                        self.vibrationTick += 1
                    elif self.vibrationTick == 3:
                        self.setActualPos(0, True)
                        self.vibrationTick = 0
                    return
            return
        
        
        ##Mid air movement
        if not self.pause:
            ##Jumping
            self.jumpTimer += seconds
            if self.jumpingUp:
                self.ignoreCollision = True
                self.position[1] -= 1
                if self.cold:
                    if self.jumpTimer >= 0.1:
                        self.jumpingUp = False
                        self.jumpingDown = True
                        self.jumpTimer = 0.0
                else:
                    if self.jumpTimer >= 0.5:
                        self.jumpingUp = False
                        self.jumpingDown = True
                        self.jumpTimer = 0.0
            elif self.jumpingDown:
                self.ignoreCollision = True
                if self.cold:
                    self.position[1] += 6
                else:
                    self.position[1] += 4
                if self.position[1] >= self.shadow.position[1]:
                    SoundManager.getInstance().stopAllSFX()
                    SoundManager.getInstance().playSFX("crash.wav")
                    self.position[1] = self.shadow.position[1]
                    self.pause = True
                    self.movingUp = False
                    self.movingDown = False
                    self.top = False
                    self.jumpingDown = False
                    self.jumpTimer = 0.0
                    return


            ##Moving
            if self.movingLeft:
                self.setActualPos(0, False)
            elif self.movingRight:
                self.setActualPos(0, True)

            if self.movingUp:
                self.setActualPos(1, False)
            elif self.movingDown:
                self.setActualPos(1, True)

            
            ##Player inside collision rect (able to be crushed)
            if self.getCollisionRect().collidepoint(position):
                self.stop()
            else:
                self.stopMotion(position)

            
        ##Ground (no movement)
        else:
            self.ignoreCollision = False
            self.jumpTimer += seconds
            if self.jumpTimer >= 0.5:
                self.jumpTimer = 0.0
                self.pause = False
                if self.desperate:
                    if self.cold:
                        self.setDirection(position)
                        SoundManager.getInstance().playSFX("big_jump.wav")
                        self.top = True
                        self.jumpingUp = True
                    else:
                        self.startRespawn()
                else:
                    self.setDirection(position)
                    SoundManager.getInstance().playSFX("big_jump.wav")
                    self.top = True
                    self.jumpingUp = True
        
        
        
        ##Set the image
        self.setImage()

class Mofos(Enemy):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "mofos.png", direction)
        self.indicatorRow = 3
        self.speed = 20
        self.maxHp = 20
        self.hp = 20
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
            if self.flashTimer >= 0.4:
                self.row -= 4

    def update(self, seconds, position = None):
        super().update(seconds)
        

class Baller(Enemy):
    def __init__(self, position=vec(0,0), direction = 3):
        super().__init__(position, "baller.png", direction)
        self.indicatorRow = 8
        self.row = direction
        self.hurtRow = 4
        self.speed = 50
        self.nFrames = 4
        self.totalFrames = 4
        self.maxHp = 5
        self.hp = 5
        self.direction = direction
        self.damage = 1
        self.type = Element(1)
        self.setSpeed()

    

    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+1, self.position[1]+1), (14,15))
    
    def getMoney(self):
        return self.getDrop()
    
    def getDrop(self):
        return FireShard((self.position[0]+3, self.position[1]+5))
    
    def bounce(self, other):
        if not self.frozen:
            side = self.calculateSide(other)
            #print(other.position)
            if side == "right":
                self.vel[0] = -self.speed
                self.row = 3
                #self.vel[1] = 0
            
            elif side == "left":
                self.vel[0] = self.speed
                self.row = 1
                #self.vel[1] = 0
            
    def draw(self, drawSurface):
        super().draw(drawSurface)
        

    def setSpeed(self, row=0):
        
        if self.direction == 3:
            self.vel[0] = -self.speed
        elif self.direction == 1:
            self.vel[0] = self.speed

    def handleCollision(self, other=None):
        if other.type == 2:
            if not self.frozen:
                self.freeze()
            if self.row < self.hurtRow:
                self.row += self.hurtRow
                self.flashTimer = 0
                self.hp -= other.damage
                if self.hp > 0:
                    SoundManager.getInstance().playSFX("enemyhit.wav")
                else:
                    self.dead = True
        elif other.type == 1:
            self.heal(other.damage)


    def update(self, seconds, position = None):
        super().update(seconds)

class Heater(Enemy):
    def __init__(self, position):
        super().__init__(position, "heater.png")
        self.indicatorRow = 0
        self.speed = 100
        self.nFrames = 1
        self.totalFrames = 1
        self.maxHp = 20
        self.hp = 20
        self.damage = 1
        self.type = Element(1)
        self.minHeight = self.position[1] + 40
        self.maxHeight = self.position[1]
        self.minWidth = self.position[0] - 40
        self.maxWidth = self.position[0]
        self.direction = 3
        self.hurtRow = 0
        self.vel = vec(-self.speed, self.speed)
        self.freezeShield = True
    
    def bounce(self, other):
        pass
    
    def setSpeed(self, row):
        self.vel = vec(-self.speed, self.speed/2)

    def updateSpeed(self):
        if self.direction == 3:
            #print(3)
            if self.position[1] >= self.minHeight:
                #print("A")
                self.vel[1] = -self.speed/2

            if self.position[0] <= self.minWidth: 
                #print("B")               
                self.vel[0] = self.speed
                self.direction = 1
                self.vel[1] = self.speed/2
        
        elif self.direction == 1:
            print(1)
            if self.position[1] >= self.minHeight:
                self.vel[1] = -self.speed/2

            if self.position[0] >= self.maxWidth:                
                self.vel[0] = -self.speed
                self.direction = 3
                self.vel[1] = self.speed/2


    def move(self, seconds):
        if not self.frozen:
            self.updateSpeed()
            self.position += self.vel*seconds
            





class Stunner(Enemy):
    def __init__(self, position=vec(0,0), direction = 0):
        super().__init__(position, "stunner.png", direction)
        self.indicatorRow = 9
        self.row = direction
        self.hurtRow = 1
        self.speed = 50
        self.nFrames = 15
        self.totalFrames = 13
        self.maxHp = 10
        self.hp = 10
        self.direction = direction
        self.damage = 2
        self.framesPerSecond = 4
        self.type = Element(2)
        self.setSpeed()

    def bounce(self, other):
        pass
    
    def handleCollision(self, other):
        return
    
    def updateFlash(self, seconds):
        return

    def setSpeed(self, row=0):
        return
    
    def move(self, seconds):
        self.position += self.vel*seconds

class FireMofos(Mofos):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, direction)

    def getDrop(self):
        return FireShard((self.position[0]+3, self.position[1]+5))
    """ def getDrop(self):
        return FireShard((self.position[0]+3, self.position[1]+5)) """
    
class Spinner(Enemy):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "spinner.png", 0)
        
        self.nFrames = 2#current max frames
        self.totalFrames = 2#Total frames
        self.indicatorRow = 7
        self.speed = 50
        self.maxHp = 10
        self.row = 0
        self.hp = self.maxHp
        self.damage = 1
        self.hurtRow = 0
        self.freezeShield = True
        self.framesPerSecond = 32

   
    def bounce(self, other):
        pass
    
    def handleCollision(self, other):
        return
    
    def updateFlash(self, seconds):
        return

    def setSpeed(self, row=0):
        return
    
    def move(self, seconds):
        MovementPatterns.diamond(self, seconds)





class Flapper(Enemy):
    """
    The direction refers to the direction it moves in,
    not to be confused with the direction it faces,
    which is how direction is used for Mofos.
    Flappers always face down. 
    """
    def __init__(self, position = vec(0,0), typeRow = 0, direction = 0):
        super().__init__(position, "flapper.png", typeRow)
        self.indicatorRow = 1
        self.typeRow = typeRow
        self.row = self.typeRow
        self.speed = 70
        self.maxHp = 5
        self.hp = self.maxHp
        self.damage = 1
        self.direction = direction
        self.hurtRow = 5
        
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

    def update(self, seconds, position = None):
        super().update(seconds)



class FireFlapper(Flapper):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, 1, direction)
        self.type = Element(1)
    
    def handleCollision(self, other):
        if other.type == 2:
            super().handleCollision(other)

class IceFlapper(Flapper):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, 2, direction)
        self.type = Element(2)
        self.freezeShield = True
    
    def handleCollision(self, other):
        if other.type == 1:
            super().handleCollision(other)

class ThunderFlapper(Flapper):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, 3, direction)
        #self.freezeShield = True
        self.type = Element(3)
    
    def handleCollision(self, other):
        if other.type == 4:
            super().handleCollision(other)

class WindFlapper(Flapper):
    pass



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

class David(Enemy):
    """
    Runs across the screen if you enter its line of sight.
    Plays a funny sound when it runs.
    """
    def __init__(self, position, direction = 1, boss = False):
        super().__init__(position, "david.png", direction)
        self.indicatorRow = 2
        self.nFrames = 1
        self.totalFrames = 1
        self.speed = 200
        self.maxHp = 30
        self.hp = self.maxHp
        self.damage = 1
        self.running = False
        self.freezeShield = True
        self.ready = True

        self.boss = boss

    def getDrop(self):
        return BigHeart((self.position[0]+3, self.position[1]+5))

    def doesCollideProjectile(self, other):
        return self.getHitBox().colliderect(other.getCollisionRect())


    def doesCollideBlock(self, block):
        if self.getHitBox().colliderect(block.getCollisionRect()):
            return True
        else:
            return False
        
    def getCollisionRect(self):
        if self.row == 1 or self.row == 5:
            return pygame.Rect((self.position), (64, 26))
        elif self.row == 3 or self.row == 7:
            return pygame.Rect((self.position[0] - (64-19), self.position[1]), (64, 26))

    def getHitBox(self):
        return pygame.Rect((self.position), (19,26))
    
    def getRunRect(self):
        if self.row == 1:
            return pygame.Rect((self.position[0] + 19, self.position[1]), (64, 26))
        elif self.row == 3:
            return pygame.Rect((self.position[0] - 64, self.position[1]), (64-19, 26))
        
    def run(self):
        if not self.running:
            
            self.running = True
            self.nFrames = 3
            self.totalFrames = 3
            
            if self.row == 1 or self.row == 5:
                self.vel[0] = self.speed
            elif self.row == 3 or self.row == 7:
                self.vel[0] = -self.speed
        

    def move(self, seconds):
        if self.running:
            self.position += self.vel * seconds
    
    def updateFlash(self, seconds):
        if self.row >= 4:
            self.flashTimer += seconds
            if self.flashTimer >= 0.5:
                self.row -= 4


    def handlePlayerCollision(self, player):
        """
        Hurts the player if it collides with its hitbox
        Runs at the player if it collides with its runRect
        """
        if self.row < 4:
            if self.getRunRect().colliderect(player.getCollisionRect()):#player collides with runRect
                if not self.running:
                    SoundManager.getInstance().playSFX("run.wav")
                self.run()
                
                

            else:
                player.handleCollision(self)
    

    def handleCollision(self, other):
        """
        Only gets damaged by arrows
        """
        if not self.running and other.type == 0:
            if self.row < self.hurtRow:
                self.row += self.hurtRow
                self.flashTimer = 0
                self.hp -= other.damage
                if self.hp > 0:
                    SoundManager.getInstance().playSFX("david.wav")
                    self.run()
                    
                else:
                    self.dead = True


    def bounce(self, other):
        """
        David turns around once he collides with a wall.
        Logic gets a little iffy here.
        """
        if self.running == False:#Stopped
            
            ##If he's in the wall
            if self.getHitBox().colliderect(other.getCollisionRect()):
                ##Get him out the wall
                if self.row == 3:
                    self.position[0] -= 1

                elif self.row == 1:
                    self.position[0] += 1

        
        else:##Runs first, stop movement, reset animation
            self.running = False
            self.totalFrames = 1
            self.nFrames = 1
            self.vel = vec(0,0)
            if self.row == 1:
                self.row = 3
            elif self.row == 3:
                self.row = 1

        



    def update(self, seconds, position = None):
        if self.dead:
        #Add death animation here if self.hp = 0
            pass

        self.unfreeze(seconds)


        super().update(seconds)

        self.updateFlash(seconds)

        ##Move
        self.move(seconds)




class Gremlin(Enemy):
    def __init__(self, position = vec(0,0), direction = 1, fileName = "gremlin.png"):
        super().__init__(position, fileName, direction)
        self.indicatorRow = 4
        self.speed = 50
        self.maxHp = 15
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

        
class GremlinB(Gremlin):
    def __init__(self, position= vec(0,0), direction = 1):
        super().__init__(position, direction, "gremlin_blue.png")
        self.maxHp = 30
        self.hp = 30
        self.damage = 2
        self.speed = 60

    def getDrop(self):
        return BigHeart((self.position[0]+3, self.position[1]+5))
    
class Dummy(Enemy):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "dummy.png", 0)
        self.indicatorRow = 5
        self.freezeShield = True
        self.nFrames = 1
        self.totalFrames = 1
        self.speed = 0
        self.maxHp = 5
        self.hp = self.maxHp
        self.damage = 0
    
    def getCollisionRect(self):
        return pygame.Rect(self.position, (16,16))
    
    def handleCollision(self, other):
        if issubclass(type(other), Bullet):
            if self.row < 1:
                self.row = 1
                self.flashTimer = 0
                self.hurt(other.damage)
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
        if enemy.frame == 2:
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
           
    

    
    
    
