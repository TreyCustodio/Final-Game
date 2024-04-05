import pygame

from . import Drawable,  Text

from utils import  vec, RESOLUTION, SpriteManager, SoundManager, INV, INFO, COORD, EQUIPPED

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

            self.large = False #Boolean determining if you display the large textbox or not

            self.charIndex = 0
            self.box_drawn = False
            self.ready_to_display = True
            self.ready_to_continue = False
            self.end = False
            self.done = False
            self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (0,0))
            self.displayTimer = 0.0

            self.lineNum = 1 #The line the text display is currently on

        def playSFX(self, name):
            SoundManager.getInstance().playSFX(name)


        def setText(self, text, icon = None, large = False):
            if large:
                self.large = large
                self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (0,0))

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
                self.drawEnd(position, drawSurface)
            elif not self.box_drawn:
                    self.drawBox(position, drawSurface)
                    if self.displayIcon != None:
                        self.drawIcon((position[0] + 106, position[1] - 32), drawSurface)
                    self.displayText(position, drawSurface)
        
            elif self.ready_to_continue:
                #drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,1)), position)
                self.drawContinue(position, drawSurface)

            elif self.displayTimer > 0 and self.displayTimer < 0.1:
                self.drawYellow1(position, drawSurface)
                #drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,3)), position)
                #self.displayText(position, drawSurface)
            else:
                self.drawYellow2(position, drawSurface)
                #drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,4)), position)
                #self.displayText(position, drawSurface)
        

        def drawIcon(self, position, drawSurface):
            box = SpriteManager.getInstance().getSprite("icon.png", (0,0))
            icon = SpriteManager.getInstance().getSprite("icon.png", self.displayIcon)
            drawSurface.blit(box, position)
            drawSurface.blit(icon, position)

        def drawBox(self, position, drawSurface):
            drawSurface.blit(self.textBox, position)
            self.box_drawn = True

        def drawContinue(self, position, drawSurface):
            if self.large:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,1)), position)
            else:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,1)), position)

        def drawYellow1(self, position, drawSurface):
            if self.large:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,3)), position)
            else:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,3)), position)
            self.displayText(position, drawSurface)
        
        def drawYellow2(self, position, drawSurface):
            if self.large:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,4)), position)
            else:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,4)), position)
            self.displayText(position, drawSurface)

        def drawEnd(self, position, drawSurface):
            if self.large:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,2)), position)
            else:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,2)), position)

        

        def displayText(self, position, drawSurface): 
            
                #drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,3)), position)
                #print(self.text)
                #print()
                #print(self.line)
                #print(self.text)
                #print(self.text[self.charIndex])
            if self.lineNum == 2:
                Text(((position[0] + 10) + (8 * self.charIndex), position[1]+34), self.line[self.charIndex]).draw(drawSurface)
            elif "&&" in self.line:
                Text(((position[0] + 10) + (8 * self.charIndex), position[1]+22), self.line[self.charIndex]).draw(drawSurface)
            else:
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
                    if self.large and self.lineNum == 1 and (not "&&" in self.line):
                        self.line = self.text[:self.text.index("\n")]
                        self.charIndex = 0
                        self.lineNum = 2
                    else:
                        self.ready_to_continue = True
                        self.line = self.text[:self.text.index("\n")]
                        self.playSFX("message-finish.wav")
                        self.charIndex = 0
                        if self.large:
                            self.lineNum = 1
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
        self.highlight = Drawable(COORD[3][4], "Objects.png", (0,0))
        self.highlighted = vec(0,0)
        

    def drawEquipped(self, drawSurf):
        #Arrow
        arrow = EQUIPPED["Arrow"]
        imageA = SpriteManager.getInstance().getSprite("item.png", (arrow, 1))
        drawSurf.blit(imageA, (COORD[14][5]))
        #Element
        element = EQUIPPED["C"]
        if element != None:
            imageE = SpriteManager.getInstance().getSprite("item.png", (element, 2))
            drawSurf.blit(imageE, (COORD[14][8]))


    def draw(self, drawSurf):
        if not self.paused:
            self.paused = True


        self.menu.draw(drawSurf)
        
        self.drawEquipped(drawSurf)
        if INV["plant"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (0,0))
            drawSurf.blit(image, (COORD[3][4]))
            Text((16*3+12, 16*4+4), str(INV["plant"]), small = True).draw(drawSurf)
        
        if INV["shoot"]:
            image = SpriteManager.getInstance().getSprite("item.png", (0,1))
            drawSurf.blit(image, (COORD[3][5]))
        
        if INV["fire"]:
            image = SpriteManager.getInstance().getSprite("item.png", (0,2))
            drawSurf.blit(image, (COORD[3][6]))
        
        if INV["cleats"]:
            image = SpriteManager.getInstance().getSprite("item.png", (1,2))
            drawSurf.blit(image, (COORD[5][6]))
        
        if INV["clap"]:
            image = SpriteManager.getInstance().getSprite("item.png", (2,2))
            drawSurf.blit(image, (COORD[7][6]))
        
        if INV["slash"]:
            image = SpriteManager.getInstance().getSprite("item.png", (3,2))
            drawSurf.blit(image, (COORD[9][6]))
        
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
        if event.type == KEYDOWN and event.key == K_c:
            if self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16*6:
                SoundManager.getInstance().playSFX("TextBox_Open.wav")
                EQUIPPED["C"] = 0
            elif self.highlight.position[0] == 16*5 and self.highlight.position[1] == 16*6:
                SoundManager.getInstance().playSFX("TextBox_Open.wav")
                EQUIPPED["C"] = 1
            elif self.highlight.position[0] == 16*7 and self.highlight.position[1] == 16*6:
                SoundManager.getInstance().playSFX("TextBox_Open.wav")
                EQUIPPED["C"] = 2
            elif self.highlight.position[0] == 16*9 and self.highlight.position[1] == 16*6:
                SoundManager.getInstance().playSFX("TextBox_Open.wav")
                EQUIPPED["C"] = 3
            else:
                SoundManager.getInstance().playSFX("bump.mp3")

        if event.type == KEYDOWN and event.key == K_z:
            ##Selecting an item and pulling up textbox
            ##Will have to switch the order of conditionals. Check position first so that the program
            ##Doesn't check every inventory slot

            if self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16*4:
                if INV["plant"] >= 1:
                    self.text = INFO["plant"]
                    return
            
            
            elif self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16*5:
                if INV["shoot"]:
                    self.text = INFO["shoot"]
                    return
                
            
            elif self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16*6:
                if INV["fire"]:
                    self.text = INFO["fire"]
                    return
            
            elif self.highlight.position[0] == 16*5 and self.highlight.position[1] == 16*6:
                if INV["cleats"]:
                    self.text = INFO["cleats"]
                    return
                
            
            elif self.highlight.position[0] == 16*7 and self.highlight.position[1] == 16*6:
                if INV["clap"]:
                    self.text = INFO["clap"]
                    return
            
            elif self.highlight.position[0] == 16*9 and self.highlight.position[1] == 16*6:
                if INV["slash"]:  
                    self.text = INFO["slash"]
                    return
            else:
                SoundManager.getInstance().playSFX("bump.mp3")
                
        if event.type == KEYDOWN and event.key == K_UP:
            if self.highlighted[1] != 0:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[1] -= 1
                self.highlight.position[1] -= 16

        elif event.type == KEYDOWN and event.key == K_DOWN:
            if self.highlighted[1] != 4:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[1] += 1
                self.highlight.position[1] += 16

        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if self.highlighted[0] != 7:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[0] += 1
                self.highlight.position[0] += 16

        elif event.type == KEYDOWN and event.key == K_LEFT:
            if self.highlighted[0] != 0:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[0] -= 1
                self.highlight.position[0] -= 16

    def update(self, seconds):
        self.timer += seconds
        if self.timer >= .5:
            self.timer = 0
        