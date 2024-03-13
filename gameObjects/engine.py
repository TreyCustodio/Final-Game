import pygame

from . import (Drawable, Player, Enemy, NonPlayer, Chest, Key, Switch, 
               WeightedSwitch, LightSwitch, TimedSwitch, LockedSwitch, Block, IBlock, HBlock,
               PushableBlock, LockBlock, Bullet, Sword)

from utils import vec, RESOLUTION

class GameEngine(object):
    import pygame

    def __init__(self):
        """
        Initialize all of the room's objects
        """   
        ###Player
        self.link = Player((RESOLUTION[0]/2, RESOLUTION[1]/2))
        self.link.position = (self.link.position[0] - self.link.image.get_size()[0]/2,
                              112)
        
        ###Puzzle-related switches and blocks
        #Blocks
        self.block = LockBlock((144,80))#Locked block
        self.block1 = Block((144,64),(5,4))#Middle disappearing block
        self.block2 = Block((128,64),(5,4))#Left
        self.block3 = Block((160,64),(5,4))#Right
        self.blockP = PushableBlock((96, 144))#PushableBlock((96, 112))#Pushable Block

        #Switches
        self.weightedSwitch = WeightedSwitch((96,144))
        self.switch = Switch((192,144))
        self.lightSwitch = LightSwitch((144,144))
        self.timedSwitch = TimedSwitch((240,144))
        self.lockedSwitch = LockedSwitch((48,144))

        ###Spawnable Objects
        self.chest = Chest((64,96), "Objects.png", (0,1))
        self.key = Key((48,96), "Objects.png", (0,2))


        ###Enemies
        #self.stalfos = Enemy((RESOLUTION[0]-64, 16), "Stalfos.png")
        #self.stalfos2 = Enemy((48,16), "Stalfos.png")
        
        #List of switches
        self.switches = [self.switch, self.weightedSwitch, self.lightSwitch, self.timedSwitch, self.lockedSwitch]
        #Interactable objects, Enemies, and Npcs
        self.npcs = []
        for i in range(3, 17):
            self.npcs.append(Enemy((16*i,16), "Stalfos.png"))
        #Spawning/Despawning objects
        self.spawning = []
        #Projectiles
        self.projectiles = []

        #Screen, background, and HUD objects
        self.size = vec(*RESOLUTION)
        self.keyCount = Drawable((0, RESOLUTION[1]-16), "KeyCount.png")
        #self.healthBar
        #self.energyMeter
        self.background = Drawable((0,0), "test.png")



        #Blocks: Collision impedes the player's movement
        self.blocks = []
        ##  Wall collision  ##
        #Left side
        for i in range(19):
            self.blocks.append(IBlock((0,i*16)))
        #Right side
        for i in range(19):
            self.blocks.append(IBlock((RESOLUTION[0]-16,i*16)))
        #Top side
        for i in range(1,18):
            self.blocks.append(IBlock((i*16, 0)))
        #Bottom side
        for i in range(1,18):
            self.blocks.append(IBlock((i*16, RESOLUTION[1]-16)))

        #If you have visible blocks for walls, start from i = 1 to 18
        ##  Block Collision    ##
        for i in range(2,8):
            self.blocks.append(Block((i*16, 64)))
        
        self.blocks.append(self.block)
        self.blocks.append(self.block1)
        self.blocks.append(self.block2)
        self.blocks.append(self.block3)

        for i in range(11,17):
            self.blocks.append(Block((i*16, 64)))
        
        #Half-block collision for beauty
        #Left Wall
        for i in range(1,12):
            self.blocks.append(HBlock((16,i*16)))
        #Right Wall
        for i in range(1,12):
            self.blocks.append(HBlock((RESOLUTION[0]-32, i*16), True))
        
    



    def draw(self, drawSurface):
        """
        Draw the objects
        """
        
        
        #Background        
        self.background.draw(drawSurface)
        
        #Blocks
        for block in self.blocks:
            block.draw(drawSurface)

        #Puzzle rewards and drops
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
                if type(n) == Enemy:
                    n.draw(drawSurface)
                else:
                    n.draw(drawSurface)
        
        if self.projectiles:
            for p in self.projectiles:
                if type(p) == Sword:
                    p.draw(drawSurface, True)
                else:
                    p.draw(drawSurface)

        #Player
        self.link.draw(drawSurface, True)

        #HUD
        self.keyCount.draw(drawSurface)
        self.keyNumber = Drawable((33, self.keyCount.position[1]), "numbers.png", (self.link.keys,0))
        self.keyNumber.draw(drawSurface)
        

    
    



    
    
    def handleEvent(self, event):
        """
        Players, enemies, and npcs handle their events
        """
        #Player
        if (self.chest in self.spawning) and self.link.getCollisionRect().colliderect(self.chest.getInteractionRect()):#Turn into method
            self.link.handleEvent(event, self.chest)
        else:
            self.link.handleEvent(event)
        #Fire bullet
        if self.link.bullet != None:
            self.projectiles.append(self.link.getBullet())
            self.link.bullet = None
        #Swing sword
        if self.link.sword != None:
            self.projectiles.append(self.link.getSlash())
            self.link.sword = None
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
                self.blocks.pop(self.blocks.index(self.block1))
                self.blocks.pop(self.blocks.index(self.block2))
                self.blocks.pop(self.blocks.index(self.block3))
                self.link.keys -= 1
            else:
                self.link.handleCollision(self.blocks[blockIndex])



        for n in self.npcs:
            #Check if it collides with the player first
            if self.link.doesCollide(n):
                #Push blocks
                if type(n) == PushableBlock:
                    n.push(self.link)
                else:
                # Handle it within the player class (enemies)
                    self.link.handleCollision(n)
        
            if issubclass(type(n),Enemy):
                if self.projectiles:
                    for p in self.projectiles:
                        if n.doesCollide(p):
                            n.handleCollision(p)
                            if type(p) == Bullet:
                                self.projectiles.pop(self.projectiles.index(p))
                        
            
            #Block collision
            if type(n) == PushableBlock:
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
        Spawning/despawning objects
        """
        ##  Spawning and despawning a chest using the weighted switch   ##
        if self.chest not in self.spawning:
            if self.weightedSwitch.pressed:
                self.spawning.append(self.chest)
        elif not self.weightedSwitch.pressed and not self.chest.interacted: #and self.chest != opened
            self.spawning.pop(self.spawning.index(self.chest))
        
        ##  Spawning and despawning a key using the light switch    ##
        if self.key not in self.spawning:
            if self.lightSwitch.pressed and not(self.key.collected):
                self.spawning.append(self.key)
        
        elif not self.lightSwitch.pressed:
            self.spawning.pop(self.spawning.index(self.key))

        
        """
        Triggering Switches
        """
        ##  Triggering the locked switch with a timed switch  ##
        if self.timedSwitch.pressed:
            #unlock if not already unlocked
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
        
        ##  Make block appear   ##
        if self.switch.pressed:
            self.npcs.insert(0, self.blockP)
        
        """
        Detecting weapon damage
        """
        """ 
        Stalfos disappearing if switch pressed

        if self.stalfos in self.npcs and self.lockedSwitch.pressed:
            self.npcs.pop(self.npcs.index(self.stalfos))
        
        if self.stalfos not in self.npcs and not self.lockedSwitch.pressed:
            self.npcs.append(self.stalfos) """
        
        ###Projectiles
        if self.projectiles:
            for p in self.projectiles:
                if p.collides(self.blocks):
                    self.projectiles.pop(self.projectiles.index(p))

        
        
        
            



    def update(self, seconds):
        """
        Update the objects that need to be updated
        """
        #Update player first
        self.link.update(seconds)
        #Update npcs
        for n in self.npcs:
            if type(n) == Enemy:
                n.update(seconds)
                if n.hp <= 0:
                    self.npcs.pop(self.npcs.index(n))

        #Update puzzle objects
        self.timedSwitch.update(seconds)
        self.lockedSwitch.update()
        #self.block.update(self.link)
        self.blockP.update(seconds, self.link, self.link.row)
        self.weightedSwitch.update(self.blockP)
        self.lightSwitch.update(self.link, self.blockP)

        if self.projectiles:
            for p in self.projectiles:
                p.update(seconds)
                if type(p) == Sword and p.timer >= p.lifetime:
                    self.projectiles.pop(self.projectiles.index(p))
                    self.link.positionLock = False

        Drawable.updateOffset(self.link, self.size)
    

