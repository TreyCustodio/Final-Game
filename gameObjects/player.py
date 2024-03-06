from . import Bullet, Animated, Enemy, NonPlayer, Block, LockBlock
from utils import SpriteManager, SCALE, RESOLUTION, vec
import pygame



class Player(Animated):
    
    def __init__(self, position=vec(0,0), direction=0):
        super().__init__(position, "Link.png", (0, direction))  
        self.nFrames = 8
        self.vel = vec(0,0)
        self.speed = 100
        self.row = direction # (0 down), (1 right), (2 up), (3 left)
        self.pushing = False
        self.walking = False
        self.colliding = -1
        self.keys = 0

        #self.gun = Bullet(position, direction)

    def getBullet(self):
        return self.gun
    
    def getSpeed(self):
        return self.speed
    
    def getCollisionRect(self):
        
        if (self.row == 1):
            newRect = pygame.Rect(0,0,10,18)
            newRect.left = int(self.position[0]+6)
            newRect.top = int(self.position[1]+5)
        elif (self.row == 3):
            newRect = pygame.Rect(0,0,10,18)
            newRect.left = int(self.position[0]+2)
            newRect.top = int(self.position[1]+5)
        else:
            newRect = pygame.Rect(0,0,14,19)
            newRect.left = int(self.position[0]+2)
            newRect.top = int(self.position[1]+5)
        return newRect
    
    def handleEvent(self, event):
        ##  Key pressed down    ##
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                #Fire bullet
                pass
            if event.key == pygame.K_UP:
                #self.walking = True
                self.row = 2
                #self.set_Sprite(0)
                self.vel[1] = -self.speed

            elif event.key == pygame.K_DOWN:
                #self.walking = True
                self.row = 0
                #self.set_Sprite(0)
                self.vel[1] = self.speed


            elif event.key == pygame.K_LEFT:
                #self.walking = True
                if self.vel[1] == 0:
                    #print("here")
                    self.row = 3
                #self.set_Sprite(0)
                self.vel[0] = -self.speed
             
            elif event.key == pygame.K_RIGHT:
                #self.walking = True
                if self.vel[1] == 0:
                    #print("here")
                    self.row = 1
                #self.set_Sprite(0)
                self.vel[0] = self.speed

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
    
    def set_Sprite(self,value):
        self.image = SpriteManager.getInstance().getSprite(self.imageName, (value, self.row))

    def handleCollision(self, other):
        ##  Player handles collision based on the type of object they collide with  ##
        if type(other) == Enemy: #Change when npc class complete
            pass
        elif type(other) == Block or type(other) == LockBlock:
            self.pushing = True
            #print("yup")
            #Rows 4, 5, 6, 7 for pushing sprites
            if self.row == 0:    #Down
                self.vel = vec(0,0)
                self.position = (self.position[0], self.position[1]-1)

            elif self.row == 1:   #Right
                print("here")
                self.vel = vec(0,0)
                self.position = (self.position[0]-1, self.position[1])

            elif self.row == 2:   #Up
                self.vel = vec(0,0)
                self.position = (self.position[0], self.position[1]+1)

            elif self.row == 3:   #Left
                self.vel = vec(0,0)
                self.position = (self.position[0]+1, self.position[1])
            

    def update(self, seconds):
        #print(self.vel[1])
        if self.vel[0] == 0 and self.vel[1] == 0:
            self.walking = False
        else:
            self.walking = True
        super().update(seconds, self.walking, self.pushing)
        self.position += self.vel * seconds
    
    def updateMovement(self):
        pass
