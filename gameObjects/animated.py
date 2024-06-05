from . import Drawable
import pygame
from utils import SpriteManager, EQUIPPED, vec, RESOLUTION

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

    def updateWeapon(self, seconds, gale = False):
        if not self.animate:
            return
        
        self.animationTimer += seconds 
        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
           
            self.frame %= self.nFrames
            
            self.animationTimer -= 1 / self.framesPerSecond
            if gale and self.animating == False:
                self.animating = True
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
                if self.chargeTimer > 0.5:
                    if self.chargeTimer > 1.5:
                        if self.chargeTimer >= 2.5:
                            ##Fully charged
                            #print("C")
                            self.idleFrame += 1
                            if self.idleFrame == 13:
                                self.idleFrame = 9
                            chargeRow = self.row + 48
                        
                        else:# 3 < timer < 5
                            ##Medium charge
                            #print("B")
                            chargeRow = self.row + 40
                            
                            
                    else:# 1 <= timer <= 3
                        ##Low charge
                        #print("A")
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
                
    def updateShotParticle(self, seconds):
        fps = 16
        self.animationTimer += seconds

        if self.animationTimer > 1 / fps:
            self.frame += 1
            self.frame %= 7
            self.animationTimer -= 1 / fps
            
            self.image = SpriteManager.getInstance().getSprite("shotsfired.png",
                                                (self.frame, self.row))
            
    def updateReverse(self, seconds):
        self.animationTimer += seconds
        
        if self.animationTimer > 1 / self.framesPerSecond:
            
            self.frame -= 1
            self.frame %= self.nFrames
            
            self.animationTimer -= 1 / self.framesPerSecond
            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, self.row))
            
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
            

    def updateEnemy(self, seconds):
        self.animationTimer += seconds
        
        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
            self.frame %= self.nFrames
            self.animationTimer -= 1 / self.framesPerSecond
            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, self.row))

"""
Represents animated images on the HUD
"""
class HudImage(Animated):
    def __init__(self, position, offset, nFrames=4, fps=2):
        super().__init__(position, fileName="drops.png", offset=(0,0))
        self.row = offset[1]
        self.nFrames = nFrames
        self.framesPerSecond = fps

    
"""
Manages images in the hud in a singleton style
"""
class HudImageManager(object):

    MONEY = None
    KEYS = None

    def initialize():
        HudImageManager.MONEY = HudImage((0, 16*10+6), offset= (0,1))
        HudImageManager.KEYS = HudImage((0, RESOLUTION[1]-16), offset=(0,3))


    def getMoney():
        return HudImageManager.MONEY
    
    def getKeys():
        return HudImageManager.KEYS

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
            self.framesPerSecond = 20
            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                    (0, 0))
        
        def setRow(self, integer=0):
            self.row = integer
            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                    (0, self.row))

        def setFrame(self, integer=0):
            self.frame = integer
            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                    (self.frame, self.row))
        
        def update(self, seconds):
            super().update(seconds)
        
        def updateIn(self, seconds):
            super().updateReverse(seconds)
        
        def reset(self):
            self.frame = 0
            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                    (0, self.row))

class Highlight(Animated):
    def __init__(self, position, flag = 0):
        """
        flags:
        0-> Regular 16x16, 1 -> quit, 2 -> Y/N prompt, 3 -> map
        """
        if flag == 0:
            super().__init__(position, "cursor.png", (0,0))
        else:
            super().__init__(position, "Objects.png", (0,0))
        
        self.frameSet = False
        self.framesPerSecond = 8
        self.nFrames = 6
        self.initialized = False
        self.displayFlag = flag
        self.timer = 0

    def setInitialized(self):
        self.initialized = True

    def setRow(self, integer):
        self.row = integer
        
    def draw(self, drawSurface):
        if self.displayFlag == 0:
            super().draw(drawSurface)
        else:
            super().draw(drawSurface, True)
    
    def drawBlack(self, drawSurface):
        pass

    def getCollisionRect(self):
        if self.displayFlag == 1:
            return pygame.Rect((self.position), (16*8,32))
        elif self.displayFlag == 2:
            return pygame.Rect((self.position), (36,32))
        elif self.displayFlag == 3:
            return pygame.Rect((self.position[0]-1, self.position[1]-1), (10,10))
        else:
            return super().getCollisionRect()
    
    def updateFlashTimer(self, seconds):
        self.timer += seconds
    
    def update(self, seconds):
        super().update(seconds)

"""
Display flags:
0 -> normal, 1 -> elements
"""
class Pointer(Animated):
    def __init__(self, position, displayFlag = 0):
        if displayFlag > 0:
            super().__init__(position, "pointer.png", (0,1))
            self.row = 1
        else:
            super().__init__(position, "pointer.png")
            if displayFlag == 2:
                self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        self.nFrames = 4
        self.framesPerSecond = 2
        self.displayFlag = displayFlag
        self.choice = 0
        self.timer = 0.0
    
    def getChoice(self):
        return self.choice
    
    def increaseChoice(self):
        self.choice += 1
    
    def decreaseChoice(self):
        self.choice -= 1
    
    def setChoice(self, integer=0):
        self.choice = integer
    
    def update(self, seconds):
        self.timer += seconds
        if self.timer >= 2.8:
            self.frame += 1
            self.frame %= self.nFrames
            self.image = SpriteManager.getInstance().getSprite(self.fileName, (self.frame, self.row))
            if self.displayFlag == 2:
                self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
            self.timer = 0.0


class Tile(Animated):
    def __init__(self, position):
        super().__init__(position, "thunderTiles.png", (0,0))
        self.nFrames = 5


class ForceField(Animated):
    """
    Should be converted into an enemy type
    or simply add a damaging effect.
    """
    def __init__(self, position, color = 0):
        super().__init__(position, "barrier.png", (0, color))
        self.top = True
        self.nFrames = 4
        self.framesPerSecond = 8
        self.dead = False
        self.row = color
        self.frame += color
    
    def update(self, seconds, position = None):
        super().update(seconds)


class Portal(Animated):
    def __init__(self, position, color):
        super().__init__(position, "portal.png", (0,color))
        self.nFrames = 2
        self.row = color

class QuestIcon(Animated):
    def __init__(self, position):
        super().__init__(position, "exclamation.png", (0,0))
        self.nFrames = 4

class ZIcon(Animated):
    def __init__(self, position):
        super().__init__(position, "z.png", (0,0))
        self.nFrames = 4

class FireIcon(Animated):
    def __init__(self, position):
        super().__init__(position, "fireIcon.png", (0,0))
        self.nFrames = 4


class ShotParticle(Animated):
    def __init__(self, position=vec(0,0)):
        super().__init__(position, "shotsfired.png", (0,0))