from . import Drawable
from utils import vec, rectAdd, SpriteManager
import pygame

"""
Blocks are static, 16x16, cube-shaped objects
that impede the player's movement.
"""
class Block(Drawable):
    def __init__(self, position=vec(0,0), offset = (5,0)):
        super().__init__(position, "Objects.png", offset)
        self.width = 16
        self.height = 16
        
    
    """ def appear(self):
        self.spawned = True
    
    def disappear(self):
        self.spawned = False """
        
    def update(self, player):
        if player.pushing == True:
            player.pushing = False

class IBlock(Block):
    """
    Invisible blocks, no need to pass in an offset
    """
    def __init__(self, position = vec(0,0)):
        super().__init__(position, (0,0))



class HBlock(Block):
    """
    Half a block (8 x 16 pixels) of collision.
    The block will be placed within a 16 x 16 space.
    If right, the collision will appear on the right.
    If left, the collision will appear on the left."""
    def __init__(self, position = vec(0,0), right = False):
        super().__init__(position, (0,0))
        self.width = 8
        self.right = right
        
    def getCollisionRect(self):
        newRect = pygame.Rect((0,0),(8,16))
        if self.right:
            newRect.left = int(self.position[0]+8)
        else:
            newRect.left = int(self.position[0])
        newRect.top = int(self.position[1])
        return newRect
    
class Trigger(IBlock):
    """
    Colliding with this invisible trigger will
    Cause text to be displayed
    """
    def __init__(self, position = vec(0,0), text="", door = -1):
        if door == 0:
            super().__init__((16*9, (16*12 + 8)))
        elif door == 2:
            super().__init__((16*9, (-6)))
        else:
            super().__init__(position)

        self.text = text
    
    def interact(self, player, engine):
        engine.displayText(self.text)
        player.vel = vec(0,0)