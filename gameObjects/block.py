from . import NonPlayer
from utils import vec, SpriteManager
import pygame

"""
Blocks are static, 16x16, cube-shaped objects
that impede the player's movement.
"""
class Block(NonPlayer):
    def __init__(self, position=vec(0,0), offset = (4,0)):
        super().__init__(position, "Objects.png", offset)
        if offset == None:
            self.set_sprite()
    
    def set_sprite(self):
        #Define a SpriteManager object in nonPlayer
        print(self.imageName)
        self.image = SpriteManager.getInstance().getSprite(self.imageName, (4,0))

    def update(self, player):
        if player.pushing == True:
            player.pushing = False

    