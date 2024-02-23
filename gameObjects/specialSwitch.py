from . import Switch
from utils import vec, SpriteManager
import pygame
"""
This file contains unique types of switches.
Every class inherits the Switch class or a
subclass of the Switch class.
"""



class WeightedSwitch(Switch):
    """
    Weighted switches must be weighed down by 
    a block in order to remain pressed.
    """
    def __init__(self, position=vec(0,0)):
        super().__init__(position, False)
        ##  Always initialize pressed as false for weighted switches.
        ##  If a weighted switch needs to be initialized
        ##  as pressed, then a block will already be initialized on it
        ##  This might happen in a link to the past. You'll hear the clicking
        ##  noise when you enter a room that has a block on a switch.
    
    def set_sprite(self):
        if self.pressed: 
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (3,1))
        else:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (2,1))

    
    def update(self, block):
        #   Unpress if no block on top
        #   Maybe craft an array of blocks,
        #   loop through, and check if it collides with any
        if self.doesCollide(block) == False:
            self.pressed = False
            self.set_sprite()


class LockedSwitch(WeightedSwitch):
    def __init__(self, position=vec(0,0)):
        super().__init__(position)
        self.locked = True
        self.remain_unlocked = False

    
    def set_sprite(self):
        if self.pressed: 
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (3,4))
        else:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (2,4))

    def press(self):
        """
        Activate the switch if it is unlocked
        """
        if not self.locked:
            super().press()
    
    def unLock(self, remain_unlocked = False):
        self.locked = False
        if remain_unlocked:
            self.remain_unlocked = True

    
    def lock(self):
        if not self.remain_unlocked:
            self.locked = True

    def changeLock(self):
        """
        Once the lock trigger is activated in collision,
        unlock the switch if its locked
        or lock the switch if its unlocked
        """
        self.locked = not self.locked
    
    def update(self):
        if self.locked and self.pressed:
            self.pressed = False
            self.set_sprite()







class LightSwitch(Switch):
    """
    These switches must be weighed down by either the
    player or a block in order to remain pressed.
    """
    def __init__(self, position=vec(0,0)):
        super().__init__(position)
    

    def set_sprite(self):
        if self.pressed:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (3,2))
        else:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (2,2))
    
    def reset(self):
        self.pressed = False
        self.set_sprite()
    
    def update(self, player, object):
        if (not self.doesCollide(player)) and (not self.doesCollide(object)):
            self.reset()
    









class TimedSwitch(LightSwitch):
    """
    Once pressed, these switches will
    deactivate after a certain time.
    Default time is 5 seconds.
    """
    def __init__(self, position=vec(0,0), time=5):
        super().__init__(position)
        self.time = time
        self.timer = 0
    
    def set_sprite(self):
        if self.pressed:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (3,3))
        else:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (2,3))
    
    #Basic framework for timed devices
    def update(self, seconds):
        if self.pressed:
            #Increment the timer
            self.timer += seconds
            if self.timer >= self.time:
                self.reset()
                self.timer = 0
    
