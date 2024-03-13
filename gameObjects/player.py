from . import Bullet, Sword, Animated, Enemy, NonPlayer, Block, LockBlock
from utils import SpriteManager, SCALE, RESOLUTION, vec
import pygame



class Player(Animated):
    
    def __init__(self, position=vec(0,0), direction=0):
        super().__init__(position, "Link.png", (0, direction))  
        #Frames, vel, speed, and row
        self.nFrames = 8
        self.vel = vec(0,0)
        self.speed = 100
        self.row = direction # (0 down), (1 right), (2 up), (3 left)
        #States
        self.pushing = False
        self.walking = False
        self.colliding = False
        #Movement locks
        self.talking = False
        self.directionLock = False
        self.positionLock = False
        self.collisionRect = pygame.Rect((self.position[0]+1,self.position[1]+7),(16,16))
        #Weapons/items
        self.keys = 0
        self.bullet = None
        self.sword = None
        self.items = []


    """
    Getter methods
    """
    ###Get weapon instances###
    def getBullet(self):
        return self.bullet

    def getSlash(self):
        return self.sword
    
    def getSpeed(self):
        return self.speed
    
    def getCollisionRect(self):
        if self.colliding:
            return self.collisionRect
        self.collisionRect = pygame.Rect((self.position[0]+1,self.position[1]+7),(16,16))
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
    

    """
    Movement and event handling
    """
    def bounce(self, direction):
        pass
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


    def handleEvent(self, event, interactableObject = None):
        #print(event)
        if not self.positionLock:
            ##  Key pressed down  ##
            if event.type == pygame.KEYDOWN:
                if interactableObject != None and event.key == pygame.K_z:
                    interactableObject.interact(self)
                if event.key == pygame.K_x:
                    #Fire bullet
                    self.bullet = Bullet(self.position, self.row)
                if event.key == pygame.K_c:
                    #Swing sword
                    self.sword = Sword(self.position, self.row)
                    self.vel = vec(0,0)
                    self.positionLock = True
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
                if event.key == pygame.K_UP:
                    #self.walking = False
                    #self.set_Sprite(0)
                    if self.vel[0] < 0:
                        self.row = 3
                    elif self.vel[0] > 0:
                        self.row = 1
                    self.vel[1] = 0
                elif event.key == pygame.K_DOWN:
                    #self.walking = False
                    #self.set_Sprite(0)
                    if self.vel[0] < 0:
                        self.row = 3
                    elif self.vel[0] > 0:
                        self.row = 1
                    self.vel[1] = 0
                elif event.key == pygame.K_LEFT:
                    if self.vel[0] == self.speed:
                        pass
                    else:
                    #self.walking = False
                    #self.set_Sprite(0)
                        self.vel[0] = 0
                elif event.key == pygame.K_RIGHT:
                    
                    #self.walking = False
                    #self.set_Sprite(0)
                        if self.vel[0] == -self.speed:
                            pass
                        else:
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







    """
    Collision detection
    """
    def blockCollision(self):
        self.colliding = True








        self.positionLock = True
        oldVel = self.vel
        self.vel = vec(0,0)
        if oldVel[0] != 0:
            if oldVel[1] != 0:
                #Velocity in both directions
                if oldVel[0] < 0:
                    self.position = vec(*(self.position[0]+4, self.position[1]))
                else:
                    self.position = vec(*(self.position[0]-4, self.position[1]))
                if oldVel[1] < 0:
                    self.position = vec(*(self.position[0], self.position[1]+4))
                else:
                    self.position = vec(*(self.position[0], self.position[1]-4))
            else:
                #Velocity in X direction
                if oldVel[0] < 0:
                    #Moving Left (3)
                    self.position = vec(*(self.position[0]+4, self.position[1]))
                else:
                    #Moving Right (1)
                    self.position = vec(*(self.position[0]-4, self.position[1]))
        elif oldVel[1] != 0:
            #Velocity in Y direction
            if oldVel[1] < 0:
                #Moving up (1)
                self.position = vec(*(self.position[0], self.position[1]+4))
            else:
                #Moving down (0)
                self.position = vec(*(self.position[0], self.position[1]-4))

        else:
            pass
            #Velocity in no direction -> Could be stuck in a wall
            
        if self.row == 0:    #Down
            
            self.position = (self.position[0], self.position[1]+1)

        elif self.row == 1:   #Right
            
            self.position = (self.position[0]+1, self.position[1])

        elif self.row == 2:   #Up
            
            self.position = (self.position[0], self.position[1]-1)

        elif self.row == 3:   #Left
            
            self.position = (self.position[0]-1, self.position[1])
        self.positionLock = False


    def handleCollision(self, other):
        ##  Player handles collision based on the type of object they collide with  ##
        if type(other) == Enemy:
            self.blockCollision()
        else:
            self.blockCollision()







    """
    Update
    """
    def update(self, seconds):
        if self.vel[0] == 0 and self.vel[1] == 0:
            self.walking = False
        else:
            self.walking = True
        super().update(seconds, self.walking, self.pushing)
        self.position += self.vel * seconds
    
    def updateMovement(self):
        pass
