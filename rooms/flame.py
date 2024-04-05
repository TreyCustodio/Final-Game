from gameObjects import *

class Flame_1(AbstractEngine):
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_1()
      
        return cls._INSTANCE
    
    class _Flame_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_1.png")
            #self.trigger1 = Trigger(door = 0)
        
        #override
        def createBlocks(self):
           pass
           
        #override
        def blockCollision(self):
           pass



class Flame_2(AbstractEngine):
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_2()
      
        return cls._INSTANCE
    
    class _Flame_2(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_1.png")
            #self.trigger1 = Trigger(door = 0)
        
        #override
        def createBlocks(self):
           pass
           
        #override
        def blockCollision(self):
           pass




class Flame_3(AbstractEngine):
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_3()
      
        return cls._INSTANCE
    
    class _Flame_3(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_1.png")
            #self.trigger1 = Trigger(door = 0)
        
        #override
        def createBlocks(self):
           pass
           
        #override
        def blockCollision(self):
           pass




class Flame_4(AbstractEngine):
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_4()
      
        return cls._INSTANCE
    
    class _Flame_4(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_1.png")
            #self.trigger1 = Trigger(door = 0)
        
        #override
        def createBlocks(self):
           pass
           
        #override
        def blockCollision(self):
           pass





class Flame_5(AbstractEngine):
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_5()
      
        return cls._INSTANCE
    
    class _Flame_5(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_1.png")
            #self.trigger1 = Trigger(door = 0)
        
        #override
        def createBlocks(self):
           pass
           
        #override
        def blockCollision(self):
           pass





class Flame_6(AbstractEngine):
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_6()
      
        return cls._INSTANCE
    
    class _Flame_6(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_1.png")
            #self.trigger1 = Trigger(door = 0)
        
        #override
        def createBlocks(self):
           pass
           
        #override
        def blockCollision(self):
           pass