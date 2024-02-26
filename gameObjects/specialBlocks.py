from . import Block
from utils import vec, SpriteManager
import pygame

"""
This file contains unique types of blocks.
All of them inherit from the Block class
"""
class PushableBlock(Block):
    def __init__(self, position=vec(0,0), heavy=False):
        super().__init__(position, (4,1))
        self.vel = vec(0,0)
        self.heavy = heavy
        self.pushing = False
    
    def push(self):
        if self.heavy:
            pass
        else:
            self.pushing = True
    
    def update(self, seconds, player, direction):
        # (0 down), (2 up)
        # (1 right), (3 left)
        if self.pushing:
            player.set_Sprite(1)
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
        else:
            player.set_Sprite(0)
