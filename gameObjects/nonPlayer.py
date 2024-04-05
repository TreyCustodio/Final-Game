from . import Drawable, Animated
from utils import SpriteManager, SCALE, RESOLUTION, vec, rectAdd, SoundManager, FLAGS, SPEECH, ICON, INV
import pygame

class NonPlayer(Animated):
    """
    Non playable objects with an additional collision rect for interaction w/ player
    """

    def __init__(self, position = vec(0,0), fileName="", offset=None):
        super().__init__(position, fileName, offset)
        self.interacted = False
        self.animate = False
    
    def getInteractionRect(self):
        oldRect = self.getCollisionRect()
        newRect = pygame.Rect((oldRect.bottomleft),(oldRect.width,5))
        return newRect
    
    
        
    def draw(self, drawSurface, drawHitbox = False):
        super().draw(drawSurface, drawHitbox)
        if drawHitbox:
            interaction = rectAdd(-Drawable.CAMERA_OFFSET, self.getInteractionRect())
            pygame.draw.rect(drawSurface, (255,255,255), interaction, 1)
    
    def interact(self, player):
        pass

    def vanish(self, lst):
        lst.pop(lst.index(self))
        return lst
    

class Chest(NonPlayer):
    """
    Your typical chest. Remains
    opened once opened.
    """
    def __init__(self, position = vec(0,0), text = "", icon = None):
        super().__init__(position, "Objects.png", (0,1))
        self.icon = icon
        self.text = text

    def interact(self, engine):#drawSurface
        if self.interacted:
            engine.displayText("Empty.", large = False)

        else:
            self.interacted = True
            self.image = SpriteManager.getInstance().getSprite("Objects.png", (1,1))
            SoundManager.getInstance().playSFX("click1.wav")
            SoundManager.getInstance().playSFX("click2.wav")
            if self.icon != None:
                engine.displayText(self.text, self.icon, large = False)
                if self.icon == ICON["plant"]:
                    INV["plant"] += 1
            else:
                engine.displayText(self.text, large = False)

class Sign(NonPlayer):
    def __init__(self, position = vec(0,0), text = ""):
        super().__init__(position, "Objects.png", (1,2))
        self.text = text

    def interact(self, engine):#drawSurface
        engine.displayText(self.text)


class Barrier(NonPlayer):
    def __init__(self, position = vec(0,0), element = 0):
        super().__init__(position, "barrier.png", (0,element))
        if element == 0:
            self.text = SPEECH["ice"]
        elif element == 1:
            self.text = SPEECH["fire"]
            self.framesPerSecond = 8
            self.row = 1
        elif element == 2:
            self.text = SPEECH["thunder"]
            self.framesPerSecond = 40
            self.row = 2
        else:
            self.text = SPEECH["wind"]
            self.row = 3


    def interact(self,engine):
        engine.displayText(self.text)

class Blessing(NonPlayer):
    def __init__(self, position = vec(0,0), element=0):
        #0 -> ice
        #1 -> fire
        #2 -> thunder
        #3 -> wind
        super().__init__(position, "blessing.png", (0,element))
        if element == 0:
            self.text = SPEECH["ice"]
        elif element == 1:
            self.text = SPEECH["fire"]
            self.framesPerSecond = 8
            self.row = 1
        elif element == 2:
            self.text = SPEECH["thunder"]
            self.framesPerSecond = 20
            self.row = 2
        else:
            self.text = SPEECH["wind"]
            self.row = 3
        self.animate = True
        self.nFrames = 4
        self.element = element

    def getCollisionRect(self):
        return super().getCollisionRect()
    
    def interact(self, engine):
        if self.element == 0:
            INV["cleats"] = True
            FLAGS[90] = True
            FLAGS[89] = True
        elif self.element == 1:
            INV["fire"] = True
            FLAGS[91] = True
            FLAGS[89] = True
        elif self.element == 2:
            INV["clap"] = True
            FLAGS[92] = True
            FLAGS[89] = True
        elif self.element == 3:
            INV["slash"] = True
            FLAGS[93] = True
            FLAGS[89] = True
        engine.displayText(self.text)
        
class Geemer(NonPlayer):
    def __init__(self, position = vec(0,0), text = "", variant = None, maxCount = 0, fps = 16):
        super().__init__(position, "geemer.png", (0,0))
        self.vel = vec(0,0)
        self.position = position
        self.text = text
        self.row = 0
        self.nFrames = 6
        self.animate = True
        self.framesPerSecond = fps
        
        self.ignoreCollision = False
        self.max = maxCount
        self.variant = variant #Repeats same line of text over and over
        self.dialogueCounter = 0 #Helpful for displaying multiple different conversations
        self.icon = ICON["geemer"]
    
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+3, self.position[1]+2),(16,16))
    
    def getInteractionRect(self):
        return pygame.Rect((self.position[0]-1,self.position[1]+9), (24,11))
    
    def set_text(self, text=""):
        """
        For when characters display different dialogue after interaction
        """
        if text != "":
            self.text = text
        elif (self.interacted and (self.variant != None)):
            
            if self.dialogueCounter > self.max:
                self.dialogueCounter = 0

            if self.dialogueCounter == 0:
                if self.variant == 0:
                    self.text = SPEECH["intro_geemer1"]
                elif self.variant == 1:
                    self.text = SPEECH["intro_switches2"]
                elif self.variant == 2:
                    self.text = SPEECH["intro_plantgeemer3"]
                return
            
            elif self.dialogueCounter == 1:
                if self.variant == 0:
                    self.text = SPEECH["intro_geemer2"]

            elif self.dialogueCounter == 2:
                if self.variant == 0:
                    self.text = SPEECH["intro_geemer3"]
                return
            

    def interact(self, engine):
        if not self.interacted:
            #Display based on variant and inventory
            if self.variant == 2:
                if INV["plant"] >= 1:
                    self.interacted = True
                    self.text = SPEECH["intro_plantgeemer2"]
                    INV["plant"] -= 1
                    self.ignoreCollision = True
                    self.framesPerSecond = 2
                    self.vel = vec(10, 0)
                else:
                    engine.displayText(self.text, self.icon)
                    return

            elif self.variant == 0 and not INV["shoot"]:
                INV["shoot"] = True
                self.interacted = True

            else:
                self.interacted = True

        elif (self.variant != None):
            self.set_text()
            self.dialogueCounter += 1

        engine.displayText(self.text, self.icon)
       

    def update(self, seconds):
        super().update(seconds)
        self.position += self.vel * seconds





"""
Pickups/replenishables
- instant recharge on thunderclap
- fill up wind meter
- health
- temporary infinite recharge
"""
class Drop(NonPlayer):
    """
    Parent class for item pickups
    """
    def __init__(self, position=vec(0,0), offset = (0,0)):
        super().__init__(position, "Objects.png", offset)
        self.timer = 0
    
    def interact(self, player):
        self.interacted = True

    def update(self, seconds):
        super().update(seconds)
        

class Heart(Drop):
    def __init__(self, position=vec(0,0)):
        super().__init__(position, (0,3))
        self.disappear = False
        
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+3,self.position[1]+5), (10,8))
    
    def interact(self, player):
        if not self.interacted:
            SoundManager.getInstance().playSFX("solve.wav")
            self.interacted = True
            if player.hp < player.max_hp:
                player.hp += 1

    def update(self, seconds):
        super().update(seconds)
        self.timer += seconds
        if self.timer >= 5:
            self.disappear = True

class BigHeart(Drop):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, (0,4))
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+1), (16,14))
    
    def interact(self, player):
        if not self.interacted:
            SoundManager.getInstance().playSFX("solve.wav")
            self.interacted = True
            if player.hp < player.max_hp:
                player.hp += 3
                if player.hp > player.max_hp: 
                    player.hp = player.max_hp

class Key(Drop):
    """
    Parent class for item pickups
    """
    def __init__(self, position=vec(0,0)):
        super().__init__(position, (0,2))
        self.animate = False#could change
        self.text = SPEECH["key"]

    def interact(self, player, engine):
        if not self.interacted:
            self.interacted = True
            player.keys += 1
            engine.textBox = True
            engine.text = self.text
            player.vel = vec(0,0)
