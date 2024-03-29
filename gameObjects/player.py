from . import Bullet, Sword, Clap, Cleats, Animated, Enemy, Geemer, PushableBlock, NonPlayer, Block, HBlock, LockBlock
from utils import SpriteManager, SoundManager, SCALE, RESOLUTION, INV, vec
import pygame



class Player(Animated):
    
    def __init__(self, position=vec(0,0), direction=2):
        super().__init__(position, "Link.png", (0, direction))  
        #Frames, vel, speed, and row
        self.nFrames = 8
        self.vel = vec(0,0)
        self.speed = 75
        self.row = direction # (0 down), (1 right), (2 up), (3 left)
        #States
        self.charging = False
        self.movingTo = None
        self.moving = False
        self.pushing = False
        self.walking = False
        self.colliding = False
        self.shooting = False
        self.fired = False
        #Movement locks
        self.talking = False
        self.key_lock = False
        self.directionLock = False
        self.positionLock = False
        self.collisionRect = pygame.Rect((self.position[0]+1,self.position[1]+7),(16,16))
        ##Weapons/items##
        self.keys = 1
        #Bullet
        self.bullet = None
        #Sword
        self.sword = None
        self.swordReady = True
        self.swordSound = "DarkLink1.wav"
        self.swordCounter = 1
        self.swordRefresher = 0
        #Thunder clap
        self.clap = None
        self.clapTimer = 0
        self.clapReady = True
        #Ice cleats
        self.cleats = None
        self.running = False
        self.runningDirection = 0

        #Else
        self.items = []
        self.hp = 5
        self.max_hp = 5
        #self.ammo = F
        #self.max_ammo = 10
        self.event = None
        self.invincible = False
        self.iframeTimer = 0

    """
    Getter methods
    """
    ###Get weapon instances###
    def getBullet(self):
        return self.bullet

    def getTackle(self):
        return self.cleats

    def getSlash(self):
        return self.sword
    
    def getDirection(self, row):
        """
        Return the direction of the player based on the row of its sprite
        """
        if row > 3:
            if row > 4 and row < 8:
                return row - 4
            elif row >= 8 and row < 12:
                return row - 8
            elif row >= 12 and row < 16:
                return row - 12
            elif row >= 16:
                return row - 16
        else:
            return row
        
    def getClap(self):
        return self.clap
    
    def getSpeed(self):
        return self.speed
    
    def getTackleRect(self):
        return pygame.Rect(((self.position[0]-7),self.position[1]-2), (32,32))
    
    def getCollisionRect(self):
        if self.colliding:
            return self.collisionRect
        self.collisionRect = pygame.Rect((self.position[0]+2,self.position[1]+6),(14,16))
        return self.collisionRect
    
    def getHitBox(self):
        if self.row == 0:
            #Down
            newRect = pygame.Rect((self.position[0]+2,self.position[1]+7),(14,15))
        elif self.row == 1:
            #Right
            newRect = pygame.Rect((self.position[0]+6,self.position[1]+7),(10,15))
        elif self.row == 2:
            #Up
            newRect = pygame.Rect((self.position[0]+2,self.position[1]+6),(14,16))
        elif self.row == 3:
            #Left
            newRect = pygame.Rect((self.position[0]+1,self.position[1]+6),(11,16))
        return newRect

    def refreshAmmo(self):
        pass
        """ if self.ammo < self.max_ammo:
            self.ammo += 1 """

    def draw(self, drawSurface, drawHitbox = False, invis = False):
        if invis:
            drawSurface.blit(SpriteManager.getInstance().getSprite("null.png"), (0,0))
        else:
            super().draw(drawSurface, drawHitbox)
    
    """
    Movement and event handling
    """
    def movingDiagonal(self):
        return (self.vel[0] != 0 and self.vel[1] != 0)
    
    def keyLock(self):
        #self.stop()
        self.key_lock = True
    
    def keyUnlock(self):
        self.key_lock = False
    
    def moveTo(self, position):
        self.moving = True
        self.movingTo = position
        self.keyLock()
        
        

        


        #while self.position != 
    
    def isArrowKey(self, event):
        return (event == pygame.K_UP or event == pygame.K_DOWN or event == pygame.K_RIGHT or event == pygame.K_LEFT)
    
    def run(self):
        self.running = True
        self.vel *= 3
        SoundManager.getInstance().playSFX("screwattack_loop.wav", -1)

    def stop(self):
        self.running = False
        self.vel = vec(0,0)
        SoundManager.getInstance().stopSFX("screwattack_loop.wav")
    
    def slow(self):
        self.running = False
        self.vel /= 3
        SoundManager.getInstance().stopSFX("screwattack_loop.wav")

    def charge(self):
        self.stop()
        self.frame = 0
        self.charging = True


    def move(self, direction):
        """
        The player moves based on its direction.
        Updates self.row and self.vel accordingly
        """
        # X -> vel[0]
        if direction == 1:#Right
            if self.vel[1] == 0:
                self.row = 1
            self.vel[0] = self.speed
        elif direction == 3:#Left
            if self.vel[1] == 0:
                self.row = 3
            self.vel[0] = -self.speed

        # Y -> vel[1]
        elif direction == 0:#Down
            self.row = direction
            self.vel[1] = self.speed
        elif direction == 2:#Up
            self.row = direction
            self.vel[1] = -self.speed

    def handleEvent(self, event, interactableObject = None, engine = None):
        
        if not self.key_lock:
            #print("A")
            ##  Key pressed down  ##
            
            if event.type == pygame.KEYDOWN and not self.charging:
                if not self.pushing:
                    if interactableObject != None and event.key == pygame.K_z:
                        self.vel = vec(0,0)
                        interactableObject.interact(engine)

                    """ if event.key == pygame.K_f:
                        self.moveTo(vec(16*4,16*10)) """

                    if event.key == pygame.K_x and INV["shoot"] and not self.fired: #and self.ammo > 0:
                        #Fire bullet
                        SoundManager.getInstance().playSFX("OOT_DekuSeed_Shoot.wav")
                        self.bullet = Bullet(self.position, self.getDirection(self.row), self.hp, self.max_hp)
                        #self.ammo -= 1
                        self.shooting = True
                        self.fired = True
                        
                    if not self.running:
                        if event.key == pygame.K_a:
                            #print("A")
                            self.charge()

                        elif event.key == pygame.K_c and self.swordReady:
                            #Swing sword
                            self.sword = Sword(self.position, self.getDirection(self.row))
                            self.frame = -1
                            self.swordReady = False
                            self.vel = vec(0,0)
                            self.positionLock = True
                            self.directionLock = True
                            self.increaseSwordCounter()
 
                        elif event.key == pygame.K_v and self.clapReady:
                            #Thunder Clap
                            self.clap = Clap(self.position)
                            self.clapReady = False
                            self.vel = vec(0,0)
                            self.positionLock = True

                        elif event.key == pygame.K_z and ( self.walking and (not self.movingDiagonal()) ):
                            #Tackle
                            self.runningDirection = self.row
                            self.run()

                        elif self.swordReady:
                            ##  Directional Movement    ##
                            if event.key == pygame.K_UP: # 2
                                self.move(2)

                            elif event.key == pygame.K_DOWN: # 0
                                self.move(0)
                                
                            elif event.key == pygame.K_LEFT: # 3
                                self.move(3)
                                
                            elif event.key == pygame.K_RIGHT: # 1
                                self.move(1)



            ## Handle if a key is released  ##
            elif event.type == pygame.KEYUP:
                if self.charging:
                    if event.key == pygame.K_a:
                        #print("C")
                        self.charging = False
                    else:
                        return
                if self.running:
                    if event.key == pygame.K_z:
                        #Stop running
                        self.slow()
                    elif event.key == pygame.K_RIGHT and self.runningDirection == 1:
                        self.stop()
                    elif event.key == pygame.K_UP and self.runningDirection == 2:
                        self.stop()
                    elif event.key == pygame.K_LEFT and self.runningDirection == 3:
                        self.stop()
                    elif event.key == pygame.K_DOWN and self.runningDirection == 0:
                        self.stop()
                    

                else:
                    if event.key == pygame.K_UP:
                        #Display the proper sprite for diagonal
                        if self.vel[0] < 0:
                            self.row = 3
                        elif self.vel[0] > 0:
                            self.row = 1
                        #Stop upward velocity
                        if self.vel[1] < 0:
                            self.vel[1] = 0

                    elif event.key == pygame.K_DOWN:
                        #Display the proper sprite for diagonal
                        if self.vel[0] < 0:
                            self.row = 3
                        elif self.vel[0] > 0:
                            self.row = 1
                        #Stop downward velocity
                        if self.vel[1] > 0:
                            self.vel[1] = 0

                    elif event.key == pygame.K_LEFT:
                        #Stop leftward velocity
                        if self.vel[0] < 0:
                            self.vel[0] = 0
                           
                    elif event.key == pygame.K_RIGHT:
                        #Stop rightward velocity
                        if self.vel[0] > 0:
                            self.vel[0] = 0
                       
        
    """
    Locking position and direction
    """
    def lockDirection(self):
        self.directionLock = True
    
    def unlockDirection(self):
        self.directionLock = False
    
    def lockPosition(self):
        self.positionLock = True
    
    def unlockPosition(self):
        self.positionLock = False

    def adjustDirection(self, side):
        if side == "bottom":
            self.row = 0
            self.vel[0] = 0
            #self.vel[1] = self.speed/2
        elif side == "right":
            self.row = 1
            self.vel[1] = 0
            #self.vel[0] = self.speed/2
        elif side == "top":
            self.row = 2
            self.vel[0] = 0
            #self.vel[1] = -self.speed/2
        elif side == "left":
            self.row = 3
            self.vel[1] = 0
            #self.vel[0] = -self.speed/2


    """
    Collision detection
    """
    def interactable(self, object):
        return self.getCollisionRect().colliderect(object.getInteractionRect())
     
    def handleCollision(self, object):
        if self.running:
            self.stop()

        elif type(object) == PushableBlock:
            side = self.calculateSide(object)
            self.pushing = True

            if object.resetting:
                if self.pushing:
                    self.pushing = False
                    if self.vel[1] > 0:
                        self.vel[1] = self.speed
                    elif self.vel[1] < 0:
                        self.vel[1] = -self.speed
                    elif self.vel[0] > 0:
                        self.vel[0] = self.speed
                    elif self.vel[0] < 0:
                        self.vel[0] = -self.speed
                    self.preventCollision(object, side)
                
            else:
                if not self.movingDiagonal():
                    self.adjustDirection(side)
                    if self.vel[1] > 0:
                        self.vel[1] = self.speed/3
                    elif self.vel[1] < 0:
                        self.vel[1] = -self.speed/3
                    elif self.vel[0] > 0:
                        self.vel[0] = self.speed/3
                    elif self.vel[0] < 0:
                        self.vel[0] = -self.speed/3

                    object.push()
                else:
                    self.preventCollision(object, side)

        elif type(object) == Geemer and object.ignoreCollision:
            return
        elif type(object) == Enemy:
            side = self.calculateSide(object)
            self.enemyCollision(object, side)

        else:
            side = self.calculateSide(object)
            self.preventCollision(object, side)

    def enemyCollision(self, enemy, side):
        if self.invincible or enemy.frozen:
            pass
        else:
            self.hp -= enemy.getDamage()
            SoundManager.getInstance().playSFX("samus_damage.wav")
            self.invincible = True
            self.knockback(side)
            
    def preventCollision(self, object, side):
        #Prevents overlapping collision rects based on side
        #self.position = vec(self.position)
        print(self.position)
        obj = object.getCollisionRect()
        coll = self.getCollisionRect()
        if side == "right":
            self.position[0] = (obj.left) - (obj.width - (obj.width - coll.width)) - 2#Line up the rects and put player 1 pixel before colliding
        elif side == "left":
            self.position[0] = (obj.left) + (obj.width - (obj.width - coll.width)) + 1
        elif side == "top":
            self.position[1] = (obj.top) + (obj.height - (obj.height - coll.height)) - 6
        elif side == "bottom":
            self.position[1] = (obj.top) - (obj.height - (obj.height - coll.height) + 6)
        SoundManager.getInstance().playSFX("bump.mp3")

    def calculateSide(self, object):
        ##  Colliding with Block    ##
        collision1 = self.collisionRect
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

    def knockback(self,side):
        if side == "right":
            self.position[0] -= 5
        elif side == "left":
            self.position[0] += 5
        elif side == "top":
            self.position[1] += 5
        elif side == "bottom":
            self.position[1] -= 5

    def inPosition(self, position):
        return self.position[0] == position[0] and self.position[1] == position[1]

    """
    Updating
    """
    ##  Determining the sound that plays when sword is swung    ##
    def increaseSwordCounter(self):
        if self.swordCounter >= 3:
            self.swordCounter = 1
        
        else:
            self.swordCounter += 1

        if self.swordCounter == 1:
            self.swordSound = "DarkLink1.wav"
        elif self.swordCounter == 2:
            self.swordSound = "DarkLink2.wav"
        elif self.swordCounter == 3:
            self.swordSound = "DarkLink3.wav"

    def update(self, seconds):
        if self.charging:
            super().update(seconds, charging = True)
            if self.frame == 15:
                #print("B")
                self.charging = False
                SoundManager.getInstance().playSFX("plasma_shot.wav")
                #self.slash = self.getSlash()
            return
        
        if self.moving:
            if self.inPosition(self.movingTo):
                self.vel = vec(0,0)
                self.movingTo = None
                self.keyUnlock()
            else:
                if self.position[0] < self.movingTo[0]:
                    self.vel[0] = self.speed
                elif self.position[0] > self.movingTo[0]:
                    self.vel[0] = -self.speed
                if self.position[1] < self.movingTo[1]:
                    self.vel[1] = self.speed
                elif self.position[1] > self.movingTo[1]:
                    self.vel[1] = -self.speed
            self.position += self.vel * seconds
            
            return
        
        if self.fired:
            self.fired = False
        
        
        #Update walking state
        if self.vel[0] == 0 and self.vel[1] == 0:
            self.walking = False
        else:
            self.walking = True
        
        #Update invincibility if needed
        if self.invincible:
            self.iframeTimer += seconds 
            if self.iframeTimer >= 2:
                self.iframeTimer = 0
                self.invincible = False

            elif self.iframeTimer <= 1.85:
                self.image = SpriteManager.getInstance().getSprite("null.png")

        #Update sword cooldown
        """ if self.swordReady == False:
            self.swordRefresher += seconds
            if self.swordRefresher >= 0.3:
                self.swordRefresher = 0
                self.swordReady = True
                self.row -= 8 """
        
        #Update clap cooldown
        if self.clapReady == False:
            self.clapTimer += seconds
            if self.clapTimer >= 5.0:
                self.clapTimer = 0
                self.clapReady = True
        
        super().update(seconds, self.walking, self.pushing, self.swordReady, self.clapReady)

        if not self.shooting:
            self.refreshAmmo()
        
        
        self.position += self.vel * seconds
        print(self.position)
    def updateMovement(self):
        pass

