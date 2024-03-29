import pygame

from . import (Drawable, HealthBar, AmmoBar, Fade, Drop, Heart, Text, Player, Enemy, NonPlayer, Sign, Chest, Key, Geemer, Switch, 
               WeightedSwitch, LightSwitch, TimedSwitch, LockedSwitch, Block, IBlock, Trigger, HBlock,
               PushableBlock, LockBlock, Bullet, Sword, Cleats, Clap)



from utils import SoundManager, vec, RESOLUTION, SPEECH, ICON, INV, COORD, FLAGS

class AE(object):
    def __init__(self):
        self.player = None
        self.resetting = False
        self.ignoreClear = False
        #Death
        self.dead = False
        self.dying = False
        #Room transitioning
        self.readyToTransition = False
        self.transporting = False
        self.tra_room = None
        self.tra_pos = None
        self.tra_keepBGM = False
        self.enemyCounter = 0
        #Flash
        self.black = Fade.getInstance()
        self.flashes = 0
        self.fading = False
        #Speaking
        self.textBox = False
        self.text = ""
        self.icon = None
        self.boxPos = vec(32,64)
        #Puzzle conditions
        self.room_set = False
        self.room_clear = False
        self.clearFlag = 0
        #Player
        #Enemy list to pass into placeEnemies
        self.enemies = []
        self.pushableBlocks = []
        self.npcs = []
        self.spawning = []
        self.projectiles = []
        self.switches = []
        self.blocks = []
        
        #Size of the room
        self.size = vec(*RESOLUTION)
        #HUD
        self.keyCount = Drawable((0, RESOLUTION[1]-16), "KeyCount.png")
        self.healthBar = HealthBar()
        self.ammoBar = AmmoBar()
        #Unique room elements:
        #self.max_enemies
        #self.enemyPlacement
        #self.bgm


    """
    Auxilary methods
    """
    def reset(self):
        self.readyToTransition = False
        self.transporting = False
        self.tra_room = None
        self.tra_pos = None
        self.tra_keepBGM = False
        self.fading = False
        if self.resetting:
            self.enemyCounter = 0
            self.room_clear = False
        if self.spawning:
            for i in range (len(self.spawning)-1, -1, -1):
                if issubclass(type(self.spawning[i]), Drop):
                    self.disappear(self.spawning[i])

    def initializeRoom(self, player= None, pos = None, keepBGM = False):
        if player != None:
            self.player = player
        else:
            self.player = Player((16*9, (16*11) - 8))
        
        if pos != None:
            self.player.position = pos 
            #self.player.position = (pos + self.player.vel)
        print(self.player.position)

        self.black.reset()
        self.createBounds()
        self.createBlocks()
        self.placeEnemies(self.enemies)
        if not keepBGM:
            if self.bgm == None:
                SoundManager.getInstance().fadeoutBGM()
            else:
                SoundManager.getInstance().playBGM(self.bgm)
        self.fading = False
        self.player.keyUnlock()

    def createBounds(self):
        """
        Creates boundaries on the outer edge of the map
        """
        #Left side
        for i in range(1, 12):
            self.blocks.append(IBlock((8,i*16)))
        #Right side
        for i in range(1, 12):
            self.blocks.append(IBlock((RESOLUTION[0]-24,i*16)))
        #Top side
        """ for i in range(1,18):
            self.blocks.append(IBlock((i*16, 0))) """
        for i in range(1,9):
            self.blocks.append(IBlock((i*16, 0)))
        for i in range(10, 18):
            self.blocks.append(IBlock((i*16, 0)))
        #Bottom side
        for i in range(1,9):
            self.blocks.append(IBlock((i*16, RESOLUTION[1]-16)))
        for i in range(10, 18):
            self.blocks.append(IBlock((i*16, RESOLUTION[1]-16)))
    
    #abstract
    def createBlocks(self):
        """
        Abstract method
        """
        pass

    def placeEnemies(self, enemyLst):
        """
        Place the enemies according to a predetermined algorithm
        """
        if self.enemyPlacement > 0:
            if self.enemyPlacement == 1:
            
                for e in enemyLst:
                    if e not in self.npcs:
                        if e.dead:
                            e.respawn()
                        self.npcs.append(e)

                enemyLst[0].position = COORD[6][3]
                enemyLst[1].position = COORD[11][3]
                enemyLst[2].position = COORD[6][7]
                enemyLst[3].position = COORD[11][7]

            

    def fade(self):
        self.player.keyLock()
        self.fading = True

    def transport(self, room=None, position=None, keepBGM = False):
        """
        Transport the player to a different room
        """
        self.fade()
        self.transporting = True
        self.tra_room = room.getInstance()
        self.tra_pos = position
        self.tra_keepBGM = keepBGM
    
    def displayText(self, text = "", icon = None):
        """
        Display text
        """
        self.textBox = True
        self.text = text
        if icon != None:
            self.icon = icon
    
    def flash(self, num = 0):
        """
        Flash the screen white
        """
        self.playSound("LA_Dungeon_Signal.wav")
        self.flashes = num

    def wait(self, time):
        """
        Halt the progression of the game for a certain amount of time
        """
        clock = pygame.time.Clock()
        seconds = 0
        while seconds < time:
            clock.tick(60)
            seconds += (clock.get_time() / 1000)
    
    def disappear(self, obj):
        if obj in self.spawning:
            self.spawning.pop(self.spawning.index(obj))
        elif obj in self.npcs:
            self.npcs.pop(self.npcs.index(obj))
        elif obj in self.projectiles:
            self.projectiles.pop(self.projectiles.index(obj))
        elif obj in self.blocks:
            self.blocks.pop(self.blocks.index(obj))
        elif obj in self.switches:
            self.switches.pop(self.switches.index(obj))
        

    def playSound(self, name):
        SoundManager.getInstance().playSFX(name)

    """
    Event control methods
    """
    def weaponControl(self):
        #Basic bullet
        if self.player.bullet != None:
            self.projectiles.append(self.player.getBullet())
            self.player.bullet = None

        #Sword swings
        if self.player.sword != None:
            self.projectiles.append(self.player.getSlash())
            self.playSound(self.player.swordSound)
            self.player.sword = None
        
        #Thunder clap
        if self.player.clap != None:
            self.projectiles.append(self.player.getClap())
            self.playSound(Clap.SOUND)
            self.player.clap = None
        
    def interactableEvents(self, event):
        """
        Handles interaction from the player
        """
        if self.spawning:
            for n in self.spawning:
                if type(n) == Chest and self.player.interactable(n):
                    self.player.handleEvent(event, n, self)

                elif (type(n) != Key) and self.player.interactable(n):
                    self.player.handleEvent(event, n, self)
                
                elif self.player.interactable(n):
                    self.player.handleEvent(event, n, self)
                else:
                    self.player.handleEvent(event)
        else:
            self.player.handleEvent(event)
    
    def handleEvent(self, event):
        
        self.weaponControl()
        self.interactableEvents(event)
    
    """
    Collision methods
    """
    def despawnOnPress(self, obj, switch):
        """
        Despawns object if the switch is pressed
        """
        if type(switch) == LightSwitch:
            if switch.pressed:
                if obj in self.blocks:
                    self.playSound("menuclose.wav")
                    self.blocks.pop(self.blocks.index(obj))
                    

            elif (obj not in self.blocks) and (obj not in self.spawning):
                if type(obj) == Block:
                    self.playSound("menuopen.wav")
                    self.blocks.append(obj)
                else:
                    self.playSound("menuopen.wav")
                    self.spawning.append(obj)

        elif switch.pressed and (obj in self.blocks or obj in self.spawning):
            if obj in self.blocks:
                self.blocks.pop(self.blocks.index(obj))
            else:
                self.spawning.pop(self.spawning.index(obj))

    def spawnOnPress(self, obj, switch):
        """
        Spawns an object if the corresponding switch is pressed
        """
        #Spawn if switch pressed
        if type(obj) == PushableBlock:
            if switch.pressed and (obj not in self.pushableBlocks):
                print("A")
                self.playSound("menuclose.wav")
                self.pushableBlocks.append(obj)
            return

        elif type(switch) == LightSwitch or type(switch) == TimedSwitch:
            if obj in self.spawning:
                if (not switch.pressed):
                    self.playSound("menuopen.wav")
                    self.disappear(obj)
            
        
        if (not obj.interacted) and switch.pressed and not(obj in self.spawning):
            self.playSound("menuclose.wav")
            self.spawning.append(obj)

    def pressSwitches(self):
        """
        Presses a switch if the player is on it
        """
        for n in self.switches:
            if self.player.doesCollide(n):
                if (not n.pressed) and type(n) != WeightedSwitch:
                    n.press()

    def npcCollision(self):

        for n in self.npcs:
        #Check if it collides with the player first
            if self.player.doesCollide(n):
                #Push blocks
                if issubclass(type(n), Enemy):
                # Handle it within the player class (enemies)
                    if self.player.running and (type(n) == Enemy):
                        if not n.frozen:
                            n.freeze()
                    self.player.handleCollision(n)
                else:
                    self.player.handleCollision(n)

            #Enemies
            if issubclass(type(n),Enemy):
                if self.projectiles:
                    for p in self.projectiles:
                        self.projectileCollision(p,n)
                        
            
    
    def pushableBlockCollision(self):
        if self.pushableBlocks:
            for block in self.pushableBlocks:
                if self.player.doesCollide(block):
                    self.player.handleCollision(block)

                for b in self.blocks:
                    if block.doesCollide(b):
                        block.reset()


                for s in self.spawning:
                    if block.doesCollide(s):
                        block.reset()

                for n in self.npcs:
                    if block.doesCollide(n):
                        block.reset()
                
            #Press a switch if the block is on it
            switchIndex = block.doesCollideList(self.switches)
            if switchIndex != -1:
                if type(self.switches[switchIndex]) == WeightedSwitch:
                    self.switches[switchIndex].press(block)
                else:
                    self.switches[switchIndex].press()
            #elif *Other possible conditions for block collision could go here. (Walls)
            else:
                pass
        
                
    def interactableCollision(self):
        if self.spawning:
            for n in self.spawning: 
                for p in self.projectiles:
                    self.projectileCollision(p, n)
                if self.player.doesCollide(n):
                    if type(n) == Key:
                        self.disappear(n)
                        n.interact(self.player, self)
                    elif issubclass(type(n), Drop):
                        self.disappear(n)
                        n.interact(self.player)
                    else:
                        self.player.handleCollision(n)
    
    #abstract
    def blockCollision(self):
        """
        Abstract method
        """
        pass
    
    def projectileCollision(self, projectile, other):
        if projectile.doesCollide(other):
            if issubclass(type(other),Enemy):
                other.handleCollision(projectile)
                if type(projectile) == Bullet:
                    self.disappear(projectile)
                    self.player.shooting = False
            elif type(projectile) == Bullet:
                self.playSound("OOT_DekuSeed_Hit.wav")
                self.disappear(projectile)
                self.player.shooting = False
            

    def handleCollision(self):
        #self.projectileCollision()
        self.npcCollision()
        self.blockCollision()
        self.interactableCollision()
        self.pressSwitches()
        self.pushableBlockCollision()
        #Call super().handleCollision()
        #Then self.spawn/despawn however you want
    
    """
    Update methods
    """
    def updateNpcs(self, seconds):
        ##Enemies
        for n in self.npcs:
            if type(n) == Enemy:
                n.update(seconds)
                if n.dead:
                    self.playSound("enemydies.wav")
                    self.disappear((n))
                    if self.player.hp < self.player.max_hp:
                        self.spawning.append(n.getDrop())
                    self.enemyCounter += 1
            
        
        if not self.ignoreClear and not self.room_clear and self.enemyCounter == self.max_enemies:
            self.playSound("room_clear.mp3")
            self.room_clear = True
    
    #Most likely to be modified for cutscenes
    def updateSpawning(self, seconds):
        ##  NPCs
        for n in self.spawning:
            if n.animate:
                n.update(seconds)
                
    def updatePlayer(self, seconds):
        if self.player.hp <= 0:
            #DIE
            pygame.quit()
        self.player.update(seconds)
    
    #abstract
    def updateSwitches(self, seconds):
        """
        Abstract method
        """
        pass

    def updateProjectiles(self, seconds):
        for p in self.projectiles:
            p.update(seconds)
            if (type(p) == Sword or type(p) == Clap) and p.timer >= p.lifetime:
                self.disappear(p)
                self.player.unlockPosition()
    
    def updatePushableBlocks(self,seconds):
        if self.pushableBlocks:
            for block in self.pushableBlocks:
                block.update(seconds, self.player, self.player.row)
                
    #abstract
    def handleClear(self):
        """
        Update the game once all enemies in the
        room are defeated.
        """
        pass

    def update(self, seconds):
        
        if self.fading:
            self.black.update(seconds)
            if self.transporting and self.black.frame == 8:

                """
                Transition here!
                """
                self.readyToTransition = True
                
            return

            

        self.updatePlayer(seconds)
        self.updateNpcs(seconds)
        self.updateSpawning(seconds)
        self.updatePushableBlocks(seconds)
        self.updateSwitches(seconds)
        self.updateProjectiles(seconds)
        if not self.ignoreClear:
            
            if self.room_clear and self.clearFlag == 0:
                self.clearFlag = 1
                self.handleClear()
        Drawable.updateOffset(self.player, self.size)
    
    """
    Draw Methods
    """
    def drawNpcs(self, drawSurface):
        if self.npcs:
            for n in self.npcs:
            #Consider making enemies appear right before the player
                if type(n) == Enemy:
                    n.draw(drawSurface)
                else:
                    n.draw(drawSurface)
        
        if self.spawning:
            for n in self.spawning:
                n.draw(drawSurface)
    
    def drawProjectiles(self, drawSurface):
        #Projectiles/weapons
        if self.projectiles:
            for p in self.projectiles:
                if type(p) == Sword or type(p) == Clap:
                    p.draw(drawSurface, True)
                #elif type(p) == Cleats:
                    #pygame.draw.rect(drawSurface, (50,255,50), self.player.getTackleRect(), 1)
                else:
                    p.draw(drawSurface)

    def drawFlash(self, drawSurface):
        self.flashes -= 1
        Drawable((0,0), "white.png").draw(drawSurface)

    def drawBlocks(self, drawSurface):
        for block in self.blocks:
            block.draw(drawSurface)

    def drawPushable(self, drawSurface):
        if self.pushableBlocks:
            for block in self.pushableBlocks:
                block.draw(drawSurface)

    def drawSwitches(self, drawSurface):
        for switch in self.switches:
            switch.draw(drawSurface)

    def drawHud(self, drawSurface):
        self.keyCount.draw(drawSurface)
        self.keyNumber = Drawable((33, self.keyCount.position[1]), "numbers.png", (self.player.keys,0))
        self.keyNumber.draw(drawSurface)
        self.healthBar.draw(drawSurface, self.player)


        self.ammoBar.draw(drawSurface, self.player)
        """ Text((1,16), "Ammo", (200,200,200)).draw(drawSurface)
        if self.player.ammo == self.player.max_ammo:
            Text((28,16), str(self.player.ammo), (0,220,0)).draw(drawSurface)
        elif self.player.ammo == 0:
            Text((28,16), str(0), (200,0,0)).draw(drawSurface)
        else:
            Text((28,16), str(self.player.ammo), (200,200,200)).draw(drawSurface) """

    def drawFade(self, drawSurface):
        self.black.draw(drawSurface)

    def draw(self, drawSurface):
        """
        Draw the objects on the drawSurface after updating them
        """
    

        if self.flashes > 0:
            self.drawFlash(drawSurface)
            return
        
        #Background
        self.background.draw(drawSurface)
        
        #Blocks
        self.drawBlocks(drawSurface)
        
        #Switches
        self.drawSwitches(drawSurface)

        #Projectiles
        self.drawProjectiles(drawSurface)
        #Npcs
        self.drawNpcs(drawSurface)

        #Pushable blocks
        self.drawPushable(drawSurface)
        
        #Player
        self.player.draw(drawSurface)

        #HUD
        self.drawHud(drawSurface)
        
        #Fade
        if self.fading:
            self.drawFade(drawSurface)


class AbstractEngine(object):
    """
    Abstract engine class for each room.
    """
    _INSTANCE = None
    
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._AE()
      
        return cls._INSTANCE

    @classmethod
    def tearDown(cls):
        if cls._INSTANCE != None:
            cls._INSTANCE = None
        return None
    
    class _AE(AE):
        def __init__(self, player = None):
            super().__init__(player)