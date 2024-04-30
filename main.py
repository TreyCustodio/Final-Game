import pygame
from UI import ScreenManager
from utils import RESOLUTION, UPSCALED
from random import randint

def main():
    #Initialize the module
    pygame.init()
    
    pygame.font.init()
    
    
    #Get the screen
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
    
    RUNNING = True
    
    while RUNNING:
        gameEngine.draw(drawSurface)
        
        pygame.transform.scale(drawSurface,
                               list(map(int, UPSCALED)),
                               screen)
        
        
        
        
        pygame.display.flip()
        gameClock = pygame.time.Clock()
        


        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                RUNNING = False
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.toggle_fullscreen()
            else:
                result = gameEngine.handleEvent(event)
                
                if result == "exit":
                    RUNNING = False
                    
        gameEngine.handleCollision()
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000
        gameEngine.update(seconds)
     
    pygame.quit()


if __name__ == '__main__':
    main()