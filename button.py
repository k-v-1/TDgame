import pygame as pg

class Button():
    def __init__(self, x, y, image, image_pressed=None, image_hover=None, single_click=True):
        self.original_image = image
        self.image = image
        # if image_pressed is None:
        #     self.image_pressed = image
        # else:
        #     self.image_pressed = image_pressed
        if image_hover is None:
            self.image_hover = image
        else:
            self.image_hover = image_hover

        self.rect = self.original_image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        action = False
        #get mouse position
        pos = pg.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.image = self.image_hover
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                # self.image = self.image_pressed
                action = True
                #if button is a single click type, then set clicked to True
                if self.single_click:
                    self.clicked = True
        else:
            self.image = self.original_image

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, self.rect)

        return action