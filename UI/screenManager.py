from FSMs import ScreenManagerFSM
from gameObjects import GameEngine, Drawable, PauseEngine
from . import TextEntry, EventMenu

from utils import vec, RESOLUTION


from pygame.locals import *


class ScreenManager(object):
      
    def __init__(self):
        self.game = GameEngine() # Add your game engine here!
        self.pauseEngine = PauseEngine()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        
        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size
        self.pausedText.position = vec(*midpoint)
        
        self.mainMenu = EventMenu("background.png", fontName="zelda")
        self.mainMenu.addOption("start", "Press ENTER to start",
                                 RESOLUTION // 2 - vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_RETURN,
                                 center="both")
        self.mainMenu.addOption("exit", "Press ESC to quit",
                                 RESOLUTION // 2 + vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_ESCAPE,
                                 center="both")
    
    
    def draw(self, drawSurf):
        """
        Drawing the game based on the state
        """
        if self.state.isInGame():
            self.game.draw(drawSurf)
        
            if self.state == "paused":
                self.pauseEngine.draw(drawSurf)
                #self.pausedText.draw(drawSurf)
            
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
    
    def handleEvent(self, event):
        if self.state in ["game", "paused"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
                
            elif self.state == "paused":
                if event.type == KEYDOWN and event.key == K_r:
                    self.state.mainMenu()
                #Pause engine handles the events if paused
                self.pauseEngine.handleEvent(event)
            else:
                self.game.handleEvent(event)

        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)
            
            if choice == "start":
                self.state.startGame()
            elif choice == "exit":
                return "exit"
     
    def handleCollision(self):
        if self.state != "paused":
            self.game.handleCollision()
    
    
    def update(self, seconds): 
        if self.state == "game":
            self.game.update(seconds)
        elif self.state == "paused":
            self.pauseEngine.update(seconds)
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
    