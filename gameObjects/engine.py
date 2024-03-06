import pygame

from . import (Drawable, Player, Enemy, NonPlayer, Key, Switch, 
               WeightedSwitch, LightSwitch, TimedSwitch, LockedSwitch, Block, 
               PushableBlock, LockBlock,Bullet)

from utils import vec, RESOLUTION

class GameEngine(object):
    import pygame

    def __init__(self):
        """
        Initialize all of the room's objects
        """   
        #Player
        self.link = Player((RESOLUTION[0]/2, RESOLUTION[1]/2))
        self.link.position = (self.link.position[0] - self.link.image.get_size()[0]/2,
                              112)
        
        
        
        #Puzzle Objects
        self.block = LockBlock((16*9,80))#Locked block

        self.blockP = PushableBlock((96, 112))

        
        self.weightedSwitch = WeightedSwitch((96,144))
        self.switch = Switch((192,144))
        self.lightSwitch = LightSwitch((144,144))
        self.timedSwitch = TimedSwitch((240,144))
        self.lockedSwitch = LockedSwitch((48,144))

        self.chest = NonPlayer((64,32), "Objects.png", (0,1))
        self.key = Key((50,96), "Objects.png", (0,2))
        #Enemies
        self.stalfos = Enemy((RESOLUTION[0]-64, 16), "Stalfos.png")
        
        #Switches array
        self.switches = [self.switch, self.weightedSwitch, self.lightSwitch, self.timedSwitch, self.lockedSwitch]
        #Blocks, enemies, and npcs
        self.npcs = [self.stalfos]
        #Spawning/Despawning objects
        self.spawning = []

        self.projectiles = []
        #Screen and background
        self.size = vec(*RESOLUTION)
        self.keyCount = Drawable((0, RESOLUTION[1]-16), "KeyCount.png")
        
        self.background = Drawable((0,0), "test.png")

        self.blocks = []
        for i in range(9):
            self.blocks.append(Block((i*16, 64)))
        self.blocks.append(self.block)
        for i in range(10,19):
            self.blocks.append(Block((i*16, 64)))
    





    def draw(self, drawSurface):
        """
        Draw the objects
        """
        #Draw some blocks
        
        
        #Background        
        self.background.draw(drawSurface)
        self.keyCount.draw(drawSurface)
        self.keyNumber = Drawable((33, self.keyCount.position[1]), "numbers.png", (self.link.keys,0))
        self.keyNumber.draw(drawSurface)

        for block in self.blocks:
            block.draw(drawSurface)

        #Puzzle rewards
        if self.spawning:
            for n in self.spawning:
                n.draw(drawSurface)
        
        #Switches
        for n in self.switches:
            n.draw(drawSurface)
        #Npcs
        if self.npcs:
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
        ##  Interactable objects    ##
        if self.spawning:
            for n in self.spawning:
                if self.link.doesCollide(n):
                    if n == self.key:
                        self.spawning.pop(self.spawning.index(self.key))
                        self.key.collect()
                        self.link.keys += 1
                    else:
                        self.link.handleCollision(n)
        for n in self.switches:
            if self.link.doesCollide(n):
                if n.pressed == False and type(n) != WeightedSwitch:
                    n.press()

        ##  Npc Collision   ##
        blockIndex = self.link.doesCollideList(self.blocks)
        if blockIndex != -1:
            if type(self.blocks[blockIndex]) == LockBlock and self.link.keys > 0:
                self.blocks.pop(blockIndex)
                self.link.keys -= 1
            else:
                self.link.handleCollision(self.blocks[blockIndex])

        for n in self.npcs:
            #Check if it collides with the player first
            if self.link.doesCollide(n):

                #Push blocks
                if type(n) == PushableBlock:
                    n.push()
                else:
                # Handle it within the player class (enemies)
                    self.link.handleCollision(n)
            
            #Block collision
            elif type(n) == PushableBlock:
                #Press a switch if the block is on it
                switchIndex = n.doesCollideList(self.switches)
                if switchIndex != -1:
                    if type(self.switches[switchIndex]) == WeightedSwitch:
                        self.switches[switchIndex].press(n)
                    else:
                        self.switches[switchIndex].press()
                #elif *Other possible conditions for block collision could go here. (Walls)
                else:
                    pass
        """
        Template for spawnable/despawning objects
        """
        ##  Spawning and despawning a chest ##
        if self.chest not in self.spawning:
            if self.weightedSwitch.pressed:
                self.spawning.append(self.chest)
        
        elif not self.weightedSwitch.pressed: #and self.chest != opened
            self.spawning.pop(self.spawning.index(self.chest))
        
        if self.key not in self.spawning:
            if self.lightSwitch.pressed and not(self.key.collected):
                self.spawning.append(self.key)
        
        elif not self.lightSwitch.pressed:
            self.spawning.pop(self.spawning.index(self.key))

        
        """
        Templates for triggering locked switches. Pick one.
        """
        ##  Triggering a locked switch with a timed switch  ##
        if self.timedSwitch.pressed:
            #Unlock triggered, so unlock if not already unlocked
            if self.lockedSwitch.locked:
                print("a")
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
        
        ##  Make block appear   ##
        if self.switch.pressed:
            self.npcs.insert(0, self.blockP)
        
        if self.stalfos in self.npcs and self.lockedSwitch.pressed:
            self.npcs.pop(self.npcs.index(self.stalfos))
        
        if self.stalfos not in self.npcs and not self.lockedSwitch.pressed:
            self.npcs.append(self.stalfos)
        
        
        
            



    def update(self, seconds):
        """
        Update the objects that need to be updated
        """
        #Update player first
        self.link.update(seconds)
        #Update npcs
        self.stalfos.update(seconds)
        #Update puzzle objects
        self.timedSwitch.update(seconds)
        self.lockedSwitch.update()
        #self.block.update(self.link)
        self.blockP.update(seconds, self.link, self.link.row)
        self.weightedSwitch.update(self.blockP)
        self.lightSwitch.update(self.link, self.blockP)


        Drawable.updateOffset(self.link, self.size)
    

