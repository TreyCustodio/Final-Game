from . import Drawable
from utils import SpriteManager, SCALE, RESOLUTION, vec
import pygame

class NonPlayer(Drawable):

    def __init__(self, position = vec(0,0), fileName="", offset=None, direction=0):
        super().__init__(position, fileName, offset)
