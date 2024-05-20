from typing import Any
from utils import SpriteManager, SCALE, RESOLUTION, EQUIPPED, INV, vec, rectAdd, SoundManager
from . import PixelBuilder
import pygame
"""
This file contains Drawable Objects, including HUD-related objects
and text-related objects.
"""

        
class Drawable(object):
    """
    Drawable object class written by Professor Matthews
    """
    
    CAMERA_OFFSET = vec(0,0)
    
    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        
        objSize = trackingObject.getSize()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (RESOLUTION // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - RESOLUTION[i])))
        
        cls.CAMERA_OFFSET = offset
        
        

    @classmethod    
    def translateMousePosition(cls, mousePos):
        newPos = vec(*mousePos)
        newPos /= SCALE
        newPos += cls.CAMERA_OFFSET
        
        return newPos
    
    def __init__(self, position=vec(0,0), fileName="", offset=None):
        
        if fileName != "":
            self.image = SpriteManager.getInstance().getSprite(fileName, offset)
        
        self.position  = vec(*position)
        self.imageName = fileName

    def draw(self, drawSurface, drawHitbox = False):
        drawSurface.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
        if drawHitbox:
            collision = rectAdd(-Drawable.CAMERA_OFFSET, self.getCollisionRect())
            pygame.draw.rect(drawSurface, (255,255,255), collision, 1)

    def getSize(self):
        return vec(*self.image.get_size())
    
    """
    Returns the x coordinate on the screen
    representing the center point
    """
    def getCenterX(self):
        size = self.getSize()
        x = size[0] // 2
        return self.position[0] + x
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass
    
    
    def getCollisionRect(self):
        newRect = self.image.get_rect()
        newRect.left = int(self.position[0])
        newRect.top = int(self.position[1])
        return newRect
    
    def doesCollide(self, other):
        return self.getCollisionRect().colliderect(other.getCollisionRect())   
    
    def doesCollideList(self, others):
        rects = [r.getCollisionRect() for r in others]
        return self.getCollisionRect().collidelist(rects)


class Level(Drawable):
    """
    Gets the image for the level using the SpriteManager
    """
    def __init__(self, fileName):
        super().__init__((0,0), "")
        self.image = SpriteManager.getInstance().getLevel(fileName)


class Number(Drawable):
    """
    If number >= 10
    """
    def __init__(self, position = vec(0,0), number = 0, row = 0):
        super().__init__(position, "numbers.png", (number,row))
        
class Text(Drawable):
    """
    Displays text using the font from A Link to the Past
    """
    import os
    if not pygame.font.get_init():
        pygame.font.init()
    FONT_FOLDER = "fonts"
    FONT = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 16)
    BOX = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 14)
    SMALL = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 12)
    
    def __init__(self, position, text, color = (255,255,255), box = False, small = False):
        super().__init__(position, "")
        if small:
            self.image = Text.SMALL.render(text, False, color)
        elif box:
            self.image = Text.BOX.render(text, False, color)
        else:
            self.image = Text.FONT.render(text, False, color)


class AmmoBar(Drawable):
    """
    Displays the currently selected arrow on the HUD
    """
    def __init__(self):
        super().__init__(vec(0,15), "ammo.png", (0,0))

    def draw(self, drawSurface, player):
        row = player.arrowCount
        if player.hp == INV["max_hp"]:
            self.image = SpriteManager.getInstance().getSprite("ammo.png", (1,row))

        elif player.hp <= INV["max_hp"]/4 or player.hp == 1:
            self.image = SpriteManager.getInstance().getSprite("ammo.png", (2,row))
        else:
            self.image = SpriteManager.getInstance().getSprite("ammo.png", (0,row))
        super().draw(drawSurface)


class DamageIndicator(Drawable):
    """
    Displays the health, name, and image
    of the currently targeted (last hit) enemy
    """
    def __init__(self):
        super().__init__(vec(RESOLUTION[0] - 58, 0), "indicator.png", (0,0) )
        self.invisible = True
        self.row = 0
        self.indicatorTimer = 0
        self.currentHp_before = 0
        self.currentHp = 0
        self.currentMaxHp = 0
        self.currentDrawPos = 0#X position of current draw position
        self.pixelBuilder = PixelBuilder()
        self.currentPixels = []
        self.pixelsToDraw = 0

        
    
    
    def draw(self, drawSurface):
        if not self.invisible:
            super().draw(drawSurface)
            if self.row > 0:
                index = 0
                for p in self.currentPixels:
                    index += 1
                    drawSurface.blit(p.getPixel(), p.getDrawPos())


    def setPixelsToDraw(self, value):
        self.pixelsToDraw = value

    def setImage(self, value, hp_before=0, hp_after=0, maxHp = 0, damage = 0):
        """
        Called every time an enemy is struck.
        Start from far right
        Calculate # of pixels to turn white based on damage and max hp
        Subtract drawPos[0] and increase the width of the pixels
        to draw by the same amount
        Turn that # of pixels white
        Wait a bit
        Gradually turn the white pixels black
        But just fill in the pixels with black according to
        hp_before

        Expects the following parameters:
        value -> int value of enemy's indicator image row
        hp_before -> enemy's hp before taking damage
        hp_after -> enemy's hp after taking damage
        maxHp -> enemy's max hp
        damage -> the damage dealt to the enemy

        MaxHp - previous hp, draw those pixels
        then draw current pixels
        """
        ##Turn invisible and return if setImage(0) called
        if value == 0:
            #self.pixelsToDraw = 0
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (0, value))
            self.invisible = True
            return
        
        self.invisible = False
        ##Reset the indicator timer
        self.indicatorTimer = 0
        ##Set the row value if not already set to that row
        if value != self.row:
            self.row = value
        
        ##Defining temporary variables
        self.currentHp_before = hp_before
        self.currentHp = hp_after
        self.currentMaxHp = maxHp
        #Temporary list object used to draw the pixels
        currentPixels = []

        
        cumulativeDamage = self.currentMaxHp - self.currentHp 
        result = self.currentMaxHp // 28
        if result == 0:
            #Figure out how to draw x pixels for every 1 pt of damage
            result = 1
        else:
            #draw 1 pixel for every result points of damage
            self.setPixelsToDraw(cumulativeDamage // result)
        

        #pixelsToDraw = int(pixelsPerHit * damage)
        #prevPixels = int(pixelsPerHit * (self.currentMaxHp - self.currentHp))
        

        ##Adjust drawPos to account for previously dealt damage
        self.currentDrawPos = (self.position[0]+53)


        ##Set the indicator imagess
        if self.currentHp <= 0:
            #Enemy dead, make the indicator invisible
            self.row = 0
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (0, 0))
            self.indicatorTimer = 0
        else:
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (0, value))

        for i in range(self.pixelsToDraw):
            self.pixelBuilder.addPixel(currentPixels, vec(self.currentDrawPos - i, self.position[1]+8), 1, 8, color = (0,0,0))
        
        self.currentPixels = currentPixels


        """         if black > 0:
            #print("B")
            ##Add black pixels
            for i in range(black):
                self.pixelBuilder.addPixel(self.currentPixels, vec(self.currentDrawPos - i, self.position[1]+8), 1, 8, color = (0,0,0))
            
            ##Add white pixels
            for i in range(black, (pixelsToDraw - black)):
                self.pixelBuilder.addPixel(self.currentPixels, vec(self.currentDrawPos - i, self.position[1]+8), 1, 8)

        else:
            #print("C")
            ##First hit
            ##Add the necessary pixels to the pixelBuilder
            ##pixelsToDraw needs to be an int for looping
            for i in range(pixelsToDraw):
                self.pixelBuilder.addPixel(self.currentPixels, vec(self.currentDrawPos - i, self.position[1]+8), 1, 8) """
        
        
    
    def update(self, seconds):
        """
        Update the pixelBuilder and indicatorTimer.
        Set the indicator to invisible after 3 seconds
        of no action.
        """
        if self.row > 0:
            #If currently targeting an enemy
            #self.pixelBuilder.update(seconds)
            self.indicatorTimer += seconds
            if self.indicatorTimer >= 3:
                #Set invisible
                self.setImage(0)




class ElementIcon(Drawable):
    """
    Displays the currently selected element on the HUD
    """
    def __init__(self):
        super().__init__(vec(15,15), "ammo.png", (0,2))

    def draw(self, drawSurface):
        equipped = EQUIPPED["C"]
        if equipped != None:
            self.image = SpriteManager.getInstance().getSprite("ammo.png", (equipped+1, 2))
        super().draw(drawSurface)
        

class EnergyBar(Drawable):
    """
    Displays the player's energy meter on the HUD.
    For Gale Slash and Thunder Clap
    """
    def __init__(self):
        super().__init__(vec(0,31), "energy.png", (0,0))
        self.element = 0
        self.flashTimer = 0

    def setElement(self, int=0):
        self.element = int
        self.image = SpriteManager.getInstance().getSprite("energy.png", (self.element,0))

    def draw(self, drawSurface):
        super().draw(drawSurface)


    
    def drawWind(self, timer, drawSurface):
        """
        fill meter as timer increases
        """
        
        #convert timer to an int and shift decimal
        if timer < 2.5:
            convertedTimer = int(timer * 10)
        else:
            convertedTimer = 25

        #print(convertedTimer)
        #28 pixels to fill
        #1 pixel on top and 1 on bottom 
        drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (2, 0)), list(map(int, self.position)))
        
        innerFlash = pygame.Surface((1,1), pygame.SRCALPHA)
        innerFlash.fill(pygame.Color(0,235,0))

        light = pygame.Surface((1,1), pygame.SRCALPHA)
        light.fill(pygame.Color(0,220,0))
        green = pygame.Surface((1,1), pygame.SRCALPHA)
        green.fill(pygame.Color(0,180,0))

        def drawBar(timer, width, drawPos, edge = False):
            if edge:
                for i in range(width):
                    if timer >= 2.5:
                        if timer < 2.7:
                            light.fill(pygame.Color(0,255,0))
                        elif timer >= 2.7 and timer < 2.9:
                            light.fill(pygame.Color(0,220,0))
                        elif timer >= 2.9:
                            light.fill(pygame.Color(0,255,0))
                    drawSurface.blit(light, (drawPos[0]+i, drawPos[1]))
                return
            
            bottomPos = drawPos
            for i in range(1, width):
                if timer >= 2.5:
                    if timer < 2.7:
                        drawSurface.blit(innerFlash, (drawPos[0]+i, drawPos[1]))
                        light.fill(pygame.Color(0,255,0))
                    elif timer >= 2.7 and timer < 2.9:
                        drawSurface.blit(green, (drawPos[0]+i, drawPos[1]))
                        light.fill(pygame.Color(0,220,0))
                    elif timer >= 2.9:
                        drawSurface.blit(innerFlash, (drawPos[0]+i, drawPos[1]))
                        light.fill(pygame.Color(0,255,0))
                    
                    
                else:
                    drawSurface.blit(green, (drawPos[0]+i, drawPos[1]))

            drawSurface.blit(light, bottomPos)
            drawSurface.blit(light, (drawPos[0]+width-1, drawPos[1]))
        
        ##Draw bottom bar of pixels
        if timer > 0:
            drawPos = vec(3,60)
            drawBar(timer, 10, drawPos, edge=True)

            ##Draw the middle part
            if timer >= 0.1:
                drawPos = vec(2, 60-convertedTimer)
                yPos = int(drawPos[1])
                for i in range(60 - yPos):
                    drawPos[1] = yPos + i
                    drawBar(timer,12, drawPos)
   

                ##Draw the top pixel
                if convertedTimer >= 25:
                    drawPos = vec(2,34)
                    drawBar(timer,12, drawPos)
            
            

                    drawPos = vec(3,33)
                    drawBar(timer, 10, drawPos, edge= True)


        """ elif timer > 0:
            print("B")
            sprite = pygame.Surface((10,1), pygame.SRCALPHA)
            sprite.fill(pygame.Color(0,255,0))
            drawPos = vec(3,60-convertedTimer)
            drawSurface.blit(sprite, drawPos) """

            
     
        """ if timer >= 2.5:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (2, 5)), list(map(int, self.position)))
        elif timer >= 1.5:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (2, 3)), list(map(int, self.position)))
        elif timer >= 0.5:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (2, 2)), list(map(int, self.position)))
        else: """
        

    def drawThunder(self, timer, drawSurface):
        if timer == 0:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (1, 5)), list(map(int, self.position)))
        else:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (1, int(timer))), list(map(int, self.position)))


class HealthBar(object):
    """
    Displays the player's health on the HUD
    Make singleton!
    """
    _INSTANCE = None


    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._HB()
        return cls._INSTANCE

    class _HB(object):
        def __init__(self):
            self.position = vec(0,0)
            self.fileName = "bar.png"

            ###Pixel IVs
            self.edge = SpriteManager.getInstance().getSprite(self.fileName, (6,0))
            ##Green pixels
            self.edgeG = SpriteManager.getInstance().getSprite(self.fileName, (7,0))
            self.green = SpriteManager.getInstance().getSprite(self.fileName, (8,0))
            ##Red pixels
            self.edgeR = SpriteManager.getInstance().getSprite(self.fileName, (0,0))
            self.red1 = SpriteManager.getInstance().getSprite(self.fileName, (1,0))
            self.red2 = SpriteManager.getInstance().getSprite(self.fileName, (2,0))
            self.red3 = SpriteManager.getInstance().getSprite(self.fileName, (3,0))
            self.red4 = SpriteManager.getInstance().getSprite(self.fileName, (4,0))
            self.red5 = SpriteManager.getInstance().getSprite(self.fileName, (5,0))
            self.red6 = SpriteManager.getInstance().getSprite(self.fileName, (9,0))
            self.red7 = SpriteManager.getInstance().getSprite(self.fileName, (10,0))
            self.edgeL = SpriteManager.getInstance().getSprite(self.fileName, (11,0))
            self.red8 = SpriteManager.getInstance().getSprite(self.fileName, (12,0))
            self.white = SpriteManager.getInstance().getSprite(self.fileName, (13,0))
            ##lowHp
            self.low1 = SpriteManager.getInstance().getSprite(self.fileName, (14,0))
            self.low2 = SpriteManager.getInstance().getSprite(self.fileName, (15,0))
            self.low3 = SpriteManager.getInstance().getSprite(self.fileName, (16,0))
            self.low4 = SpriteManager.getInstance().getSprite(self.fileName, (17,0))
            self.low5 = SpriteManager.getInstance().getSprite(self.fileName, (18,0))
            #White flashing
            self.low6 = SpriteManager.getInstance().getSprite(self.fileName, (19,0))
            self.low7 = SpriteManager.getInstance().getSprite(self.fileName, (20,0))
            self.low8 = SpriteManager.getInstance().getSprite(self.fileName, (21,0))
            self.low9 = SpriteManager.getInstance().getSprite(self.fileName, (22,0))
            self.low10 = SpriteManager.getInstance().getSprite(self.fileName, (23,0))
            self.whiteL = SpriteManager.getInstance().getSprite(self.fileName, (24,0))

            ###other IVs
            self.drawPos = vec(16,0)
            self.pixelsToDraw = 0
            self.drawn = False
            self.reloading = False
            self.hurtTimer = 0
            self.flashTick = 0#Ticks every 0.2 seconds
            self.drawingHurt = False
            self.damageToDraw = 0
            self.fillerPixels = 0 #Background of red hp bar
            self.subtractingPixels = False
            self.drawingHeal = False

        
        def getLength(self):
            return 17 + (INV["max_hp"] * 5) + 2

        def getTotalPixels(self):
            return INV["max_hp"] * 5
        
        def getHeartImage(self, player):
            #print(self.getLength())
            if player.hp == INV["max_hp"]:
                return SpriteManager.getInstance().getSprite(self.fileName, (0,1))
            elif player.hp <= INV["max_hp"] / 4:
                return SpriteManager.getInstance().getSprite(self.fileName, (0,3))
            else:
                return SpriteManager.getInstance().getSprite(self.fileName, (0,2))
        
        def blit(self, drawSurface, color):
            drawSurface.blit(color, self.drawPos)
            self.drawPos[0] += 1


        def drawFull(self, drawSurface, player):
            ##Green##
            pixelsToDraw = INV["max_hp"] * 5
            drawSurface.blit(self.edgeG, self.drawPos)
            self.drawPos[0]+= 1
            for i in range(pixelsToDraw):
                drawSurface.blit(self.green, self.drawPos)
                self.drawPos[0] += 1
            drawSurface.blit(self.edgeG, self.drawPos)
            self.drawPos[0] += 1
            drawSurface.blit(self.edge, self.drawPos)
            self.drawPos = vec(16,0)


        ##  For hurt:
        ##  Draws in 2 stages: blinking and subtracting
        def drawRed(self, drawSurface, player, low = False):
            blackPix = (INV["max_hp"] * 5) - (player.hp * 5)
            pixelsToDraw = player.hp * 5
            if low == True:
                self.blit(drawSurface, self.edgeL)
            else:
                self.blit(drawSurface, self.red6)

            ##Regular red pixels
            if self.drawingHurt:
                for i in range(pixelsToDraw):
                    if low == True:
                        self.blit(drawSurface, self.low1)
                    else:
                        drawSurface.blit(self.red1, self.drawPos)
                        self.drawPos[0] += 1

                if self.subtractingPixels:
                    print("subtracting")
                    ##Subtracting
                    """
                    Each frame, the number of red1 to draw decreases by 1
                    and the number of red5 to draw increases.
                    """
                    for i in range(self.damageToDraw):
                        if low == True:
                            self.blit(drawSurface, self.low1)
                        else:
                            drawSurface.blit(self.red1, self.drawPos)
                            self.drawPos[0] += 1

                    for i in range(self.pixelsToDraw):
                        ##Filler
                        if low == True:
                            self.blit(drawSurface, self.low5)
                        else:
                            drawSurface.blit(self.red5, self.drawPos)
                            self.drawPos[0] += 1


                else:
                    print("Blinking")
                    ##Blinking
                    for i in range(self.damageToDraw-2):
                        if self.flashTick % 2 == 0:
                            if low == True:
                                self.blit(drawSurface, self.whiteL)
                            else:
                                drawSurface.blit(self.white, self.drawPos)
                                self.drawPos[0] += 1
                        else:
                            if low == True:
                                self.blit(drawSurface, self.low1)
                            else:
                                drawSurface.blit(self.red1, self.drawPos)
                                self.drawPos[0] += 1

                    ##2 pixels for shading
                    if self.flashTick % 2 == 0:
                        if low == True:
                            self.blit(drawSurface, self.whiteL)
                            self.blit(drawSurface, self.whiteL)
                        else:
                            drawSurface.blit(self.white, self.drawPos)
                            self.drawPos[0] += 1
                            drawSurface.blit(self.white, self.drawPos)
                            self.drawPos[0] += 1

                    else:
                        if low == True:
                            self.blit(drawSurface, self.low2)
                            self.blit(drawSurface, self.low3)

                        else:
                            drawSurface.blit(self.red2, self.drawPos)
                            self.drawPos[0] += 1
                            drawSurface.blit(self.red3, self.drawPos)
                            self.drawPos[0] += 1

                for i in range(self.fillerPixels):
                    if low == True:
                        self.blit(drawSurface, self.low5)
                    else:
                        drawSurface.blit(self.red5, self.drawPos)
                        self.drawPos[0] += 1
                
                if low == True:
                    self.blit(drawSurface, self.edgeL)
                else:
                    self.blit(drawSurface, self.red6)


            elif self.drawingHeal:
                ##Cant be healing and hurting
                pass

                        
            else:
                ##Regular draw routine
                ##Make it flash on low
                for i in range(pixelsToDraw-2):
                    if low == True:
                        self.blit(drawSurface,self.low1)
                    else:
                        drawSurface.blit(self.red1, self.drawPos)
                        self.drawPos[0] += 1
                
                ##2 pixels for shading
                if low == True:
                    self.blit(drawSurface, self.low2)
                    self.blit(drawSurface, self.low3)
                    #print(blackPix)
                    for i in range(blackPix):
                        print("A")
                        self.blit(drawSurface, self.low5)
                    
                    self.blit(drawSurface, self.edgeL)
                else:
                    drawSurface.blit(self.red2, self.drawPos)
                    self.drawPos[0] += 1
                    drawSurface.blit(self.red3, self.drawPos)
                    self.drawPos[0] += 1

                    for i in range(blackPix):
                        drawSurface.blit(self.red5, self.drawPos)
                        self.drawPos[0] += 1

                    drawSurface.blit(self.red6, self.drawPos)
                    self.drawPos[0] += 1

            drawSurface.blit(self.edge, self.drawPos)
            self.drawPos = vec(16,0)

        def drawHeart(self, drawSurface, player):
            drawSurface.blit(self.getHeartImage(player), self.position)

        def drawFirst(self, drawSurface, player):
            """
            self.pixelsToDraw starts at 0.
            Every frame, in update, self.pixelsToDraw increments.
            Eventually self.pixelsToDraw == (INV["max_hp"] * 5) + 1
            """
            if not pygame.mixer.get_busy():
                SoundManager.getInstance().playSFX("OOT_MagicRefill.wav")
            for i in range(self.pixelsToDraw):
                drawPos = vec(16,0)
                if i >= 0:
                    drawSurface.blit(self.edgeG, drawPos)
                    drawPos[0] += 1
                if i >= 1:
                    for j in range(i):
                        drawSurface.blit(self.green, drawPos)
                        drawPos[0] += 1
                if i >= (INV["max_hp"] * 5) - 1:
                    drawSurface.blit(self.edgeG, drawPos)
                    drawPos[0] += 1
                if i == INV["max_hp"] * 5:
                    drawSurface.blit(self.edge, drawPos)
                    self.drawn = True
                    self.pixelsToDraw = 0
                    player.keyUnlock()
                    SoundManager.getInstance().stopSFX("OOT_MagicRefill.wav")
        

        def drawHurt(self, hp, damage):
            """
            Turn damage * 5 pixels red
            Interrupt healing
            """
            self.drawingHeal = False
            self.drawingHurt = True
            self.hurtTimer = 0
            self.flashTick = 0
            self.damageToDraw += (damage * 5)
            self.fillerPixels = ((INV["max_hp"] - hp) * 5) - 5

        def drawHeal(self, amountHealed):
            return
            self.drawingHeal = True

        def draw(self, drawSurface, player):
            """
            Green at full, red at low.
            Draw 5 pixels of the healthbar per 1 hp
            """
            ##Full Health
            if player.hp == INV["max_hp"]:
                self.drawFull(drawSurface, player)
            
            elif player.hp == 1 or player.hp <= INV["max_hp"] / 4:
                self.drawRed(drawSurface, player, low = True)
            ##Regular Display
            else:
                self.drawRed(drawSurface, player)
                

        def reload(self):
            self.reloading = True
            self.pixelsToDraw = INV["max_hp"]
            self.drawPos = vec(18+self.pixelsToDraw, 0)


        def update(self, seconds):
            """
            Draws 1 pixel of the healthbar
            each frame on initialization.
            """
            if self.drawingHurt:
                if self.subtractingPixels:
                    self.damageToDraw -= 1
                    self.pixelsToDraw += 1
                    if self.damageToDraw == 0:
                        self.pixelsToDraw = 0
                        self.fillerPixels = 0
                        self.subtractingPixels = False
                        self.drawingHurt = False
                else:
                    self.hurtTimer += seconds
                    if self.hurtTimer >= 0.2:
                        self.flashTick += 1
                        #Iframes last 2 seconds or 10 flashTicks
                        if self.flashTick == 5:
                            self.subtractingPixels = True
                            #set up for first round of pixel subtraction
                            self.damageToDraw -= 1
                            self.pixelsToDraw += 1
                            self.flashTick = 0
                        self.hurtTimer = 0
                

            elif self.reloading:
                ##Reload the hp bar after getting an upgrade
                self.pixelsToDraw -= 1
            elif not self.drawn:
                ##Initialization of the healthbar
                self.pixelsToDraw += 1

        

        
        

        









        """ if player.hp == INV["max_hp"]:
            pixelsToDraw = INV["max_hp"] * 5
            for i in range(pixelsToDraw):
                ##
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,1))
            super().draw(drawSurface)
            return
        
        elif player.hp <= INV["max_hp"] / 4:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,3))
        else:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,2))
        
        super().draw(drawSurface)

        pixelCount = 93 // INV["max_hp"]
        pixelsToDraw = pixelCount * player.hp
        
        for i in range(pixelsToDraw-3):
            pixel = SpriteManager.getInstance().getSprite("pixels.png", (0,0))
            drawSurface.blit(pixel, (self.position[0]+17+i, self.position[1]+2))
        for i in range(3):
            pixel = SpriteManager.getInstance().getSprite("pixels.png", (i+1,0))
            drawSurface.blit(pixel, (self.position[0]+17+(pixelsToDraw-3)+i, self.position[1]+2))
 """
        
        """ if player.hp == INV["max_hp"]:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,1))

        elif player.hp <= INV["max_hp"]/5 or player.hp == 1:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,6))
        elif player.hp <= INV["max_hp"]/3.5:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,5))
            #Text((20,0), str(self.player.hp), (255,0,0)).draw(drawSurface)

        elif player.hp <= INV["max_hp"] / 2.5:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,4))

        elif player.hp <= INV["max_hp"]/1.5:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,3))
            #Text((20,0), str(self.player.hp), (225,228,0)).draw(drawSurface)    
        else:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,2)) """
            
        

class Highlight(Drawable):
    def __init__(self, position, flag = 0):
        """
        flags:
        0-> Regular 16x16, 1 -> quit, 2 -> Y/N prompt, 3 -> map
        """
        super().__init__(position, "Objects.png", (0,0))
        self.displayFlag = flag
        self.timer = 0

    def draw(self, drawSurface):
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
