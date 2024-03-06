from . import Drawable
from utils import SpriteManager

class Animated(Drawable):
    
    def __init__(self, position=(0,0), fileName="", offset = (0,0)):
        super().__init__(position, fileName, offset)
        self.fileName = fileName
        self.row = 0
        self.frame = 0
        self.nFrames = 1
        self.animate = True
        self.framesPerSecond = 16
        self.animationTimer = 0
        self.FSManimated = None
    
    def update(self, seconds, walking = None, pushing = None):#Will have to convert these states into FSMS
        if self.FSManimated:
            self.FSManimated.updateState()
            
        if not self.animate:
            return
        
        self.animationTimer += seconds 
           
        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
            #print(self.frame)
            #print(walking)
            #print(pushing)
            self.frame %= self.nFrames
            self.animationTimer -= 1 / self.framesPerSecond

            if walking != None:
                if walking == True:
                    if pushing:
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame+1, 4 + self.row))#Pushing sprites begin at row 4
                    else:
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, self.row))
                else:
                    self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (0, self.row))
            else:
                self.image = SpriteManager.getInstance().getSprite(self.fileName,#Not accessed by the player (walking always passed)
                                                (self.frame, self.row))
