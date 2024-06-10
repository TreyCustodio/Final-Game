from . import Drawable, Animated

class Boulder(Drawable):
    def __init__(self, position):
        super().__init__(position, fileName="boulder.png", offset=(0,0))
        self.render = True
        
    def handleCollision(self, projectile, engine):
        if projectile.id == "bombo":
            engine.disappear(self)