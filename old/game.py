import pygame
from drawable import Drawable
from player import Player
from spriteManager import SpriteManager
from vector import vec
from textbox import Textbox
from constants import RESOLUTION, UPSCALED


def main():

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Trey Custodio")
    font1 = pygame.font.SysFont("Garamond", 30)
    #message = font1.render("", False, (220, 0, 0))

    screen = pygame.display.set_mode(list(map(int, UPSCALED)))
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))

    link = Player("Link.png", (RESOLUTION[0]/2, RESOLUTION[1]/2), 2)
    link2 = Player("Link.png", (RESOLUTION[0]/2, (RESOLUTION[1]/2)-50), 0)
    link.position = (link.position[0] - link.image.get_size()[0]/2, link.position[1] - link.image.get_size()[1]/2)
    textBox = Textbox((50,50))
    npcs = [link2]
    gameClock = pygame.time.Clock()

    
    
    RUNNING = True
    while RUNNING:

        drawSurface.fill((0,0,0))
        link.draw(drawSurface, True)
        for n in npcs:
            n.draw(drawSurface, True)
        
        textBox.draw(drawSurface)
        # drawSurface.blit(message, (10,50))
        pygame.display.flip()
        pygame.transform.scale(drawSurface, UPSCALED, screen)

        ##  Event Handling  ##
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                            (event.type == pygame.KEYDOWN and \
                             event.key == pygame.K_ESCAPE):

                RUNNING = False
            
            else:
                ##  Characters in the world handle their events ##
                link.handleEvent(event)
        
        ##  Touching an Npc ##
        for n in npcs:
            if link.getCollisionRect().colliderect(n.getCollisionRect()):
                link.handleCollision(n)


        gameClock.tick()
        seconds = gameClock.get_time() / 1000
        link.update(seconds)


    pygame.quit()

if __name__ == '__main__':
    main()