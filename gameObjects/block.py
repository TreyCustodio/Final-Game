from . import Drawable, Animated
from utils import vec, RESOLUTION, COORD, rectAdd, SpriteManager
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
    Invisible blocks
    """
    def __init__(self, position = vec(0,0), offset = (0,0)):
        super().__init__(position, offset)



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
        elif door == 3:
            super().__init__((0, 6*16))
            
        elif door == 2:
            super().__init__((16*9, (-6)))

        elif door == 1:
            super().__init__((RESOLUTION[0]-16, 6*16))

        elif door == 5:
            super().__init__(position, (1,0))
        else:
            super().__init__(position)
        
        self.door = door
        self.text = text
    
    def getCollisionRect(self):
        if self.door == 0 or self.door == 2:
            return pygame.Rect((self.position[0]-8, self.position[1]), (32, 16))
        elif self.door == 1 or self.door == 3:
            return pygame.Rect((self.position[0],self.position[1]-8), (16,32))
        else:
            return super().getCollisionRect()
    def interact(self, player, engine):
        engine.displayText(self.text)
        player.vel = vec(0,0)

class Torch(Animated):
    def __init__(self, position = vec(0,0), color = 0, lit = True):
        if lit:
            super().__init__(position, "torch.png", (0,color))
        else:
            super().__init__(position, "torch.png", (0,4))
            color = 4

        self.lit = lit
        self.nFrames = 4
        self.framesPerSecond = 8

        self.row = color
        if color == 1 or color == 3:
            self.frame = 2
    
    def light(self):
        if not self.lit:
            self.row = 0
            self.lit = True
    