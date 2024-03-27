from utils import SpriteManager, SCALE, RESOLUTION, vec, rectAdd

import pygame


        
class Drawable(object):
    
    CAMERA_OFFSET = vec(0,0)
    
    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        
        objSize = trackingObject.getSize()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (RESOLUTION // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - RESOLUTION[i])))
        
        cls.CAMERA_OFFSET = offset
        
        

    @classmethod    
    def translateMousePosition(cls, mousePos):
        newPos = vec(*mousePos)
        newPos /= SCALE
        newPos += cls.CAMERA_OFFSET
        
        return newPos
    
    def __init__(self, position=vec(0,0), fileName="", offset=None):
        if fileName != "":
            self.image = SpriteManager.getInstance().getSprite(fileName, offset)
        
        self.position  = vec(*position)
        self.imageName = fileName

    def draw(self, drawSurface, drawHitbox = False):
        drawSurface.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
        if drawHitbox:
            collision = rectAdd(-Drawable.CAMERA_OFFSET, self.getCollisionRect())
            pygame.draw.rect(drawSurface, (255,255,255), collision, 1)

    def getSize(self):
        return vec(*self.image.get_size())
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass
    
    
    def getCollisionRect(self):
        newRect = self.image.get_rect()
        newRect.left = int(self.position[0])
        newRect.top = int(self.position[1])
        return newRect
    
    def doesCollide(self, other):
        return self.getCollisionRect().colliderect(other.getCollisionRect())   
    
    def doesCollideList(self, others):
        rects = [r.getCollisionRect() for r in others]
        return self.getCollisionRect().collidelist(rects)


class Level(Drawable):
    def __init__(self, fileName):
        super().__init__((0,0), "")
        self.image = SpriteManager.getInstance().getLevel(fileName)
        
class Text(Drawable):
    import os
    if not pygame.font.get_init():
        pygame.font.init()
    FONT_FOLDER = "fonts"
    FONT = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 16)
    BOX = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 14)
    SMALL = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 12)
    
    def __init__(self, position, text, color = (255,255,255), box = False, small = False):
        super().__init__(position, "")
        if small:
            self.image = Text.SMALL.render(text, False, color)
        elif box:
            self.image = Text.BOX.render(text, False, color)
        else:
            self.image = Text.FONT.render(text, False, color)
            
class AmmoBar(Drawable):
    def __init__(self):
        super().__init__(vec(0,16), "ammo.png", (0,0))

    def draw(self, drawSurface, player):
        if player.hp == player.max_hp:
            self.image = SpriteManager.getInstance().getSprite("ammo.png", (1,0))

        elif player.hp <= player.max_hp/5 or player.hp == 1:
            self.image = SpriteManager.getInstance().getSprite("ammo.png", (2,0))
        else:
            self.image = SpriteManager.getInstance().getSprite("ammo.png", (0,0))
        super().draw(drawSurface)

class HealthBar(Drawable):
    def __init__(self):
        super().__init__(vec(0,0), "bar.png", (0,0))
    
    def draw(self, drawSurface, player):
        

        if player.hp == player.max_hp:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,1))

        elif player.hp <= player.max_hp/5 or player.hp == 1:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,6))
        elif player.hp <= player.max_hp/3.5:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,5))
            #Text((20,0), str(self.player.hp), (255,0,0)).draw(drawSurface)

        elif player.hp <= player.max_hp / 2.5:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,4))

        elif player.hp <= player.max_hp/1.5:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,3))
            #Text((20,0), str(self.player.hp), (225,228,0)).draw(drawSurface)    
        else:
            self.image = SpriteManager.getInstance().getSprite("bar.png", (0,2))
            
        super().draw(drawSurface)

