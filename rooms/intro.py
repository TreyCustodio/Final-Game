from gameObjects import *

class Intro_1(AbstractEngine):
    """
    Initialization
    """
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Intro_1()
      
        return cls._INSTANCE

    class _Intro_1(AE):
        def __init__(self):

            """
            Initial conditions
            """
            super().__init__()
            self.player = Player((16*9, (16*11) - 8))
            #Music
            self.bgm = "Nujabes_Decade.mp3"
            #Puzzle conditions
            self.enemyPlacement = 0
            self.max_enemies = 4
            
            """
            Puzzle objects
            """
            #Blocks
            self.block = LockBlock((144,80))#Locked block
            self.block1 = Block((144,64),(5,4))#Middle disappearing block
            self.block2 = Block((128,64),(5,4))#Left
            self.block3 = Block((160,64),(5,4))#Right
            
            self.blockP = PushableBlock((16*6,16*8))#PushableBlock((96, 112))#Pushable Block
            
            self.rblock1 = Block((16*3, 16*5), (5,2))
            self.rblock2 = Block((16*5, 16*5), (5,2))
            self.rblock3 = Block((16*4, 16*6), (5,2))
            self.rblock4 = Block((16*11, 16*5), (5,2))
            self.rblock5 = Block((16*12, 16*6), (5,2))
            self.rblock6 = Block((16*14, 16*5), (5,2))
            self.rblock7 = Block((16*13, 16*6), (5,2))

            self.gblock1 = Block((16*8, 16*5), (5,3))
            self.gblock2 = Block((16*8, 16*6), (5,3))
            self.gblock3 = Block((16*9, 16*6), (5,3))
            self.gblock4 = Block((16*10, 16*6), (5,3))
            self.gblock5 = Block((16*10, 16*5), (5,3))
            
            self.yblock1 = Block((144,16*1), (5,5))
            self.yblock2 = Block((144-16,16*1), (5,5))
            self.yblock3 = Block((144+16,16*1), (5,5))

            self.trigger1 = Trigger((16*9, (16*12)+8), SPEECH["intro_entrance"])
            
            self.trigger2 = Trigger(COORD[9][0], SPEECH["intro_entrance"])
            self.trigger2.position[1] -= 6
            
            #add self.yblock1-3 back
            self.blocks = [self.trigger1,  self.trigger2, 
                           #self.block, self.block1, self.block2, self.block3,
                            #self.yblock1, self.yblock2, self.yblock3,
                           self.rblock1, self.rblock2, self.rblock3, self.rblock4,
                        self.rblock5, self.rblock6, self.rblock7]

            #Switches
            self.weightedSwitch = WeightedSwitch((16*4,16*10))
            self.lockedSwitch = LockedSwitch((16*3,16*7))
            self.lightSwitch = LightSwitch((144,16*8))
            self.timedSwitch = TimedSwitch((16*14,16*10))
            self.switch = Switch((16*15,16*7))
            self.switches = [self.switch, self.weightedSwitch, self.lightSwitch, self.timedSwitch, self.lockedSwitch]
            
            #Npcs
            self.npcs = []
            for i in range(4, 6):
                self.npcs.append(Enemy((16*i,16), "Stalfos.png"))
            for i in range(14, 16):
                self.npcs.append(Enemy((16*i,16), "Stalfos.png"))

            #Spawnable Objects
            self.chest = Chest(COORD[2][5], SPEECH["intro_chest"], ICON["plant"])
            #self.sign = Sign((COORD[8][2]), SPEECH["intro_sign"])
            self.key = Key((COORD[4][5]))
            
            self.geemer = Geemer(((16*12)+5,(16*5)-2), SPEECH["intro_geemer"], 0, 2)
            self.geemer2 = Geemer(((16*6)+8, (16*5)-2), SPEECH["intro_switches"], 1)
            self.geemer2.frame = 2
            self.geemer2.framesPerSecond = 8
            self.geemer3 = Geemer((self.lightSwitch.position[0]-2, self.lightSwitch.position[1]-2), SPEECH["intro_plantgeemer"], 2)
            self.geemer3.framesPerSecond = 6
            self.geemer4 = Geemer((COORD[2][8]), SPEECH["intro_pushableblocks"])
            self.spawning = [#self.sign, 
                            self.geemer, self.geemer2, self.geemer3, self.geemer4]
            
            #Projectiles/weapons
            

            """
            Display elements
            """
            #Background/room
            #self.background = Drawable((0,0), "test.png")
            self.background = Level("test.png")

            


        """
        Auxilary
        """
        #override
        def createBlocks(self):
            for i in range(2,8):
                self.blocks.append(Block((i*16, 64)))

            for i in range(11,17):
                self.blocks.append(Block((i*16, 64)))   

        """
        Draw
        """
        def draw(self, drawSurface):
            super().draw(drawSurface)
        
        """
        Collision
        """
        #override
        def blockCollision(self):
            for b in self.blocks:
                for p in self.projectiles:
                    if p.doesCollide(b):
                        self.playSound("OOT_DekuSeed_Hit.wav")
                        self.disappear(p)
                        self.player.shooting = False
                if self.player.doesCollide(b):
                    if type(b) == LockBlock and self.player.keys > 0:
                        self.playSound("LA_Dungeon_Teleport_Appear.wav")
                        self.disappear(b)
                        self.disappear(self.blocks)
                        self.disappear(self.block1)
                        self.disappear(self.block2)
                        self.disappear(self.block3)
                        self.player.keys -= 1
                    elif type(b) == Trigger:
                        if b == self.trigger1:
                            self.player.handleCollision(b)
                            b.interact(self.player, self)
                        elif b == self.trigger2:
                            self.transport(Intro_2, (16*9, (16*11) - 8), keepBGM=True)
                    else:
                        self.player.handleCollision(b)

        def handleCollision(self):
            """
            Handles collision between the player and objects,
            including puzzle objects like switches and blocks.
            """
            super().handleCollision()


            self.spawnOnPress(self.key, self.timedSwitch)
            self.spawnOnPress(self.blockP, self.switch)

            self.spawnOnPress(self.chest, self.weightedSwitch)
            self.despawnOnPress(self.rblock1, self.lightSwitch)
            self.despawnOnPress(self.yblock1, self.lockedSwitch)

            if self.yblock1 not in self.blocks:
                self.disappear(self.yblock2)
                self.disappear(self.yblock3)
            if self.rblock1 not in self.blocks:
                self.disappear(self.rblock2)
                self.disappear(self.rblock3)
                self.disappear(self.rblock4)
                self.disappear(self.rblock5)
                self.disappear(self.rblock6)
                self.disappear(self.rblock7)
            elif self.rblock2 not in self.blocks:
                self.blocks.append(self.rblock2)
                self.blocks.append(self.rblock3)
                self.blocks.append(self.rblock4)
                self.blocks.append(self.rblock5)
                self.blocks.append(self.rblock6)
                self.blocks.append(self.rblock7)
            
        """
        Events
        """
        def handleEvent(self, event):
            """
            Players, enemies, and npcs handle their events.
            Handles primary weapon mechanics
            """
            
            super().handleEvent(event)

        """
        Update
        """
        #override
        def handleClear(self):
            self.lockedSwitch.unlock()
            self.geemer2.set_text(SPEECH["intro_roomclear"])
        
        #override
        def updateSpawning(self,seconds):
            ##  NPCs
            for n in self.spawning:
                if n.animate:
                    n.update(seconds)
                    if n.position[0] >=  16*11:
                        n.vel = vec(0,0)
                        n.ignoreCollision = False
        
        #override
        def updateSwitches(self, seconds):
            for s in self.switches:
                _type = type(s)
                if _type == WeightedSwitch:
                    s.update(self.blockP)
                elif _type == LightSwitch:
                    s.update(self.player, self.blockP)
                elif _type == LockedSwitch:
                    s.update()
                elif _type == TimedSwitch:
                    s.update(seconds)

        def update(self, seconds):
            
            """
            Update the objects that need to be updated
            """
            super().update(seconds)
            
                


class Intro_2(AbstractEngine):
    
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Intro_2()
      
        return cls._INSTANCE

    class _Intro_2(AE):
        """
        Initialization
        """
        def __init__(self):

            """
            Initial conditions
            """
            super().__init__()
            #print((16*9, 16*12))
            #print(COORD[9][11])
            
            self.trigger1 = Trigger(COORD[9][12], SPEECH["intro_entrance"])
            self.trigger1.position[1] += 8
            self.trigger2 = Trigger(COORD[9][0], SPEECH["intro_entrance"])
            self.trigger2.position[1] -= 6

           
            #Music
            self.bgm = "Nujabes_Decade.mp3"
            #Puzzle conditions
            self.resetting = True
            self.enemyPlacement = 1
            self.max_enemies = 4
            """
            Puzzle objects
            """
            #Blocks
            self.blockP = PushableBlock((16*6,16*8))#PushableBlock((96, 112))#Pushable Block
            

            #Switches
            
            #Npcs


            #Spawnable Objects
            self.spawning = [Geemer(COORD[2][9], SPEECH["intro_combat"], fps = 32)]
            
            #Projectiles/weapons

            """
            Display elements
            """
            #Background/room
            self.background = Level("intro_2.png")

            self.enemies = [(Enemy((0,0), "Stalfos.png")) for i in range (4)]


        """
        Auxilary
        """
        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)

        """
        Draw
        """
        def draw(self, drawSurface):
            super().draw(drawSurface)
        
        """
        Collision
        """
        #override
        def blockCollision(self):
            for b in self.blocks:
                if self.player.doesCollide(b):
                    if type(b) == Trigger:
                        if b == self.trigger1:
                            self.transport(Intro_1, COORD[9][1], keepBGM=True)
                        elif b == self.trigger2:
                            self.transport(Intro_3, (16*9, (16*11)-8))
                    else:
                        self.player.handleCollision(b)

        def handleCollision(self):
            """
            Handles collision between the player and objects,
            including puzzle objects like switches and blocks.
            """
            super().handleCollision()
            
        """
        Events
        """
        def handleEvent(self, event):
            """
            Players, enemies, and npcs handle their events.
            Handles primary weapon mechanics
            """
            super().handleEvent(event)


        """
        Update
        """
        #override
        def handleClear(self):
            pass
        
        #override
        def updateSpawning(self,seconds):
            ##  NPCs
            for n in self.spawning:
                if n.animate:
                    n.update(seconds)
                    
        
        #override
        def updateSwitches(self, seconds):
            for s in self.switches:
                _type = type(s)
                pass

        def update(self, seconds):
            """
            Update the objects that need to be updated
            """
            super().update(seconds)



class Intro_3(AbstractEngine):

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Intro_3()
      
        return cls._INSTANCE

    class _Intro_3(AE):

        def __init__(self):
            super().__init__()
            self.bgm = None
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("intro_3.png")
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
        
        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            for i in range(1,12):
                self.blocks.append(Block(COORD[7][i]))
            for i in range(1,12):
                self.blocks.append(Block(COORD[11][i]))
        
        #override
        def blockCollision(self):
            
            for b in self.blocks:
                if self.player.doesCollide(b):
                    if type(b) == Trigger:
                        if b == self.trigger1:
                            self.transport(Intro_2, COORD[9][1])
                        elif b == self.trigger2:
                            self.transport(Grand_Chapel, (16*9, (16*11)-8))
                            print(self.player.position)
                    else:
                        self.player.handleCollision(b)

class Grand_Chapel(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Intro_4()
      
        return cls._INSTANCE
    
    class _Intro_4(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "Hymn.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("grand_chapel.png")
            self.trigger1 = Trigger(door = 0)
        
        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)
            if FLAGS[1] == False:
                self.displayText("        Grand  Chapel    ")
                FLAGS[1] = True

        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)

        #override
        def blockCollision(self):
            for b in self.blocks:
                if self.player.doesCollide(b):
                    if type(b) == Trigger:
                        if b == self.trigger1:
                            self.transport(Intro_3, COORD[9][1])
                else:
                    self.player.handleCollision(b)
            