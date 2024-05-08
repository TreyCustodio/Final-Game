import pygame

from UI import EventManager
from . import (Drawable, Slash, Blizzard, HealthBar, ElementIcon, EnergyBar, Blessing, Torch, AmmoBar, Fade, Drop, Heart, Text, Player, Enemy, NonPlayer, Sign, Chest, Key, Geemer, Switch, 
               WeightedSwitch, DamageIndicator, LightSwitch, TimedSwitch, LockedSwitch, Block, IBlock, Trigger, HBlock,
               PushableBlock, LockBlock, Bullet, Sword, Clap, Slash, Flapper, Number,
               Tile, Portal, Buck, Map)




from utils import SoundManager, vec, RESOLUTION, SPEECH, ICON, INV, COORD, FLAGS, EQUIPPED, UPSCALED
class DamageNumberManager(object):
    def __init__(self):
        self.numbers = []
        
    def addNumber(self, position, value):
        self.numbers.append(DamageNumber(position, value))
    
    def draw(self, engine, drawSurface):
        for num in self.numbers:
            engine.drawNumber(num.damagePos, num.damage, drawSurface, row = 3)
    
    
    def updateNumbers(self, engine, seconds):
        for num in self.numbers:
            num.damagePos[1] -= 20 * seconds
            if num.damagePos[1] <= num.maxDamagePos:
                self.numbers.pop(self.numbers.index(num))


class DamageNumber(object):
    def __init__(self, position, damage):
        self.damage = damage
        self.damagePos = position
        self.maxDamagePos = self.damagePos[1]-8


class AE(object):
    def __init__(self):
        """
        __init__ is only ever called once
        """
        self.healthBarDrawn = False

        self.area = 0
        self.roomId = 0
        self.itemsToCollect = 0
        self.mapCondition = False #True if pink, False if green


        self.damageNums = DamageNumberManager()
        self.player = None
        self.resetting = False
        self.ignoreClear = False
        self.dropCount = 0
        self.pause_lock = False

        #Death
        self.dead = False
        self.dying = False
        self.deathTimer = 0

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
        self.largeText = False
        self.icon = None
        self.boxPos = vec(30,64)
        self.promptResult = False
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
        self.torches = []
        self.doors = []
        self.tiles = []
        self.drops = []
        self.indicator = DamageIndicator()
        self.moneyImage = Drawable((0, 16*10+6), fileName="Objects.png", offset= (0,6))
        
        

        #Size of the room
        self.size = vec(*RESOLUTION)
        #HUD
        

        #self.transparentSurf = pygame.Surface(RESOLUTION)
        #self.transparentSurf.set_alpha(200)
        self.keyCount = Drawable((0, RESOLUTION[1]-16), "KeyCount.png")
        self.healthBar = HealthBar.getInstance()
        self.ammoBar = AmmoBar()
        self.elementIcon = ElementIcon()
        self.energyBar = EnergyBar()
        #Unique room elements:
        #self.max_enemies
        #self.enemyPlacement
        #self.bgm
    

    """
    Auxilary methods
    """
    def reset(self):
        self.promptResult = False
        self.indicator.setImage(0)
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
        self.dropCount = 0


    def deathReset(self):
        self.enemyCounter
        self.promptResult = False
        self.boxPos = vec(30,64)
        self.player = None
        self.pause_lock = False
        self.dead = False
        self.dying = False
        self.deathTimer = 0
        self.indicator.setImage(0)
        self.readyToTransition = False
        self.transporting = False
        self.tra_room = None
        self.tra_pos = None
        self.tra_keepBGM = False
        self.fading = False

        if self.spawning:
            for i in range (len(self.spawning)-1, -1, -1):
                if issubclass(type(self.spawning[i]), Drop):
                    self.disappear(self.spawning[i])
        self.dropCount = 0

        


    def initializeRoom(self, player= None, pos = None, keepBGM = False):
        """
        Called every time you enter the room
        1. create wall boundaries
        2. adjust wall collision for doors in self.doors
        3. call createBlocks
        4. place the enemies in self.enemies
        """
        EventManager.getInstance().toggleFetching()
        #SoundManager.getInstance().stopAllSFX()
        EQUIPPED["room"] = self.roomId
        if player != None:
            self.player = player
            self.player.position = pos 
        else:
            self.player = Player(vec(16*9, (16*11) - 8))
    
        #if pos != None:
        
            #self.player.position = (pos + self.player.vel)
        

        self.black.reset()
        self.createBounds()
        self.setDoors()
        self.createBlocks()
        self.placeEnemies(self.enemies)
        if not keepBGM:
            #SoundManager.getInstance().fadeoutBGM()
            if self.bgm != None:
                SoundManager.getInstance().playBGM(self.bgm)
        self.fading = False
        self.player.keyDownUnlock()
        self.player.keyUnlock()



    def createBounds(self):
        """
        Creates boundaries on the outer edge of the map
        """
        #Left side
        for i in range(1, 5):
            self.blocks.append(IBlock((8,i*16)))
        for i in range(8, 12):
            self.blocks.append(IBlock((8,i*16)))
        #Right side
        for i in range(1, 5):
            self.blocks.append(IBlock((RESOLUTION[0]-24,i*16)))
        for i in range(8, 12):
            self.blocks.append(IBlock((RESOLUTION[0]-24,i*16)))
        #Top side
        for i in range(1,8):
            self.blocks.append(IBlock((i*16, 0)))
        for i in range(11, 18):
            self.blocks.append(IBlock((i*16, 0)))
        #Bottom side
        for i in range(1,8):
            self.blocks.append(IBlock((i*16, RESOLUTION[1]-16)))
        for i in range(11, 18):
            self.blocks.append(IBlock((i*16, RESOLUTION[1]-16)))
    

    def setDoors(self):
        """
        Adjust the boundaries to fit doors
        """
        if 0 not in self.doors:
            self.blocks.append(IBlock((8*16, RESOLUTION[1]-16)))
            self.blocks.append(IBlock((9*16, RESOLUTION[1]-16)))
            self.blocks.append(IBlock((10*16, RESOLUTION[1]-16)))
        else:
            self.blocks.append(IBlock((16*8-8, RESOLUTION[1]-16)))
            self.blocks.append(IBlock((16*10+8, RESOLUTION[1]-16)))
        
        if 1 not in self.doors:        
            self.blocks.append(IBlock((RESOLUTION[0]-24, 5*16)))
            self.blocks.append(IBlock((RESOLUTION[0]-24, 6*16)))
            self.blocks.append(IBlock((RESOLUTION[0]-24, 7*16)))
        else:
            self.blocks.append(IBlock((RESOLUTION[0]-24, 16*7+8)))
            self.blocks.append(IBlock((RESOLUTION[0]-24, 16*5-8)))
        if 2 not in self.doors:   
            self.blocks.append(IBlock((8*16, 0)))
            self.blocks.append(IBlock((9*16, 0)))
            self.blocks.append(IBlock((10*16, 0)))
        else:
            self.blocks.append(IBlock((8*16-8, 0)))
            self.blocks.append(IBlock((16*10+8, 0)))
        if 3 not in self.doors:
            self.blocks.append(IBlock((8, 5*16)))
            self.blocks.append(IBlock((8, 6*16)))
            self.blocks.append(IBlock((8, 7*16)))
            
        else:
            self.blocks.append(IBlock((8, 16*7+8)))
            self.blocks.append(IBlock((8, 16*5-8)))
    
    #abstract
    def createBlocks(self):
        """
        Abstract method
        """
        pass

    def placeEnemies(self, enemyLst):
        """
        Place the enemies according to a predetermined algorithm.
        The algorithm is selected based on the integer corresponding to
        self.enemyPlacement
        """
        self.enemyCounter = 0
        def refresh():
            for e in enemyLst:
                """ if e not in self.npcs:
                    if e.dead: """
                if e not in self.npcs:
                    self.npcs.append(e)
                e.respawn()
    
        if self.enemyPlacement > 0:
            if self.enemyPlacement == 1:
                """
                Four in the center
                """
                enemyLst[0].position = COORD[6][3]
                enemyLst[1].position = COORD[11][3]
                enemyLst[2].position = COORD[6][7]
                enemyLst[3].position = COORD[11][7]
                refresh()

            elif self.enemyPlacement == 2:
                """
                """
                
                enemyLst[0].position = COORD[6][3]
                enemyLst[1].position = COORD[11][3]
                enemyLst[2].position = COORD[6][7]
                enemyLst[3].position = COORD[11][7]

                enemyLst[4].position = COORD[14][3]
                enemyLst[5].position = COORD[3][3]
                enemyLst[6].position = COORD[14][7]
                enemyLst[7].position = COORD[3][7]
                refresh()
        else:
            for i in range(self.max_enemies):
                enemyLst[i].position = enemyLst[i].initialPos
            refresh()
            """ for e in enemyLst:
                if not e.dead and e not in self.npcs:
                    self.npcs.append(e)
                if not e.frozen:
                    e.freeze(playSound=False)
                    e.freezeTimer = 4.0 """
                

                    

    def fade(self):
        self.player.keyLock()
        self.fading = True

    def transport(self, room=None, position=None, keepBGM = False, intro = False):
        """
        Transport the player to a different room.
        room -> room (class) name in majestus.py
        position -> 0-3 representing cardinal direction, or a specific coordinate
        keepBgm -> keeps the bgm
        intro -> special properties for transport because no player yet
        """
        EventManager.getInstance().startTransition()
        if intro:
            self.transporting = True
            self.tra_room = room.getInstance()
            return
        
        self.player.keyDownLock()
        self.fade()
        self.transporting = True
        self.tra_room = room.getInstance()
        if position == 0:
            self.tra_pos = vec(16*9, 16*11)
        elif position == 1:
            self.tra_pos = vec(16*16, 16*6 - 8)
        elif position == 2:
            self.tra_pos = vec(16*9, 8)
        elif position == 3:
            self.tra_pos = vec(16*2, 16*6-8)
        else:
            self.tra_pos = position
            
        self.tra_keepBGM = keepBGM
        if not keepBGM:
            SoundManager.getInstance().fadeoutBGM()
        
        pygame.event.clear()

        
    def displayText(self, text = "", icon = None, large = True):
        """
        Display text
        """
        self.textBox = True
        self.text = text
        self.largeText = large
        if icon != None:
            self.icon = icon
        if self.player != None:
            self.player.stop()
    
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

        #Flames
        if self.player.sword != None:
            self.projectiles.append(self.player.getFlame())
            self.playSound(self.player.swordSound)
            self.player.sword = None
        
        #Thunder clap
        if self.player.clap != None:
            self.projectiles.append(self.player.getClap())
            self.playSound(Clap.SOUND)
            self.player.clap = None
        
        #Gale slash
        if self.player.slash != None:
            self.projectiles.append(self.player.getSlash())
            self.playSound("plasma_shot.wav")
            self.player.slash = None
        
        #Blizzard
        if self.player.blizzard != None and self.player.blizzard not in self.projectiles:
            self.projectiles.append(self.player.getBlizzard())
            #self.playSound("")

        if self.player.hook != None:
            self.projectiles.append(self.player.getHook())
            self.player.hook = None

    def interactableEvents(self, event):
        """
        Handles interaction from the player
        """
        if self.spawning:
            for n in self.spawning:
                if not n.drop and self.player.interactable(n):
                    self.player.handleEvent(event, n, self)
                    return
                
        self.player.handleEvent(event)

    def interactableEvents_C(self, event):
        if self.spawning:
            for n in self.spawning:
                if not n.drop and self.player.interactable(n):
                    self.player.handleEvent_C(event, n, self)
                    return
                
        self.player.handleEvent_C(event)


    def handleEvent(self, event):
        self.interactableEvents(event)
    
    def handleEvent_C(self, event):
        self.interactableEvents_C(event)
    
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
                    if self.player.running:
                        if not n.freezeShield and not n.frozen:
                            self.player.stop()
                            n.freeze()

                    if not n.frozen:
                        if not self.player.invincible:
                            if n.handlePlayerCollision(self.player):
                                self.player.handleCollision(n)
                                #player should be invincible now
                                if self.player.invincible and not self.healthBar.drawingHurt:
                                    self.healthBar.drawHurt(self.player.hp, n.damage)
                else:
                    self.player.handleCollision(n)

            #Enemies
            if issubclass(type(n),Enemy):
                if self.projectiles:
                    for p in self.projectiles:
                        self.projectilesOnEnemies(p,n)
                        
    def pushableBlockCollision(self):
        if self.pushableBlocks:
            for block in self.pushableBlocks:
                self.projectilesOnBlocks(block)
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
    
    def enemyCollision(self, other):
        for e in self.npcs:
            if e.doesCollideBlock(other):
                e.bounce(other)

    def interactableCollision(self):
        if self.spawning:
            for n in self.spawning: 
                if not issubclass(type(n), Drop):
                    for p in self.projectiles:
                        self.projectilesOnSpawning(p, n)
                    self.enemyCollision(n)

                if self.player.doesCollide(n):
                    if type(n) == Key:
                        self.disappear(n)
                        n.interact(self.player, self)
                    elif issubclass(type(n), Drop):
                        self.disappear(n)
                        self.dropCount -= 1
                        n.interact(self.player)
                    else:
                        self.player.handleCollision(n)
    
    
    #Add self.enemyCollision(block)
    #Add self.projectilesOnBlocks(block)
    #abstract
    def blockCollision(self):
        """
        Abstract method
        """
        pass
    
    def projectilesOnEnemies(self, projectile, other):
        if other.doesCollideProjectile(projectile):
            if not projectile.hit:
                other.handleCollision(projectile)
                if other.hit:
                    ##Display the damage indicator
                    hp_after = other.hp
                    hp_before = other.hp + projectile.damage
                    self.indicator.setImage(other.indicatorRow, hp_before, hp_after, other.maxHp, projectile.damage)

                    ##Display damage numbers appropriately
                    if projectile.id == "slash" or projectile.id == "blizz":
                        self.damageNums.addNumber(vec(projectile.position[0]+8, projectile.position[1]), projectile.damage)
                    else:
                        self.damageNums.addNumber(vec(projectile.position[0], projectile.position[1]), projectile.damage)
                    other.hit = False
                projectile.handleCollision(self)
                
                
               


    def projectilesOnSpawning(self, projectile, other):
        if projectile.doesCollide(other):
            if not projectile.hit:
                projectile.handleCollision(self)

    """ def projectileCollision(self, projectile, other):
        if other.doesCollideProjectile(projectile):
            other.handleCollision(projectile)
            self.indicator.setImage(other.indicatorRow, other.hp, other.maxHp)
            projectile.handleCollision(self) 


         if issubclass(type(other),Enemy):
            if other.doesCollideProjectile(projectile):
                other.handleCollision(projectile)
                self.indicator.setImage(other.indicatorRow, other.hp, other.maxHp)
                projectile.handleCollision(self)
                

        elif projectile.doesCollide(other):
            if type(projectile) == Bullet:
                self.playSound("OOT_DekuSeed_Hit.wav")
                self.disappear(projectile)
                self.player.arrowCount += 1
                self.player.shooting = False """
            

    def projectilesOnBlocks(self, block):
        for p in self.projectiles:
            if not p.hit:
                if p.doesCollide(block):
                #p.handleCollision(self)
                    p.handleCollision(self)
    
    def projectilesOnTorches(self, torch):
        for p in self.projectiles:
            if p.type == 1 and p.doesCollide(torch):
                torch.light()


    def handleCollision(self):
        #self.projectileCollision()
        self.npcCollision()
        if not self.dying:
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
            #if issubclass(type(n), Enemy):
            n.update(seconds)
            if n.dead:
                self.playSound("enemydies.wav")
                self.disappear((n))
                if self.dropCount < 5:
                    if self.player.hp == INV["max_hp"]:
                        drop = n.getMoney()
                        if drop != None:
                            self.spawning.append(drop)
                    else:
                        drop = n.getDrop()
                        
                        if drop != None:
                            self.spawning.append(drop)
                    self.dropCount += 1
                self.enemyCounter += 1
            
        
        if not self.ignoreClear and not self.room_clear and self.enemyCounter == self.max_enemies:
            self.playSound("room_clear.mp3")
            self.room_clear = True
    
    #Most likely to be modified for cutscenes
    def updateSpawning(self, seconds):
        

        ##  NPCs
        for n in self.spawning:
            n.update(seconds)
            if n.disappear:
                self.disappear(n)
                self.dropCount -= 1
          
    

    def updatePlayer(self, seconds):
        if self.player.dying:
            self.player.update(seconds)
            if self.player.headingOut:
                self.boxPos = vec(32,RESOLUTION[1]-74)
                
                self.displayText("Aight, Imma head out.&&")
                self.player.headingOut = False
                self.player.walking = True
                self.player.vel[1] = 0
                self.player.vel[0] = self.player.speed
                
                
        elif self.player.hp <= 0:
            
            #DIE
            self.player.die()
            self.pause_lock = True
            self.dying = True
            SoundManager.getInstance().fadeoutBGM()
            self.player.update(seconds)
            #pygame.quit()
        
        else:
            self.player.update(seconds)
    
    #abstract
    def updateSwitches(self, seconds):
        """
        Abstract method
        """
        pass

    def updateProjectiles(self, seconds):
        for p in self.projectiles:
            p.update(seconds, self)

            
            """ if type(p) == Clap:
                if p.frame == 4:
                    self.disappear(p)
            elif type(p) == Slash:
                if (p.position[0] <= 0 or p.position[0] >= RESOLUTION[0]) or (p.position[1] <= 0 or p.position[1] >= RESOLUTION[1]):
                    self.disappear(p)
            elif (type(p) == Sword) and p.frame == 4: #and p.timer >= p.lifetime:
                self.disappear(p)
            elif type(p) == Blizzard and not self.player.freezing:
                self.disappear(p)
                #self.player.unlockPosition() 
            """
    
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
    
    def updateHUD(self, seconds):
        self.indicator.update(seconds)
        self.damageNums.updateNumbers(self, seconds)
        self.healthBar.update(seconds)
        

    def handlePrompt(self):
        pass


    def update(self, seconds):

        if not self.mapCondition:
            if self.itemsToCollect == 0:
                self.mapCondition = True
           
                Map.getInstance().rooms[self.area][self.roomId].clearRoom()
                
        if not FLAGS[20] and INV["flameShard"] > 0:
            FLAGS[20] = True
            self.displayText(SPEECH["flameShard"])
            
        if self.promptResult:
            self.handlePrompt()
        if self.dying:
            
            self.updatePlayer(seconds)
            if self.player.dead:
                self.deathTimer += seconds
                if self.deathTimer >= 2:
                    self.dead = True
                



        if self.fading:
            self.black.update(seconds)
            if self.transporting and self.black.frame == 8:
                """
                Transition here!
                """
                self.readyToTransition = True
                
            return

            
        if self.torches:
            for t in self.torches:
                t.update(seconds)
        self.updatePlayer(seconds)
        self.updateNpcs(seconds)
        self.updateSpawning(seconds)
        self.updatePushableBlocks(seconds)
        self.updateSwitches(seconds)
        self.updateProjectiles(seconds)
        self.updateHUD(seconds)
        if self.tiles:
            for t in self.tiles:
                t.update(seconds)
        if not self.ignoreClear:
            if self.room_clear and self.clearFlag == 0:
                self.clearFlag = 1
                self.handleClear()
        
        Drawable.updateOffset(self.player, self.size)
    

    """
    Draw Methods
    """
    def drawNpcs(self, drawSurface):
        if self.spawning:
            for n in self.spawning:
                if self.player.interactable(n):
                    n.setInteractable()
                else:
                    if n.interactable:
                        n.interactable = False
                n.draw(drawSurface)

        if self.torches:
            for n in self.torches:
                if not n.lit and self.player.interactable(n):
                    n.setInteractable()
                elif n.interactable:
                    n.interactable = False

        if self.npcs:
            for n in self.npcs:
            #Consider making enemies appear right before the player
                if issubclass(type(n), Enemy):
                    n.draw(drawSurface)
                else:
                    n.draw(drawSurface)
        
        
        
    
    def drawProjectiles(self, drawSurface):
        #Projectiles/weapons
        if self.projectiles:
            for p in self.projectiles:
                p.draw(drawSurface)
                """ if type(p) == Sword or type(p) == Clap:
                    p.draw(drawSurface, True)
                
                else:   
                    p.draw(drawSurface) """

    def drawFlash(self, drawSurface):
        self.flashes -= 1
        Drawable((0,0), "white.png").draw(drawSurface)

    def drawBlocks(self, drawSurface):
        for block in self.blocks:
            block.draw(drawSurface)
        if self.torches:
            for torch in self.torches:
                torch.draw(drawSurface)

    def drawPushable(self, drawSurface):
        if self.pushableBlocks:
            for block in self.pushableBlocks:
                block.draw(drawSurface)

    def drawSwitches(self, drawSurface):
        for switch in self.switches:
            switch.draw(drawSurface)

    def drawDamage(self, drawSurface):
        self.damageNums.draw(self, drawSurface)
        
        
    def drawHud(self, drawSurface):
        
        self.moneyImage.draw(drawSurface)

        
        Number((16, 16*10+4), row = 1).draw(drawSurface)
        if INV["money"] == INV["wallet"]:
            self.drawNumber(vec(28, 16*10+4), INV["money"], drawSurface, row = 2)
        else:
            self.drawNumber(vec(28, 16*10+4), INV["money"], drawSurface)
            #Number((28, 16*10+4), INV["money"]).draw(drawSurface)


        self.keyCount.draw(drawSurface)
        Number((28, self.keyCount.position[1]), self.player.keys).draw(drawSurface)
        if self.healthBar.drawn:
            self.healthBar.draw(drawSurface, self.player)
        else:
            self.healthBar.drawFirst(drawSurface, self.player)
        
        self.ammoBar.draw(drawSurface, self.player)
        self.elementIcon.draw(drawSurface)
        self.indicator.draw(drawSurface)
        self.drawNumber(vec(0,0), self.player.hp, drawSurface)
        self.drawDamage(drawSurface)

        

        if EQUIPPED["C"] == 2:
            self.energyBar.drawThunder(self.player.clapTimer, drawSurface)

        elif EQUIPPED["C"] == 3:
            
            self.energyBar.drawWind(self.player.chargeTimer, drawSurface)
        else:
            self.energyBar.draw(drawSurface)
        
        if self.player.drunk:
            self.drawNumber(vec(0,64), int(self.player.drunkTimer), drawSurface, row = 3)
        #pygame.transform.scale(self.transparentSurf,
                               #list(map(int, UPSCALED)),
                               #self.transparentScreen)
        
        #self.keyCount.draw(self.transparentSurf)
        
        #if wind selected
        

        """ Text((1,16), "Ammo", (200,200,200)).draw(drawSurface)
        if self.player.ammo == self.player.max_ammo:
            Text((28,16), str(self.player.ammo), (0,220,0)).draw(drawSurface)
        elif self.player.ammo == 0:
            Text((28,16), str(0), (200,0,0)).draw(drawSurface)
        else:
            Text((28,16), str(self.player.ammo), (200,200,200)).draw(drawSurface) """

    def drawFade(self, drawSurface):
        self.black.draw(drawSurface)

    def drawTiles(self, drawSurface):
        if self.tiles:
            for t in self.tiles:
                t.draw(drawSurface)


    def drawNumber(self, position, number, drawSurface, row = 0):
        if number >= 10:
            currentPos = vec(position[0]-3, position[1])
            number = str(number)
            for char in number:
                Number(currentPos, int(char), row).draw(drawSurface)
                currentPos[0] += 6
        else:
            Number(position, number, row).draw(drawSurface)


    def draw(self, drawSurface):
        """
        Draw the objects on the drawSurface after updating them
        """
    
        if self.dying:
            Drawable(fileName="b.png").draw(drawSurface)
            self.player.draw(drawSurface)
            return
        
        if self.flashes > 0:
            self.drawFlash(drawSurface)
            return
        
        #Background/Tiles
        
        self.background.draw(drawSurface)
        self.drawTiles(drawSurface)
        
        #Blocks
        self.drawBlocks(drawSurface)

        #Switches
        self.drawSwitches(drawSurface)

        #Projectiles
        
        #Npcs
        self.drawNpcs(drawSurface)

        #Pushable blocks
        self.drawPushable(drawSurface)
        
        self.drawProjectiles(drawSurface)
        #Player
        self.player.draw(drawSurface)

        #HUD
        self.drawHud(drawSurface)
        
        #Fade
        if self.fading:
            self.drawFade(drawSurface)

        self.weaponControl()

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