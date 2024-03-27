import pygame

from . import Drawable,  Text

from utils import  vec, RESOLUTION, SpriteManager, SoundManager, INV, INFO, COORD

from pygame.locals import *

class TextEngine(object):
    
    _INSTANCE = None
    
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._TE()
      
        return cls._INSTANCE

    @classmethod
    def tearDown(cls):
        if cls._INSTANCE != None:
            cls._INSTANCE = None
        return None

    class _TE(object):
        def __init__(self):
            self.text = ""
            self.line = ""
            self.displayIcon = None

            self.charIndex = 0
            self.box_drawn = False
            self.ready_to_display = True
            self.ready_to_continue = False
            self.end = False
            self.done = False
            self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (0,0))
            self.displayTimer = 0.0

        def playSFX(self, name):
            SoundManager.getInstance().playSFX(name)


        def setText(self, text, icon = None):
            if icon != None and self.displayIcon == None:
                self.displayIcon = icon

            self.text = text
            if len(self.text) <= 8:
                #self.playSFX("TextBox_Short.wav")
                pass
            else:
                self.playSFX("TextBox_Open.wav")
            if "\n" in self.text:
                self.line = self.text[self.charIndex:self.text.index("\n")]
            else:
                #1 line
                self.line = self.text
        
        def draw(self,position,drawSurface):
            if self.end:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,2)), position)
            elif not self.box_drawn:
                    self.drawBox(position, drawSurface)
                    if self.displayIcon != None:
                        self.drawIcon((position[0] + 106, position[1] - 32), drawSurface)
                    self.displayText(position, drawSurface)
        
            elif self.ready_to_continue:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,1)), position)
            
            elif self.displayTimer > 0 and self.displayTimer < 0.1:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,3)), position)
                self.displayText(position, drawSurface)
            else:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,4)), position)
                self.displayText(position, drawSurface)
        

        def drawIcon(self, position, drawSurface):
            box = SpriteManager.getInstance().getSprite("icon.png", (0,0))
            icon = SpriteManager.getInstance().getSprite("icon.png", self.displayIcon)
            drawSurface.blit(box, position)
            drawSurface.blit(icon, position)

        def drawBox(self, position, drawSurface):
            drawSurface.blit(self.textBox, position)
            self.box_drawn = True


        def displayText(self, position, drawSurface): 
            
                #drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,3)), position)
                #print(self.text)
                #print()
                #print(self.line)
                #print(self.text)
                #print(self.text[self.charIndex])
            Text(((position[0] + 10) + (8 * self.charIndex), position[1]+7), self.line[self.charIndex]).draw(drawSurface)
            self.charIndex += 1
            self.playSFX("message.wav")
        
            if self.charIndex == len(self.line):
                SoundManager.getInstance().stopAllSFX()
                self.text = self.text[self.charIndex+1:]
                if self.text == "":
                    #SoundManager.getInstance().stopAllSFX()
                    self.end = True
                    self.ready_to_continue = True
                    self.playSFX("OOT_Dialogue_Done.wav")
                    self.charIndex = 0
                elif "\n" in self.text:
                    self.ready_to_continue = True
                    self.line = self.text[:self.text.index("\n")]
                    self.playSFX("message-finish.wav")
                    self.charIndex = 0
                else:
                    self.ready_to_continue = True
                    self.line = self.text
                    self.charIndex = 0
                    self.playSFX("message-finish.wav")
            
                        
                
                
                

        def handleEvent(self, event):
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_z) and self.ready_to_continue:
                if self.end == True:
                    self.playSFX("WW_Textbox_Close.wav")
                    self.done = True
                else:
                    self.playSFX("OOT_Dialogue_Next.wav")
                    self.box_drawn = False
                    self.ready_to_continue = False

        def update(self, seconds):
            self.displayTimer += seconds
            if self.displayTimer >= 0.2:
                self.ready_to_display = True
                self.displayTimer = 0




class PauseEngine(object):


    def __init__(self):
        """
        Initialize item icons.
        Screen is 304 x 200
        [               ]  
        

        [               ]
        128 x 96 space
        16 x 16 squares
        beggining at (3,1)

        if self.link.hasItem:
        items.append(item)
        for i in items:
            i.draw
        
        """
        self.paused = False
        self.textBox = False
        self.text = ""
        self.icon = None
        self.boxPos = vec(30,64)

        self.menu = Drawable((0,0), "Pause.png")
        self.timer = 0
        self.highlight = Drawable((48,16), "Objects.png", (0,0))
        self.highlighted = vec(0,0)
        
    def draw(self, drawSurf):
        if not self.paused:
            self.paused = True

        self.menu.draw(drawSurf)
        if INV["plant"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (0,0))
            drawSurf.blit(image, (COORD[3][1]))
            Text((16*3+12, 16+4), str(INV["plant"]), small = True).draw(drawSurf)
            
        
        if self.timer >= .3:
            self.highlight.draw(drawSurf)
        else:
            self.highlight.draw(drawSurf, True)

    def handleEvent(self, event):
        """
           0    1    2   3   4   5   6   7
        0
        1
        2
        3
        4
        5

        min offset[0] = 0
        max offset[0] = 7
        min offset[1] = 0
        max offset[1] = 5
        """
        if event.type == KEYDOWN and event.key == K_z:
            if INV["plant"] >= 1:
                if self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16:
                    self.text = INFO["plant"]
                    return
        if event.type == KEYDOWN and event.key == K_UP:
            if self.highlighted[1] != 0:
                self.highlighted[1] -= 1
                self.highlight.position[1] -= 16
        elif event.type == KEYDOWN and event.key == K_DOWN:
            if self.highlighted[1] != 5:
                self.highlighted[1] += 1
                self.highlight.position[1] += 16
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if self.highlighted[0] != 7:
                self.highlighted[0] += 1
                self.highlight.position[0] += 16
        elif event.type == KEYDOWN and event.key == K_LEFT:
            if self.highlighted[0] != 0:
                self.highlighted[0] -= 1
                self.highlight.position[0] -= 16

    def update(self, seconds):
        self.timer += seconds
        if self.timer >= .5:
            self.timer = 0
        