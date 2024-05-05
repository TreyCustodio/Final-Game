from utils import SpriteManager, SCALE, RESOLUTION, EQUIPPED, INV, vec, rectAdd

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



class DamageNum(Text):
    """
    Expects the damage an enemy receives as a paramater
    and displays the damage dealt.
    """
    def __init__(self, position, num = 0):
        super().__init__(position, str(num), color = (255, 0, 0))    


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
        self.row = 0
        self.indicatorTimer = 0
        self.currentHp = 0
        self.currentMaxHp = 0
        self.pixel = pygame.Surface((1,1), pygame.SRCALPHA)
        
    
    def draw(self, drawSurface):
        #24*8 rectangle to fill with black from right to left
        #on 1/4 hp fill the pixel with dark red
        super().draw(drawSurface)
        pixelCount = 24
        #pixel


    def setImage(self, value, hp = 0, maxHp = 0):
        """
        Change the frame based on the enemy's hp
        """
        self.currentHp = hp
        self.currentMaxHp = maxHp
        self.indicatorTimer = 0
        if value != self.row:
            self.row = value
        
        self.image = SpriteManager.getInstance().getSprite("indicator.png", (0, value))
        if hp <= 0:
            self.row = 0
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (0, 0))
            self.indicatorTimer = 0

        """ elif hp == maxHp:
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (0, value))

        elif hp <= maxHp/4:
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (4, value))
        
        elif hp <= maxHp/2:
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (3, value))
        
        elif hp <= maxHp/1.333:
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (2, value))
        
        else:
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (1, value))
            self.indicatorTimer = 0 """
    
    def update(self, seconds):
        if self.row > 0:
            self.indicatorTimer += seconds
            if self.indicatorTimer >= 3:
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


class HealthBar(Drawable):
    """
    Displays the player's health on the HUD
    """
    def __init__(self):
        super().__init__(vec(0,0), "bar.png", (0,0))
    
    #93 pixels to fill
    #3 pixels at the end
    #93 // maxHP = # of pixels each point of health is worth

    def draw(self, drawSurface, player):
        if player.hp == INV["max_hp"]:
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
