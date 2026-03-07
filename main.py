import pyxel
import webbrowser
import random
#obj à atteindre pour avoir skin
#faire un fond transparent pour le menu pause

# TODO: verifier que l'esquive marche
        
class Game: #classe qui cree le jeu et qui possede la boucle de jeu
    """classe principale gérant l'ensemble du jeu"""
    def __init__(self,width:int,height:int,nom_jeu:str):
        self.width = width#largeur ecran
        self.height = height#hauteur ecran
        self.nom = nom_jeu #nom du jeu en str
        self.pos_cible = [0,0]#position vers lequel les mobs se dirigent
        self.chute = True
        
        self.debug = False
        self.liste_menu = ["Playing", "GameOver", "Start", "Amelioration"]#liste des menus utilisables dans le jeu
        #Playing: etat de jeu d'attaque contre les mobs
        #GameOver: fin du jeu
        #Start: menu de départ avnt le lancement du jeu
        #Amelioration: choix de la statistique à améliorer        
        
        self.pause = False#en pause si True et jouable quand False
        
        
        self.menu_actuel = "Start"
        self.fps = 30#nombre de frame que le jeu affiche par seconde
        pyxel.init(self.width, self.height, title= "Potato et Le Royaume Infesté",fps=self.fps) #initialisation du jeu
        pyxel.load("res.pyxres")
        
        
        #Etape d'amélioration en 2etapes: 0: choix stat a gagner 1: affichage des stats de la game
        self.etape_stat = 0 #après chaque fin de vague 0 -> choix des stat 1-> reprendre la partie
        self.position_curseur = 0#position du curseur qui permet de choisir quel option on choisit dans les menus
        self.player = Player("JOUEUR1",self)#initialisation joueur
        
        #Creation de liste qui garderont les valeurs de leurs classes respectives
        self.liste_mob = []
        self.liste_balles = []
        self.liste_armes = [Armes("Pistolet",3,1,self,self.player,10),
                            Armes("Sniper",50,5,self,self.player,20),
                              Armes("Mitraillette",2,2,self,self.player,7)]

        self.arme_principale = 0#arme utilisé à un temps t
        self.counter = self.fps*3 #decompte avant fin du jeu pour que l'explosion marche bien 30 est le nb de frame par seconde
        
        
        self.difficulte_max = 100
        
        
        self.liste_difficulte = [1.3, 1.5 ,2]#liste des difficultés possible
        #facile difficile et infernale
        self.difficulte_choisie = 0#indice du niveau de difficulté prenant ses valeurs dans liste_difficulte
        self.num_vague = 0
        self.temps_vague_initiale = 5#variable qui ne change pas#temps par défaut de la vague
        self.temps_vague = 5#temps avant fin de la vague en frame
        
        #stat
        self.nb_kill = 0#compte le nb de kill de mob fait au long de tt les vagues
        self.nb_balles_rates = 0
        
        
        self.choix = []
        #Load la timelape nommé "res.pyrex"
        pyxel.run(self.update, self.draw)
        

        #Postion de la camera
        self.cam_x = 0
        self.cam_y = 0    
    
    
    
    
    def afficher_aide(self):
        """affiche une aide sur les touches pouvant etre utilisées"""
        pyxel.text(16, self.height - self.height//4, "Mouvement : ZQSD", 8)
        pyxel.text(16, self.height - self.height//5, "Attaquer : [ Espace ]", 8)#affiche l'aide
        pyxel.text(16, self.height - self.height//7, "M: autoshoot on/off", 8)
        self.affichage_curseur(pyxel.width//2 -pyxel.width //8 - 18, pyxel.height//3 +9*self.position_curseur, 9)#affiche le curseur lors du choix        
        
    
    
    
    def collisions(self,instance1:object,instance2:object):
        """Appelle les differentes fonctions qui vérifient les collisions
        renvoie True si l'instance 1 est dans l'instance 2
        prend en parametre deux instances"""

        # position x des deux instances
        x1 = instance1.x
        x2=instance2.x
        
        # position y des deux instances
        y1 = instance1.y
        y2=instance2.y
        
        #taille des deux instances pour que les collisions soient plus fidèles 
        taille1 = instance1.taille
        taille2 = instance1.taille
        
        if (x1 <= x2 <= x1+taille1 or x1<= x2+taille2  <= x1+taille1) and (y1 <= y2 <= y1+taille1 or y1<= y2+taille2  <= y1+taille1) :
            return True
    
    def changer_arme_principale(self):
        """change l'arme principale avec la suivante dans la liste des liste_armes possible"""
        dernier_indice_possible = len(self.liste_armes) -1
        if dernier_indice_possible == self.arme_principale:
            self.arme_principale = 0

        else:
            self.arme_principale +=1
        
    def reset_partie(self):
        """méthode qui permet de relancer une partie après une défaite, tt reset au niveau de départ"""
        
        self.changer_menu("Playing")
        self.position_curseur = 0
        self.player = Player("JOUEUR1",self)
        self.liste_mob = []
        self.liste_balles = []
        self.counter = self.fps*3 #decompte avant fin du jeu pour que l'explosion marche bien 30 est le nb de frame par seconde
        self.temps_vague = self.temps_vague_initiale#on reprend la valeur par défaut
        
        self.etape_stat = 0 #après chauqe fin de vague 0 -> choix des stat 1-> reprendre la partie
        self.arme_principale = 0
        self.num_vague =0
        self.nb_kill = 0
        #stats
        self.nb_kill = 0
        self.nb_balles_rates =0


    
            
        

    def update(self):     
        """Met à jour le jeu"""
        
        if self.menu_actuel == "Playing":#menu de combat contre les mobs
            if pyxel.btnp(pyxel.KEY_P):#pour mettre une pause
                if self.pause == False:
                    self.pause =True
                else:
                    self.pause = False
            if self.pause == False:
                self.update_playing()
                
        #-------------------------------------
        #commande de débug et/ou d'aide au dev
        if pyxel.btn(pyxel.KEY_O):
            pyxel.mouse(False)
            print(pyxel.mouse_x, pyxel.mouse_y)
            
        if pyxel.btn(pyxel.KEY_I):
            pyxel.mouse(True)

     

    def update_playing(self):
        """Fonction qui lorsque le mode de jeu est playing met le jeu à jour"""
                
        if self.player.is_alive(): # boucle du jeu qui verifie si le joueur est mort
                #ici si le player est vivant
                self.cam_x = max(0, self.player.x - self.width // 2 + 2) #On evite qu'il puisse sortir de la tilemap
                self.cam_y = max(0, self.player.y - self.height // 2 + 2) #On evite aussi qu'il puisse sortir de la tilemap
                self.player.update()
                
                # if self.player.i %int((self.num_vague+1)*(70 - self.liste_difficulte[int(self.difficulte_choisie)])) ==0:
                
                if self.player.i % (30 *3) ==0:#gère la frequence de pop de mobs au jeu
                    if self.num_vague < 10:
                        for i in range(self.num_vague+1):
                            self.liste_mob.append(Mob(10,10,10,self.player,self, random.randint (1, 4)))
                            # faire apparaitre les mobs dans une liste

                    else: #pour les vagues après la vague 10
                        for i in range(self.num_vague):
                            vie =random.randint(self.num_vague-5,self.num_vague)
                            damage = random.randint(self.num_vague-5,self.num_vague)

                            self.liste_mob.append(Mob(vie,damage,10,self.player,self, random.randint(1, 4)))



                for balle in self.liste_balles:#fais bouger les balles et gère la suppression de celles -ci si on va trop loin
                    balle.move()
                    if balle.is_alive == False:
                        self.liste_balles.remove(balle)

                
                    for mob in self.liste_mob:
                        if self.collisions(mob,balle):
                            mob.degat(self.player.attaque*balle.arme_instance.degats) #degats au mob selon les points d'attaque du joueur
                            balle.is_alive = False
                        if not mob.is_alive():
                            self.nb_kill +=1#augmente le nb de kill de la partie


                for mob in self.liste_mob:#verifie collision entre le joueur et le mob et donne des dégats au joueur si collision
                    if pyxel.frame_count % 15 ==0:
                        self.pos_cible = [self.player.x,self.player.y] #envoie cible des mobs pour ajouter un deplacement moins linéaire
                    if self.collisions(self.player,mob):
                        self.player.degats()


                    mob.update(self.pos_cible)
                    if not mob.is_alive():
                        self.liste_mob.remove(mob)
                
                

                            
                #implémentation de la fin de la vague
                
                
                if self.temps_vague <= 0:
                    print("fin")
                    self.changer_menu("Amelioration")
                elif self.player.i % self.fps == 0 :
                    self.temps_vague -= 1
                    

                        

                
                        
        else:
            
            self.counter-=1 
            if len(self.player.liste_explosions) !=0 or (len(self.player.liste_explosions) ==1 and self.player.liste_explosions[0].taille_max == self.player.liste_explosions[0].etape-1):
                
                    self.player.update()
                    self.player.draw_explosions()
                
            
            
            if  self.counter <=0 or (len(self.player.liste_explosions) ==1 and self.player.liste_explosions[0].taille_max == self.player.liste_explosions[0].etape+1):
                self.changer_menu("GameOver")
            
       
            

        


    def draw(self):
        """permet d'afficher tout les éléments du jeu"""
        if self.menu_actuel =="Playing" and self.pause== False:
            #On règle la camera
            pyxel.camera(self.cam_x, self.cam_y)
            pyxel.cls(0)
            
            #On dessine la tilemap
            pyxel.bltm(0,0,0, self.cam_x, self.cam_y, 1000, 1000)
            
            if self.debug:
                self.player.draw_hitbox()
    
            for mob in self.liste_mob:
                    if self.debug:
                        mob.draw_hitbox()
                    mob.draw()
            for balle in self.liste_balles:
                balle.draw()

            self.player.draw()
            
            #On remet la camera à 0,0 pour garder l'UI fixe
            pyxel.camera()

            pyxel.text(self.width-15, 5, str(self.temps_vague), 7)#affiche le temps restant avant la fin de la vague
            pyxel.text(self.width//2, 5,str(self.num_vague), 7)#affiche num de vague
        
        if self.menu_actuel == "Start":
            self.draw_menu_start()
        
        elif self.menu_actuel == "Amelioration":
            self.draw_menu_stat()
            
        elif self.menu_actuel == "GameOver":#si le joueur est mort
            self.draw_menu_fin()
            
        
        if self.chute:
            #ligne a modifier si on veut le réutiliser
            self.draw_chute_nb(19- (pyxel.frame_count//3))
        
        
            
        
        if self.pause == True:
            self.draw_menu_pause()
    def draw_chute_nb(self, count):
        #(19- (pyxel.frame_count//7))
        if count != 0:
            pyxel.rect(0, 0, 128, 131-(7*(19-count)), 0)
            for j in range(count):
                s = ""
                for i in range(18): 
                    s= s+ str(int((random.random()*100)))
                
                # s.replace(".", "", -1)
                pyxel.text(0, 0+7*j, s, 3)#3 11
        else:
            self.chute = False
            

    def draw_menu_start(self):
        """dessine le menu de départ lorsque le menu est 'Start' dans lequel on choisit de jouer on de quitter le jeu"""
        pyxel.cls(0)        
        
        #décor arrière plan qui défile (cascade?)
        # pyxel.bltm(0, 0, 0, 0, 0, self.width, self.height)A ESSAYER SUR CAPYTALE
        
        option = {0: "Jouer",
                  1: "Credit",
                  2: "Sortie"}#tableau des options possible
        
        for i in range(len(option)):
            pyxel.text(pyxel.width//2 -18, pyxel.height//3 +9*i, option[i], 9)
        
        self.afficher_aide()
        
        
        
        option_choisie = self.choix_option(option)
        if  option_choisie != None:
            if option_choisie ==0:
                self.changer_menu("Playing")
            elif option_choisie ==1:
                print("Redirection vers le Github")
                webbrowser.open_new("https://github.com/quentinpags/POO_Project1")
                
            elif option_choisie ==2:
                webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
                pyxel.quit()#on quitte le jeu
                
    def draw_menu_pause(self):
        """dessine le menu Pause lors de l'appuie sur la touche P"""
        pyxel.cls(0)
        pyxel.text(self.width//2-10, 1, "Pause", 6)
        option = {0: "Continuer",
                  1: "Sortie"}#tableau des options possible lors dans le menu pause
        
        for i in range(len(option)):
            pyxel.text(pyxel.width//2 -15, pyxel.height//3 +9*i, option[i], 9)
        
        self.afficher_aide()
        
        
        
        option_choisie = self.choix_option(option)
        if  option_choisie != None:
            if option_choisie ==0:
                self.pause = False
            
            elif option_choisie ==1:
                webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
                pyxel.quit()
        
    
               
    def draw_menu_stat(self):
        """menu après une vague pour choisir une statistique"""
        
        pyxel.cls(0)
        if self.choix == []:
            
            for i in range(1,4):
                choix= random.random()
                self.choix.append(choix)
        
        
        if self.etape_stat ==0:
            for i in range(1,4):
                
                #Affichage des noms des boosts
                #1. Couleur des textes
                x_boost = self.width // 4 - 90 + 45 * i
                y_boost = self.height // 2

                if self.choix[i-1] < 0.20:
                    pyxel.bltm(x_boost, y_boost, 0, 64, 1280, 64, 64)
                    nom_boost = "FORCE"
                    couleur = 10 
                
                elif self.choix[i-1] < 0.40:
                    pyxel.bltm(x_boost, y_boost, 0, 64, 1216, 64, 64)
                    nom_boost = "DEFENSE"
                    couleur = 12 
                    
                else:
                    pyxel.bltm(x_boost, y_boost, 0, 0, 1216, 64, 64)
                    nom_boost = "VIE +"
                    couleur = 8 
                    

                # 2. Affichage du texte
                x_texte = x_boost + (32 - len(nom_boost) * 4 // 2)
                pyxel.text(x_texte, y_boost - 10, nom_boost, couleur)
                        
                #Affichage des sprites des boosts

                if self.choix[i-1] <0.20:
                    #force
                    pyxel.bltm(self.width//4-90 +45*i, self.height//2, 0, 64, 1280, 64, 64, scale=1)
                    if self.debug:
                        pyxel.rect(self.width//4-90 +45*i, self.height//2, 18, 18, 9)
                        pyxel.text(self.width//4-90 +45*i, self.height//2, "Force +", 2)
                    
                elif self.choix[i-1] < 0.40:
                    pyxel.bltm(self.width//4-90 +45*i, self.height//2, 0, 64, 1216, 64, 64, scale=1)
                    if self.debug:
                        pyxel.rect(self.width//4-90 +45*i, self.height//2, 18, 18, 9)#defense
                        pyxel.text(self.width//4-90 +45*i, self.height//2, "Defense +", 2)
                # elif self.choix[i-1] <0.60:
                #     pyxel.bltm(self.width//4-90 +45*i, self.height//2, 0, 0, 1216, 64, 64, scale=1)
                #     if self.debug:
                #         pyxel.rect(self.width//4-90 +45*i, self.height//2, 18, 18, 9)#regen
                #         pyxel.text(self.width//4-90 +45*i, self.height//2, "Regen +",2)
                
                else:
                    pyxel.bltm(self.width//4-90 +45*i, self.height//2, 0, 0, 1216, 64, 64, scale=1)
                    if self.debug:
                        pyxel.rect(self.width//4-90 +45*i, self.height//2, 18, 18, 9)
                        pyxel.text(self.width//4-90 +45*i, self.height//2, "Vie +",2)
                    #vie_max
                # else:
                #      pyxel.bltm(self.width//4-90 +45*i, self.height//2, 0, 0, 1280, 64, 64)
                #      if self.debug:
                #          pyxel.rect(self.width//4-90 +45*i, self.height//2, 18, 18, 9)#degats
                #          pyxel.text(self.width//4-90 +45*i, self.height//2, "Vitesse +", 2) 
                #      pyxel.bltm(self.width//4-90 +45*i, self.height//2, 0, 64, 1280, 64, 64, scale=1)
                #      if self.debug:
                #         pyxel.rect(self.width//4-90 +45*i, self.height//2, 18, 18, 9)
                #         pyxel.text(self.width//4-90 +45*i, self.height//2, "Force +", 2)
                
                    
                 
         
            choix_option = self.choix_option(self.choix)
            
            if choix_option != None:
                if choix_option == 0:
                    self.choix_stat(self.choix[0])
                    
                    
                elif choix_option == 1:
                    self.choix_stat(self.choix[1])
                    
                    
                elif choix_option == 2:
                    self.choix_stat(self.choix[2])
                    
                self.etape_stat = 1
                
                
            self.affichage_curseur(self.width//4-20 +47*self.position_curseur, self.height - 20, 7)

            #Caractéristiques du titre affiché dans l'étape 0 des stats

            message = "CHOISISSEZ VOTRE BOOST"# Affiche le titre du choix de stat

            # (Largeur écran / 2) - (Longueur du texte * 4 / 2) 
            x_texte = (pyxel.width // 2) - (len(message) * 4 // 2)

            pyxel.text(x_texte, 35 , message, 7) 
            pyxel.rect(0, 5, pyxel.width, 15, 1)  # rectangle de fond du titre
            pyxel.line(0, 5, pyxel.width, 5, 7) 
            pyxel.line(0, 20, pyxel.width, 20, 7) #lignes séparant le texte
            pyxel.text(x_texte, 10, "AMELIORATION DISPONIBLE !", 7) 
                
        elif self.etape_stat ==1:
            
            opt= ["vie : "+str(self.player.vie_max), "degats / attaques : "+str(self.player.attaque),"defense : "+str(self.player.defense), "vitesse : "+str(self.player.vitesse),
                  "ennemis tues : "+str(self.nb_kill),"balles rates : "+str(self.nb_balles_rates)]
            for i in range(len(opt)):
                pyxel.text(0, 0+8*i, opt[i], 12)
            
            
            option = {0:"Vague Suivante",
                      1:"Changer de perso"}
            
            choix_option = self.choix_option(option)
            if choix_option == 0:
                self.player.vie = self.player.vie_max
                self.changer_menu("Playing")
                self.creer_nouv_vague()
                self.choix = []
            
            elif choix_option == 1:
                #change l'etat de skin
                if self.player.ensemble_skin_actuel == self.player.skin2:
                    self.player.ensemble_skin_actuel = self.player.skin1
                else:
                    self.player.ensemble_skin_actuel = self.player.skin2
                
            pyxel.blt(self.width-20, self.height-20, 0, self.player.ensemble_skin_actuel["h"][0], self.player.ensemble_skin_actuel["h"][1], 16,16, colkey=2)
            #le skin à la hauteur h a des coordonnées qui sont dans l'angle en haut à gauche de la plaquette de sprite, on fait un carré à partir de ça et cela marche
            pyxel.text(0, 90, "-------------------------------------------------------------", 9)
            
            self.affichage_curseur(self.width//8 +3, self.height//2+30+self.position_curseur*8, 9)
            for j in range(len(option)):
                pyxel.text(self.width//8 +25, self.height//2+30+8*j, option[j], 9)
                
                
            
            
    def choix_stat(self, nb):
        """ajoute des points de stat en fonction de l'aptitude choisie dans la fonction choix_option"""
        
        if nb <0.20:
            self.player.ajouter_statistique("attaque", 5)#force  
            print("ajout de force")
            
        elif nb < 0.40:
            self.player.ajouter_statistique("defense", 0.05)#defense#5% de dégats en -
            print("ajout de defense")
        # elif nb <0.60:
        #     self.player.ajouter_statistique("regeneration", 5)#regen
        #     print("ajout de regen")
        else:
            self.player.ajouter_statistique("vie", 5)#vie_max
            print("ajout de vie")
        # else:
        #     self.player.ajouter_statistique("esquive", 1)#degats
        #     print("ajout d'esquive")
            
            
    def draw_menu_fin(self):
        """Fonction qui affiche le jeu lorsque le mode de jeu est fin"""
        
        pyxel.cls(9)
        pyxel.text(pyxel.width//2 -18, pyxel.height//3 +9, "Game Over", 0)
        option = {0:"Try Again",
                  1:"Sortie"}
        
        
        for i in range(len(option)):#crée l'affichage du menu
            pyxel.text(pyxel.width//2 -18, pyxel.height//3 +30 +10*i, option[i], 8)
        
        
        
        #COPIE DE draw_menu_start:
        option_choisie = self.choix_option(option)
        self.affichage_curseur(pyxel.width//2 -32, pyxel.height//3 +30 +10*self.position_curseur, 0)#affiche le curseur lors du choix

        if  option_choisie != None:
            if option_choisie ==0:
                self.reset_partie()
             
                
            elif option_choisie ==1:
                webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
                pyxel.quit()

    def affichage_curseur(self, x, y, col):
        pyxel.text(x, y, "<X>", col)
        
    def menu(self):
        """debug pour savoir ds quel menu on est"""
        if self.menu_actuel == "GameOver":
            print('This is the end...')
        
        elif self.menu_actuel == "Pause":
            print('pause activée')
            
        elif self.menu_actuel == "Start":
            print('Menu de départ')
            
            
        elif self.menu_actuel =="Playing":
            print('partie en cours')
    
    def changer_menu(self, menu_remplacement):
        """change le menu actuel par le menu_remplacement"""
        
        #verifie que le menu est dans la liste des menus utilisables
        for menu in self.liste_menu:
            if str(menu_remplacement) == str(menu) :
                self.menu_actuel = str(menu_remplacement)
                
    def choix_option(self, liste_option):
        """gere l'appuie sur les touches haut bas et entree pour rendre le menu fonctionnel
        et renvoie l'id  de la position du curseur"""
        if pyxel.btnr(pyxel.KEY_UP) or pyxel.btnr(pyxel.KEY_LEFT):
            self.position_curseur -= 1
        
        elif pyxel.btnr(pyxel.KEY_DOWN) or pyxel.btnr(pyxel.KEY_RIGHT) :
            self.position_curseur += 1
            
        if self.position_curseur <0:
            self.position_curseur = len(liste_option)-1
        
        if self.position_curseur > len(liste_option)-1:
            self.position_curseur = 0
            
        if  self.chute == False and (pyxel.btnr(pyxel.KEY_RETURN) or pyxel.btnr(pyxel.KEY_KP_ENTER)):
            return self.position_curseur
        
        elif pyxel.btn(pyxel.KEY_A):#pour choisir aléatoirement un menu
            return random.randint(0, len(liste_option)-1)
    
        
    def creer_nouv_vague(self):
        self.player.x = pyxel.width//2 -2 #faire spawn le perso au milieu de l'écran
        self.player.y = pyxel.height//2 -2
        self.liste_balles = []
        self.liste_explosion = []
        self.liste_mob = []
        self.num_vague +=1
        self.changer_menu("Playing")
        self.temps_vague = int(self.temps_vague_initiale* ((self.num_vague+1) *self.liste_difficulte[int(self.difficulte_choisie)]))#cycle de vague/amelioration voir ligne44
        self.etape_stat = 0
        
        
        

    
    

class Player: #classe qui cree le joueur
    def __init__(self,nom:str,game_instance:object):
        """In: nom -> le nom du joueur"""

        self.nom = nom
        self.x = pyxel.width//2 -2 #faire spawn le perso au milieu de l'écran
        self.y = pyxel.height//2 -2
        self.defense = 0
        self.attaque = 1
        self.vie_max = 200 #vie initiale
        self.vie = 10
        self.game_instance = game_instance
        self.vitesse = 1 #vitesse de deplacement
        self.esquive = 0 #pourcentage de chance qu'il esquive des dégats
        self.regeneration = 1#% de vie par secondes
        self.cote = "g"#va a gauche
        self.liste_explosions = []
        self.taille = 8
        self.i =0# variable qui permet de compter chaque iteration de la fonction update et permet d'enlever dépendance a pyxel.frame_count, se met a jour quand le player est update donc quand le jeu est en train de tourner (evite les bugs avec les pauses) 
        
        self.autoshoot = True
        
        self.last_damage = 0
        self.last_shot = 0
        
        
        
        self.skin1 = {"b":[8, 48, 8, 8], "h":[0, 48, 8, 8],"g":[8, 56, 8, 8],"d":[8, 56, -8, 8]}#définition des coordonées de chaque coté du skin
        self.skin2 = {"b":[72, 64, 8, 8], "h":[64, 64, 8, 8],"g":[72, 72, 8, 8],"d":[72, 72, -8, 8]}
        
        self.ensemble_skin_actuel = self.skin1 #montre quel skin est le utilisé actuellement
        
        # self.tir_possible = True#permet de fluidifier le tir
        
        # self.num_skin ={0:[[x, y, img, u, v, w, h],[x, y, img, u, v, w, h]]}#comporte l'id du skin et les différentes animations
    
        
    
    def regen(self):
        """redonne de la vie au player """
        if self.vie < self.vie_max:
            if self.last_damage > 30 and self.last_shot > 30 and self.i % 15 == 0:
                self.vie += 3
        else:
            self.vie = self.vie_max
            
            

                
    def ajouter_statistique(self, type_statistique, montant):
        """ajoute des le type de statistique au joueur"""

        if type_statistique == "esquive":
            self.esquive += montant
        elif type_statistique == "attaque":
            self.attaque += montant
        
        elif type_statistique == "vie":
            self.vie_max += montant #on augment plus la vie que la vit et l'att car plus de dégats causés
        
        elif type_statistique == "regeneration":
            self.regeneration += montant 
        elif type_statistique == "defense":
            self.defense += montant
     
        
    
    def boutons(self):
        """Fonction qui permet de gérer la fonctions des touches"""

        if self.is_alive():
            if pyxel.btn(pyxel.KEY_D): # aller a droite
                if (self.x < 500) :#eviter de sortir de l'écran
                    self.x = self.x + self.vitesse

            if pyxel.btn(pyxel.KEY_Q):#aller a gauche
                if (self.x > 0) :
                    self.x = self.x - self.vitesse
                    

            if pyxel.btn(pyxel.KEY_S): #descendre
                if (self.y <500) : #eviter de sortir de l'écran
                    self.y = self.y + self.vitesse
            if pyxel.btn(pyxel.KEY_Z): #monter
                if (self.y > 0) : 
                    self.y = self.y - self.vitesse
                    
            if self.autoshoot == True:
                if self.game_instance.liste_armes[self.game_instance.arme_principale].peut_tirer():
                    self.game_instance.liste_armes[self.game_instance.arme_principale].creer_balle()
                    self.last_shot = 0
                    
            elif self.autoshoot == False: 
            
                if pyxel.btn(pyxel.KEY_SPACE):
                    if self.game_instance.liste_armes[self.game_instance.arme_principale].peut_tirer():
                        self.game_instance.liste_armes[self.game_instance.arme_principale].creer_balle()
                        self.last_shot = 0
            
            
                
                    
            if pyxel.btnr(pyxel.KEY_M):
                if self.autoshoot == True:
                    self.autoshoot = False
                elif self.autoshoot == False:
                    self.autoshoot = True
                

            
            #visee avec les touches de directions:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.cote = "d"
            if pyxel.btn(pyxel.KEY_LEFT):
                self.cote = "g"
            if pyxel.btn(pyxel.KEY_UP):
                self.cote = "h"
            if pyxel.btn(pyxel.KEY_DOWN):
                self.cote = "b"
                
            
            if pyxel.btnp(pyxel.KEY_U) : #pour le debug
  
                self.game_instance.changer_arme_principale()



            
     
        
    def degats(self,nb_degats:int=1):
        """
        Fonction qui prend en parametre le nb de degats a enlever au joueur
        et lui enlève
        """
        chance = random.randint(0,100)
        esquive = 1
        if self.esquive < 60:
            if chance < self.esquive: #si le joueur arrive a esquiver
                esquive = 0#esquive = 0 si player arrive à  et 1 si arrive pas
        elif self.esquive >=60:
            if chance <= 60:
                esquive = 0
        if self.defense <70:
            self.vie -= (1-self.defense) *nb_degats * esquive
        elif self.defense >=70:
            self.vie -= 0.30 *nb_degats * esquive
            
        
        
        if self.vie <0:
            self.vie =0
        if self.is_alive():
            self.liste_explosions.append(Explosion(self.x,self.y))
        else:
            self.liste_explosions.append(Explosion(self.x,self.y,150))
            
            
        if esquive == 1:#si on arrive pas à esquiver l'attaque
            self.last_damage = 0


        
            

        


    def is_alive(self):
        """
        Fonction qui renvoie True si le joueur est vivant (vie>0)
        """
        if self.vie > 0:
            return True
        
        else:
            return False

    def update(self):
        """déplacement avec les touches de direction"""
        for explosion in self.liste_explosions:
            if not explosion.is_alive():
                self.liste_explosions.remove(explosion)

        self.boutons() #verifie appui de boutons
        self.i+=1
        self.last_damage, self.last_shot = self.last_damage + 1, self.last_shot + 1
        self.regen()#gère l'ajout de vie si inactivité de la part du joueur


    def draw(self):
        """Permet de dessiner le joueur"""
        self.draw_explosions()
        if self.is_alive():
            
            # pyxel.rect(self.x,self.y,5,5,6) debug player
            self.draw_health()
            
            # if self.cote == "b": #le player tire vers le bas 
            #     pyxel.blt(self.x, self.y, 0, 8, 48, 8, 8, colkey=2)

            # elif self.cote == "h": #le player tire vers le haut 
            #     pyxel.blt(self.x, self.y, 0, 0, 48, 8, 8,colkey=2)

            # elif self.cote == "g":  #le player tire vers la gauche 
            #     pyxel.blt(self.x, self.y, 0, 8, 56, 8, 8,colkey=2)

            # elif self.cote == "d":  #le player tire vers la droite 
            #     pyxel.blt(self.x, self.y, 0, 0, 56, 8, 8,colkey=2)
            
            pyxel.blt(self.x, self.y, 0, self.ensemble_skin_actuel[self.cote][0], self.ensemble_skin_actuel[self.cote][1], self.ensemble_skin_actuel[self.cote][2], self.ensemble_skin_actuel[self.cote][3], colkey=2)

        self.draw_health()

    def draw_hitbox(self):
        """Permet de dessiner la hitbox du joueur
        Pour le DEBUG"""
        pyxel.rect(self.x-1,self.y-1,7,7,9) #7= taille player + 2 pour que l'on voie un peu le rectangle

    
    def draw_explosions(self):
        """Dessine les explosions du joueur"""
        x = self.x
        y = self.y
        for explosion in self.liste_explosions:
            if explosion.is_alive():
                explosion.x =x+2
                explosion.y = y+2
                explosion.draw()


    def draw_health(self):
        """affiche la barre de vie à gauche"""
        
       # for i in range(self.vie):
       #     pyxel.rect(8*i, 0, 8, 8, 1+i)
        height = 6   
        length = 31
        col = 3
        
        
        
        if self.vie_max //2 > self.vie:
            col = 4
        elif self.vie_max //3 > self.vie:
            col = 5
        
        
        if self.vie >=1:
            pyxel.rect(1+self.game_instance.cam_x, 1+self.game_instance.cam_y, length*(self.vie/self.vie_max), height, col)
            pyxel.rect(1+length*(self.vie/self.vie_max)+ self.game_instance.cam_x, 1+self.game_instance.cam_y, length - length*(self.vie/self.vie_max), height, 0)
            
        
        
            
        
         
            
            
            
            
            
        pyxel.rectb(0+self.game_instance.cam_x, 0+self.game_instance.cam_y, 32, 8, 6)#contour de la barre de vie
        # pyxel.rectb(0, 0, 3.2*(i+1), 8, 2)
class Armes:
    def __init__(self,nom:str,degats:int,vitesse:int, game_instance:object,player_instance:object,frequence:int):
        """ 
        nom: nom de l'arme
        vitesse: vitesse des balles
        Frequence : + c'est bas plus les balles sont rapprochées
        """

        self.nom = nom
        self.degats = degats #ajouter degats aux balles
        self.vitesse = vitesse
        self.game_instance = game_instance
        self.player_instance = player_instance
        self.frequence = frequence
        self.frequence_i = 0

    def peut_tirer(self):
        """Renvoie True si la balle peut etre tiree"""
        self.frequence_i +=1
        if self.frequence == self.frequence_i:
            self.frequence_i = 0
            return True
        
        else:
            return False
        

    def creer_balle(self):
        self.game_instance.liste_balles.append(Bullets(self.player_instance.x,
                                                        self.player_instance.y,
                                                        self.player_instance.cote,
                                                        self.game_instance,
                                                        self,
                                                        self.vitesse,
                                                        self.game_instance.arme_principale
                                                        ))

class Bullets:
    def __init__(self,x:int,y:int,direction:str,game_instance:object,instance,vitesse:int = 1,type_arme = 0):
        self.x = x
        self.y = y
        self.direction = direction #"g"gauche,"d"droite,"b"bas,"h"haut
        self.vitesse = vitesse
        self.type_arme = type_arme
        self.is_alive = True
        self.game_instance = game_instance
        self.arme_instance = instance
        self.player = Player("JOUEUR1",self)
        self.liste_armes = [Armes("Pistolet",3,1,self,self.player,10),
                            Armes("Sniper",50,5,self,self.player,20),
                              Armes("Mitraillette",2,2,self,self.player,7)]

    def move(self):
        if self.direction == "g":
            self.x -= self.vitesse

        elif self.direction == "d":
            self.x +=self.vitesse
        
        elif self.direction == "b":
            self.y +=self.vitesse

        elif self.direction == "h":
            self.y -=self.vitesse

        if ((self.x<0 or self.x > 550) or (self.y<0 or self.y > 550)):
            self.is_alive = False
            self.game_instance.nb_balles_rates +=1
            

    def draw(self):
        #pyxel.rect(self.x,self.y, 2,2,9)
        #Cette fonction permettra d'avoir différents types de munitions en fonction de l'arme
        arme = self.type_arme
        if arme == 0 or 2: # 0 correspond au Pistolet et 2 à la Mitrailleuse   
            if self.direction == "h":
                pyxel.blt(self.x, self.y, 0, 32, 32, 8, 8,colkey=2)
            if self.direction == "b":
                pyxel.blt(self.x, self.y, 0, 32, 40, 8, 8,colkey=2)
            if self.direction == "g":
                pyxel.blt(self.x, self.y, 0, 40, 40, 8, 8,colkey=2)
            if self.direction == "d":
                pyxel.blt(self.x, self.y, 0, 40, 32, 8, 8,colkey=2)
        
        if arme == 1:
            if self.direction == "h":
                pyxel.blt(self.x, self.y, 0, 48, 32, 8, 8,colkey=2)
            if self.direction == "b":
                pyxel.blt(self.x, self.y, 0, 48, 40, 8, 8,colkey=2)
            if self.direction == "g":
                pyxel.blt(self.x, self.y, 0, 56, 40, 8, 8,colkey=2)
            if self.direction == "d":
                pyxel.blt(self.x, self.y, 0, 56, 32, 8, 8,colkey=2)

class Mob:
    def __init__(self, vie:int, damage:int, attack_speed:int, player:object,game_instance:object, type_mob):
        """initialisation de la creation de mob
        Player est la l'instance du joueur """
        self.vie = vie
        self.damage = damage
        self.attack_speed = attack_speed
        self.vitesse = 1
        self.taille = 5
        self.game_instance = game_instance
        self.type_mob = type_mob
        self.cote_Mob = "b"#Le Mob va vers le bas
        self.frame_count = 0
        
        positionnement = random.randint(1,4)
        if positionnement == 1: #fait spawn les mobs en haut 
            self.x= random.randint(self.game_instance.cam_x + 2,self.game_instance.cam_x+pyxel.width-7)
            self.y = -5

        elif positionnement == 2: #fait spawn les mobs à gauche
            self.x = self.game_instance.cam_x -5
            self.y = random.randint(self.game_instance.cam_y + 2,self.game_instance.cam_y + pyxel.height-7)

        elif positionnement == 3:#fait spawn les mobs à droite
            self.x = self.game_instance.cam_x +pyxel.width
            self.y = random.randint(self.game_instance.cam_y + 2, self.game_instance.cam_y +pyxel.height-7)

        elif positionnement == 4: #fais spawn les mobs en bas
            self.x = random.randint(self.game_instance.cam_x + 2, self.game_instance.cam_x +pyxel.width-7)
            self.y = self.game_instance.cam_y + pyxel.height


        self.cooldown_state = 3
        self.cooldown_max = random.randint(3,7)
        self.player = player
    

       
    def is_alive(self):
        """renvoie True si le mob est mort"""
        if self.vie > 0:
            return True
        elif self.vie <= 0:
            return False
        
    def peut_bouger(self):
        """renvoie True si le mob peut bouger
        sinon renvoie False"""
        if self.cooldown_state == 0:
            self.cooldown_state = self.cooldown_max
            return True
        else:
            self.cooldown_state -=1
            return False
    
    def degat(self,nb_degats:int):
        """Fais descendre les Points de vie du mob en fonction du nombre de dégat reçu"""
        self.vie -= nb_degats
            
    
    def update(self, tableau_cible:list):
        """Prend en parametre tableau contenant les coordonnes cibles vers lesquels ils doivent se deplacer 
        tableau sous forme [x,y]
        la variable cooldown existe pour que les mobs se deplacent de facon plus saccadees"""

        self.frame_count += 1 #le compteur de frame augmente de 1 à chaque frame
        if self.peut_bouger():
            #verifie si le mob peut jouer -> verifie son cooldown est ok;permet que le mob avance de maniere plus 'zombie' 
            self.move(tableau_cible)
            
    def move(self, tableau_cible:list):
        """Deplace le mob vers le joueur et met à jour sa direction"""
        player_x = tableau_cible[0]
        player_y = tableau_cible[1]
        mob_x = self.x
        mob_y = self.y
        
        if player_y-5 >= mob_y:
            self.y += self.vitesse
            self.cote_Mob = "b" #permet au mob de regarder vers le bas si le joueur est plus bas que lui

        elif player_y+5 <= mob_y:
            self.y -= self.vitesse
            self.cote_Mob = "h" #permet au mob de regarder vers le haut si le joueur est plus haut que lui

        if player_x+5 <= mob_x:
            self.x -= self.vitesse

        elif player_x-5 >= mob_x:
            self.x += self.vitesse
        

    def draw(self):
        if self.player.is_alive():
            

            # On calcule quel sprite utiliser (0 ou 1) et on divise par 10 pour changer de sprite toutes les 10 frames (vitesse de l'animation)
            animation_frame = (self.frame_count // 10) % 2 
        
            # Calcul de l'offset X sur la planche de sprites
            # Si l'animation_frame est 0, l'offset est 0
            # Si l'animation_frame est 1, l'offset est 8 (largeur du sprite)
            u_offset = animation_frame * 8
            if self.type_mob == 1:

                if self.cote_Mob == "b": 
                    # le sprite 1 est en (0, 64), le sprite 2 est en (8, 64)
                    pyxel.blt(self.x, self.y, 0, 0 + u_offset, 64, 8, 8, colkey=2)

                elif self.cote_Mob == "h": 
                    # le sprite 1 est en (0, 72), le sprite 2 est en (8, 72) 
                    pyxel.blt(self.x, self.y, 0, 0 + u_offset, 72, 8, 8, colkey=2)

            elif self.type_mob == 2:

                if self.cote_Mob == "b": 
                    # le sprite 1 est en (0, 80), le sprite 2 est en (8, 80)
                    pyxel.blt(self.x, self.y, 0, 0 + u_offset, 80, 8, 8, colkey=2)

                elif self.cote_Mob == "h": 
                    # le sprite 1 est en (0, 88), le sprite 2 est en (8, 88) 
                    pyxel.blt(self.x, self.y, 0, 0 + u_offset, 88, 8, 8, colkey=2)

            elif self.type_mob == 3:

                if self.cote_Mob == "b": 
                    # le sprite 1 est en (0, 128), le sprite 2 est en (8, 128)
                    pyxel.blt(self.x, self.y, 0, 0 + u_offset, 128, 8, 8, colkey=2)

                elif self.cote_Mob == "h": 
                    # mêmes sprites car ce mob n'a pas de sprite de lui regardant le joueur vers le haut 
                    pyxel.blt(self.x, self.y, 0, 0 + u_offset, 128, 8, 8, colkey=2)

            elif self.type_mob == 4:

                if self.cote_Mob == "b": 
                    # le sprite 1 est en (32, 128), le sprite 2 est en (40, 128)
                    pyxel.blt(self.x, self.y, 0, 32 + u_offset, 128, 8, 8, colkey=2)

                elif self.cote_Mob == "h":  
                    pyxel.blt(self.x, self.y, 0, 32 + u_offset, 128, 8, 8, colkey=2)

                
        


    def draw_hitbox(self):
            """Dessine hitbox Mob"""
            pyxel.rect(self.x-1,self.y-1,7,7,9) #7= taille mob + 2 pour que l'on voie un peu le rectangle
    
    
class Explosion:
    def __init__(self ,x:int,y:int,taille_max:int= 5):
        self.taille_max = taille_max
        self.x = x+2#pour que l'explosion ait pour centre a peu près le centre du player (vu que le player fait 5 par 5)
        self.y = y+2
        self.etape = 0
        self.alive = True
        
    
    def draw(self):
        """Dessine les explosions"""
        
        
        self.etape += 1
        pyxel.circ(self.x,self.y,self.etape,9)

    def is_alive(self):
        """Renvoie True si l'explosion est encore en vie 
        -> doit encore être visible"""
        if self.etape == self.taille_max:
            self.alive = False
        return self.alive
        

jeu = Game(128,128,"JEU")#lance le jeu

