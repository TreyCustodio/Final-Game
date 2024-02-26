import pygame

from . import Drawable, Player, Enemy, NonPlayer, Switch, WeightedSwitch, LightSwitch, TimedSwitch, LockedSwitch, Block

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
        self.weightedSwitch = WeightedSwitch((50,150))
        self.lightSwitch = LightSwitch((150,150))
        self.timedSwitch = TimedSwitch((200,150))
        self.lockedSwitch = LockedSwitch((250,150))
        self.chest = NonPlayer((50,50), "Objects.png", (0,1))
        #Enemies
        self.stalfos = Enemy((RESOLUTION[0]/2, (RESOLUTION[1]/2)-50), "Stalfos.png")
        
        #Switches/puzzle object array
        self.switches = [self.switch, self.weightedSwitch, self.lightSwitch, self.timedSwitch, self.lockedSwitch]
        #Blocks, enemies, and npcs
        self.npcs = [self.block, self.stalfos]
        self.chests = []

        #Screen and background
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "test.png")
    

    def draw(self, drawSurface):
        """
        Draw the objects
        """
        #Background        
        self.background.draw(drawSurface)

        #Puzzle rewards
        """ if self.weightedSwitch.pressed:
            self.chests.append(self.chest) """
        """ elif self.chest in self.npcs:
            self.npcs.pop(self.npcs.index(self.chest)) """
        #Switches
        for n in self.switches:
            n.draw(drawSurface)
        #Npcs
        for n in self.npcs:
            #Consider making enemies appear right before the player
            if n == self.stalfos:
                n.draw(drawSurface)
            else:
                n.draw(drawSurface)
        
        #Player last
        self.link.draw(drawSurface)

    def handleEvent(self, event):
        """
        Players, enemies, and npcs handle their events
        """
        #Player
        self.link.handleEvent(event)
        #Enemy

        #Npcs
    
    def handleCollision(self):
        """
        Handles collision between the player and objects,
        including puzzle objects like switches and blocks.
        """
        
        for n in self.switches:
            if self.link.doesCollide(n):
                if n.pressed == False and type(n) != WeightedSwitch:
                    n.press()
        #Handle each npc's collision
        for n in self.npcs:

            #Check if it collides with the player first
            if self.link.doesCollide(n):

                #Push blocks
                if type(n) == Block:
                    n.push()
                else:
                # Handle it within the player class (enemies)
                    self.link.handleCollision(n)
            
            #Block collision
            elif type(n) == Block:
                #Press a switch if the block is on it
                switchIndex = n.doesCollideList(self.switches)
                if switchIndex != -1:
                    self.switches[switchIndex].press()
                #elif *Other possible conditions for block collision could go here. (Walls)
                else:
                    pass
        """
        Template for spawnable/despawning objects
        """
        ##  Spawning and despawning a chest ##
        if not self.weightedSwitch.pressed:
            if self.chest in self.npcs: #and self.chest != opened
                self.npcs.pop(self.npcs.index(self.chest))
        elif self.chest not in self.npcs:
            self.npcs.append(self.chest)
        
        """
        Templates for triggering locked switches. Pick one.
        """
        ##  Triggering a locked switch with a timed switch  ##
        if self.timedSwitch.pressed:
            #Unlock triggered, so unlock if not already unlocked
            if self.lockedSwitch.locked:
                self.lockedSwitch.unLock()
        elif self.lockedSwitch.pressed:
                #lock it back if its still pressed after the timed switch resets
                self.lockedSwitch.lock()
        
        ##  Triggering a locked switch with a light switch  ##
        """ if self.lightSwitch.pressed:
            if self.lockedSwitch.locked:
                self.lockedSwitch.unLock()
        elif self.lockedSwitch.pressed:
            self.lockedSwitch.lock() """
        
        
        
            

    def update(self, seconds):
        #Update player first
        self.link.update(seconds)
        #Update npcs
        self.stalfos.update(seconds)
        #Update puzzle objects
        self.timedSwitch.update(seconds)
        self.lockedSwitch.update()
        self.block.update(seconds, self.link, self.link.direction)
        self.weightedSwitch.update(self.block)
        self.lightSwitch.update(self.link, self.block)


        Drawable.updateOffset(self.link, self.size)
    

