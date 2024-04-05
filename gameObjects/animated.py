from . import Drawable
from utils import SpriteManager, EQUIPPED

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

    def updateWeapon(self, seconds):
        if not self.animate:
            return
        self.animationTimer += seconds 
        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
           
            self.frame %= self.nFrames
            
            self.animationTimer -= 1 / self.framesPerSecond
        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, self.row))
    
    def startAnimation(self, frame, state):
        pass


    def updatePlayer(self, seconds):
        """
        Update the player based on their states
        """
        self.animationTimer += seconds
        ##Animate Charging Sprite
        
        
        if self.freezing:
            if self.frame >= 4:
                self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                                   (self.frame+5, self.row+8))
                if self.frame == 6:
                    self.freezing = False
                    self.keyUnlock()
                    return
                
                else:
                    if self.animationTimer > 1 / 8:
                        self.frame += 1
                        self.animationTimer -= 1 / 8
                    return

            if self.animationTimer > 1 / 8:
                self.frame += 1
                self.frame %= 4
                self.animationTimer -= 1 / 8

            iceFrame = self.frame+5
            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                                   (iceFrame, self.row+8))
            return
        

        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
            self.frame %= self.nFrames
            self.animationTimer -= 1 / self.framesPerSecond

            
            if self.charging:
                if self.chargeTimer > 1:
                    if self.chargeTimer > 3:
                        if self.chargeTimer >= 5:
                            ##Fully charged
                            self.idleFrame += 1
                            if self.idleFrame == 13:
                                self.idleFrame = 9
                            chargeRow = self.row + 48
                        
                        else:# 3 < timer < 5
                            ##Medium charge
                            chargeRow = self.row + 40
                            
                            
                    else:# 1 <= timer <= 3
                        ##Low charge
                        chargeRow = self.row + 32

                else:# 0 < timer < 1
                    ##No charge
                    chargeRow = self.row + 24

                if self.walking:
                    if self.pushing:#Pushing charging
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                         (self.frame+1, chargeRow + 4))
                    else:#Walking charging
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, chargeRow))
                else:#Idle charging
                    if self.charged:
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.idleFrame, chargeRow))
                    else:
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (0, chargeRow))
                    

            elif not self.swordReady:##Fire attack
                self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                            (self.frame, self.row+8))
                if self.frame == 4:
                    self.swordReady = True

            elif self.running:##Running
                self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                            (self.frame, self.row+12))
            
            elif self.walking:
                if EQUIPPED["C"] == 2 and self.clapReady:

                    if self.pushing:##Clapready Pushing
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame+1, self.row+20))
                    
                    else:##Clapready Walking
                        self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, self.row+16))
                    
                
                        
                elif self.pushing:##Base Pushing
                    self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                            (self.frame+1, 4 + self.row))#Pushing sprites begin at row 4
                
                else:
                    ##Base Walking
                    self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                            (self.frame, self.row))
           
            else:##Idle
                
                if EQUIPPED["C"] == 2 and self.clapReady:##Clapready Idle
                    self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (0, self.row+16))
        
                else:##Base Idle
                    self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                            (0, self.row))
                

    def update(self, seconds):
        if not self.animate:
            return

        if self.FSManimated:
            self.FSManimated.updateState()
            
        
        self.animationTimer += seconds
        
        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
            self.frame %= self.nFrames
            self.animationTimer -= 1 / self.framesPerSecond
            self.image = SpriteManager.getInstance().getSprite(self.fileName,
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
            