import pygame
from drawable import Drawable

class Npc(Drawable):
    def __init__(self, fileName, position):
        super().__init__(fileName, position)
    
    def draw(self, drawSurface):
        super().draw(drawSurface)
    
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pass
