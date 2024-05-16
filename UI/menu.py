from gameObjects import Drawable, Text, Pointer
from utils.vector import vec, magnitude
from utils import SoundManager
from . import TextEntry

import pygame

class AbstractMenu(Drawable):
    def __init__(self, background, fontName="default",
                 color=(255,255,255)):
        super().__init__((0,0), background)
        
        self.options = {}
        
        self.color = color      
        self.font = fontName
     
    def addOption(self, key, text, position, center=None):
        self.options[key] = TextEntry(position, text, self.font,
                                  self.color)
        optionSize = self.options[key].getSize()
        
        if center != None:
            if center == "both":
                offset = optionSize // 2
            elif center == "horizontal":
                offset = vec(optionSize[0] // 2, 0)
            elif center == "vertical":
                offset = vec(0, optionSize[1] // 2)
            else:
                offset = vec(0,0)
            
            self.options[key].position -= offset
 
    def draw(self, surface):
        super().draw(surface)
        
        for item in self.options.values():
           item.draw(surface)


class EventMenu(AbstractMenu):
    def __init__(self, background, fontName="default",
                color=(255,255,255)):
        super().__init__(background, fontName, color)
        self.pointer = Pointer(vec(16*6-8, 98))
        self.eventMap = {}
        self.pointerTick = 0
     
    def addOption(self, key, text, position, eventLambda=None,
                                              center=None):
        super().addOption(key, text, position, center)      
        if eventLambda:
            self.eventMap[key] = eventLambda
    
    def draw(self, drawSurf):
        super().draw(drawSurf)
        self.pointer.draw(drawSurf)

    def addEvent(self, key, eventLambda):
        """
        Adjust the options for starting the game
        if you're using a controller
        """
        self.eventMap[key] = eventLambda
        

    def editText(self, key, text):
        position = vec(self.options[key].position[0] + 18, self.options[key].position[1])
        self.options[key] = Text(position, text)

    def getChoice(self):
        return self.pointer.getChoice()
    
    def handleEvent(self, event):
        
        if self.pointer.choice == 0:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.pointer.increaseChoice()
                self.pointer.position[1] = self.options["continue"].position[1]
                SoundManager.getInstance().playSFX("FF_cursor.wav")
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.pointer.setChoice(2)
                self.pointer.position[0] += 16
                self.pointer.position[1] = self.options["quit"].position[1]
                SoundManager.getInstance().playSFX("FF_cursor.wav")

        elif self.pointer.choice == 1:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.pointer.decreaseChoice()
                self.pointer.position[1] = self.options["start"].position[1]
                SoundManager.getInstance().playSFX("FF_cursor.wav")

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.pointer.position[0] += 16
                self.pointer.increaseChoice()
                self.pointer.position[1] = self.options["quit"].position[1]
                SoundManager.getInstance().playSFX("FF_cursor.wav")

        elif self.pointer.choice == 2:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.pointer.decreaseChoice()
                self.pointer.position[0] -= 16
                self.pointer.position[1] = self.options["continue"].position[1]
                SoundManager.getInstance().playSFX("FF_cursor.wav")

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.pointer.setChoice(0)
                self.pointer.position[0] -= 16
                self.pointer.position[1] = self.options["start"].position[1]
                SoundManager.getInstance().playSFX("FF_cursor.wav")

    def update(self, seconds):
        super().update(seconds)
        if self.pointerTick < 10:
            self.pointer.position[0] += 1
            self.pointerTick += 1
        else:
            self.pointer.position[0] -= 1
            self.pointerTick += 1
            if self.pointerTick >= 20:
                self.pointerTick = 0

    
    
        
    
    
        
        

