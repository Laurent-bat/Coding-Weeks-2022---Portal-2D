from affichage import *


"""
    Dans ce fichier :
        Boucle principale du jeu
"""

while game_variables["running"]:
    if game_variables["game_paused"]:
        if game_variables["music"]:#gestin de la musique
            if pygame.mixer.music.get_busy():
                affichage_menu(game_variables["menu_state"], dt)
            else:
                pygame.mixer.music.load("images/music/level_"+str(game_variables["music_playing"])+".wav")
                pygame.mixer.music.play(0)
                game_variables["music_playing"]+=1
                if game_variables["music_playing"] ==15:
                    pygame.mixer.music.queue("images/music/menus.wav")
                    game_variables["music_playing"]=0
                affichage_menu(game_variables["menu_state"], dt)
        else:
            affichage_menu(game_variables["menu_state"], dt)
    else:
        ########## Calcul du framerate
        perso=entites_variables["perso"]
        blocs=entites_variables["blocs"]
        porte=entites_variables["porte"]
        boutons=entites_variables["boutons"]
        cubes=entites_variables["cubes"]
        murs=entites_variables["murs"]
        dialogue=entites_variables["dialogue"]
        portails=entites_variables["portail"]
        lvc=entites_variables["lvc"]
        dt=0.016 if clock.get_fps()==0 else 1/clock.get_fps()
        ########## Gestion des events
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONUP:
                if not dialogue[0+3*lvc].fini:
                    dialogue[0+3*lvc].fini=True
                    entites_variables["lvc"]=1-entites_variables["lvc"]
            if event.type == pygame.QUIT:
                game_variables["running"] = False  # ferme la fenêtre de jeu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ouvre l'écran de pause
                    game_variables["game_paused"] = True
                if event.key == pygame.K_e:
                    if perso.attache is None:
                        cc, dd = None, -1
                        for c in cubes:
                            ddd = distance(
                                (perso.x+perso.sx/2, perso.y+perso.sy/2), (c.x+c.sx/2, c.y+c.sy/2))
                            if ddd < dd or dd == -1 and c.carriable:
                                cc, dd = c, ddd
                        if not dd == -1 and dd <= distance((-perso.sx/2, -perso.sy/2), (c.sx/2, c.sy/2)):
                            perso.attrape(cc)
                    else:
                        perso.lache()
                perso.deplacement_key_down(event.key)
            if event.type == pygame.KEYUP:
                perso.deplacement_key_up(event.key)
        pos = pygame.mouse.get_pos()
        pos = (pos[0]/ratio_x, pos[1]/ratio_y)
        for x in perso.col.keys():
            perso.col[x]=False
        for b in boutons:
            b.etat_p = False
        perso.portal = None
        for c in cubes:
            c.portal=None
        for p in portails.values():
            if p is not None:
                p.actualise(dt)
                collision_portail_joueur(p, perso)
                for c in cubes:
                    collision_portail_cube(p, c)
        collision_joueur_blocs(perso, blocs, portails,dt)
        collision_joueur_cubes(perso, cubes,dt)
        collision_joueur_murs(perso, murs,dt)
        for x in cubes:
            if x.proprietaire == None:
                collision_cube_blocs(x, blocs, portails, dt)
                collision_cube_boutons(x, boutons, dt)
                collision_cube_murs(x, murs, dt)
        for x in cubes:
            if x.proprietaire == None:
                collision_cube_cubes(x, cubes, dt)
        x, y = -1, -1
        if perso.arme is not None:
            _, _, (x, y), _ = collision_rayon_blocs(Rayon(perso.arme.rayon.x, perso.arme.rayon.y,pos[0]-perso.arme.rayon.x, pos[1]-perso.arme.rayon.y), blocs, murs)
        perso.actualise(pos, x, y,portails,blocs,murs, dt)  # ajouter pos avant le dt
        for x in murs:
            x.actualise(dt)
        for x in cubes:
            x.actualise(dt)
        for b in boutons:
            if not b.etat_p and b.etat == True:
                b.action_bouton()
        if game_variables["level"]==11:
            porte.anim_name="gateau"
            porte.etat=True
        elif not porte.etat and sum([b.etat for b in boutons]) == len(boutons):
            porte.action_porte()
        elif porte.etat and sum([b.etat for b in boutons]) != len(boutons):
            porte.action_porte()
        for m in murs:
            if not m.etat and boutons[m.conditions[0]].etat:
                m.action_mur()
            elif m.etat and not boutons[m.conditions[0]].etat:
                m.action_mur()
        porte.actualise(dt)

        # screen.fill((141,128,112))
        screen.blit(bg[0], (0,0))
        affichage_porte(porte)

        affichage_perso(perso)
        for p in portails.values():
            if p is not None:
                affichage_portal(p)
        for x in cubes:
            if x.proprietaire==None:
                affichage_cube(x)
        for x in blocs:
            affichage_bloc(x)
        for x in boutons:
            affichage_bouton(x)
        for x in murs:
            affichage_mur(x)
        
        if game_variables["level"]==0:
            affichage_dialogue(Dialogue("deplacements:fleches ou Z,Q,S,D",True,100), 800, 100, 500, 100, BLACK, font=menu_font,txt_color=BLANC)
            affichage_dialogue(Dialogue("prendre, lacher le cube: Touche E",True,100), 800, 178, 500, 100, BLACK, font=menu_font,txt_color=BLANC)
            affichage_dialogue(Dialogue("poser un portail bleu: Clic gauche",True,100), 800, 256, 500, 100, BLACK, font=menu_font,txt_color=BLANC)
            affichage_dialogue(Dialogue("poser un portail orange: Clic droit",True,100), 800, 334, 500, 100, BLACK, font=menu_font,txt_color=BLANC)
        if len(dialogue)>0: 
            if lvc==0:
                couleur_1=BLUE
                couleur_2=ROUGE
            if lvc==1:
                couleur_2=BLUE
                couleur_1=ROUGE   
            dialogue[0].actualise()
            dialogue[3].actualise()
            if not dialogue[0+3*lvc].fini:
                affichage_boite_de_dialogue(dialogue[0+3*lvc])
                affichage_dialogue(dialogue[0+3*lvc], 800, 700, 400, 100, BLACK, font=menu_font,txt_color=couleur_1)
                affichage_dialogue(dialogue[1+3*lvc], 800, 825, 400, 100, BLACK, font=menu_font,txt_color=couleur_1)
                affichage_dialogue(dialogue[2+3*lvc], 800, 950, 400, 100, BLACK, font=menu_font,txt_color=couleur_1)
            elif not dialogue[0+3*(1-lvc)].fini:
                affichage_boite_de_dialogue(dialogue[3-3*lvc])
                affichage_dialogue(dialogue[3-3*lvc], 800, 700, 400, 100, BLACK, font=menu_font,txt_color=couleur_2)
                affichage_dialogue(dialogue[4-3*lvc], 800, 825, 400, 100, BLACK, font=menu_font,txt_color=couleur_2)
                affichage_dialogue(dialogue[5-3*lvc], 800, 950, 400, 100, BLACK, font=menu_font,txt_color=couleur_2)
        position_porte=(porte.x+(porte.sx)/2,porte.y+(porte.sy)/2)
        if collision_point_boite(position_porte,perso) and porte.etat:
            game_variables["level"]+=1
            change_levels(game_variables["level"])
        pygame.display.flip()
        clock.tick(60)
        
pygame.quit()
