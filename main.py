import pygame
from UI import ScreenManager, Xbox, EventManager
from utils import RESOLUTION, UPSCALED
from random import randint

def main():
    ##Initialize the module
    pygame.init()
    pygame.font.init()

    ##Set the screen up
    flags = pygame.SCALED
    screen = pygame.display.set_mode(list(map(int, UPSCALED)), flags=flags)
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))

    rand = randint(0,1)
    if rand == 1:
        pygame.display.set_caption("Majestus: I'll learn pixel art one day...")
    else:
        pygame.display.set_caption("Majestus: Not a Zelda clone I swear!")

    iconSurf = pygame.Surface((32,32))
    
    image = pygame.image.load("displayIcon.png").convert()
    iconSurf.blit(image, (0,0))
    pygame.display.set_icon(iconSurf)
    
    gameEngine = ScreenManager()
    eventManager = EventManager.getInstance()

    controller = Xbox()
    def setJoystick():
        ##Set up joystick
        joysticks = pygame.joystick.get_count()
        if joysticks == 0:
            gameEngine.setController("key")
            gameEngine.controllerSet = False

        elif not gameEngine.controllerSet:
            for i in range(pygame.joystick.get_count()):
                controller.setValue(pygame.joystick.Joystick(i))
                gameEngine.setController(controller.name)
                gameEngine.controllerSet = True
            

    RUNNING = True
    while RUNNING:
        
        pygame.transform.scale(drawSurface,
                               list(map(int, UPSCALED)),
                               screen)
        pygame.display.flip()
        gameClock = pygame.time.Clock()
        setJoystick()
        gameEngine.draw(drawSurface)
        eventManager.handleEvents(gameEngine)
        gameEngine.handleCollision()
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000
        gameEngine.update(seconds)
     
    pygame.quit()


if __name__ == '__main__':
    main()