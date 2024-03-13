from . import Drawable
from utils import SpriteManager, SCALE, RESOLUTION, vec, rectAdd
import pygame

class NonPlayer(Drawable):
    """
    Non playable objects with an additional collision rect for interaction w/ player
    """

    def __init__(self, position = vec(0,0), fileName="", offset=None):
        super().__init__(position, fileName, offset)
    
    def getInteractionRect(self):
        oldRect = self.getCollisionRect()
        newRect = pygame.Rect((oldRect.bottomleft),(oldRect.width,5))
        return newRect
    
    def draw(self, drawSurface, drawHitbox = False):
        super().draw(drawSurface, drawHitbox)
        if drawHitbox:
            interaction = rectAdd(-Drawable.CAMERA_OFFSET, self.getInteractionRect())
            pygame.draw.rect(drawSurface, (255,255,255), interaction, 1)
    
    def interact(self, player):
        pass

    def vanish(self, lst):
        lst.pop(lst.index(self))
        return lst
    

class Chest(NonPlayer):
    """
    Your typical chest. Remains
    opened once opened.
    """
    def __init__(self, position = vec(0,0), fileName="", offset=None):
        super().__init__(position, fileName, offset)
        self.interacted = False
        self.contents = None

    def setContents(self, fileName = "", offset = None):
        """
        Set the image for the chest's contents
        """
        self.contents = SpriteManager.getInstance().getSprite(fileName, offset)

    def interact(self, player):#drawSurface
        self.interacted = True
        player.talking = True
        self.image = SpriteManager.getInstance().getSprite("Objects.png", (1,1))
        player.talking = False

    
class Key(Drawable):
    """
    Parent class for item pickups
    """
    def __init__(self, position=vec(0,0), fileName="", offset = None):
        super().__init__(position, fileName, offset)
        self.collected = False

    def collect(self):
        self.collected = True
