from drawable import Drawable
from constants import RESOLUTION, UPSCALED
import pygame

class Textbox(Drawable):
    def __init__(self, position, top = False):
        super().__init__("TextBox.png", position)
        self.surface = pygame.Surface(list(map(int, (self.image.get_size()[0],self.image.get_size()[1]) )))
        self.top = top #Lets the program know to draw the textbox at the top of the screen
        self.text = "" #Text inside the box

    def set_text(self, text):
        self.text = text
    
    def draw(self, drawSurface):
        #Textbox will appear at the bottom of the screen
        if self.top != True:
            self.surface.blit(self.image, list(map(int, (drawSurface.get_width()-self.image.get_size()[0]- (drawSurface.get_width()-self.image.get_size()[0])/2, drawSurface.get_height()-self.image.get_size()[1]-20) )))
        else:
            self.surface.blit(self.image, list(map(int, (drawSurface.get_width()-self.image.get_size()[0]- (drawSurface.get_width()-self.image.get_size()[0])/2, drawSurface.get_height()-(self.image.get_size()[1]*2 )))))