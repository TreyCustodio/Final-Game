from . import Drawable, Enemy, NonPlayer, Block
from utils import SpriteManager, SCALE, RESOLUTION, vec
import pygame

class Player(Drawable):
    def __init__(self, position=vec(0,0), fileName="", direction=2):
        super().__init__(position, fileName, (0, direction))
        self.vel = vec(0,0)
        self.speed = 100
        self.direction = direction # (0 down), (1 right), (2 up), (3 left)
    
    def getSpeed(self):
        return self.speed
    
    def getCollisionRect(self):
        
        if (self.direction == 1):
            newRect = pygame.Rect(0,0,10,18)
            newRect.left = int(self.position[0]+6)
            newRect.top = int(self.position[1]+5)
        elif (self.direction == 3):
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
            if event.key == pygame.K_UP:
                # move up
                self.direction = 2
                self.set_Sprite(0)
                self.vel[1] = -self.speed
            elif event.key == pygame.K_DOWN:
                # move down
                self.direction = 0
                self.set_Sprite(0)
                self.vel[1] = self.speed
            elif event.key == pygame.K_LEFT:
                    # move left!
                self.direction = 3
                self.set_Sprite(0)
                self.vel[0] = -self.speed
            elif event.key == pygame.K_RIGHT:
                    # move right!
                self.direction = 1
                self.set_Sprite(0)
                self.vel[0] = self.speed


        ## Handle if a key is released  ##
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                # move up
                self.set_Sprite(0)
                self.vel[1] = 0
            elif event.key == pygame.K_DOWN:
                # move down
                self.set_Sprite(0)
                self.vel[1] = 0
            elif event.key == pygame.K_LEFT:
                # move left
                self.set_Sprite(0)
                self.vel[0] = 0
            elif event.key == pygame.K_RIGHT:
                # move right!
                self.set_Sprite(0)
                self.vel[0] = 0
    
    def set_Sprite(self,value):
        self.image = SpriteManager.getInstance().getSprite(self.imageName, (value, self.direction))

    def handleCollision(self, other):
        ##  Player handles collision based on the type of object they collide with  ##
        if type(other) == NonPlayer: #Change when npc class complete
            self.vel = vec(0,0)
            self.set_Sprite(1)
            if self.direction == 0:    #Down
                self.position = (self.position[0], self.position[1]-1)

            elif self.direction == 1:   #Right
                self.position = (self.position[0]-1, self.position[1])

            elif self.direction == 2:   #Up
                self.position = (self.position[0], self.position[1]+1)

            elif self.direction == 3:   #Left
                self.position = (self.position[0]+1, self.position[1])
        elif type(other) == Enemy:
            pass
                

    def update(self, seconds):
        self.position += self.vel * seconds
    
    def updateMovement(self):
        pass
