from FSMs import ScreenManagerFSM
from gameObjects import PauseEngine, TextEngine
from rooms import *

from utils import SoundManager
from . import TextEntry, EventMenu

from utils import vec, RESOLUTION

from pygame.locals import *


class ScreenManager(object):
      
    def __init__(self):
        self.game = None # Add your game engine here!
        self.pauseEngine = PauseEngine()
        self.textEngine = None
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        
        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size
        self.pausedText.position = vec(*midpoint)
        
        self.mainMenu = EventMenu("null.png", fontName="zelda")
        self.mainMenu.addOption("start", "Press ENTER to start",
                                 RESOLUTION // 2 - vec(0,25),
                                 lambda x: x.type == KEYDOWN and x.key == K_RETURN,
                                 center="both")
        self.mainMenu.addOption("tutorial", "Press SPACE for testing",
                                 RESOLUTION // 2 + vec(0,25),
                                 lambda x: x.type == KEYDOWN and x.key == K_SPACE,
                                 center="both")
        self.mainMenu.addOption("exit", "Press ESC to quit",
                                 RESOLUTION // 2 + vec(0,75),
                                 lambda x: x.type == KEYDOWN and x.key == K_ESCAPE,
                                 center="both")
    
    #Displaying Text
    def draw(self, drawSurf):
        """
        Drawing the game based on the state
        """
        if self.state.isInGame():
            self.game.draw(drawSurf)
            if self.game.textBox:
                    self.state.speak()
                    self.textEngine = TextEngine.getInstance()
                    self.textEngine.setText(self.game.text, self.game.icon)
        if self.state == "textBox":
            if self.pauseEngine.paused:
                self.textEngine.draw(self.pauseEngine.boxPos, drawSurf)
            else:
                self.textEngine.draw(self.game.boxPos, drawSurf)
            return
        
        if self.state == "paused":
            self.pauseEngine.draw(drawSurf)
            #self.pausedText.draw(drawSurf)
            
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
    
    #Entering game, pausing
    def handleEvent(self, event):
        if self.state == "game":
            if event.type == KEYDOWN and event.key == K_RETURN:
                SoundManager.getInstance().playSFX("OOT_PauseMenu_Open.wav")
                self.state.pause()
                return
            else:
                self.game.handleEvent(event)

        elif self.state == "paused":
            if event.type == KEYDOWN and event.key == K_r:
                self.state.toMain()

            elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_x):
                self.pauseEngine.paused = False
                SoundManager.getInstance().playSFX("OOT_PauseMenu_Close.wav")
                self.state.pause()

            else:
                self.pauseEngine.handleEvent(event)
                if self.pauseEngine.text != "":
                    self.state.speakP()
                    self.textEngine = TextEngine.getInstance()
                    self.textEngine.setText(self.pauseEngine.text)
                
        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)
            if choice == "start":
                return "exit"
            elif choice == "tutorial":
                #self.game = Intro_1.getInstance()
                self.game = Intro_3.getInstance()
                self.game.initializeRoom(keepBGM=True)
                self.state.startGame()
            elif choice == "exit":
                return "exit"
            
        elif self.state == "textBox":
            self.textEngine.handleEvent(event)
            if self.textEngine.done:
                if self.pauseEngine.paused:
                    self.pauseEngine.textBox = False
                    self.pauseEngine.text = ""
                    self.state.speakP()
                else:
                    self.game.textBox = False
                    self.game.text = ""
                    self.game.icon = None
                    self.state.speak()
                self.textEngine = TextEngine.tearDown()

    #Only runs if in game
    def handleCollision(self):
        if self.state == "game":
            self.game.handleCollision()
    
    #Update all states
    def update(self, seconds): 
        if self.state == "game":
            self.game.update(seconds)
            if self.game.readyToTransition:
                pos = self.game.tra_pos
                player = self.game.player
                newGame = self.game.tra_room
                keepBGM = self.game.tra_keepBGM
                self.game.reset()
                self.game = AbstractEngine.tearDown()
                self.game = newGame
                self.game.initializeRoom(player, pos, keepBGM)


        elif self.state == "textBox":
            self.textEngine.update(seconds)
        elif self.state == "paused":
            self.pauseEngine.update(seconds)
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)