from FSMs import ScreenManagerFSM
from gameObjects import PauseEngine, TextEngine
from rooms import *

from utils import SoundManager
from . import TextEntry, EventMenu

from utils import vec, RESOLUTION

from pygame.locals import *


class ScreenManager(object):
      
    def __init__(self):
        self.inIntro = False
        self.game = None # Add your game engine here!
        self.pauseEngine = PauseEngine()
        self.textEngine = TextEngine.getInstance()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        
        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size
        self.pausedText.position = vec(*midpoint)
        
        self.mainMenu = EventMenu("title_screen.png", fontName="zelda")
        self.mainMenu.addOption("start", "Press ENTER to start",
                                 RESOLUTION // 2 + vec(0,5),
                                 lambda x: x.type == KEYDOWN and x.key == K_RETURN,
                                 center="both")
        self.mainMenu.addOption("tutorial", "Press SPACE to start in Grand Chapel",
                                 RESOLUTION // 2 + vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_SPACE,
                                 center="both")
        """ self.mainMenu.addOption("exit", "Press ESC to quit",
                                 RESOLUTION // 2 + vec(0,75),
                                 lambda x: x.type == KEYDOWN and x.key == K_ESCAPE,
                                 center="both") """
    
    #Displaying Text
    def draw(self, drawSurf):
        """
        Drawing the game based on the state
        """
        if self.state.isInGame():
            self.game.draw(drawSurf)
            if self.game.textBox:
                    self.state.speak()
                    #self.textEngine = TextEngine.getInstance()
                    if "Y/N" in self.game.text:
                        self.textEngine.setText(self.game.text, self.game.icon, prompt = True)
                        
                    else:
                        self.textEngine.setText(self.game.text, self.game.icon, self.game.largeText)
                        
        if self.state == "textBox":
            if self.pauseEngine.paused:
                self.textEngine.draw(self.pauseEngine.boxPos, drawSurf)
            elif self.inIntro:
                self.textEngine.draw(self.intro.boxPos, drawSurf)
            else:
                self.textEngine.draw(self.game.boxPos, drawSurf)
            return
        
        if self.state == "paused":
            self.pauseEngine.draw(drawSurf)
            #self.pausedText.draw(drawSurf)
            
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
        
        elif self.state == "intro":
            self.intro.draw(drawSurf)
            if self.intro.textBox:
                self.state.speakI()
                #self.textEngine = TextEngine.getInstance()
                self.textEngine.setText(self.intro.text, self.intro.icon, self.intro.largeText)
            
    

    #Entering game, pausing
    def handleEvent(self, event):
        if self.state == "game":
            if not self.game.pause_lock:
                if event.type == pygame.WINDOWMOVED:
                    self.state.pause()
                    return

                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.game.player.stop()
                    SoundManager.getInstance().playSFX("OOT_PauseMenu_Open.wav")
                    Map.getInstance().updateHighlight()
                    self.state.pause()
                    return
                elif event.type == KEYDOWN and event.key == K_LSHIFT:
                    self.game.player.stop()
                    SoundManager.getInstance().playSFX("OOT_PauseMenu_Open.wav")
                    Map.getInstance().updateHighlight()
                    self.state.pause()
                    self.pauseEngine.mapOpen = True
                    return
                
                else:
                    self.game.handleEvent(event)

        elif self.state == "paused":
            if event.type == KEYDOWN and event.key == K_r:
                self.state.toMain()

            elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_LSHIFT):
                self.pauseEngine.paused = False
                SoundManager.getInstance().playSFX("OOT_PauseMenu_Close.wav")
                self.pauseEngine.mapOpen = False
                self.state.pause()

            else:
                self.pauseEngine.handleEvent(event)
                if self.pauseEngine.text != "":
                    
                    self.state.speakP()
                    #self.textEngine = TextEngine.getInstance()
                    if "Y/N" in self.pauseEngine.text:
                        self.textEngine.setText(self.pauseEngine.text, prompt = True)
                        
                    else:
                        self.textEngine.setText(self.pauseEngine.text)
                
        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)

            if choice == "start":
                if FLAGS[51]:
                    self.game = Grand_Chapel.getInstance()
                    self.game.initializeRoom()
                    self.state.startGame()

                elif FLAGS[50]:
                    self.game = Entrance.getInstance()
                    self.game.initializeRoom()
                    self.state.startGame()
                    
                else:
                    FLAGS[50] = True
                    self.intro = Intro_Cut.getInstance()
                    self.inIntro = True
                    self.state.toIntro()
            
            elif choice == "tutorial":
                """Testing and Freeplay"""
                self.game = Grand_Chapel.getInstance()
                self.game.initializeRoom()
                self.state.startGame()

            elif choice == "exit":
                return "exit"
            
        elif self.state == "textBox":
            if event.type == KEYDOWN and event.key == K_SPACE:
                if self.pauseEngine.paused:
                    self.pauseEngine.textBox = False
                    self.pauseEngine.text = ""
                    self.state.speakP()
                elif self.inIntro:
                    ##Skip the intro
                    self.intro.textBox = False
                    self.intro.text = ""
                    self.intro.icon = None
                    self.intro.fading = True
                    self.state.speakI()
                    self.intro.fading = True
                    self.intro.textInt = 9
                    
                    
                else:
                    self.game.textBox = False
                    self.game.text = ""
                    self.game.icon = None
                    self.state.speak()
                #self.textEngine = TextEngine.tearDown()
                self.textEngine.reset()
                return
                    ##Close the textBox

            self.textEngine.handleEvent(event)
            if self.textEngine.done:
                if self.pauseEngine.paused:
                    if "Y/N" in self.pauseEngine.text:
                        
                        self.pauseEngine.promptResult = self.textEngine.promptResult
                        if self.pauseEngine.promptResult:
                            if self.pauseEngine.promptFlag == "potion":
                                INV["potion"] -= 1
                                self.game.player.heal(3)
                            elif self.pauseEngine.promptFlag == "beer":
                                INV["beer"] -= 1
                                self.game.player.drink()
                            elif self.pauseEngine.promptFlag == "joint":
                                INV["joint"] -= 1
                                self.game.player.smoke()
                            elif self.pauseEngine.promptFlag == "speed":
                                INV["speed"] -= 1
                                self.game.player.smoke()

                            elif self.pauseEngine.promptFlag == "syringe":
                                if self.game.player.hp > INV["max_hp"]//4:
                                    self.game.player.hp //=4
                                    if self.game.player.hp < 1:
                                        self.game.player.hp = 1
                                
                        

                    self.pauseEngine.textBox = False
                    self.pauseEngine.text = ""
                    self.state.speakP()

                elif self.inIntro:
                    self.intro.textBox = False
                    self.intro.text = ""
                    self.intro.icon = None
                    if self.intro.textInt == 9:
                        self.intro.fading = True
                    self.state.speakI()
                else:
                    if "Y/N" in self.game.text:
                        self.game.promptResult = self.textEngine.promptResult
                    self.game.textBox = False
                    self.game.text = ""
                    self.game.icon = None
                    self.state.speak()
                #self.textEngine = TextEngine.tearDown()
                self.textEngine.reset()
        elif self.state == "intro":
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.intro.fading = True
                self.intro.textInt = 9

    #Only runs if in game
    def handleCollision(self):
        if self.state == "game":
            self.game.handleCollision()
    
    #Update all states
    def update(self, seconds): 
        if self.state == "game":
            self.game.update(seconds)
            if self.game.dead:
                self.state.die()
                self.game.deathReset()
                self.game = AbstractEngine.tearDown()
                self.game = None
            
            elif self.game.readyToTransition:
                pos = self.game.tra_pos
                player = self.game.player
                newGame = self.game.tra_room
                keepBGM = self.game.tra_keepBGM
                self.game.reset()
                self.game = AbstractEngine.tearDown()
                self.game = newGame
                self.game.initializeRoom(player, pos, keepBGM)
            """ elif self.game.introDone:
                self.game = Intro_1.getInstance()
                self.game.initializeRoom()
                #self.state.startGame() """

        elif self.state == "textBox":
            self.textEngine.update(seconds)
        elif self.state == "paused":
            self.pauseEngine.update(seconds)
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)

        elif self.state == "intro":
            self.intro.update(seconds)
            if self.intro.introDone:
                ##Transition to Entrance##
                self.inIntro = False
                self.game = Entrance.getInstance()
                self.game.initializeRoom()
                self.state.toGame()
                