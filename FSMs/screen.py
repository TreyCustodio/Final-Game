from . import AbstractGameFSM
from statemachine import State


class ScreenManagerFSM(AbstractGameFSM):
    mainMenu = State(initial=True)
    game     = State()
    paused   = State()
    textBox = State()
    
    speak =  game.to(textBox) | textBox.to(game)
    speakP = paused.to(textBox) | textBox.to(paused)
    pause = game.to(paused) | paused.to(game) | \
            mainMenu.to.itself(internal=True)
    toMain = game.to(mainMenu) | paused.to(mainMenu)
    startGame = mainMenu.to(game)
    quitGame  = game.to(mainMenu) | \
                paused.to.itself(internal=True)
    
    def isInGame(self):
        return self == "game" or self == "paused"
    
    def on_enter_game(self):
        pass
        #self.obj.game.link.updateMovement()
    