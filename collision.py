from utils import *

"""
    Dans ce fichier :
        collision entre un joueur et un bloc
        collision entre un joueur et une liste de blocs
        collision entre un cube et un bloc
        collision entre un cube et une liste de blocs
        collision entre un joueur et un mur
        collision entre un joueur et une liste de murs
        collision entre un cube et un mur
        collision entre un cube et une liste de murs
        collision entre un cube et un bouton
        collision entre un cube et une liste de boutons
        collision entre un joueur et un cube
        collision entre un joueur et une liste de cubes
        collision entre un cube et un cube
        collision entre un cube et une liste de cubes
        collision entre une boite et un point
        collision entre un rayon et un bloc
        collision entre un rayon et une liste de blocs
        collision entre un portail et un bloc
        collision entre un portail et une liste de blocs
        collision entre un portail et un joueur
        collision entre un portail et un cube
"""

def collision_joueur_bloc(j,b,ps,dt=0.016):
    """
    Paramêtres : Joueur (Class Joueur) , Bloc (Class Bloc) , Portails (Class Portal)
    Modifie le joueur : vx , vy , col , x , y
    """
    if j.x+j.sx>b.x and j.x<b.x+b.sx and j.y+j.sy+j.vy*dt>=b.y and j.y+j.vy*dt<=b.y+b.sy:
        if j.y+j.sy<=b.y and (ps["bleu"] is None or ps["orange"] is None or j.portal is None or j.portal.angle!=90):
            j.vy=0
            j.y=b.y-j.sy
            j.col["b"]=True
        elif j.portal is not None and ps["bleu"] is not None and ps["orange"] is not None:
            if j.portal.angle==90 and j.y+j.sy/2+j.vy*dt>=j.portal.y:
                j.teleport(j.portal,ps[{"bleu":"orange",'orange':"bleu"}[j.portal.anim_name]])
                return True
            elif j.portal.angle in [0,180,-180]:
                if j.y+j.sy+j.vy*dt>=j.portal.y+j.portal.sy/2:
                    j.vy=0
                    j.y=j.portal.y+j.portal.sy/2-j.sy
                    j.col["b"]=True
        if j.y>=b.y+b.sy and (ps["bleu"] is None or ps["orange"] is None or j.portal is None or j.portal.angle!=270):
            j.vy=0
            j.y=b.y+b.sy
            j.col["h"]=True
        elif j.portal is not None and ps["bleu"] is not None and ps["orange"] is not None:
            if j.portal.angle==270 and j.y+j.sy/2+j.vy*dt<=j.portal.y:
                j.teleport(j.portal,ps[{"bleu":"orange",'orange':"bleu"}[j.portal.anim_name]])
                return True
            elif j.portal.angle in [0,180,-180]:
                if j.y+j.vy*dt<=j.portal.y-j.portal.sy/2:
                    j.vy=0
                    j.y=j.portal.y-j.portal.sy/2
                    j.col["h"]=True
    if j.x+j.sx+j.vx*dt>b.x and j.x+j.vx*dt<b.x+b.sx and j.y+j.sy>=b.y and j.y<=b.y+b.sy:
        if j.x+j.sx<=b.x and (ps["bleu"] is None or ps["orange"] is None or j.portal is None or j.portal.angle!=180):
            j.vx=0
            j.x=b.x-j.sx
            j.col["d"]=True
        elif j.portal is not None and ps["bleu"] is not None and ps["orange"] is not None:
            if j.portal.angle==180 and j.x+j.sx/2+j.vx*dt>=j.portal.x:
                j.teleport(j.portal,ps[{"bleu":"orange",'orange':"bleu"}[j.portal.anim_name]])
                return True
            elif j.portal.angle in [90,270,-90]:
                if j.x+j.sx+j.vx*dt>=j.portal.x+j.portal.sy/2:
                    j.vx=0
                    j.x=j.portal.x+j.portal.sy/2-j.sx
                    j.col["d"]=True
        if j.x>=b.x+b.sx and (ps["bleu"] is None or ps["orange"] is None or j.portal is None or j.portal.angle!=0):
            j.vx=0
            j.x=b.x+b.sx-j.vx*dt
            j.col["g"]=True
        elif j.portal is not None and ps["bleu"] is not None and ps["orange"] is not None:
            if j.portal.angle==0 and j.x+j.sx/2+j.vx*dt<=j.portal.x:
                j.teleport(j.portal,ps[{"bleu":"orange",'orange':"bleu"}[j.portal.anim_name]])
                return True
            elif j.portal.angle in [90,270,-90]:
                if j.x+j.vx*dt-15<=j.portal.x-j.portal.sy/2:
                    j.vx=0
                    j.x=j.portal.x-j.portal.sy/2
                    j.col["g"]=True
def collision_joueur_blocs(j,bs,ps,dt=0.016):
    """
    Paramêtres : Joueur (Class Joueur) , Liste des Blocs (Liste Class Bloc) , Portails (Dictionnaire of Portal)
    Modifie le joueur : vx , vy , col , x , y
    """
    for c in bs:
        aaaa=collision_joueur_bloc(j,c,ps,dt)
        if aaaa:
            return
def collision_cube_bloc(c,b,ps,dt=0.016):
    """
    Paramêtres : Cube (Class Cube) , Bloc (Class Bloc) , Portails (Dictionnaire of Portal)
    Modifie le cube : vx , vy , col , x , y
    """
    # if c.x+c.sx>b.x and c.x<b.x+b.sx and c.y+c.sy+c.vy*dt>=b.y and c.y+c.sy<=b.y:
    #     c.vy=0
    #     c.y=b.y-c.sy
    #     c.col["b"]=True
    # if c.x+c.sx>b.x and c.x<b.x+b.sx and c.y+c.vy*dt<=b.y+b.sy and c.y>=b.y+b.sy:
    #     c.vy=0
    #     c.y=b.y+b.sy
    #     c.col["h"]=True
    # if c.x+c.sx+c.vx*dt>=b.x and c.x+c.vx*dt<=b.x+b.sx and c.y+c.sy>b.y and c.y<b.y+b.sy:
    #     if c.x+c.sx<=b.x:
    #         c.x=b.x-c.sx
    #         c.col["d"]=True
    #         c.vx*=-1
    #     elif c.x<b.x:
    #         c.x=b.x-c.sx
    #         c.col["d"]=True
    #         c.vx*=-1
    # if c.x+c.vx*dt<=b.x+b.sx and c.x+c.sx+c.vx*dt>=b.x and c.y+c.sy>b.y and c.y<b.y+b.sy:
    #     if c.x>=b.x+b.sx:
    #         c.x=b.x+b.sx
    #         c.col["g"]=True
    #         c.vx*=-1
    #     elif c.x>b.x:
    #         c.x=b.x+b.sx
    #         c.col["g"]=True
    #         c.vx*=-1
    if c.x+c.sx>=b.x and c.x<=b.x+b.sx and c.y+c.sy+c.vy*dt>=b.y and c.y+c.vy*dt<=b.y+b.sy:
        if c.y+c.sy<=b.y and (ps["bleu"] is None or ps["orange"] is None or c.portal is None or c.portal.angle!=90):
            c.vy=0
            c.y=b.y-c.sy
            c.col["b"]=True
        elif c.portal is not None and ps["bleu"] is not None and ps["orange"] is not None:
            if c.portal.angle==90 and c.y+c.sy/2+c.vy*dt>=c.portal.y:
                c.teleport(c.portal,ps[{"bleu":"orange",'orange':"bleu"}[c.portal.anim_name]])
                return
            elif c.portal.angle in [0,180,-180]:
                if c.y+c.sy+c.vy*dt>=c.portal.y+c.portal.sy/2:
                    c.vy=0
                    c.y=c.portal.y+c.portal.sy/2-c.sy
                    c.col["b"]=True
        if c.y>=b.y+b.sy and (ps["bleu"] is None or ps["orange"] is None or c.portal is None or c.portal.angle!=270):
            c.vy=0
            c.y=b.y+b.sy
            c.col["h"]=True
        elif c.portal is not None and ps["bleu"] is not None and ps["orange"] is not None:
            if c.portal.angle==270 and c.y+c.sy/2+c.vy*dt<=c.portal.y:
                c.teleport(c.portal,ps[{"bleu":"orange",'orange':"bleu"}[c.portal.anim_name]])
                return
            elif c.portal.angle in [0,180,-180]:
                if c.y+c.vy*dt<=c.portal.y-c.portal.sy/2:
                    c.vy=0
                    c.y=c.portal.y-c.portal.sy/2
                    c.col["h"]=True
    if c.x+c.sx+c.vx*dt>=b.x and c.x+c.vx*dt<=b.x+b.sx and c.y+c.sy>=b.y and c.y<=b.y+b.sy:
        if c.x+c.sx<=b.x and (ps["bleu"] is None or ps["orange"] is None or c.portal is None or c.portal.angle!=180):
            if c.x+c.sx<=b.x:
                c.x=b.x-c.sx
                c.col["d"]=True
                c.vx*=-1
            elif c.x<b.x:
                c.x=b.x-c.sx
                c.col["d"]=True
                c.vx*=-1
        elif c.portal is not None and ps["bleu"] is not None and ps["orange"] is not None:
            if c.portal.angle==180 and c.x+c.sx/2+c.vx*dt>=c.portal.x:
                c.teleport(c.portal,ps[{"bleu":"orange",'orange':"bleu"}[c.portal.anim_name]])
                return
            elif c.portal.angle in [90,270,-90]:
                if c.x+c.sx+c.vx*dt>=c.portal.x+c.portal.sy/2:
                    c.vx=0
                    c.x=c.portal.x+c.portal.sy/2-c.sx
                    c.col["d"]=True
        if c.x>=b.x+b.sx and (ps["bleu"] is None or ps["orange"] is None or c.portal is None or c.portal.angle!=0):
            if c.x>=b.x+b.sx:
                c.x=b.x+b.sx
                c.col["g"]=True
                c.vx*=-1
            elif c.x>b.x:
                c.x=b.x+b.sx
                c.col["g"]=True
                c.vx*=-1
        elif c.portal is not None and ps["bleu"] is not None and ps["orange"] is not None:
            if c.portal.angle==0 and c.x+c.sx/2+c.vx*dt<=c.portal.x:
                c.teleport(c.portal,ps[{"bleu":"orange",'orange':"bleu"}[c.portal.anim_name]])
                return
            elif c.portal.angle in [90,270,-90]:
                if c.x+c.vx*dt<=c.portal.x-c.portal.sy/2:
                    c.vx=0
                    c.x=b.x+b.sx-c.vx*dt
                    c.col["g"]=True
def collision_cube_blocs(c,bs,ps,dt=0.016):
    """
    Paramêtres : Cube (Class Cube) , Liste des Blocs (Liste Class Bloc) , Portails (Dictionnaire of Portal)
    Modifie le cube : vx , vy , col , x , y
    """
    for x in bs:
        if c.proprietaire==None:
            collision_cube_bloc(c,x,ps,dt)
def collision_joueur_mur(p,m,dt=0.016):
    """
    Paramêtres : Joueur (Class Joueur) , Mur (Class Mur)
    Modifie le Joueur : vx , vy , col , x , y
    """
    if p.x+p.sx>m.x and p.x<m.x+m.sx and p.y+p.sy+p.vy*dt>=m.y and p.y+p.sy<=m.y:
        p.vy=0
        p.y=m.y-p.sy
        p.col["b"]=True
    if p.x+p.sx>m.x and p.x<m.x+m.sx and p.y+p.vy*dt<=m.y+m.sy and p.y>=m.y+m.sy:
        p.vy=0
        p.y=m.y+m.sy
        p.col["h"]=True
    if p.x+p.sx+p.vx*dt>=m.x and p.x+p.vx*dt<=m.x+m.sx and p.x+p.sx<=m.x and p.y+p.sy>m.y and p.y<m.y+m.sy:
        p.x=m.x-p.sx
        p.col["d"]=True
        p.vx=0
    elif p.x+p.vx*dt<=m.x+m.sx and p.x>=m.x+m.sx and p.x+p.sx+p.vx*dt>=m.x and p.y+p.sy>m.y and p.y<m.y+m.sy:
        p.x=m.x+m.sx
        p.col["g"]=True
        p.vx=0
def collision_joueur_murs(p,ms,dt=0.016):
    """
    Paramêtres : Joueur (Class Joueur) , Liste de Murs (List Class Mur)
    Modifie le Joueur : vx , vy , col , x , y
    """
    for m in ms:
        if not m.etat:
            collision_joueur_mur(p,m)
def collision_cube_mur(c,m,dt=0.016):
    """
    Paramêtres : Cube (Class Cube) , Mur (Class Murs)
    Modifie le cube : vx , vy , col , x , y
    """
    if c.x+c.sx>m.x and c.x<m.x+m.sx and c.y+c.sy+c.vy*dt>=m.y and c.y+c.sy<=m.y:
        c.vy=0
        c.y=m.y-c.sy
        c.col["b"]=True
    if c.x+c.sx>m.x and c.x<m.x+m.sx and c.y+c.vy*dt<=m.y+m.sy and c.y>=m.y+m.sy:
        c.vy=0
        c.y=m.y+m.sy
        c.col["h"]=True
    if c.x+c.sx+c.vx*dt>=m.x and c.x+c.vx*dt<=m.x+m.sx and c.y+c.sy>m.y and c.y<m.y+m.sy:
        if c.x+c.sx<=m.x:
            c.x=m.x-c.sx
            c.col["d"]=True
            c.vx*=-1
        elif c.x<m.x:
            c.x=m.x-c.sx
            c.col["d"]=True
            c.vx*=-1
    if c.x+c.vx*dt<=m.x+m.sx and c.x+c.sx+c.vx*dt>=m.x and c.y+c.sy>m.y and c.y<m.y+m.sy:
        if c.x>=m.x+m.sx:
            c.x=m.x+m.sx
            c.col["g"]=True
            c.vx*=-1
        elif c.x>m.x:
            c.x=m.x+m.sx
            c.col["g"]=True
            c.vx*=-1
def collision_cube_murs(c,ms,dt=0.016):
    """
    Paramêtres : Cube (Class Cube) , Liste de Murs (List Class Mur)
    Modifie le Cube : vx , vy , col , x , y
    """
    for m in ms:
        if not m.etat:
            collision_cube_mur(c,m)
def collision_cube_bouton(c,b,dt=0.016):
    """
    Paramêtres : Cube (Class Cube) , Bouton (Class Bouton)
    Modifie le cube : vx , vy , col , x , y
    Modifie le bouton : etat_p , etat
    """
    #le b.y qu'on veut =b.y+b.sy-b.h[b.anim_name]
    #le b.sy qu'on veut =b.h[b.anim_name]
    if c.x+c.sx>b.x and c.x<b.x+b.sx and c.y+c.sy+c.vy*dt>=b.y and c.y<b.y+b.sy:
        b.etat_p=True
    if c.x+c.sx>b.x and c.x<b.x+b.sx and c.y+c.sy+c.vy*dt>=b.y+b.sy-b.h[b.anim_name] and c.y+c.sy<=b.y+b.sy-b.h[b.anim_name]:
        c.vy=0
        c.y=b.y+b.sy-b.h[b.anim_name]-c.sy
        c.col["b"]=True
        if not b.etat:
            b.action_bouton()
    if c.x+c.sx>b.x and c.x<b.x+b.sx and c.y+c.vy*dt<=b.y+b.sy and c.y>=b.y+b.sy:
        c.vy=0
        c.y=b.y+b.sy
        c.col["h"]=True
    if c.x+c.sx+c.vx*dt>=b.x and c.x+c.vx*dt<=b.x+b.sx and c.y+c.sy>b.y+b.sy-b.h[b.anim_name] and c.y<b.y+b.sy:
        if c.x+c.sx<=b.x:
            c.x=b.x-c.sx-c.vx*dt
            c.col["d"]=True
            c.vx*=-1
        elif c.x<b.x:
            c.vy=0
            c.y=b.y+b.sy-b.h[b.anim_name]-c.sy
            c.col["b"]=True
            if not b.etat:
                b.action_bouton()
    if c.x+c.vx*dt<=b.x+b.sx and c.x+c.sx+c.vx*dt>=b.x and c.y+c.sy>b.y+b.sy-b.h[b.anim_name] and c.y<b.y+b.sy:
        if c.x>=b.x+b.sx:
            c.x=b.x+b.sx-c.vx*dt
            c.col["g"]=True
            c.vx*=-1
        elif c.x>b.x:
            c.vy=0
            c.y=b.y+b.sy-b.h[b.anim_name]-c.sy
            c.col["b"]=True
            if not b.etat:
                b.action_bouton()
def collision_cube_boutons(c,bs,dt=0.016):
    """
    Paramêtres : Cube (Class Cube) , Boutons (Liste Class Bouton)
    Modifie le cube : vx , vy , col , x , y
    Modifie le bouton : etat_p , etat
    """
    for x in bs:
        if c.proprietaire==None:
            collision_cube_bouton(c,x,dt)
def collision_joueur_cube(j,c,dt=0.016):
    """
    Paramêtres : Joueur (Class Joueur) , Cube (Class Cube)
    Modifie le joueur : vx , vy , col , x , y
    Modifie le cube   : vx , vy , col , x , y
    """
    if j.x+j.sx>c.x and j.x<c.x+c.sx and j.y+j.sy+j.vy*dt>=c.y and j.y+j.sy<=c.y:
        j.vy=0
        j.y=c.y-j.sy
        j.col["b"]=True
        c.col["h"]=True
    elif j.x+j.sx>c.x and j.x<c.x+c.sx and j.y+j.vy*dt<=c.y+c.sy and j.y>=c.y+c.sy:
        j.vy=0
        j.y=c.y+c.sy
        j.col["h"]=True
        c.col["b"]=True
    if j.x+j.sx+j.vx*dt>=c.x+c.vx*dt and j.x+j.vx*dt<=c.x+c.sx+c.vx*dt and j.y+j.sy>c.y and j.y<c.y+c.sy:
        if c.x>j.x:
            j.x=c.x-j.sx-j.vx*dt
            j.col["d"]=True
            c.col["g"]=True
            if c.movable and j.canPush:
                c.vx=j.vx
        else:
            j.x=c.x+c.sx-j.vx*dt
            j.col["g"]=True
            c.col["d"]=True
            if c.movable and j.canPush:
                c.vx=j.vx
def collision_joueur_cubes(j,cs,dt=0.016):
    """
    Paramêtres : Joueur (Class Joueur) , Cubes (Liste Class Cube)
    Modifie le joueur : vx , vy , col , x , y
    Modifie les cubes : vx , vy , col , x , y
    """
    for x in cs:
        if x.proprietaire==None:
            collision_joueur_cube(j,x,dt)
def collision_cube_cube(c1,c2,dt=0.016):
    """
    Paramêtres : Cube (Class Cube) , Cube (Class Cube)
    Modifie les cubes   : vx , vy , col , x , y
    """
    if c1.x+c1.sx+c1.vx*dt>=c2.x+c2.vx*dt and c1.x+c1.vx*dt<=c2.x+c2.sx+c2.vx*dt and c1.y+c1.sy+c1.vy*dt>=c2.y+c2.vy*dt and c1.y+c1.vy*dt<=c2.y+c2.sy+c2.vy*dt:
        if c1.x>=c2.x and (c1.vx!=0 or c2.vx!=0):
            if not c1.col["d"]:
                c1.col["g"]=True
                c2.col["d"]=True
                c1.x=c2.x+c2.sx
                vv=c1.m*(c1.vx+c2.vx)/(c1.m+c2.m)
                if c2.movable :c2.vx=vv
                if c1.movable :c1.vx=vv
            else:
                c1.col["g"]=True
                c2.col["d"]=True
                c1.x=c2.x+c2.sx
        elif c1.x<=c2.x and (c1.vx!=0 or c2.vx!=0):
            if not c1.col["g"]:
                c1.col["d"]=True
                c2.col["g"]=True
                c1.x=c2.x-c1.sx
                vv=c1.m*(c1.vx+c2.vx)/(c1.m+c2.m)
                if c2.movable :c2.vx=vv
                if c1.movable :c1.vx=vv
            else:
                c1.col["d"]=True
                c2.col["g"]=True
                c1.x=c2.x-c1.sx
        elif c1.y<=c2.y and c2.vy-c1.vy<0 and (c1.vy!=0 or c2.vy!=0) and c1.x+c1.sx>c2.x and c1.x<c2.x+c2.sx:
            c1.col["b"]=True
            c2.col["h"]=True
            c1.y=c2.y-c1.sy
            c1.vy=c2.vy
def collision_cube_cubes(c,cs,dt=0.016):
    """
    Paramêtres : Cube (Class Cube) , Cubes (Liste Class Cube)
    Modifie les cubes   : vx , vy , col , x , y
    """
    for x in cs:
        if (not (x.x==c.x and x.y==c.y) ) and x.proprietaire==None:
            collision_cube_cube(c,x,dt)
def collision_point_boite(p,b):
    """
    Paramêtre : Point Tuple (x,y) , Boite (Class : x,y,sx,sy)
    Renvoie : Booleen indicant si le point se trouve dans la boite
    """
    return p[0]>=b.x and p[0]<=b.x+b.sx and p[1]>=b.y and p[1]<=b.y+b.sy
def collision_rayon_bloc(r,b):
    """
    Paramêtre : Rayon (Class Rayon) , Bloc (Class Bloc)
    Renvoie : Booleen indicant si il y a une collision , le point de la collision (x,y) , la distance (int) , la normale au plan de collision ("g":0,"d":1,"h":2,"b":3)
    """
    # r : (x,y,dx,dy) pas necessairement normé y vers le bas
    # METHODE : intersection de droite
    if r.dx==0: # cas trivial : droite verticale - prise en compte de la direction
        if r.x>=b.x and r.x<=b.x+b.sx and r.dy*(b.y-r.y)>0:
            point=(r.x,(b.y if r.dy>0 else b.y+b.sy))
            return True,point,distance(point,(r.x,r.y)),2+(r.dy>0)
        else:
            return False,(None,None),None,None
    else: # cas général : récupérer l'équation de la droite décrivant le rayon : (D) := y=ax+h
        a=r.dy/r.dx # coef directeur
        h=r.y-a*r.x # ordonné à l'origine
        points_collisions=[] # points de collision potentiel
        points=[(b.x,b.y),(b.x+b.sx,b.y),(b.x+b.sx,b.y+b.sy),(b.x,b.y+b.sy)] # point du bloc
        trait=[(points[0],points[1]),(points[1],points[2]),(points[3],points[2]),(points[0],points[3])] # arêtes du bloc avec y1<y2 et x1<x2
        for ((x1,y1),(x2,y2)) in trait:
            if x1==x2: # cas arête vertical
                yy=h+a*x1 # y de la collision
                if y1<=yy<=y2: # si la collision est dans le bloc
                    points_collisions.append((x1,yy,(r.dx>0)))
            elif y1==y2: # cas horizontal
                if a!=0: # cas a=0 pas interessant ici
                    xx=(y1-h)/a # x de la collision
                    if x1<=xx<=x2: # si la collision est dans le bloc
                        points_collisions.append((xx,y1,2+(r.dy>0)))
            else: # CAS IMPOSSIBLE
                assert False
        d,x,y,t=-1,0,0,0 # variable pour le recherche de max
        for (xx,yy,tt) in points_collisions:
            dd=distance((xx,yy),(r.x,r.y))
            if dd<=d or d==-1:
                d,x,y,t=dd,xx,yy,tt
        if d==-1: # si il n'y a aucune collision
            return False,(None,None),None,None
        else:
            return True,(x,y),d,t
def collision_rayon_blocs(r,bs,ms=[]):
    """
    Paramêtres : rayon (Class Rayon) , Liste des Blocs (Liste Class Bloc) , Liste des Murs (Liste Class Mur)
    Renvoie : l'indice du bloc collidé (int) , la distance (float) , le point de la collision Tuple (x,y) , angle trigo (float en degre)
    Renvoie : -1 , la distance (float) , le point de la collision Tuple (x,y) , angle trigo (float en degre)    Si un mur est placé devant
    """
    # print(r.x,r.y,r.dx,r.dy,bs[0].x,bs[0].y,bs[0].sx,bs[0].sy)
    i,d,x,y,t=-1,-1,-2,-2,0
    for m in ms:
        if not m.etat:
            a,(xx,yy),dd,tt=collision_rayon_bloc(r,m)
            if a and (xx-r.x)*r.dx>=0 and (yy-r.y)*r.dy>=0 and (dd<d or d==-1):
                d,x,y,t=dd,xx,yy,tt
    for (ii,b) in enumerate(bs):
        a,(xx,yy),dd,tt=collision_rayon_bloc(r,b)
        if a and (xx-r.x)*r.dx>=0 and (yy-r.y)*r.dy>=0 and (dd<d or d==-1):
            i,d,x,y,t=ii,dd,xx,yy,tt
    # print(x,y)
    return i,d,(x,y),[0,180,270,90][t]
def collision_portail_bloc(p,b):
    """
    Paramêtres : Portail (Class Portal_frame) , Bloc (Class Bloc)
    Renvoie : True si il y a une collision False sinon
    """
    if p.angle in [0,180,-180]:
        if p.x+p.sx/2>=b.x and p.x-p.sx/2<=b.x+b.sx and p.y+p.sy/2>=b.y and p.y-p.sy/2<=b.y+b.sy:
            return True
        else:
            return False
    elif p.angle in [90,270,-90]:
        if p.x+p.sy/2>=b.x and p.x-p.sy/2<=b.x+b.sx and p.y+p.sx/2>=b.y and p.y-p.sx/2<=b.y+b.sy:
            return True
        else:
            return False
    else:
        print("ERREUR : Angle non pris en compte dans collision_portail_bloc")
        return False
def collision_portail_blocs(p,bs):
    """
    Paramêtres : Portail (Class Portal_frame) , Blocs (Liste Class Bloc)
    Renvoie : True si il le portail ne peut pas etre placé False sinon
    """
    for b in bs:
        if collision_portail_bloc(p,b):
            if p.angle==180 and b.x<p.x:
                return True
            elif p.angle==90 and b.y<p.y:
                return True
            elif p.angle==0 and b.x+b.sx>p.x:
                return True
            elif p.angle==270 and b.y+b.sy>p.y:
                return True
    return False
def collision_portail_joueur(p,j,dt=0.016):
    """
    Paramêtres : Portail (Class Portal_frame) , joueur (Class Personnage)
    Modifie le perso : portal
    """
    if p.angle in [0,180,-180]:
        if p.x+p.sx/2>=j.x+j.vx*dt and p.x-p.sx/2<=j.x+j.sx+j.vx*dt and p.y+p.sy/2>=j.y+j.vy*dt and p.y-p.sy/2<=j.y+j.sy+j.vy*dt:
            j.portal=p
    elif p.angle in [90,270,-90]:
        if p.x+p.sy/2>=j.x+j.vx*dt and p.x-p.sy/2<=j.x+j.sx+j.vx*dt and p.y+p.sx/2>=j.y+j.vy*dt and p.y-p.sx/2<=j.y+j.sy+j.vy*dt:
            j.portal=p
    else:
        print("ERREUR : Angle non pris en compte dans collision_portail_bloc")
        return False
def collision_portail_cube(p,c,dt=0.016):
    """
    Paramêtres : Portail (Class Portal_frame) , Cube (Class Cube)
    Modifie le perso : portal
    """
    if p.angle in [0,180,-180]:
        if p.x+p.sx/2>=c.x+c.vx*dt and p.x-p.sx/2<=c.x+c.sx+c.vx*dt and p.y+p.sy/2>=c.y+c.vy*dt and p.y-p.sy/2<=c.y+c.sy+c.vy*dt:
            c.portal=p
    elif p.angle in [90,270,-90]:
        if p.x+p.sy/2>=c.x+c.vx*dt and p.x-p.sy/2<=c.x+c.sx+c.vx*dt and p.y+p.sx/2>=c.y+c.vy*dt and p.y-p.sx/2<=c.y+c.sy+c.vy*dt:
            c.portal=p
    else:
        print("ERREUR : Angle non pris en compte dans collision_portail_bloc")
        return False
