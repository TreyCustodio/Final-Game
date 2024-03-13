from . import Block
from utils import vec, SpriteManager
import pygame

"""
This file contains unique types of blocks.
All of them inherit from the Block class
"""
class LockBlock(Block):
    """
    Requires a key to unlock -> handled in engine
    """
    def __init__(self, position=vec(0,0)):
        super().__init__(position, (4,4))

class BreakableBlock(Block):
    """
    A block that can be broken by the player
    """
    def __init__(self, position=vec(0,0)):
        super().__init__(position, (4,1))
        self.broken = False
    
    def brake(self):
        self.broken = True

class PushableBlock(Block):
    """
    A block that can be pushed by the player
    """
    def __init__(self, position=vec(0,0), heavy=False):
        super().__init__(position, (5,1))
        self.vel = vec(0,0)
        self.heavy = heavy
        self.pushing = False
    
    def push(self, player):
        if self.heavy:
            pass
        else:
            self.pushing = True
            player.lockDirection()
    
    def update(self, seconds, player, direction):
        # (0 down), (2 up)
        # (1 right), (3 left)
        if self.pushing:
            player.pushing = True
            if direction == 0:
                self.vel = vec(0, player.getSpeed())
            elif direction == 2:
                self.vel = vec(0, -player.getSpeed())
            elif direction == 1:
                self.vel = vec(player.getSpeed(), 0)
            else:
                self.vel = vec(-player.getSpeed(), 0)

            
            self.position += self.vel * (seconds)
            self.pushing = False
            self.vel = (0,0)
        elif player.pushing == True:
            player.pushing = False
