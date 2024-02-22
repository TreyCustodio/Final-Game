from drawable import Drawable
from spriteManager import SpriteManager
from vector import vec, rectAdd
import pygame

class Player(Drawable):
    def __init__(self, fileName, position, direction=2):
        super().__init__(fileName, position, (0,direction))
        self.vel = vec(0,0)
        self.speed = 250
        self.direction = direction # (0 down), (1 right), (2 up), (3 left)
    
    def handleEvent(self, event):
        ##  Key pressed down    ##
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # move up
                self.direction = 2
                self.image = self.SM.getSprite(self.fileName, (0,2))
                self.vel[1] = -self.speed
            elif event.key == pygame.K_DOWN:
                # move down
                self.direction = 0
                self.image = self.SM.getSprite(self.fileName, (0,0))
                self.vel[1] = self.speed
            elif event.key == pygame.K_LEFT:
                    # move left!
                self.direction = 3
                self.image = self.SM.getSprite(self.fileName, (0,3))
                self.vel[0] = -self.speed
            elif event.key == pygame.K_RIGHT:
                    # move right!
                self.direction = 1
                self.image = self.SM.getSprite(self.fileName, (0,1))
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
        self.image = self.SM.getSprite(self.fileName, (value, self.direction))

    def handleCollision(self, other):
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

    def update(self, seconds):
        self.position += self.vel * seconds
    
