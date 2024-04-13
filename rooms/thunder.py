from gameObjects import *


class Thunder_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Thun_1()
      
        return cls._INSTANCE
    
    class _Thun_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("thunder_1.png")
            #self.trigger1 = Trigger(door = 0)
        
        #override
        def createBlocks(self):
           pass
           
        #override
        def blockCollision(self):
           pass