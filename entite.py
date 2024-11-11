import numpy as np
import pygame
from collision import *
from json import loads


"""
    Dans ce fichier :
        fun load_level(path,level_name_in_the_json)
        class Rayon(x,y,dx,dy)
        class Personnage (x=0, y=0, sx=30, sy=70)
        class Bloc (x, y, sx, sy)
        class Bouton (x, y)
        class Porte (x, y)
        class Portal (x, y, angle, couleur)
        class Cube (x, y)
        class Arme(Proprio)
        class Mur(x,y)
        class Dialogue(x,y,dialogue)
"""

# Liste des classes


def load_level(src, level_name):
    ctx = None
    try:
        f = open(src, "r")
        ctx = loads(f.read())[level_name]
        f.close()
    except FileNotFoundError:
        print("ERROR LOADING FILE CONTAINING LEVELS - File Not Found : "+src)
        return None, None, None, None, None
    except:
        print("ERROR LOADING FILE CONTAINING LEVELS - Incorrect file format : "+src)
        return None, None, None, None, None
    p = Personnage(ctx["perso"]["x"], ctx["perso"]["y"], ctx["perso"]["sx"], ctx["perso"]["sy"])
    p.ay = ctx["info"]["gravity"]
    bbs = []
    pporte = Porte(ctx["info"]["porte"]["x"], ctx["info"]["porte"]["y"], ctx["info"]["porte"]["sx"], ctx["info"]["porte"]["sy"])
    bts = []
    cbs = []
    ms = []
    dg=[]
    lvc=0
    for x in ctx["blocs"]:
        if "sprite" in x:
            if "repeat" in x:
                if "portal" in x:
                    bbs.append(
                        Bloc(x["x"], x["y"], x["sx"], x["sy"], x["sprite"], x["repeat"], x["portal"]))
                else:
                    bbs.append(Bloc(x["x"], x["y"], x["sx"],
                               x["sy"], x["sprite"], x["repeat"]))
            else:
                if "portal" in x:
                    bbs.append(Bloc(x["x"], x["y"], x["sx"],
                               x["sy"], x["sprite"], portal=x["portal"]))
                else:
                    bbs.append(
                        Bloc(x["x"], x["y"], x["sx"], x["sy"], x["sprite"]))
        else:
            if "repeat" in x:
                if "portal" in x:
                    bbs.append(
                        Bloc(x["x"], x["y"], x["sx"], x["sy"], repeat=x["repeat"], portal=x["portal"]))
                else:
                    bbs.append(Bloc(x["x"], x["y"], x["sx"],
                               x["sy"], repeat=x["repeat"]))
            else:
                if "portal" in x:
                    bbs.append(Bloc(x["x"], x["y"], x["sx"],
                               x["sy"], portal=x["portal"]))
                else:
                    bbs.append(Bloc(x["x"], x["y"], x["sx"], x["sy"]))
    for x in ctx["boutons"]:
        bts.append(Bouton(x["x"], x["y"], x["sx"], x["sy"]))
    for x in ctx["cubes"]:
        cbs.append(Cube(x["x"], x["y"], x["sx"], x["sy"], x["m"]))
    for x in ctx["murs"]:
        ms.append(Mur(x["x"], x["y"], x["sx"], x["sy"], x["condition"]))
    if "dialogue" in ctx:
        for x in ctx["dialogue"]:
            dg.append(Dialogue(x["dialogue_gentil_1"],True))
            dg.append(Dialogue(x["dialogue_gentil_2"],True))
            dg.append(Dialogue(x["dialogue_gentil_3"],True))
            dg.append(Dialogue(x["dialogue_villain_1"],False))
            dg.append(Dialogue(x["dialogue_villain_2"],False))
            dg.append(Dialogue(x["dialogue_villain_3"],False))
    if "le_villain_commence" in ctx:
        lvc=ctx["le_villain_commence"]["lvc"]
    return p, bbs, pporte, bts, cbs, ms, dg, lvc


class Rayon:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
class Personnage:
    def __init__(self, x=0, y=0, sx=50, sy=100):
        self.x = x  # Position du joueur
        self.y = y
        self.sx = sx  # Taille du joueur
        self.sy = sy
        self.m = 50  # Masse du joeur
        self.vx = 0  # Vitesse du joueur
        self.vy = 0
        self.vit = 330
        self.ax = 0  # Acceleration du joueur
        self.ay = 1500  # Gravite
        self.arme = Arme(self)  # Arme liée au personnage
        self.canPush = True  # Peut pousser un cube
        self.canCarry = True  # Peut soulever un cube
        self.col = {'h': False, 'g': False, 'b': False,
                    'd': False}  # Colision (False=Pas en colision)
        self.attache = None
        self.direction = True  # Par convention, True est vers la droite
        self.portal = None  # variable renvoyant au portail dans lequel le joueur se trouve
        self.sprites = {"courir": ["courir_1", "courir_2", "courir_3",
                                   "courir_4", "courir_5", "courir_6"], "stand": ["still"]}
        self.anim_name = "stand"
        self.anim_i = 0
        self.alpha = 1  # coefficient de frottement
        self.vitTerminale = 1.6*self.ay

    def deplacement_key_down(self, Cdd):
        # Deplacement droite (Fleche droite et "d")
        if (Cdd == 1073741903 or Cdd == 100) and self.col['d'] == False:
            self.vx = self.vit
            self.anim_name = "courir"
            self.anim_i = 0
        # Deplacement gauche (Fleche gauche et "q")
        if (Cdd == 1073741904 or Cdd == 113) and self.col['g'] == False:
            self.vx = -self.vit
            self.anim_name = "courir"
            self.anim_i = 0
        # Deplacement saut (Fleche haut, "z" et spacebar)
        if (Cdd == 1073741906 or Cdd == 122 or Cdd == 32) and self.col['b'] == True:
            self.vy = -600

    def deplacement_key_up(self, Cdd):
        # Deplacement droite (Fleche droite et "d")
        if self.vx > 0 and (Cdd == 1073741903 or Cdd == 100):
            self.vx = 0
            self.anim_name = "stand"
            self.anim_i = 0
        # Deplacement gauche (Fleche gauche et "q")
        if self.vx < 0 and (Cdd == 1073741904 or Cdd == 113):
            self.vx = 0
            self.anim_name = "stand"
            self.anim_i = 0

    def attrape(self, objet):
        objet.attrape(self)
        self.attache = objet

    def lache(self):
        self.attache.lache()
        self.attache = None

    def teleport(self, portal_in, portal_out, dt=0.016):
        dif_angle = portal_in.angle-portal_out.angle
        MR = np.array([[np.cos(dif_angle*np.pi/180), -np.sin(dif_angle*np.pi/180)],
                      [np.sin(dif_angle*np.pi/180), np.cos(dif_angle*np.pi/180)]])
        V1 = np.array([-self.vx, -self.vy])
        V2 = np.dot(MR, V1)
        if portal_out.angle % 180 == 0:
            self.vx, self.vy = V2[0], V2[1]
        if portal_out.angle % 180 == 90:
            self.vx, self.vy = V2[0], V2[1]
        self.x = portal_out.x-self.sx/2+self.vx*dt
        self.y = portal_out.y-self.sy/2+self.vy*dt

    def actualise(self, souris, x, y,portails,blocs,murs, dt=0.016):
        self.x += self.vx*dt  # Parametre Personnage
        self.y += self.vy*dt
        self.vx += self.ax*dt
        self.vy += self.ay*dt
        if self.vy != 0:                                                        # Creation d'une vitesse critique
            self.vy = round(self.vy*np.exp(self.alpha/(-1*abs(self.vy))))
        if abs(self.vy) >= self.vitTerminale:
            self.vy = self.vitTerminale*np.sign(self.vy)

        # Determiner la direction
        self.direction = souris[0] > self.x+self.sx/2
        if not self.attache is None:
            if self.direction:  # Determiner ou se situe le bloc soulevé
                self.attache.x = self.x+self.sx/2+self.attache.decx
                self.attache.y = self.y+self.sy/2+self.attache.decy
            else:
                self.attache.x = self.x+self.sx/2-self.attache.decx-self.attache.sx
                self.attache.y = self.y+self.sy/2+self.attache.decy
            self.attache.vx = self.vx
            self.attache.vy = self.vy
            self.attache.ax = self.ax
            self.attache.ay = self.ay
        if self.arme is not None:                                               # Si le joueur a une arme
            self.arme.x = self.x+(1/2)*self.sx+self.arme.decx
            self.arme.y = self.y+(1/2)*self.sy+self.arme.decy
            # paramétrage du rayon
            self.arme.rayon.x = self.arme.x
            self.arme.rayon.y = self.arme.y-self.arme.sy/2
            # Si on a un point de collision entre le rayon sortant de l'arme et les blocs de la scène
            if x >= 0 and y >= 0:
                self.arme.rayon.dx = x-self.arme.rayon.x
                self.arme.rayon.dy = y-self.arme.rayon.y
                # Si il y a un click gauche de la souris
                if pygame.mouse.get_pressed()[2]:
                    i, d, (x, y), angle = collision_rayon_blocs(Rayon(
                        self.arme.rayon.x, self.arme.rayon.y, x-self.arme.rayon.x, y-self.arme.rayon.y), blocs, murs)
                    if i != -1:
                        pp = Portal(x, y, angle, "orange")
                        if not collision_portail_blocs(pp, blocs) and blocs[i].can_portal:
                            pp.bloc = blocs[i]
                            portails["orange"] = pp
                # Si il y a un click droit de la souris
                elif pygame.mouse.get_pressed(3)[0]:
                    i, d, (x, y), angle = collision_rayon_blocs(Rayon(
                        self.arme.rayon.x, self.arme.rayon.y, x-self.arme.rayon.x, y-self.arme.rayon.y), blocs, murs)
                    if i != -1:
                        pp = Portal(x, y, angle, "bleu")
                        if not collision_portail_blocs(pp, blocs) and blocs[i].can_portal:
                            pp.bloc = blocs[i]
                            portails["bleu"] = pp
            # Si on n'a pas de collision entre le rayon et les blocs, on prend la souris
            elif x == -2 and y == -2:
                self.arme.rayon.dx = souris[0]-self.arme.rayon.x
                self.arme.rayon.dy = souris[1]-self.arme.rayon.y
            self.arme.calcul_angle(souris[0], souris[1])

        self.anim_i = (dt*10+self.anim_i) % len(self.sprites[self.anim_name])
class Bloc:
    def __init__(self, x, y, sx, sy, sprite="bloc", repeat=False, portal=1):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.repeat = repeat
        self.sprites = {"bloc": [sprite], "no": ["no"]}
        self.anim_name = "bloc" if portal else "no"
        self.anim_i = 0
        self.can_portal = portal == 1
class Bouton:
    def __init__(self, x, y, sx=20, sy=20):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        # hauteur du boutons de haut en bas dependant de son etat
        self.h = {"on": sy*2/9, "off": sx*2/5}
        self.sprites = {"off": ["bouton_off"], "on": ["bouton_on"]}
        self.anim_name = "off"
        self.anim_i = 0
        self.etat = False  # Convention: etat False = bouton relaché
        # Etat provisoire sert a tester si il y a un cube dessus | Convention: etat False = bouton relaché
        self.etat_p = False

    def action_bouton(self):
        self.etat = not self.etat
        if self.etat:
            self.anim_name = "on"
        else:
            self.anim_name = "off"
class Porte:
    def __init__(self, x, y, sx=100, sy=100):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.sprites = {"porte_ouverte": ["porte_4"],
                        "porte_fermee": ["porte_0"],
                        "porte_anim_ouvre": ["porte_1", "porte_2", "porte_3"],
                        "porte_anim_ferme": ["porte_3", "porte_2", "porte_1"],
                        "gateau":["gateau"]}
        self.anim_name = "porte_fermee"
        self.anim_i = 0
        self.etat = False  # Convention: etat False =  Porte fermee

    def action_porte(self):
        if self.etat:
            self.anim_name = "porte_anim_ferme"
        else:
            self.anim_name = "porte_anim_ouvre"
        self.anim_i = 0
        self.etat = not self.etat

    def actualise(self, dt):
        if (self.anim_name == "porte_anim_ouvre" or self.anim_name == "porte_anim_ferme") and self.anim_i < len(self.sprites["porte_anim_ouvre"]):
            self.anim_i += dt*10
        if self.anim_i >= len(self.sprites["porte_anim_ouvre"]):
            if self.anim_name == "porte_anim_ouvre":
                self.anim_name = "porte_ouverte"
            if self.anim_name == "porte_anim_ferme":
                self.anim_name = "porte_fermee"
            self.anim_i = 0
class Portal:
    def __init__(self, x, y, angle, couleur):
        self.x = x  # x,y position du centre
        self.y = y
        self.sx = 20
        self.sy = 100
        self.angle = angle  # angle en degrés !
        self.bloc = None  # référence le bloc auquel le portal frame est rattaché
        self.sprites = {"bleu": ["bleu_0", "bleu_1", "bleu_2"],
                        "orange": ["orange_0", "orange_1", "orange_2"]}
        self.anim_name = couleur
        self.anim_i = 0

    def actualise(self, dt=0.016):
        self.anim_i = (self.anim_i+10*dt) % len(self.sprites[self.anim_name])
class Cube:
    def __init__(self, x, y, sx=20, sy=20, m=50):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.vx = 0
        self.vy = 0
        self.m = m
        self.movable = False
        self.carriable = True
        self.alpha = 1  # Coefficient de frottement
        self.ax = 0
        self.ay = 1000
        self.proprietaire = None  # définit quel personnage détient le cube
        self.decx = 0
        self.decy = 0
        self.portal = None  # variable renvoyant au portail dans lequel le joueur se trouve
        self.vitTerminale = 1.6*self.ay
        self.col = {'h': False, 'g': False, 'b': False,
                    'd': False}  # Colision (False=Pas en colision)
        self.sprites = {"cube": ["cube_0", "cube_1", "cube_2"], "cube_still": [
            "cube_still_0", "cube_still_1", "cube_still_2", "cube_still_3"]}
        self.anim_name = "cube"
        self.anim_i = 0

    def teleport(self, portal_in, portal_out, dt=0.016):
        dif_angle = portal_in.angle-portal_out.angle
        MR = np.array([[np.cos(dif_angle*np.pi/180), -np.sin(dif_angle*np.pi/180)],
                      [np.sin(dif_angle*np.pi/180), np.cos(dif_angle*np.pi/180)]])
        V1 = np.array([-self.vx, -self.vy])
        V2 = np.dot(MR, V1)
        if portal_out.angle % 180 == 0:
            self.vx, self.vy = V2[0], V2[1]
        if portal_out.angle % 180 == 90:
            self.vx, self.vy = V2[0], V2[1]
        self.x = portal_out.x-self.sx/2+self.vx*dt
        self.y = portal_out.y-self.sy/2+self.vy*dt

    def actualise(self, dt):
        if self.proprietaire == None and (self.movable or not self.col["b"]):
            self.x += self.vx*dt
            self.y += self.vy*dt
            self.vx += self.ax*dt
            self.vy += self.ay*dt
            if self.vx != 0 and self.col["b"]:
                self.vx = round(self.vx*np.exp(self.alpha/(-1*abs(self.vx))))
            if self.vy != 0:                                                        # Creation d'une vitesse critique
                self.vy = round(self.vy*np.exp(self.alpha/(-1*abs(self.vy))))
            if abs(self.vy) >= self.vitTerminale:
                self.vy = self.vitTerminale*np.sign(self.vy)
        self.col = {'h': False, 'g': False, 'b': False, 'd': False}
        self.anim_i = (dt*10 + self.anim_i) % len(self.sprites[self.anim_name])

    def attrape(self, perso):
        self.proprietaire = perso
        self.decx = perso.sx/2
        self.decy = -(1/6)*perso.sy

    def lache(self):
        self.proprietaire = None
class Arme:
    def __init__(self, perso):
        self.proprietaire = perso
        self.sx = 40
        self.sy = 25
        self.decx = 0
        self.decy = 0
        self.angle = 0
        self.rayon = Rayon(0, 0, 0, 0)
        self.x = perso.x+(1/2)*perso.sx+self.decx
        self.y = perso.y+(1/2)*perso.sy+self.decy
        # Indique les portals frame tirés. Convention False= non-tiré
        self.etat = (False, False)
        # et on indique en premier le bleu et en second l'orange.
        self.sprites = {"arme": ["arme"]}
        self.anim_name = "arme"
        self.anim_i = 0

    def active_bleu(self):
        if self.etat == (False, False):
            self.etat = (True, False)
            self.anim_name = "arme_portail_bleu"

        if self.etat == (False, True):
            self.etat = (True, True)
            self.anim_name = "arme_deux_portails"

    def active_orange(self):
        if self.etat == (False, False):
            self.etat = (False, True)
            self.anim_name = "arme_portail_orange"

        if self.etat == (True, False):
            self.etat = (True, True)
            self.anim_name = "arme_deux_portails"

    def calcul_angle(self, sourisx, sourisy):
        deltax = sourisx-self.x
        deltay = sourisy-self.y
        norme = np.sqrt(deltax**2 + deltay**2)
        sin = deltay/norme
        if sin >= 0:
            self.angle = np.arccos(deltax/norme)*180/np.pi

        else:
            self.angle = -np.arccos(deltax/norme)*180/np.pi
class Mur:
    def __init__(self, x, y, sx, sy, conditions):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.etat = False         # Convention: etat False =  mur fermé
        self.conditions = conditions
        self.sprites = {"close": ["door_closed_0", "door_closed_1"], "open": ["door_opened_0", "door_opened_1"],
                        "ouverture": ["door_anim_0", "door_anim_1", "door_anim_2", "door_anim_3", "door_anim_4", "door_anim_5"],
                        "fermeture": ["door_anim_5", "door_anim_4", "door_anim_3", "door_anim_2", "door_anim_1", "door_anim_0"]}
        self.anim_name = "close"
        self.anim_i = 0

    def action_mur(self):
        if self.etat:
            self.anim_name = "fermeture"
        else:
            self.anim_name = "ouverture"
        self.anim_i = 0
        self.etat = not self.etat

    def actualise(self, dt=0.016):
        self.anim_i += dt*10
        if self.anim_i >= len(self.sprites["ouverture"]):
            if self.anim_name == "ouverture":
                self.anim_name = "open"
            if self.anim_name == "fermeture":
                self.anim_name = "close"
            self.anim_i = 0
        self.anim_i = self.anim_i % len(self.sprites[self.anim_name])
class Dialogue:
    def __init__(self, dialogue,locuteur=True,maxi=7):
        self.x = 0
        self.y = 0
        self.sx = 2000
        self.sy = 1100
        self.i=0
        self.max=maxi
        self.dialogue = dialogue
        self.fini=False
        self.anim_name = "gentil_glados" 
        # Convention: True signifie que gentil glados parle, et false, vilain glados
        self.locuteur = locuteur
        self.sprites = {"gentil_glados": ["gentil_0", "gentil_1"], "vilain_glados": [
            "vilain_0", "vilain_1"]}
        if self.locuteur:
            self.anim_name = "gentil_glados"
        else:
            self.anim_name = "vilain_glados"
        
        self.anim_i = 0

    def actualise(self, dt=0.016):
        self.anim_i += dt*3
        self.anim_i = self.anim_i % len(self.sprites[self.anim_name])



# Test des fonctions
if __name__ == '__main__':
    from entite import *
    p = Personnage(150, 0)
    ps={"bleu":None,"orange":None}
    p.sx, p.sy = 45, 100
    p.vx = 500
    b = Bloc(200, 0, 100, 200)
    print("TEST DU PROGRAMME")
    print("Test collision entre un personnage et un bloc : ")
    print("Verfication de la prise en compte de la vitesse")
    collision_joueur_blocs(p, [b],ps)
    assert p.col["d"]
    p.vx = 0
    collision_joueur_blocs(p, [b],ps)
    assert p.col["d"]
    print("Test Reussi : La vitesse est prise en compte")
    print("Test collision entre un rayon et un bloc : ")
    b = Bloc(200, 0, 100, 200)
    r = Rayon(250, 250, 0, -1)
    assert collision_rayon_bloc(r, b) == (True, (250, 200), 50.0, 2)
    b = Bloc(200, 50, 100, 200)
    r = Rayon(250, 20, 0, 1)
    assert collision_rayon_blocs(r, [b]) == (0, 30.0, (250, 50), 90)
    b = Bloc(100, 100, 100, 100)
    r = Rayon(0, 150, 1, 0)
    assert collision_rayon_blocs(r, [b]) == (0, 100.0, (100, 150.0), 180)
    b = Bloc(100, 100, 100, 100)
    r = Rayon(250, 150, -1, 0)
    assert collision_rayon_blocs(r, [b]) == (0, 50.0, (200, 150.0), 0)
    b = Bloc(100, 100, 100, 100)
    r = Rayon(0, 0, 1, 1)
    assert collision_rayon_blocs(r, [b]) == ( 0, 141.4213562373095, (100, 100.0), 180)
    b = Bloc(0, 300, 800, 50)
    r = Rayon(298.9999999999996, 313.9399999999998, -
              206.55208333333292, -313.9399999999998)
    r = Rayon(200, 200, 50, 50)
    print(collision_rayon_blocs(r, [b]))
    print("Test Reussi : Collision entre un rayon et un bloc")
    print("Test collision entre un portail et les blocs : ")
    bbs = [Bloc(200, 200, 50, 50), Bloc(200, 250, 50, 50)]
    portail = Portal(200, 250, 180, "bleu")
    assert not collision_portail_blocs(portail, bbs)
    bbs = [Bloc(200, 200, 50, 50), Bloc(
        200, 250, 50, 50), Bloc(150, 200, 50, 50)]
    portail = Portal(200, 250, 180, "bleu")
    assert collision_portail_blocs(portail, bbs)
    print("Test Reussi : Collision entre un portail et les blocs")
