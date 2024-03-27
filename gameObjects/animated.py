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
    
    def update(self, seconds, walking = None, pushing = None, swordReady = False, clapReady = False, charging = False):#Will have to convert these states into FSMS
        if not self.animate:
            return

        if self.FSManimated:
            self.FSManimated.updateState()
            
        
        self.animationTimer += seconds 
        if charging:
            if self.animationTimer > 1 / 8:
                self.frame += 1
                self.frame %= 16
                self.animationTimer -= 1 / 8

            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                                   (self.frame, self.row+24))
            return
        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
            self.frame %= self.nFrames
            self.animationTimer -= 1 / self.framesPerSecond

            
            
            if walking != None:
                
                

                if not swordReady:
                    self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, self.row+8))
                    if self.frame == 4:
                        self.swordReady = True
                elif self.running:
                    self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, self.row+12))
                elif walking == True:
                    if clapReady:
                        if pushing:
                            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                    (self.frame+1, self.row+20))
                        else:
                            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                    (self.frame, self.row+16))
                        return
                    if pushing:
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame+1, 4 + self.row))#Pushing sprites begin at row 4
                    else:
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, self.row))
                else:
                    
                    if clapReady:
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                    (0, self.row+16))
                        
                    else:
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (0, self.row))
            else:
                
                self.image = SpriteManager.getInstance().getSprite(self.fileName,#Not accessed by the player (walking always passed)
                                                (self.frame, self.row))

class Fade():
    """
    If there's only going to be one animation of fades, a singleton class works.
    However, there is the possibility of using the fade differently for each room.
    But I could also just use methods on the one instance to change its appearance as well.
    """

    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._FA()
        return cls._INSTANCE

    class _FA(Animated):
        def __init__(self):
            super().__init__((0,0), "black.png", (0,0))
            self.nFrames = 9
            self.framesPerSecond = 32
        
        def update(self, seconds):
            if self.frame < 9:
                super().update(seconds)
        
        def reset(self):
            self.frame = 0
            self.image = SpriteManager.getInstance().getSprite(self.fileName,#Not accessed by the player (walking always passed)
                                                    (self.frame, self.row))
            