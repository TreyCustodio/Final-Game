import pygame

from . import Drawable, Player, Enemy, NonPlayer, Switch, Block

from utils import vec, RESOLUTION

class GameEngine(object):
    import pygame

    def __init__(self):   
        #Player
        self.link = Player((RESOLUTION[0]/2, RESOLUTION[1]/2), "Link.png", 2)
        self.link.position = (self.link.position[0] - self.link.image.get_size()[0]/2,
                              self.link.position[1] - self.link.image.get_size()[1]/2)
        #Puzzle Objects
        self.block = Block((100,100))
        self.switch = Switch((100,150))
        self.weightedSwitch = Switch((50,150), True)
        self.chest = NonPlayer((50,50), "Objects.png", (0,1))
        #Enemies
        self.stalfos = Enemy((RESOLUTION[0]/2, (RESOLUTION[1]/2)-50), "Stalfos.png", 0)
        
        self.npcs = [self.switch, self.weightedSwitch, self.block, self.stalfos]

        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "test.png")
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        if self.weightedSwitch.pressed:
            self.chest.draw(drawSurface)
        for n in self.npcs:
            if n == self.stalfos:
                n.draw(drawSurface, True)
            else:
                n.draw(drawSurface)
        self.link.draw(drawSurface)

    def handleEvent(self, event):
        self.link.handleEvent(event)
    
    def handleCollision(self):
        # Maybe don't check every npc once we get bigger
        for n in self.npcs:
            if self.link.doesCollide(n):
                if type(n) == Switch:
                    if (n.pressed == False and n.weighted == False):
                        n.press()
                elif type(n) == Block:
                    n.push()
                else:
                # Handle it based on its type (enemy vs char)
                    self.link.handleCollision(n)
            elif type(n) == Switch and n.weighted == True:
                if n.doesCollide(self.block):
                    n.press(self.block)
                    self.npcs.append(self.chest)
            

    def update(self, seconds):
        self.link.update(seconds)
        self.block.update(seconds, self.link, self.link.direction)
        if self.chest in self.npcs:
            self.weightedSwitch.update(self.block)
            if self.weightedSwitch.pressed == False:
                self.npcs.pop(self.npcs.index(self.chest))
                pass
        Drawable.updateOffset(self.link, self.size)
    

