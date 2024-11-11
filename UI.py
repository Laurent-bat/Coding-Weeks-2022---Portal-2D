import pygame
from collision import *

"""
    Dans ce fichier :
        class Button_UI(x=200, y=100, sx=100, sy=50)
        class Button_UI_img(img_on, x=200, y=100, sx=100, sy=50, img_off=None))
"""

class Button_UI:
    def __init__(self,  x=200, y=100, sx=100, sy=50):
        self.x = x  # position du boutton
        self.y = y
        self.sx = sx  # taille du boutton
        self.sy = sy
        self.clicked = False
        self.sprites = {"not_clicked": [
            "not_clicked"], "clicked": ["not_clicked"]}
        self.anim_name = "not clicked"
        self.anim_i = 0

    def is_clicked(self):
        action = False
        pos = pygame.mouse.get_pos()
        if collision_point_boite(pos, self):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action

class Button_UI_img:
    def __init__(self, img_on, x=200, y=100, sx=100, sy=50,ratio_x=1536/2000,ratio_y=1100/864,img_off=None):
        self.x = x*ratio_x # position du boutton
        self.y = y*ratio_y
        self.sx = sx*ratio_x  # taille du boutton
        self.sy = sy*ratio_y
        self.ratio_x=ratio_x
        self.ratio_y=ratio_y
        self.img_on = pygame.transform.scale(pygame.image.load(
            "images/"+img_on+".png").convert_alpha(), (self.sx, self.sy))
        if img_off == None:
            self.img_off = pygame.transform.scale(
                pygame.image.load("images/"+img_on+".png").convert_alpha(), (self.sx, self.sy))
        else:
            self.img_off = pygame.transform.scale(pygame.image.load(
                "images/"+img_off+".png").convert_alpha(), (self.sx, self.sy))
        self.clicked = False
        self.sprites = {"not_clicked": [
            "not_clicked"], "clicked": ["not_clicked"]}
        self.anim_name = "not clicked"
        self.anim_i = 0
        self.etat = False  # convention, etat = False quand not_clicked

    def is_clicked(self):
        action = False
        (x,y) = pygame.mouse.get_pos()
        if collision_point_boite((x*self.ratio_x,y*self.ratio_y), self):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.etat = not self.etat
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action
