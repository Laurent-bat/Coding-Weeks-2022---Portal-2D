import pygame
from UI import *
from collision import collision_point_boite
from entite import *
"""
    Dans ce fichier :
        Initialisation de Pygame
        Chargement des images
        Fonctions d'affichage
            anim_load : dictionnaire contenant tous les sprites automatiquement chargé quand on importe le fichier
            affichage_perso(perso)
            affichage_arme(arme)
            affichage_porte(porte)
            affichage_bouton(bouton)
            affichage_bloc(bloc)
            affichage_cube(cube)
            affichage_portal(portal)
            affichage_mur(mur)
        Fonctions d'affichage de l'UI
            affichage_image
            affichage_bouton_ui_text
            affichage_button_ui_img
            affichage_menu
            class menu
"""

################################################### pygame initialization
pygame.font.init()
pygame.init()
clock = pygame.time.Clock()
info = pygame.display.Info()  # création du mode plein écran
width = info.current_w
height = info.current_h
screen = pygame.display.set_mode((width, height))
ratio_x = width/2000
ratio_y = height/1100
dt = 0.016
#programIcon = pygame.image.load('images/icon.png')
#pygame.display.set_icon(programIcon)



def get_save():
    verif = open('save.save', 'a')
    verif.close()
    HSpreced = open('save.save', 'r')
    HS = HSpreced.read()
    HSpreced.close()
    return 1 if len(HS) == 0 else int(HS)
def save():
    nvHS = open('save.save', 'w')
    nvHS.write(str(game_variables["max_level"]))
    nvHS.close()

level_charge=get_save()

# Game variables
menu_font = pygame.font.SysFont('freesansbold.ttf', 90)
game_variables = {"running": True,
                  "game_paused": True,
                  'menu_state': "Main",
                  "music": True,
                  "sound": True,
                  "level": level_charge,
                  "max_level":level_charge,
                  "music_playing":0
                  }
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BLACK=(0,0,0)

################################################### Creation des entitées
def run(level):
    game_variables["level"]=level
    return load_level("levels.json", 'level'+str(level))
perso, blocs, porte, boutons, cubes, murs, dialogue_glados,lvc = load_level("levels.json",'level3')

entites_variables={
    "perso":perso,
    "blocs":blocs,
    "porte":porte,
    "boutons":boutons,
    "cubes":cubes,
    "murs":murs,
    "portail":{"bleu": None, "orange": None},
    "dialogue": dialogue_glados,
    "lvc":lvc
}

# Chargement des images
anim = {"courir_0": "running_0",
        "still": "perso_still",
        "porte_0": "porte_0",
        "porte_1": "porte_1",
        "porte_2": "porte_2",
        "porte_3": "porte_3",
        "porte_4": "porte_4",
        'bouton_off': 'bouton_0',
        'bouton_on': 'bouton_1',
        'bloc': 'bloc',
        'cube': 'cube',
        'cube_0': 'bloc_a_soulever_0',
        'cube_1': 'bloc_a_soulever_1',
        'cube_2': 'bloc_a_soulever_2',
        'courir_0': 'anim_perso_0',
        'courir_1': 'anim_perso_1',
        'courir_2': 'anim_perso_2',
        'courir_3': 'anim_perso_3',
        'courir_4': 'anim_perso_4',
        'courir_5': 'anim_perso_5',
        'courir_6': 'anim_perso_6',
        'orange_0': 'portail_orange_0',
        'orange_1': 'portail_orange_1',
        'orange_2': 'portail_orange_2',
        'bleu_0': 'portail_bleu_0',
        'bleu_1': 'portail_bleu_1',
        'bleu_2': 'portail_bleu_2',
        'door_anim_0': 'door_anim_0',
        'door_anim_1': 'door_anim_1',
        'door_anim_2': 'door_anim_2',
        'door_anim_3': 'door_anim_3',
        'door_anim_4': 'door_anim_4',
        'door_anim_5': 'door_anim_5',
        'door_closed_0': 'door_closed_0',
        'door_closed_1': 'door_closed_1',
        'door_opened_0': 'door_opened_0',
        'door_opened_1': 'door_opened_1',
        "no": "Bloc_pas_de_portail",
        'arme': 'portalgunavecbras',
        "gentil_0": 'boite_dial_bas__bas',
        "gentil_1": 'boite_dial_bas__haut',
        "vilain_0": 'boite_dial_bas__bas',
        "vilain_1": 'boite_dial_haut__bas',
        "bg":"background_clair",
        "cadenas":"cadenas",
        "gateau":"gateau"
        }
anim_load = {k: pygame.image.load(
    "images/"+anim[k]+".png").convert_alpha() for k in anim.keys()}

# Fonctions d'affichage


def load_image(src):
    '''Permet de charger l'image en focntion de la source récupérée dans anim.  '''
    return (pygame.image.load("images/"+src+".png").convert())
def affichage_perso(perso):
    '''Affichage des images relatives au personnage en fonction de son état '''
    screen.blit(pygame.transform.flip(pygame.transform.scale(anim_load[perso.sprites[perso.anim_name][int(
        perso.anim_i)]], (perso.sx*ratio_x, perso.sy*ratio_y)), not perso.direction, False), (perso.x*ratio_x, perso.y*ratio_y))
    pygame.draw.line(screen, (0, 0, 0), (perso.arme.rayon.x*ratio_x, perso.arme.rayon.y*ratio_y),
                     ((perso.arme.rayon.x+perso.arme.rayon.dx)*ratio_x, (perso.arme.rayon.y+perso.arme.rayon.dy)*ratio_y))
    if perso.arme == None:
        if not perso.attache == None:
            affichage_cube(perso.attache)
    else:
        affichage_arme(perso)
        if not perso.attache == None:
            cube = perso.attache
            d = distance([0, 0], [perso.arme.rayon.dx, perso.arme.rayon.dy])
            dx = perso.arme.rayon.dx/d
            dy = perso.arme.rayon.dy/d
            screen.blit(pygame.transform.scale(anim_load[cube.sprites[cube.anim_name][int(
                cube.anim_i)]], (cube.sx*ratio_x, cube.sy*ratio_y)), ((perso.arme.rayon.x+dx*50-cube.sx/2)*ratio_x, (perso.arme.rayon.y+dy*50-cube.sy/2)*ratio_y))
def blitRotate(image, pos, originPos, angle):
    """_summary_
    Args:
        image (une image): l'image qu'on veut afficher
        pos (tuple (x,y)): position du pivot dans le screen
        originPos (tuple (x,y)): position du pivot dans l'image
        angle (int en degré): rotation de l'image
    """
    # offset from pivot to center
    image_rect = image.get_rect(
        topleft=(pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x,
                            pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    screen.blit(rotated_image, rotated_image_rect)
def affichage_arme(perso):
    image = pygame.transform.flip(pygame.transform.scale(anim_load[perso.arme.sprites[perso.arme.anim_name]
                                                                   [int(perso.arme.anim_i)]], (perso.arme.sx*ratio_x, perso.arme.sy*ratio_y)), not perso.direction, False)
    if perso.direction:
        blitRotate(image, (perso.arme.x*ratio_x, perso.arme.y*ratio_y),
                   (0, 15), -perso.arme.angle)
    else:
        blitRotate(image, (perso.arme.x*ratio_x, perso.arme.y*ratio_y),
                   (perso.arme.sx-10, 15), 180-perso.arme.angle)
def affichage_porte(porte):
    '''Affichage de l'animation relatives aux portes en fonction de leur état d'ouverture'''
    screen.blit(pygame.transform.scale(anim_load[porte.sprites[porte.anim_name][int(
        porte.anim_i)]], (porte.sx*ratio_x, porte.sy*ratio_y)), (porte.x*ratio_x, porte.y*ratio_y))
def affichage_bouton(bouton):
    '''Affichage de l'animation relatives aux bouttons (soit en état on, soit en ettat off)'''
    screen.blit(pygame.transform.scale(anim_load[bouton.sprites[bouton.anim_name][bouton.anim_i]], (
        bouton.sx*ratio_x, bouton.sy*ratio_y)), (bouton.x*ratio_x, bouton.y*ratio_y))
def affichage_bloc(bloc):
    '''Affichage des blocs'''
    if bloc.repeat:
        for i in range(bloc.sx//50):
            for j in range(bloc.sy//50):
                screen.blit(pygame.transform.scale(anim_load[bloc.sprites[bloc.anim_name][bloc.anim_i]], (
                    50*ratio_x, 50*ratio_y)), (bloc.x*ratio_x+i*50*ratio_x, bloc.y*ratio_y+j*50*ratio_y))
    else:
        screen.blit(pygame.transform.scale(anim_load[bloc.sprites[bloc.anim_name][bloc.anim_i]], (
            bloc.sx*ratio_x, bloc.sy*ratio_y)), (bloc.x*ratio_x, bloc.y*ratio_y))
def affichage_cube(cube):
    '''Affichage des cubes'''
    screen.blit(pygame.transform.scale(anim_load[cube.sprites[cube.anim_name][int(
        cube.anim_i)]], (cube.sx*ratio_x, cube.sy*ratio_y)), (cube.x*ratio_x, cube.y*ratio_y))
def affichage_portal(portal):
    '''Affichage de l'animation relatives aux portes en fonction de leur état d'ouverture'''
    image_tourne = pygame.transform.rotate(
        anim_load[portal.sprites[portal.anim_name][int(portal.anim_i)]], portal.angle)
    if portal.angle in [90, 270, -90]:
        screen.blit(pygame.transform.scale(image_tourne, (portal.sy*ratio_x, portal.sx*ratio_y)),
                    ((portal.x-portal.sy/2)*ratio_x, (portal.y-portal.sx/2)*ratio_y))
    elif portal.angle in [0, 180, -180]:
        screen.blit(pygame.transform.scale(image_tourne, (portal.sx*ratio_x, portal.sy*ratio_y)),
                    ((portal.x-portal.sx/2)*ratio_x, (portal.y-portal.sy/2)*ratio_y))
    else:
        print("Angle non supporté dans affichage portail")
def affichage_mur(mur):
    '''Affichage des murs'''
    if mur.sx*ratio_x >= mur.sy*ratio_y:
        screen.blit(pygame.transform.scale(pygame.transform.rotate(anim_load[mur.sprites[mur.anim_name][int(
            mur.anim_i)]], 90), (mur.sx*ratio_x, mur.sy*ratio_y)), (mur.x*ratio_x, mur.y*ratio_y))
    else:
        screen.blit(pygame.transform.scale(anim_load[mur.sprites[mur.anim_name][int(
            mur.anim_i)]], (mur.sx*ratio_x, mur.sy*ratio_y)), (mur.x*ratio_x, mur.y*ratio_y))
bg=[pygame.transform.scale(anim_load["bg"],(width,height))]
# Fonctions de gestion de menu
def resume():
    game_variables["menu_state"]="Pause"
    game_variables["game_paused"] = False
def change_levels(level):
    if level==12:
        game_variables['level'] = 0
        game_variables['menu_state'] = "Credit"
        game_variables["game_paused"] = True
    else:
        if level>game_variables["max_level"]:
            game_variables["max_level"]=level
        perso, blocs, porte, boutons, cubes, murs,dialogue,lvc= run(level)
        entites_variables["perso"]=perso
        entites_variables["blocs"]=blocs
        entites_variables["porte"]=porte
        entites_variables["boutons"]=boutons
        entites_variables["cubes"]=cubes
        entites_variables["murs"]=murs
        entites_variables["dialogue"]=dialogue
        entites_variables["portail"]={"bleu": None, "orange": None}
        entites_variables["lvc"]=lvc
        game_variables["menu_state"]="Pause"
        game_variables["game_paused"] = False
def quit():
    save()
    game_variables["running"] = False
def change_menu(txt):
    game_variables['menu_state'] = txt
def reset():
    change_levels(game_variables["level"])
def change_music():
    if game_variables["music"]:
            pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    game_variables["music"] = not game_variables["music"]
def change_sound():
    game_variables["sound"] = not game_variables["sound"]
def pass_function():
    pass

# Fonctions d'affichage de UI


def affichage_image(img, position=(0, 0), size=(None, None)):
    image = pygame.image.load("images/"+img+".png").convert_alpha()
    x, y = position
    sx, sy = size
    if sx == None:
        if sy == None:
            screen.blit(image, (x, y))
        else:
            screen.blit(pygame.transform.scale(image, (image.get_width(), sy)), (x, y))
    elif sy == None:
        screen.blit(pygame.transform.scale(image, (sx, image.get_height())), (x, y))
    else:
        screen.blit(pygame.transform.scale(image, (sx, sy)), (x, y))
def affichage_bouton_ui_text(text, button, button_color=ROUGE, txt_color=BLANC, font=menu_font):
    pygame.draw.rect(screen, button_color,(button.x, button.y, button.sx, button.sy))
    img = font.render(text, True, txt_color,)
    screen.blit(pygame.transform.scale(
        img, (button.sx, button.sy)), (button.x, button.y))
    
def affichage_boite_de_dialogue(dialogue):
    if dialogue.max > dialogue.i:
        screen.blit(pygame.transform.scale(anim_load[dialogue.sprites[dialogue.anim_name][int(dialogue.anim_i)]], (dialogue.sx*ratio_x, dialogue.sy*ratio_y)), (0, 0))
def affichage_dialogue(dialogue, x, y, sx, sy, color=BLACK, font=menu_font, txt_color=BLANC):
    dialogue.i += dt
    img = font.render(dialogue.dialogue, True, txt_color,color)
    rectangle=img.get_rect()
    rectangle.center = ((x +sx/2)*ratio_x,(y+sy/2)*ratio_y)
    if dialogue.max > dialogue.i:
        screen.blit(img,rectangle)
    if dialogue.max <= dialogue.i:
        dialogue.fini=True
    
def affichage_button_ui_img(button):
    if button.etat:
        screen.blit(button.img_off, (button.x, button.y))
    else:
        screen.blit(button.img_on, (button.x, button.y))
def affichage_menu(menu_state, dt=0.016):
    """ Fonction permettant de circuler entre les différents menus, prenant en entrée la plage de menu correspondant.
    Menus disponibles : "Pause"
    """
    Menu_dico[menu_state].affiche_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_variables["running"] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_variables["game_paused"] = False
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            for b in Menu_dico[menu_state].boutons.keys():
                if Menu_dico[menu_state].boutons[b][0] == "bouton_img" and collision_point_boite((x,y),Menu_dico[menu_state].boutons[b][1]):
                    if Menu_dico[menu_state].boutons[b][2] == change_menu or Menu_dico[menu_state].boutons[b][2] == change_levels:
                        Menu_dico[menu_state].boutons[b][2](Menu_dico[menu_state].boutons[b][3])
                    else:
                        Menu_dico[menu_state].boutons[b][2]()
                        Menu_dico[menu_state].boutons[b][1].etat=not Menu_dico[menu_state].boutons[b][1].etat

    pygame.display.flip()
    clock.tick(60)
class Menu:
    def __init__(self, Boutons):
        self.x = 0
        self.y = 0
        self.sx = width
        self.sy = height
        # Boutons etant un dictionnaire {"nom" : (is_image,bouton_ui,fonction,img)}
        self.boutons = Boutons

    def affiche_Boutons(self):
        for b in self.boutons.keys():
            if self.boutons[b][0] == "bouton_img":
                affichage_button_ui_img(self.boutons[b][1])
                if self.boutons[b][2]==change_levels:
                    if self.boutons[b][3]>game_variables["max_level"]:
                        screen.blit(pygame.transform.scale(anim_load["cadenas"], (self.boutons[b][1].sx,self.boutons[b][1].sy)),(self.boutons[b][1].x,self.boutons[b][1].y))
                x, y = pygame.mouse.get_pos()
                # detect if mouse is on the button
                if collision_point_boite((x, y), self.boutons[b][1]):
                    s = pygame.Surface(
                        (self.boutons[b][1].sx, self.boutons[b][1].sy))
                    s.set_alpha(64)
                    s.fill((0, 0, 0))
                    screen.blit(
                        s, (self.boutons[b][1].x, self.boutons[b][1].y))
            elif self.boutons[b][0] == "image":
                affichage_image(self.boutons[b][1], self.boutons[b][2], self.boutons[b][3])
    def affiche_menu(self):
        self.affiche_Boutons()


# Dictionnaire des menus

Menu_dico = {
    'Main':  Menu({
        "Main_menu":("image","main_menu_bg",(0,0),(width,height)),
        " Play ": ("bouton_img", Button_UI_img("play", 500, 600, 400, 100,ratio_x,ratio_y), change_levels,game_variables["level"]),
        " Quit ": ("bouton_img", Button_UI_img("quit", 1100, 800, 400, 100,ratio_x,ratio_y), quit),
        " Levels ": ("bouton_img", Button_UI_img("levels",1100, 600, 400, 100,ratio_x,ratio_y), change_menu, "Levels_0"),
        " Options ": ("bouton_img", Button_UI_img("options", 500, 800, 400, 100,ratio_x,ratio_y), change_menu, "Options_main")
    }),
    'Credit':  Menu({
        "Credit":("image","image_credit",(0,0),(width,height)),
        " Main ": ("bouton_img", Button_UI_img("main_menu", 800, 900, 400, 100,ratio_x,ratio_y), change_menu, "Main")
    }),
    "Pause": Menu({
        "background":("image","menu_pause",(0,0),(width,height)),
        " Resume ": ("bouton_img", Button_UI_img('resume', 500, 600, 400, 100,ratio_x,ratio_y), resume),
        " Reset ": ("bouton_img", Button_UI_img("reset", 1100, 800, 400, 100,ratio_x,ratio_y), reset),
        " Main ": ("bouton_img", Button_UI_img("main_menu", 500, 800, 400, 100,ratio_x,ratio_y), change_menu, "Main"),
        " Options ": ("bouton_img", Button_UI_img('options', 1100, 600, 400, 100,ratio_x,ratio_y), change_menu, "Options_pause")
    }),
    "Options_pause": Menu({
        "background":("image","background",(0,0),(width,height)),
        " Sound ": ("bouton_img", Button_UI_img("son_on", 900, 250, 200, 200,ratio_x,ratio_y, img_off='son_off'), change_sound),
        " Music ": ("bouton_img", Button_UI_img("musique_on", 900, 700, 200, 200,ratio_x,ratio_y, img_off="musique_off"), change_music),
        " Back ": ("bouton_img", Button_UI_img("back", 75, 950, 100, 100,ratio_x,ratio_y), change_menu, "Pause")
    }),
    "Options_main": Menu({
        "background":("image","background",(0,0),(width,height)),
        " Sound ": ('bouton_img', Button_UI_img("son_on", 900, 250, 200, 200,ratio_x,ratio_y, img_off='son_off'), change_sound),
        " Music ": ('bouton_img', Button_UI_img("musique_on", 900, 700, 200, 200,ratio_x,ratio_y, img_off="musique_off"), change_music),
        " Back ": ('bouton_img', Button_UI_img("back", 75, 950, 100, 100,ratio_x,ratio_y), change_menu, "Main")
    }),
    "Levels_0": Menu({
        "background":("image","background",(0,0),(width,height)),
        "lvl_0": ('bouton_img',Button_UI_img("levels/level_0",125,150,500,275,ratio_x,ratio_y),change_levels,0 ),
        "lvl_1": ('bouton_img',Button_UI_img("levels/level_1",750,150,500,275,ratio_x,ratio_y),change_levels,1 ),
        "lvl_2": ('bouton_img',Button_UI_img("levels/level_2",1375,150,500,275,ratio_x,ratio_y),change_levels,2 ),
        "lvl_3": ('bouton_img',Button_UI_img("levels/level_3",125,540,500,275,ratio_x,ratio_y),change_levels,3 ),
        "lvl_4": ('bouton_img',Button_UI_img("levels/level_4",750,540,500,275,ratio_x,ratio_y),change_levels,4 ),
        "lvl_5": ('bouton_img',Button_UI_img("levels/level_5",1375,540,500,275,ratio_x,ratio_y),change_levels,5 ),       
        " Back ": ('bouton_img', Button_UI_img("back", 75, 950, 100, 100,ratio_x,ratio_y), change_menu, "Main"),
        " Next ": ("bouton_img", Button_UI_img("next", 1825, 950, 100, 100,ratio_x,ratio_y), change_menu, "Levels_1")
    }),
    "Levels_1": Menu({
        "background":("image","background",(0,0),(width,height)),
        "lvl_6": ('bouton_img',Button_UI_img("levels/level_6",125,150,500,275,ratio_x,ratio_y),change_levels,6 ),
        "lvl_7": ('bouton_img',Button_UI_img("levels/level_7",750,150,500,275,ratio_x,ratio_y),change_levels,7 ),
        "lvl_8": ('bouton_img',Button_UI_img("levels/level_8",1375,150,500,275,ratio_x,ratio_y),change_levels,8 ),
        "lvl_9": ('bouton_img',Button_UI_img("levels/level_9",125,540,500,275,ratio_x,ratio_y),change_levels,9 ),
        "lvl_10": ('bouton_img',Button_UI_img("levels/level_10",750,540,500,275,ratio_x,ratio_y),change_levels,10 ),
        " Back ": ('bouton_img', Button_UI_img("back", 75, 950, 100, 100,ratio_x,ratio_y), change_menu, "Levels_0"),
        #" Next ": ("bouton_img", Button_UI_img("next", 1825, 950, 100, 100,ratio_x,ratio_y), change_menu, "Levels_1")
    })
}

# Test des fonctions
if __name__ == '__main__':
    from entite import *
    from collision import *
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    running = True
    perso = Personnage()
    dt = 0.016
    blocs = [Bloc(0, 250, 400, 20), Bloc(
        0, 350, 600, 20), Bloc(580, 250, 20, 100)]
    portails = {"bleu": None, "orange": None}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                perso.deplacement_key_down(event.key)

            if event.type == pygame.KEYUP:
                perso.deplacement_key_up(event.key)
        x,y=pygame.mouse.get_pos()
        x,y=x/ratio_x,y/ratio_y
        collision_joueur_blocs(perso, blocs, portails)
        perso.actualise((x,y),0,0,dt,portails,blocs)
        for  b in blocs:    
            affichage_bloc(b)
        affichage_perso(perso)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
