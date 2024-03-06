from . import Drawable
from utils import SpriteManager, SCALE, RESOLUTION, vec
import pygame

class NonPlayer(Drawable):

    def __init__(self, position = vec(0,0), fileName="", offset=None):
        super().__init__(position, fileName, offset)

    def vanish(self, lst):
        lst.pop(lst.index(self))
        return lst
    
class Key(NonPlayer):
    def __init__(self, position=vec(0,0), fileName="", offset = None):
        super().__init__(position, fileName, offset)
        self.collected = False

    def collect(self):
        self.collected = True
    
