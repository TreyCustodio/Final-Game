import pygame
from utils import SpriteManager, SCALE, RESOLUTION, vec
from . import Drawable

class Bullet(Drawable):
    def __init__(self, position, direction):
        super().__init__(position, "Bullet.png", (0,direction))
        self.damage = 1
        self.vel = vec(0,0)
    
    def update(self, seconds):
        self.position += self.vel * seconds