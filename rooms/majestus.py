from gameObjects import *
from utils import INTRO
"""
This file contains all data pertaining
to each room's engine. Each class represents
a room's engine, and they all inherit from
AbstractEngine.
"""

"""
Intro Cutscene
"""
class Intro_Cut(AbstractEngine):

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._Intro_Cut()
        return cls._INSTANCE
    
    class _Intro_Cut(AE):
        def __init__(self):
            
            self.fading = False
            self.player = None
            self.largeText = False
            self.introDone = False
            self.textBox = False
            self.text = ""
            self.icon = None
            self.boxPos = vec(32,64)
            self.textInt = 0
            self.background = Level("intro_cut.png")

            self.timer = 0
            SoundManager.getInstance().playBGM("still-dreaming.mp3")
        
        def displayText(self, text = "", icon = None, large = True):
            """
            Display text
            """
            self.textBox = True
            self.text = text
            self.largeText = large
          

        def draw(self, drawSurface):
            
            if self.fading:
                Fade.getInstance().draw(drawSurface)
                return

            elif self.textInt >= 4:
                self.boxPos = vec(32, RESOLUTION[1]-(64+32))
                Drawable(fileName = "gods.png").draw(drawSurface)
            elif self.textInt >= 2:
                self.boxPos = vec(32,7)
                Level(fileName = "majestus.png").draw(drawSurface)
            else:
                self.background.draw(drawSurface)

            if self.textInt < 2:
                Text(vec(0,0), text = "Press START to skip text").draw(drawSurface)
            
        
        
        def handleEvent(self):
            pass

        def handleCollision(self):
            pass

        def update(self, seconds):
            """
            Fade within Intro engine,
            ScreenManager fades In after introDone == True
            """
            if self.textInt > 8:
                if Fade.getInstance().frame == 8:
                    self.timer += seconds
                    if self.timer >= 0.5:
                        SoundManager.getInstance().fadeoutBGM()
                        self.introDone = True
                        return
                    return
                else:
                    Fade.getInstance().update(seconds)
                    return
                
            self.timer += seconds
            if self.timer >= 1:
                self.displayText(INTRO[self.textInt], large = True)
                self.timer = 0
                self.textInt += 1
                
                
                    
"""
Testing
"""
class Knight(AbstractEngine):

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Kn()
      
        return cls._INSTANCE
    
    class _Kn(AE):
        def __init__(self):
            super().__init__()
            self.bgm = None
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("test.png")
            self.boss = LavaKnight(vec(RESOLUTION[0]//2-16, RESOLUTION[1]//2-16))
            self.npcs = [
                self.boss,
                Bopper(COORD[2][2]),
                Bopper(COORD[16][2]),
                Bopper(COORD[2][9]),
                Bopper(COORD[16][9]),
            ]
            self.spawning = [ 
                #GreenHeart(vec(16*2, 16*10))
                ]
            self.playingMusic = False

        #override
        def createBlocks(self):
           return
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if False:
                        return
                        self.transport(Room, 0, keepBGM=True)
                    else:
                        self.player.handleCollision(b)

        def update(self, seconds):
            super().update(seconds)
            if not self.playingMusic:
                if self.boss.jumpingUp:
                    self.playBgm("megalomania.mp3")
                    self.playingMusic = True
            elif self.boss.dead:
                self.fadeBgm()
"""
Entrance Hall
"""

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
            self.itemsToCollect = 1
            self.roomId = 1
            #Music
            self.bgm = "Furious_Anger.mp3"
            #Puzzle conditions
            self.enemyPlacement = 0
            self.max_enemies = 2
            
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
            #self.rblock4 = Block((16*11, 16*5), (5,2))
            #self.rblock5 = Block((16*12, 16*6), (5,2))
            #self.rblock6 = Block((16*14, 16*5), (5,2))
            #self.rblock7 = Block((16*13, 16*6), (5,2))

            self.gblock1 = Block((16*8, 16*5), (5,3))
            self.gblock2 = Block((16*8, 16*6), (5,3))
            self.gblock3 = Block((16*9, 16*6), (5,3))
            self.gblock4 = Block((16*10, 16*6), (5,3))
            self.gblock5 = Block((16*10, 16*5), (5,3))
            
            self.yblock1 = Block((144,16*1), (5,5))
            self.yblock2 = Block((144-16,16*1), (5,5))
            self.yblock3 = Block((144+16,16*1), (5,5))

            self.trigger1 = Trigger(door = 0)
            
            self.trigger2 = Trigger(door = 2)
            self.trigger2.position[1] -= 6
            
            self.doors = [0,2]
            #add self.yblock1-3 back
            self.blocks = [self.trigger1,  self.trigger2, 
                           self.block, self.block1, self.block2, self.block3,
                            self.yblock1, self.yblock2, self.yblock3,
                           self.rblock1, self.rblock2, self.rblock3]

            #Switches
            self.weightedSwitch = WeightedSwitch((16*4,16*10))
            self.lockedSwitch = LockedSwitch(COORD[7][6])
            self.lightSwitch = LightSwitch(COORD[11][6])
            self.timedSwitch = TimedSwitch((16*14,16*10))
            self.switch = Switch((16*15,16*7))
            
            self.switches = [self.switch, self.weightedSwitch, self.lightSwitch, self.timedSwitch, self.lockedSwitch]
            
            #Npcs
            self.npcs = []
            for i in range(4, 5):
                self.enemies.append(Gremlin((16*i,32), direction = 1))

            for i in range(14, 15):
                self.enemies.append(Gremlin((16*i,32), direction = 3))

            #Spawnable Objects
            self.chest = Chest(COORD[2][5], SPEECH["intro_chest"], ICON["plant"])
            #self.sign = Sign((COORD[8][2]), SPEECH["intro_sign"])
            self.key = Key((COORD[4][5]))
            
            self.geemer2 = Geemer(((16*7)-3, (16*5)-4), SPEECH["intro_switches"], 1)
            self.geemer2.frame = 2
            self.geemer2.framesPerSecond = 8


            self.geemer3 = Geemer((self.lightSwitch.position[0]-2, self.lightSwitch.position[1]-2), SPEECH["intro_plantgeemer"], 2)
            self.geemer3.framesPerSecond = 6
            self.geemer4 = Geemer((COORD[2][8]), SPEECH["intro_pushableblocks"])
            self.spawning = [
                            self.geemer2, self.geemer3, self.geemer4,
                            ]
            
            #Projectiles/weapons
            

            """
            Display elements
            """
            #Background/room
            self.background = Level("test.png")

            
        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            
            
            super().initializeRoom(player, pos, keepBGM)
            if FLAGS[2] == False:
                self.displayText("       Entrance Hall    ", large = False)
                FLAGS[2] = True

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
        
        

        """
        Collision
        """
        #override
        def blockCollision(self):
            for b in self.blocks:
                self.enemyCollision(b)
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if type(b) == LockBlock and INV["keys"] > 0:
                        self.playSound("LA_Dungeon_Teleport_Appear.wav")
                        self.disappear(b)
                        self.disappear(self.blocks)
                        self.disappear(self.block1)
                        self.disappear(self.block2)
                        self.disappear(self.block3)
                        INV["keys"] -= 1
                    elif type(b) == Trigger:
                        if b == self.trigger1:
                            self.transport(Entrance, 2)
                        elif b == self.trigger2:
                            self.transport(Intro_2, 0, keepBGM=True)
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
                self.itemsToCollect = 0
                self.disappear(self.yblock2)
                self.disappear(self.yblock3)
            if self.rblock1 not in self.blocks:
                self.disappear(self.rblock2)
                self.disappear(self.rblock3)
                # self.disappear(self.rblock4)
                # self.disappear(self.rblock5)
                # self.disappear(self.rblock6)
                # self.disappear(self.rblock7)
            elif self.rblock2 not in self.blocks:
                self.blocks.append(self.rblock2)
                self.blocks.append(self.rblock3)
                # self.blocks.append(self.rblock4)
                # self.blocks.append(self.rblock5)
                # self.blocks.append(self.rblock6)
                # self.blocks.append(self.rblock7)
            
     

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
            super().updateSpawning(seconds)

            if self.geemer3.position[0] >= 16*13:
                self.geemer3.vel = vec(0,0)
                self.geemer3.ignoreCollision = False
            
        
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
            self.roomId = 2
            self.ignoreClear = True
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.trigger3 = Trigger(door = 3)
            self.doors = [0,2,3]
            

           
            #Music
            self.bgm = None
            self.bgm = "Furious_Anger.mp3"
            #Puzzle conditions
            self.resetting = True
            self.enemyPlacement = 2
            self.max_enemies = 4
            """
            Puzzle objects
            """
            #Blocks
            self.blockP = PushableBlock((16*6,16*8))#PushableBlock((96, 112))#Pushable Block
            

            #Switches
            
            #Npcs
            self.npcs = [#Spinner(COORD[5][7]), 
                         #GremlinB(COORD[5][7])
                         #Flapper(COORD[2][9]), 
                         #FireFlapper(COORD[3][9]),
                         #FireFlapper(COORD[4][9]),
                         #FireFlapper(COORD[5][9]),
                         #FireFlapper(COORD[6][9]),
                         #IceFlapper(COORD[4][9]), 
                         #ThunderFlapper(COORD[5][9]), 
                         #WindFlapper(COORD[6][9])
                         ]

            #Spawnable Objects
            self.spawning = [Geemer(COORD[2][9], SPEECH["intro_combat"], fps = 32),
                             Geemer(COORD[12][2], SPEECH["skipping_text"], fps = 50)]
            
            #Projectiles/weapons

            """
            Display elements
            """
            #Background/room
            self.background = Level("intro_2.png")

            
            
            for i in range(2):
                self.enemies.append(Mofos(direction = 1))
            for i in range(2):
                self.enemies.append(Mofos(direction = 3))

            self.enemies.append(Spinner())
            self.enemies.append(Spinner())
            self.enemies.append(Spinner())
            self.enemies.append(Spinner())
            


            """ 
            self.enemies.append(Flapper(direction = 1))#Right, Top
            
            self.enemies.append(Flapper(direction = 2))#Left, Bottom

            self.enemies.append(Flapper(direction = 1))#Right, Top

            self.enemies.append(Flapper(direction = 0))#Left, Top """

            


            
            


        """
        Auxilary
        """
        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            self.blocks.append(self.trigger3)

        """
        Draw
        """
        
        
        """
        Collision
        """
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if type(b) == Trigger:
                        if b == self.trigger1:
                            self.transport(Intro_1, 2, keepBGM=True)
                        elif b == self.trigger2:
                            self.transport(Alpha_Flapper, 0)
                        elif b == self.trigger3:
                            self.transport(Geemer_1, 1)
                    else:
                        self.player.handleCollision(b)

        
        #override
        def handleClear(self):
            pass


class Geemer_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Geemer_1()
      
        return cls._INSTANCE
    
    class _Geemer_1(AE):
        def __init__(self):
            super().__init__()
            self.roomId = 9
            self.bgm = "Nujabes_Decade.mp3"
            self.ignoreClear = True
            self.resetting = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("geemer_1.png")
            self.doors = [1,2]
            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 2)
            self.spawning = [
                Geemer((16*11, 16*5 - 4), text = SPEECH["town_1"], color = 1)
            ]
            self.enemies = [
                Baller(COORD[3][6], direction = 1)
            ]
            self.max_enemies = 1
            self.enemyPlacement = 0

        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            for i in range(2,8):
                self.blocks.append(IBlock(COORD[i][4]))
            for i in range(11,17):
                self.blocks.append(IBlock(COORD[i][4]))
            for i in range(2,17):
                self.blocks.append(IBlock(COORD[i][8]))
            
            
            for i in range(1,4):
                self.blocks.append(IBlock(COORD[7][i]))
            for i in range(1,4):
                self.blocks.append(IBlock(COORD[11][i]))
            for i in range(9,12):
                self.blocks.append(IBlock(COORD[7][i]))
            for i in range(9,12):
                self.blocks.append(IBlock(COORD[11][i]))
           
        #override
        def blockCollision(self):
           for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Intro_2, 3)
                    elif b == self.trigger2:
                        self.transport(Shop, 0, keepBGM=True)
                    else:
                        self.player.handleCollision(b)


class Shop(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Shop()
      
        return cls._INSTANCE
    
    class _Shop(AE):
        def __init__(self):
            super().__init__()
            self.roomId = 10
            self.bgm = "Nujabes_Decade.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("test.png")
            self.trigger1 = Trigger(door = 0)
            self.doors = [0]

            self.shopKeep = Geemer((16*9-2,16*6), text = SPEECH["shopkeep"])
            self.potion = Potion(COORD[4][6])
            self.spawning = [
                self.shopKeep,
                self.potion
            ]

            self.selectedItem = ""

        def handlePrompt(self):
            if self.selectedItem == "potion":
                INV["money"] -= 5
                self.displayText("You bought a potion!&&\nUse it on the pause menu\nto restore a bit of health.\n")
                INV["potion"] += 1
                self.promptResult = False
                self.selectedItem = ""

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Geemer_1, 2, keepBGM=True)
                    else:
                        self.player.handleCollision(b)

class Alpha_Flapper(AbstractEngine):

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._AF()
      
        return cls._INSTANCE
    
    class _AF(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "tension.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("alpha_flapper.png")
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.doors = [0,2]
            self.flapper = AlphaFlapper(vec(16*8 + 8, 16*3))
            self.npcs = [self.flapper]
            self.textInt = 0
            self.obstacles = [
            ]
            for i in range(3):
                self.obstacles.append(ForceField(COORD[8+i][1], render=False))
            for i in range(3):
                self.obstacles.append(ForceField(COORD[8+i][11], render = False))
            

        def bsl(self, enemy, bossTheme):
            super().bsl(enemy, bossTheme)
            for o in self.obstacles:
                o.setRender()


        def bse(self):
            super().bse()
            for o in self.obstacles:
                o.vanish()
            FLAGS[110] = True

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                self.enemyCollision(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Intro_2, 2)
                    elif b == self.trigger2:
                        self.transport(Intro_3, 0)
                    else:
                        self.player.handleCollision(b)

        def update(self, seconds):
            if FLAGS[110]:
                super().update(seconds)
                return
            if self.fightingBoss:
                super().update(seconds)
            elif self.player.position[1] <= 16*6:
                if self.textInt == 1:
                    self.bsl(self.flapper, "ing.mp3")
                elif self.textInt == 0:
                    self.player.stop()
                    self.player.keyUnlock()
                    SoundManager.getInstance().fadeoutBGM()
                    self.displayText("Skreeeeeeee!&&\nOutsider!&&\n")
                    self.textInt += 1
            else:
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
            self.roomId = 3
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("intro_3.png")
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.torches = []
            self.npcs = [Dummy((COORD[8][5])), 
                         Dummy((COORD[9][5])), 
                         Dummy((COORD[10][5]))
                         ]
            self.doors = [0,2]

            
        
       
        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            for i in range(1,12):
                self.blocks.append(Block(COORD[7][i], offset = (5,6)))
            for i in range(1,12):
                self.blocks.append(Block(COORD[6][i], offset = (5,6)))
            for i in range(1,12):
                self.blocks.append(Block(COORD[11][i], offset = (5,6)))
            for i in range(1,12):
                self.blocks.append(Block(COORD[12][i], offset = (5,6)))

            for j in range(2,6,2):
                for i in range(1,12):
                    self.torches.append(Torch((COORD[j][i])))
            for j in range(3,7,2):
                for i in range(1,12):
                    self.torches.append(Torch((COORD[j][i]),2))
            for j in range(14, 17, 2):
                for i in range(1,12):
                    self.torches.append(Torch((COORD[j][i]),3))
            for j in range(13, 17, 2):
                for i in range(1,12):
                    self.torches.append(Torch((COORD[j][i]),1))


        
        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if type(b) == Trigger:
                        if b == self.trigger1:
                            self.transport(Alpha_Flapper, 2)
                        elif b == self.trigger2:
                            self.transport(Grand_Chapel, 0)
                            
                    else:
                        self.player.handleCollision(b)

        

        def update(self, seconds):
            super().update(seconds)
            

class Grand_Chapel_L(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._ChapelL()
      
        return cls._INSTANCE
    
    class _ChapelL(AE):
        def __init__(self):
            super().__init__()
            self.roomId = 7
            self.bgm = "hymn.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("grand_chapel_L.png")
            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 0)
            self.trigger3 = Trigger(door = 2)
            self.doors = [0,1,2]

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Grand_Chapel, 3, keepBGM=True)
                    elif b == self.trigger2:
                        self.transport(Flame_entrance, 2)
                    elif b == self.trigger3:
                        self.transport(Frost_1, 0)
                    else:
                        self.player.handleCollision(b)


class Grand_Chapel_R(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._ChapelR()
      
        return cls._INSTANCE
    
    class _ChapelR(AE):
        def __init__(self):
            super().__init__()
            self.roomId = 8
            self.bgm = "hymn.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("grand_chapel_R.png")
            self.trigger1 = Trigger(door = 3)
            self.trigger2 = Trigger(door = 0)
            self.trigger3 = Trigger(door = 2)
            self.doors = [0,2,3]

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Grand_Chapel, 1, keepBGM=True)
                    elif b == self.trigger2:
                        self.transport(Thunder_1, 3)
                    elif b == self.trigger3:
                        self.transport(Gale_1, 0)
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
            self.roomId = 4
            self.bgm = "hymn.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("grand_chapel.png")
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 3)
            self.trigger3 = Trigger(door = 2)
            self.trigger4 = Trigger(door = 1)
            
            self.portal = Portal(COORD[14][3], 3)



            self.fire = Blessing((COORD[3][4]), 0)
            self.ice = Blessing((COORD[6][4]), 1)
            self.thunder = Blessing((COORD[12][4]), 2)
            self.wind = Blessing((COORD[15][4]), 3)



            self.geemer = Geemer((16*9 - 4, 16*6), text = SPEECH["chapel_geemer"], color = 1)
            self.prompt = Geemer((16*11-4, 16*9), text = "Y/NDo you want to die?")
            

            self.spawning = [self.ice,
                             self.fire,
                             self.thunder,
                             self.wind,
                             self.geemer,
                             self.prompt
                            
                             ]
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            self.blocks.append(self.trigger3)
            self.blocks.append(self.trigger4)

            self.doors = [0,1,2,3]
        
        def handlePrompt(self):
            if self.promptResult:
                if self.selectedItem == 0:
                    if INV["flameShard"] >= INV["flameCost"]:
                        INV["flameShard"] -= INV["flameCost"]
                        if INV["flameCost"] == 1:
                            INV["flameCost"] = 5
                            self.fire.updateCost()
                        self.displayText("Flames upgraded!")
                    else:
                        self.displayText("Not enough shards.")
                    self.promptResult = False

                elif self.selectedItem == 1:
                    if INV["frostShard"] >= INV["frostCost"]:
                        INV["frostShard"] -= INV["frostCost"]
                        if INV["frostCost"] == 1:
                            INV["frostCost"] = 5
                            self.fire.updateCost()
                        self.displayText("Ice upgraded!")
                    else:
                        self.displayText("Not enough shards.")
                    self.promptResult = False

                elif self.selectedItem == 2:
                    if INV["boltShard"] >= INV["boltCost"]:
                        INV["boltShard"] -= INV["boltCost"]
                        if INV["boltCost"] == 1:
                            INV["boltCost"] = 5
                            self.fire.updateCost()
                        self.displayText("Bolt upgraded!")
                    else:
                        self.displayText("Not enough shards.")
                    self.promptResult = False

                if self.selectedItem == 3:
                    if INV["galeShard"] >= INV["galeCost"]:
                        INV["galeShard"] -= INV["galeCost"]
                        if INV["galeCost"] == 1:
                            INV["galeCost"] = 5
                            self.fire.updateCost()
                        self.displayText("Gale upgraded!")
                    else:
                        self.displayText("Not enough shards.")
                    self.promptResult = False

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)
            self.fire.updateCost()

            if FLAGS[1] == False:
                self.displayText("        Grand  Chapel    ", large = False)
                FLAGS[1] = True
                FLAGS[51] = True

        #override
        def createBlocks(self):
            pass
            

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Intro_3, 2)
                    elif b == self.trigger2:
                        self.transport(Grand_Chapel_L, 1, keepBGM=True)
                    elif b == self.trigger4:
                        self.transport(Grand_Chapel_R, 3, keepBGM=True)
                    elif b == self.trigger3:
                        self.transport(Chamber_Access, 0)
                    elif b == self.portal:
                        #self.transport(Gale_1, (16*9, 16*9))
                        pass
                    else:
                        self.player.handleCollision(b)
        
        def update(self, seconds):
            super().update(seconds)
            if not FLAGS[88] and FLAGS[89]:
                self.spawning.pop(self.spawning.index(self.ice))
                self.spawning.pop(self.spawning.index(self.fire))
                self.spawning.pop(self.spawning.index(self.thunder))
                self.spawning.pop(self.spawning.index(self.wind))
                FLAGS[88] = True
            self.portal.update(seconds)

class Chamber_Access(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Access()
      
        return cls._INSTANCE
    
    class _Access(AE):
        def __init__(self):
            super().__init__()
            self.roomId = 5
            self.bgm = None
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("intro_3.png")
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.doors = [0,2]
            self.npcs = [ForceField(COORD[7][8], 1), ForceField(COORD[8][8], 1), ForceField(COORD[9][8], 1), ForceField(COORD[10][8], 1), ForceField(COORD[11][8], 1),
                         ForceField(COORD[7][6], 2), ForceField(COORD[8][6], 2), ForceField(COORD[9][6], 2), ForceField(COORD[10][6], 2), ForceField(COORD[11][6], 2),
                         ForceField(COORD[7][4], 3), ForceField(COORD[8][4], 3), ForceField(COORD[9][4], 3), ForceField(COORD[10][4], 3), ForceField(COORD[11][4], 3),
                         ForceField(COORD[7][2],4), ForceField(COORD[8][2], 4), ForceField(COORD[9][2], 4), ForceField(COORD[10][2], 4), ForceField(COORD[11][2], 4)]
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            for i in range(1,12):
                self.blocks.append(Block(COORD[6][i], offset=(5,6)))
                self.blocks.append(Block(COORD[12][i], offset=(5,6)))

           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Grand_Chapel, 2)
                    else:
                        self.player.handleCollision(b)

class Freeplay(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._FP()
        return cls._INSTANCE
    
    class _FP(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("entrance.png")
            self.npcs = [
                David((COORD[2][5]), 1),
                Flapper(COORD[5][5]),
                Mofos(COORD[12][5]),
                Gremlin(COORD[8][1], direction = 1)
            ]
        
        
        

        #override
        def createBlocks(self):
            pass
            

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    self.player.handleCollision(b)
                self.enemyCollision(b)
        
        def update(self, seconds):
            super().update(seconds)




class Entrance(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._EN()
        return cls._INSTANCE
    
    class _EN(AE):
        def __init__(self):
            super().__init__()
            self.healthBarLock = True
            self.bgm = "droplets.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("entrance.png")
            self.door1 = Trigger(door = 2)
            self.trigger1 = Trigger(text = SPEECH["intro_entrance"], door = 0)

            self.geemer = Geemer((16*8, 16*4), SPEECH["intro_geemer"], 0, 2)
            self.spawning.append(self.geemer)
            self.npcs = [
                ]
            self.doors = [0,2]

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)
        
        #override
        def createBlocks(self):
            self.blocks.append(self.door1)
            self.blocks.append(self.trigger1)
            #self.blocks.append(self.door2)
            for i in range(1,12):
                self.blocks.append(IBlock(COORD[7][i]))

            for i in range(1,12):
                self.blocks.append(IBlock(COORD[11][i]))
            

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.door1:
                        self.transport(Intro_1, (16*9, (16*11) - 8))
                    elif b == self.trigger1:
                        self.player.position[1] = 16*11
                        b.interact(self.player, self)
                    else:
                        self.player.handleCollision(b)
                self.enemyCollision(b)
        
        def update(self, seconds):
            if self.healthBarLock:
                self.player.keyLock()
                self.timer += seconds
                if self.timer >= 1.0:
                    self.player.keyUnlock()
                    self.healthBarLock = False
                    self.timer = 0
            super().update(seconds)





"""
Fire
"""
class Flame_entrance(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_entrance()
      
        return cls._INSTANCE
    
    class _Flame_entrance(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pso.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_entrance.png")
            self.doors = [2,3]
            self.trigger1 = Trigger(door = 3)
            self.trigger2 = Trigger(door = 2)
            self.trigger3 = Trigger(vec(16*13 - 2, 16*5), width = 20, height = 12)
            self.motionTick = 0
            self.motionTimer = 0.0
            self.geemer = Geemer(COORD[4][3], text = SPEECH["flame_entrance_geemer"])
            self.spawning = [self.geemer,
                             Geemer((COORD[15][6]), text = SPEECH["flame_entrance_geemer2"])
            ]
            self.enemies = [Baller(COORD[8][10]),
                         Baller(COORD[10][10], 1)]
        #override
        def createBlocks(self):
           for i in range(11, 16):
               for j in range(3, 6):
                if i == 13 and j == 5:
                    pass
                elif j == 5:
                    if i == 12:
                        self.blocks.append(IBlock(COORD[i][j], width = 14))
                    elif i == 14:
                        self.blocks.append(IBlock((16*i +2, 16*j), width = 14))
                    else:
                        self.blocks.append(IBlock(COORD[i][j]))
                else:
                    self.blocks.append(IBlock(COORD[i][j]))
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Flame_1, 1, keepBGM=False)
                    elif b == self.trigger2:
                        self.transport(Grand_Chapel_L, 0)
                    elif b == self.trigger3:
                        self.transportPos(Flame_dispensary, vec(16*9, 16*8))
                    else:
                        self.player.handleCollision(b)

        def update(self, seconds):
            super().update(seconds)
            if self.motionTick == 0:
                self.geemer.position[0] += 0.2
            elif self.motionTick == 1:
                pass
            elif self.motionTick == 2:
                self.geemer.position[0] -= 0.2
            elif self.motionTick == 3:
                pass
            """ elif self.motionTick == 2:
                self.geemer.position[0] -= 0.2
            elif self.motionTick == 3:
                self.geemer.position[1] -= 0.2 """
            self.motionTimer += seconds
            if self.motionTimer >= 2.0:
                self.motionTimer = 0.0
                self.motionTick += 1
                self.motionTick %= 4

class Flame_dispensary(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._FD()
      
        return cls._INSTANCE
    
    class _FD(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "Jhene.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("dispensary_flame.png")
            self.trigger1 = Trigger(vec(16*9, 16*9 + 12), height = 12)
            self.shopkeep = Geemer(vec(16*9 - 2, 16*4), variant = "dispo")
            self.spawning = [self.shopkeep]

        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            for i in range(6, 13):
                if i == 9:
                    pass
                else:
                    self.blocks.append(IBlock((16*i, 16*9 + 8)))

            for i in range(6, 13):
                self.blocks.append(IBlock(COORD[i][2]))
            for i in range(3, 9):
                self.blocks.append(IBlock(COORD[5][i]))
            for i in range(3, 9):
                self.blocks.append(IBlock(COORD[13][i]))



        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transportPos(Flame_entrance, vec(16*13, 16*6))
                    else:
                        self.player.handleCollision(b)

        def handlePrompt(self):
            if self.selectedItem == "roll":
                INV["plant"] -= 1
                self.displayText("He rolled you a blunt!&&\nSmoke it to see things\nunseen by the sober eye!\n")
                INV["joint"] += 1
                self.promptResult = False
                self.selectedItem = ""

class Flame_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_1()
      
        return cls._INSTANCE
    
    class _Flame_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = False
            self.max_enemies = 8
            self.enemyPlacement = 2
            self.background = Level("flame_1.png")
            self.enemies = [FireFlapper() for i in range(6)]
            self.enemies.append(Flapper())
            self.enemies.append(Flapper())
            self.doors = [1,2,3]
            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 2)
            self.trigger3 = Trigger(door=3)

            self.obstacles = [
                Boulder((16*2 -10, 16*4 - 8)),
                Boulder((16*4 -10, 16*6 - 8)),
                Boulder((16*2 -10, 16*7 + 8))
                ]

            self.lockedSwitch = LockedSwitch(COORD[9][6])
            
            self.switches.append(self.lockedSwitch)
            self.yblock1 = Block((144,16*1), (5,5))
            self.yblock2 = Block((144-16,16*1), (5,5))
            self.yblock3 = Block((144+16,16*1), (5,5))
            self.blocks.append(self.yblock1)
            self.blocks.append(self.yblock2)
            self.blocks.append(self.yblock3)

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            if FLAGS[3] == False:
                self.displayText("    Corridor of the Flame", large = False)
                FLAGS[3] = True
            
            super().initializeRoom(player, pos, keepBGM)


        def handleClear(self):
            self.lockedSwitch.unlock()
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_entrance, 3, keepBGM=False)
                elif b == self.trigger2:
                    self.transport(Flame_2, 0, keepBGM=True)
                elif b == self.trigger3:
                    self.transport(Flame_4, 1, keepBGM=True)
                else:
                    self.player.handleCollision(b)        

        def handleCollision(self):
            super().handleCollision()
            self.despawnOnPress(self.yblock1, self.lockedSwitch)
            if self.yblock1 not in self.blocks:
                self.disappear(self.yblock2)
                self.disappear(self.yblock3)

class Flame_2(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_2()
      
        return cls._INSTANCE
    
    class _Flame_2(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = False
            self.max_enemies = 4
            self.enemyPlacement = 1
            self.background = Level("flame_2.png")
            self.enemies = [FireFlapper(), Mofos(), FireFlapper(), GremlinB()]
            

            self.doors = [0,2,3]
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.trigger3 = Trigger(door = 3)

            self.portal = Portal(COORD[9][6], 0)
            self.chest = Chest(COORD[9][9], SPEECH["first_bombo"], ICON["bombo"])
            
            self.obstacles = [Boulder((16*2 -10, 16*4 - 8)),
                Boulder((16*4 -10, 16*6 - 8)),
                Boulder((16*2 -10, 16*7 + 8))
                ]
            

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)


        def handleClear(self):
            
            #self.displayText("The raging flames have\nbeen graciously doused!\n")
            self.spawning.append(self.chest)

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_1, 2, keepBGM=True)
                elif b == self.trigger2:
                    self.transport(Flame_5, 0, keepBGM=True)
                elif b == self.trigger3:
                    self.transport(Flame_3, 1, keepBGM=True)
                elif b == self.portal:
                    self.transport(Grand_Chapel, 0)
                else:
                    self.player.handleCollision(b)        

        def update(self, seconds):
            super().update(seconds)
            self.portal.update(seconds)

class Flame_5(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_5()
      
        return cls._INSTANCE
    
    class _Flame_5(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = True
            self.background = Level("flame_5.png")
            self.enemyPlacement = 0
            self.max_enemies = 0
            #self.enemies = [FireFlapper(), Mofos(), FireFlapper(), GremlinB()]
            self.npcs = [Bopper(COORD[9][3]),
                         Bopper(COORD[5][5]),
                         Bopper(COORD[13][5])]

            self.doors = [0]
            
            self.chest = Chest(COORD[13][9], SPEECH["bombo_expansion"], ICON["bombo"])
            self.spawning = [
                Sign(COORD[7][9], SPEECH["boppers"]),
                self.chest
            ]
            self.obstacles = [
                Boulder((16*12 + 8, 16*9 - 8))
            ]
            self.trigger1 = Trigger(door = 0)
            

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)


        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_2, 2, keepBGM=True)
                else:
                    self.player.handleCollision(b)        

        def update(self, seconds):
            super().update(seconds)

class Flame_3(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_3()
      
        return cls._INSTANCE
    
    class _Flame_3(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = True
            self.background = Level("flame_3.png")
            self.enemyPlacement = 3
            self.max_enemies = 4
            self.enemies = [Mofos(direction=0), Mofos(direction=2), Baller(direction=1), Baller(direction=3),
                            Mofos(direction = 0), Mofos(direction = 2)]
            self.npcs = [
                         #Bopper(COORD[9][3]),
                         #Bopper(COORD[5][5]),
                         #Bopper(COORD[13][5])
                         ]

            self.doors = [0, 1]
            
            #self.chest = Chest(COORD[13][9], SPEECH["bombo_expansion"], ICON["bombo"])
            self.spawning = [
                #Sign(COORD[7][9], SPEECH["boppers"]),
                #self.chest
            ]
            self.obstacles = [
                #Boulder((16*12 + 8, 16*9 - 8))
            ]

            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 0)
            

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)


        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_2, 3, keepBGM=True)
                elif b == self.trigger2:
                    self.transport(Flame_4, 2, keepBGM=True)
                else:
                    self.player.handleCollision(b)        

        def update(self, seconds):
            super().update(seconds)


class Flame_4(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_4()
      
        return cls._INSTANCE
    
    class _Flame_4(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = True
            self.background = Level("flame_4.png")
            self.enemyPlacement = 0
            self.max_enemies = 0
            #self.enemies = [FireFlapper(), Mofos(), FireFlapper(), GremlinB()]
            self.npcs = [
                        Heater(COORD[9][6])
                         #Bopper(COORD[9][3]),
                         #Bopper(COORD[5][5]),
                         #Bopper(COORD[13][5])
                         ]

            self.doors = [0, 1, 2]
            
            #self.chest = Chest(COORD[13][9], SPEECH["bombo_expansion"], ICON["bombo"])
            self.spawning = [
                #Sign(COORD[7][9], SPEECH["boppers"]),
                #self.chest
            ]
            self.obstacles = [
                #Boulder((16*12 + 8, 16*9 - 8))
            ]
            
            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 0)
            self.trigger3 = Trigger(door = 2)
            

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)


        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_1, 3, keepBGM=True)
                elif b == self.trigger2:
                    self.transport(Flame_6, 2, keepBGM=True)
                elif b == self.trigger3:
                    self.transport(Flame_3, 0, keepBGM=True)
                else:
                    self.player.handleCollision(b)        

        def update(self, seconds):
            super().update(seconds)

class Flame_6(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_6()
      
        return cls._INSTANCE
    
    class _Flame_6(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = True
            self.background = Level("flame_4.png")
            self.enemyPlacement = 4
            self.max_enemies = 1
            self.stomper = Stomper(boss=True)
            self.stomper.unPause(position = vec(16*8 - 6, 16*5))
            self.enemies = [
                        self.stomper
                        ]
            
            self.npcs = [
                Bopper(COORD[3][10]),
                Bopper(COORD[15][10])
            ]
            self.stomperTimer = 0.0

            self.doors = [0,2,3]
            
            if not FLAGS[61]:
                self.spawning = [
                    Geemer(vec(16*8 - 8, 16*5 + 8))

                ]
            
            if FLAGS[62]:
                self.spawning = [
                    Geemer(vec(16*10, 16*5 + 8), text = SPEECH["post_stomper"])
                ]

            self.obstacles = [
                #Boulder((16*12 + 8, 16*9 - 8))
            ]
            
            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 0)
            self.trigger3 = Trigger(door = 2)

            self.inCutscene = False
            self.textInt = 0
            self.miniBoss = False
        
        def deathReset(self):
            super().deathReset()
            self.removeObstacles()
            self.miniBoss = False

        def removeObstacles(self):
            for o in self.obstacles:
                o.vanish()

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            if not FLAGS[62]:
                super().initializeRoom(player, pos, keepBGM)
            else:
                if len(self.spawning) == 0:
                    self.spawning = [
                    Geemer(vec(16*10, 16*5 + 8), text = SPEECH["post_stomper"])
                ]
                super().initializeRoom(player, pos, keepBGM, placeEnemies=False)

 
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_1, 3, keepBGM=True)
                elif b == self.trigger2:
                    pass
                elif b == self.trigger3:
                    self.transport(Flame_3, 0, keepBGM=True)
                else:
                    self.player.handleCollision(b)        

        def beginMiniBoss(self):
            self.miniBoss = True
            SoundManager.getInstance().playBGM("LA_FinalBoss.mp3")
            for i in range(3):
                self.obstacles.append(ForceField(COORD[8+i][1]))
            self.stomper.ignoreCollision = False
            self.stomper.frozen = False

        def update(self, seconds):
            if FLAGS[62]:
                if self.miniBoss:
                    SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)
                    SoundManager.getInstance().playBGM(self.bgm)
                    self.removeObstacles()
                    self.miniBoss = False

                else:
                    super().update(seconds)

            elif FLAGS[61]:
                if self.stomper.dead:
                    if self.stomperTimer == 0.0:
                        SoundManager.getInstance().fadeoutBGM()
                        self.displayText("The boss will have a\ngreat time avenging me!!\n")
                        self.stomperTimer += seconds
                    elif self.stomperTimer >= 0.3:
                        FLAGS[62] = True
                        super().update(seconds)
                    else:
                        self.stomperTimer += seconds
                    return
                elif self.miniBoss:
                    super().update(seconds)
                elif self.player.position[1] >= 20:
                    self.beginMiniBoss()
                else:
                    super().update(seconds, updateEnemies=False)
            else:
                super().update(seconds, updateEnemies=False)
                if self.inCutscene:
                    if self.textInt == 2:
                        self.stomper.update(seconds, position = vec(16*8 - 6, 16*5))
                        if self.stomper.pause:
                            self.spawning.pop(0)
                            self.inCutscene = False
                            return
                        

                    if self.stomperTimer >= 1.0:
                        if self.textInt == 0:
                            self.displayText("Whoa, man! Chill out!&&\nPlease, my Goddess Estelle,\nsave me from this fiend!\n")
                        elif self.textInt == 1:
                            self.displayText("Shutup, ant.&&\nYour Goddess can't save you.&&\nWithout the power of ice,\nyou're a feeble creature!\n")
                        self.textInt += 1
                        self.stomperTimer = 0.0
                    else:
                        self.stomperTimer += seconds

                elif len(self.spawning) == 0:
                    if self.miniBoss:
                        if self.stomperTimer >= 1.0:
                            self.beginMiniBoss()                            
                            self.stomperTimer = 0.0
                            FLAGS[61] = True
                            self.player.keyUnlock()
                            self.inCutscene = False
                        else:
                            self.stomperTimer += seconds

                    elif self.stomperTimer >= 2.0:
                        self.stomperTimer = 0.0
                        self.displayText("Ah! Yet another human!&&\nCrushing you is way more\nfun than crushing Geemers!\nThe boss won't even have\nto waste his time with you!\nGood riddance, outsider!&&\n")
                        self.miniBoss = True
                    else:
                        self.stomperTimer += seconds
                
                elif self.player.position[1] >= 20:
                    self.inCutscene = True
                    self.player.stop()
                    self.player.keyLock()
                    SoundManager.getInstance().fadeoutBGM()
"""
Thunder
"""
class Thunder_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Thun_1()
      
        return cls._INSTANCE
    
    class _Thun_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "voyager.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("thunder_1.png")
            self.doors = [3, 0, 2]
            self.toChapel = Trigger(door = 3)
            self.trigger = Trigger(door = 0)
            self.trigger2 = Trigger(door=2)
            self.geemer = Geemer((16*2, 16*5-8), text = SPEECH["menu_reminder"])
            self.geemer2 = Geemer(COORD[9][6], text = SPEECH["thunder_1"])
            self.geemer3 = Geemer((16*9-4, 16), text = SPEECH["thunder_2"], hungry = True, feedText=SPEECH["thunder_fead"])
            self.geemer3.framesPerSecond = 1
            self.spawning.append(self.geemer)
            self.spawning.append(self.geemer2)
            self.spawning.append(self.geemer3)
            for j in range(1,12):
                for i in range(2,17):
                    self.tiles.append(Tile((i*16, j*16)))

            #self.trigger1 = Trigger(door = 0)
        

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            if FLAGS[4] == False:
                self.displayText("     Alcove of the Bolt", large = False)
                FLAGS[4] = True
            
            super().initializeRoom(player, pos, keepBGM)
        
        
        #override
        def createBlocks(self):
           self.blocks.append(self.toChapel)
           self.blocks.append(self.trigger)
           self.blocks.append(self.trigger2)
               
           
        #override
        def blockCollision(self):
           for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.toChapel:
                       self.transport(Grand_Chapel_R, 0)
                    elif b == self.trigger:
                        self.transport(Thunder_2, 2, keepBGM=True)
                    elif b == self.trigger2:
                        self.transport(Thunder_3, 0, keepBGM=True)
                    else:
                       self.player.handleCollision(b)

        def update(self,seconds):
            super().update(seconds)
            if self.geemer3.fead:
                if self.geemer3.position[0] >= 16*11:
                    self.geemer3.ignoreCollision = False
                    self.geemer3.vel = vec(0,0)

class Thunder_2(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Thun_2()
      
        return cls._INSTANCE
    
    class _Thun_2(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "voyager.mp3"
            self.ignoreClear = False
            self.max_enemies = 8
            self.enemyPlacement = 2
            self.background = Level("thunder_2.png")
            self.doors = [2]
            
            self.chest = Chest(COORD[9][6], SPEECH["plant"], ICON["plant"])
            
            self.trigger = Trigger(door = 2)
            self.enemies = [
                ThunderFlapper(),ThunderFlapper(),ThunderFlapper(),ThunderFlapper(),
                IceFlapper(),IceFlapper(),IceFlapper(),IceFlapper()
            ]

            self.npcs = [
                Dummy(COORD[7][6]),
                Dummy(COORD[9][4]),
                Dummy(COORD[11][6]),
                Dummy(COORD[9][8])
            ]
            self.tiles = [
                Tile(COORD[7][4]),Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),Tile(COORD[11][4]),
                Tile(COORD[7][5]),Tile(COORD[8][5]),Tile(COORD[9][5]), Tile(COORD[10][5]),Tile(COORD[11][5]),
                Tile(COORD[7][6]),Tile(COORD[8][6]),Tile(COORD[9][6]), Tile(COORD[10][6]),Tile(COORD[11][6]),
                Tile(COORD[7][7]),Tile(COORD[8][7]),Tile(COORD[9][7]), Tile(COORD[10][7]),Tile(COORD[11][7]),
                Tile(COORD[7][8]),Tile(COORD[8][8]),Tile(COORD[9][8]), Tile(COORD[10][8]),Tile(COORD[11][8])
                #Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),
                #Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),

            ]
            

            #self.trigger1 = Trigger(door = 0)
        

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            
            super().initializeRoom(player, pos, keepBGM)
        
        
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger)
           
               
        def handleClear(self):
            self.spawning.append(self.chest)

        #override
        def blockCollision(self):
           for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.trigger:
                        self.transport(Thunder_1, 0, keepBGM=True)
                    else:
                       self.player.handleCollision(b)


class Thunder_3(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Thun_3()
      
        return cls._INSTANCE
    
    class _Thun_3(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "voyager.mp3"
            self.ignoreClear = True
            self.resetting = True
            self.max_enemies = 26
            self.enemyPlacement = 0
            self.background = Level("thunder_3.png")
            self.doors = [0]
            
           
            
            self.trigger = Trigger(door = 0)
            
            self.portal = Portal(COORD[9][6], 2)
            self.blocks.append(self.portal)
            self.sign = Sign(COORD[9][3], text = SPEECH["thunder_sign"])
            self.spawning.append(self.sign)
            self.enemies = [
                Dummy(COORD[7][8]),
                Dummy(COORD[8][8]),
                Dummy(COORD[9][8]),
                Dummy(COORD[10][8]),
                Dummy(COORD[11][8]),

                Dummy(COORD[7][7]),
                Dummy(COORD[8][7]),
                Dummy(COORD[9][7]),
                Dummy(COORD[10][7]),
                Dummy(COORD[11][7]),

                Dummy(COORD[7][6]),
                Dummy(COORD[8][6]),
                Dummy(COORD[10][6]),
                Dummy(COORD[11][6]),

                Dummy(COORD[7][5]),
                Dummy(COORD[8][5]),
                Dummy(COORD[9][5]),
                Dummy(COORD[10][5]),
                Dummy(COORD[11][5]),

                Dummy(COORD[7][4]),
                Dummy(COORD[8][4]),
                Dummy(COORD[9][4]),
                Dummy(COORD[10][4]),
                Dummy(COORD[11][4]),

                GremlinB(COORD[2][9], direction = 1),
                GremlinB(COORD[16][9], direction = 3),
                GremlinB(COORD[2][2], direction = 1),
                GremlinB(COORD[16][2], direction = 3)
            ]
            self.tiles = [
                Tile(COORD[7][4]),Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),Tile(COORD[11][4]),
                Tile(COORD[7][5]),Tile(COORD[8][5]),Tile(COORD[9][5]), Tile(COORD[10][5]),Tile(COORD[11][5]),
                Tile(COORD[7][6]),Tile(COORD[8][6]), Tile(COORD[10][6]),Tile(COORD[11][6]),
                Tile(COORD[7][7]),Tile(COORD[8][7]),Tile(COORD[9][7]), Tile(COORD[10][7]),Tile(COORD[11][7]),
                Tile(COORD[7][8]),Tile(COORD[8][8]),Tile(COORD[9][8]), Tile(COORD[10][8]),Tile(COORD[11][8])
                #Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),
                #Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),

            ]
            

            #self.trigger1 = Trigger(door = 0)
        

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            
            super().initializeRoom(player, pos, keepBGM)
        
        
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger)
           
               

        #override
        def blockCollision(self):
           for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.trigger:
                        self.transport(Thunder_1, 2, keepBGM=True)
                    elif b == self.portal:
                        self.transport(Grand_Chapel, 0)
                    else:
                       self.player.handleCollision(b)

        def update(self, seconds):
            super().update(seconds)
            self.portal.update(seconds)

"""
Frost
"""
class Frost_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Frost_1()
      
        return cls._INSTANCE
    
    class _Frost_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "LA_color.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("frost_1.png")
            self.doors = [0]
            self.toChapel = Trigger(door = 0)
            #self.trigger1 = Trigger(door = 0)
            self.torch1 = Torch((COORD[7][5]), lit = False)
            self.torch2 = Torch((COORD[11][5]), lit = False)

            self.chest = Chest(COORD[9][3], text = SPEECH["david"])
            self.spawning.append(self.chest)
            self.weightedSwitch = WeightedSwitch((16*9,16*8))
            self.switches.append(self.weightedSwitch)
            self.blockP = PushableBlock((16*6,16*8))
            self.david = David(COORD[9][6], boss = True)
            #self.david.hp = 1
            self.portal = Portal(COORD[9][6], 1)
            self.torches.append(self.torch1)
            self.torches.append(self.torch2)

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            if FLAGS[5] == False:
                self.displayText("      Abyss of the Frost", large = False)
                FLAGS[5] = True
            
            super().initializeRoom(player, pos, keepBGM)
        #override
        def createBlocks(self):
           self.blocks.append(self.toChapel)
           
           
        #override
        def blockCollision(self):
            for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.toChapel:
                       self.transport(Grand_Chapel_L, 2)
                    elif b == self.portal:
                        self.transport(Grand_Chapel, 0)
                    else:
                       self.player.handleCollision(b)


            for t in self.torches:
                if self.player.doesCollide(t):
                    self.player.handleCollision(t)
                self.projectilesOnTorches(t)
        
        def handleCollision(self):
            super().handleCollision()
            if self.blockP not in self.pushableBlocks and (self.torch1.lit and self.torch2.lit):
                self.playSound("menuclose.wav")
                self.pushableBlocks.append(self.blockP)
            if not self.david.dead:
                if self.weightedSwitch.pressed:
                    if self.david not in self.npcs:
                        self.npcs.append(self.david)
        
        def update(self, seconds):
            super().update(seconds)
            if self.david.dead:
                if self.portal not in self.blocks:
                    self.blocks.append(self.portal)
                    self.playSound("room_clear.mp3")
                    self.displayText("David has been slain!&&")
                self.portal.update(seconds)



"""
Gale
"""
class Gale_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Gale_1()
      
        return cls._INSTANCE
    
    class _Gale_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "windFortress.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("gale_1.png")
            self.doors = [0,2]
            self.portal = Portal(COORD[8][10], 3)
            self.trigger1 = Trigger(door = 0)
            self.sign = Sign(COORD[9][4], text = SPEECH["gale_sign"])
            self.spawning.append(self.sign)
            self.npcs = [
                David(COORD[2][8]),
                David(COORD[16][6], direction = 3),
                David(COORD[2][4]),
                David(COORD[16][2], direction = 3),
                GremlinB(COORD[8][5], direction = 1),
                GremlinB(COORD[10][5], direction = 3)
            ]
            #self.trigger1 = Trigger(door = 0)
        


        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            if FLAGS[6] == False:
                self.displayText("      Grove of the Gale", large = False)
                FLAGS[6] = True
            
            super().initializeRoom(player, pos, keepBGM)

        #override
        def createBlocks(self):
           self.blocks.append(self.portal)
           self.blocks.append(self.trigger1)
           
        #override
        def blockCollision(self):
           for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.portal:
                       self.transport(Grand_Chapel, COORD[14][4])
                    elif b == self.trigger1:
                        self.transport(Grand_Chapel_R, 2)
                    else:
                       self.player.handleCollision(b)


        def update(self, seconds):
            super().update(seconds)
            self.portal.update(seconds)