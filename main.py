import pyxel
import webbrowser
import random



        
class Game: #classe qui cree le jeu et qui possede la boucle de jeu
    def __init__(self,width:int,height:int,nom_jeu:str):
        self.width = width
        self.height = height
        self.nom = nom_jeu #str
        self.hitbox = False
        self.pos_cible = [0,0]#position vers lequel les mobs se dirigent
        
        
        
        self.liste_menu = ["Playing", "GameOver", "Start", "Amelioration"]#liste des menus disponibles
        self.pause = False
        
        self.menu_actuel = "Start" 
        self.fps = 30
        pyxel.init(self.width, self.height, title= "Potato et Le Royaume Infesté",fps=self.fps) #initialisation du jeu
        
        self.position_curseur = 0
        self.player = Player("JOUEUR1",self)
        self.liste_mob = []
        self.liste_balles = []
        self.counter = self.fps*3 #decompte avant fin du jeu pour que l'explosion marche bien 30 est le nb de frame par seconde
        pyxel.run(self.update, self.draw)
        
    
        
    
    def collisions(self,instance1,instance2):
        """Appelle les differentes fonctions qui vérifient les collisions
        renvoie True si l'instance 1 est dans l'instance 2
        prend en parametre deux instances"""

        x1 = instance1.x
        x2=instance2.x
        
        y1 = instance1.y
        y2=instance2.y
        taille1 = instance1.taille
        taille2 = instance1.taille 
        
        if (x1 <= x2 <= x1+taille1 or x1<= x2+taille2  <= x1+taille1) and (y1 <= y2 <= y1+taille1 or y1<= y2+taille2  <= y1+taille1) :
            return True
            
        
    def reset_partie(self):
        """méthode qui permet de relancer une partie après une défaite, tt reset au niveau de départ"""
        
        self.changer_menu("Playing")
        self.position_curseur = 0
        self.player = Player("JOUEUR1",self)
        self.liste_mob = []
        self.counter = self.fps*3 #decompte avant fin du jeu pour que l'explosion marche bien 30 est le nb de frame par seconde


    def choix_option(self, liste_option):
        """gere l'appuie sur les touches haut bas et entree pour rendre le menu fonctionnel
        et renvoie l'id  de la position du curseur"""
        if pyxel.btnr(pyxel.KEY_UP):
            self.position_curseur -= 1
        
        elif pyxel.btnr(pyxel.KEY_DOWN):
            self.position_curseur += 1
            
        if self.position_curseur <0:
            self.position_curseur = len(liste_option)-1
        
        if self.position_curseur > len(liste_option)-1:
            self.position_curseur = 0
            
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            return self.position_curseur
            
        
        
    
        
        
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
                
        
        
    

        

    def update(self):     
        """Fonction qui est appelée par pyxel pour mettre a jour le jeu"""
        if self.menu_actuel == "Playing":
            if pyxel.btnp(pyxel.KEY_P):
                if self.pause == False:
                    self.pause =True
                
                else:
                    self.pause = False
                    
            if self.pause == False:
                self.update_playing()
        
        # if self.menu_actuel == "Playing" and self.pause == True:
        if pyxel.btn(pyxel.KEY_O):
            pyxel.mouse(False)
            print(pyxel.mouse_x, pyxel.mouse_y)
            
        if pyxel.btn(pyxel.KEY_I):
            pyxel.mouse(True)

        


            


            

    def update_playing(self):
        """Fonction qui lorsque le mode de jeu est playing met le jeu à jour"""
        
                
        if self.player.is_alive(): # boucle du jeu qui verifie si le joueur est mort
                #ici si le player est vivant
                #mettre la suite du jeu ici
                self.player.update()
                if pyxel.frame_count %90 ==0:
                    self.liste_mob.append(Mob(10,10,10,10,self.player))
                    # faire apparaitre les mobs dans une liste

                for mob in self.liste_mob:
                    if pyxel.frame_count % 15 ==0:
                        self.pos_cible = [self.player.x,self.player.y] #envoie cible des mobs pour ajouter un deplacement moins linéaire
                    if self.collisions(self.player,mob):
                        self.player.degats()


                    mob.update(self.pos_cible)
                    if not mob.is_alive():
                        self.liste_mob.remove(mob)
                
                for balle in self.liste_balles:#fais bouger les balles
                    balle.move()
                    if balle.is_alive == False:
                        self.liste_balles.remove(balle)

                for balle in self.liste_balles:#collisions enbtre balle et mobs
                    for mob in self.liste_mob:
                        if self.collisions(mob,balle):
                            self.liste_mob.remove(mob)
                            self.liste_balles.remove(balle)

                
                        
        else:
            
            self.counter-=1
            if len(self.player.liste_explosions) !=0 or (len(self.player.liste_explosions) ==1 and self.player.liste_explosions[0].taille_max == self.player.liste_explosions[0].etape-1):
                
                    self.player.update()
                    self.player.draw_explosions
                
            
            
            if  self.counter <=0 or (len(self.player.liste_explosions) ==1 and self.player.liste_explosions[0].taille_max == self.player.liste_explosions[0].etape+1):
                self.changer_menu("GameOver")
            
       
            

        


    def draw(self):
        """permet d'afficher le jeu"""
        if self.menu_actuel =="Playing" and self.pause== False:
            pyxel.cls(0)
            if self.hitbox:
                self.player.draw_hitbox()
    
            

            for mob in self.liste_mob:
                    if self.hitbox:
                        mob.draw_hitbox()
                    mob.draw()
            for balle in self.liste_balles:
                balle.draw()


            self.player.draw()
        
        if self.menu_actuel == "Start":
            self.draw_menu_start()
        
        if self.menu_actuel == "Amelioration":
            self.draw_menu_stat()
            
        elif self.menu_actuel == "GameOver":#si le joueur est mort
            self.draw_menu_fin()
            
        elif self.pause == True:
            self.draw_menu_pause()
               
    def draw_menu_stat(self):
        """menu après une vague pour choisir une statistique"""
        #TODO: ajouter des infos pour les nerds, choisir stat pui re entré pour commencer, num de la vague, ration kill dégats
        #une note sur le gameplay, avec un commentaire?
        pyxel.cls(0)
        option = []
        for i in range(1,4):
            choix= random.random()
            if choix <0.20:
                #force
                pyxel.rect(self.width//8 +20*i, self.height//2, 18, 18, 9)
                
            elif choix < 0.40:
                pyxel.rect(self.width//8 +20*i, self.height//2, 18, 18, 9)#defense
            elif choix <0.60:
                pyxel.rect(self.width//8 +20*i, self.height//2, 18, 18, 9)#regen
            elif choix < 0.80:
                pyxel.rect(self.width//8 +20*i, self.height//2, 18, 18, 9)#vie_max
            else:
                pyxel.rect(self.width//8 +20*i, self.height//2, 18, 18, 9)#degats
                
            option.append(random.random())
            
        option = {0:"Vague Suivante"}
        self.affichage_curseur(self.width//8 +3, self.height//2+25, 9)
        option_choisie = self.choix_option(option)
        if option_choisie == 0:
            self.changer_menu("Playing")
        
        
        pyxel.text(self.width//8 +20, self.height//2+25, "Reprendre", 9)
            
            
            
            
            
        
        
            
            
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


    def draw_menu_pause(self):
        pyxel.cls(0)
        pyxel.text(self.width//2-10, 1, "Pause", 6)
        option = {0: "Continuer",
                  1: "Sortie"}#tableau des options possible
        
        for i in range(len(option)):
            pyxel.text(pyxel.width//2 -15, pyxel.height//3 +9*i, option[i], 9)
        
        pyxel.text(8, self.height - self.height//4, "Mouvement : ZQSD", 8)
        pyxel.text(16, self.height - self.height//5, "Attaquer : [ Espace ]", 8)#affiche l'aide
        self.affichage_curseur(pyxel.width//2 -pyxel.width //8 - 18, pyxel.height//3 +9*self.position_curseur, 9)
        
        
        
        option_choisie = self.choix_option(option)
        if  option_choisie != None:
            if option_choisie ==0:
                self.pause = False
            
            elif option_choisie ==1:
                webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
                pyxel.quit()
        
    def affichage_curseur(self, x, y, col):
        pyxel.text(x, y, "<X>", col)
        
    def draw_menu_start(self):
        """dessine le menu de départ lorsque le menu est 'Start' dans lequel on choisit de jouer on de quitter le jeu"""
        pyxel.cls(0)        
        
        #décor arrière plan qui défile (cascade?)
        # pyxel.bltm(0, 0, 0, 0, 0, self.width, self.height)A ESSAYER SUR CAPYTALE
        
        option = {0: "Jouer",
                  1: "Sortie"}#tableau des options possible
        
        for i in range(len(option)):
            pyxel.text(pyxel.width//2 -18, pyxel.height//3 +9*i, option[i], 9)
        
        pyxel.text(8, self.height - self.height//4, "Mouvement : ZQSD", 8)
        pyxel.text(16, self.height - self.height//5, "Attaquer : [ Espace ]", 8)#affiche l'aide
        self.affichage_curseur(pyxel.width//2 -pyxel.width //8 - 18, pyxel.height//3 +9*self.position_curseur, 9)#affiche le curseur lors du choix
        
        
        option_choisie = self.choix_option(option)
        if  option_choisie != None:
            if option_choisie ==0:
                self.changer_menu("Playing")
            
            elif option_choisie ==1:
                webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
                pyxel.quit()
        

    
    

class Player: #classe qui cree le joueur
    def __init__(self,nom:str,game_instance:object):
        """In: nom -> le nom du joueur"""

        self.nom = nom
        self.x = pyxel.width//2 -2 #faire spawn le perso au milieu de l'écran
        self.y = pyxel.height//2 -2
        self.defense = 0
        self.attaque = 1
        self.vie_max = 200 #vie initiale
        self.vie = 200
        self.game_instance = game_instance
        self.vitesse = 1 #vitesse de deplacement
        
        self.regeneration = 1#% de vie par secondes
        self.cote = "g"#va a gauche
        self.liste_explosions = []
        self.taille = 5
        
        
    def ajouter_arme(self, num):
        """ajoute une arme aux armes possédées par le joueur"""
        self.liste_arme_joueur.append(jeu.liste_arme[num])
        print("ajout de l'arme", jeu.liste_arme[num])
    
                
    def ajouter_statistique(self, type_statistique, montant):
        """ajoute des le type de statistique au joueur"""

        if type_statistique == "vitesse":
            self.vitesse += montant
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
            if pyxel.btn(pyxel.KEY_D):
                # self.cote = "d"
                if (self.x < pyxel.width-5) :#eviter de sortir de l'écran
                    self.x = self.x + self.vitesse

            if pyxel.btn(pyxel.KEY_Q):
                # self.cote = "g"
                if (self.x > 0) :
                    self.x = self.x - self.vitesse
                    

            if pyxel.btn(pyxel.KEY_S):
                # self.cote = 'b'
                if (self.y < pyxel.height-5) :
                    self.y = self.y + self.vitesse
            if pyxel.btn(pyxel.KEY_Z):
                # self.cote = 'h'
                if (self.y > 0) : 
                    self.y = self.y - self.vitesse
                    
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.game_instance.liste_balles.append(Bullets(self.x,self.y,self.cote))

                
                

            
            #visee avec les touches de directions:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.cote = "d"
            if pyxel.btn(pyxel.KEY_LEFT):
                self.cote = "g"
            if pyxel.btn(pyxel.KEY_UP):
                self.cote = "h"
            if pyxel.btn(pyxel.KEY_DOWN):
                self.cote = "b"
                
            
            





        if pyxel.btn(pyxel.KEY_U) : #pour le debug
  
            self.degats(5)



            
     
        
    def degats(self,nb_degats:int=1):
        """
        Fonction qui prend en parametre le nb de degats a enlever au joueur
        et lui enlève
        """
        self.vie -= nb_degats
        if self.vie <0:
            self.vie =0
        if self.is_alive():
            self.liste_explosions.append(Explosion(self.x,self.y))
        else:
            self.liste_explosions.append(Explosion(self.x,self.y,150))
            


        
            

        


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


    def draw(self):
        """Permet de dessiner le joueur"""
        self.draw_explosions()
        if self.is_alive():
            pyxel.rect(self.x,self.y,5,5,6)
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
            pyxel.rect(1, 1, length*(self.vie/self.vie_max), height, col)
            pyxel.rect(1+length*(self.vie/self.vie_max), 1, length - length*(self.vie/self.vie_max), height, 0)
            
        
        
            
        
         
            
            
            
            
            
        pyxel.rectb(0, 0, 32, 8, 6)#contour de la barre de vie
        # pyxel.rectb(0, 0, 3.2*(i+1), 8, 2)
        

class Bullets:
    def __init__(self,x:int,y:int,direction:str,vitesse:int = 1):
        self.x = x
        self.y = y
        self.direction = direction #"g"gauche,"d"droite,"b"bas,"h"haut
        self.vitesse = vitesse
        self.is_alive = True

    def move(self):
        if self.direction == "g":
            self.x -= self.vitesse

        elif self.direction == "d":
            self.x +=1
        
        elif self.direction == "b":
            self.y +=1

        elif self.direction == "h":
            self.y -=1

        if not ((0<self.x< pyxel.width+5) or (0<self.y< pyxel.height+5)):
            self.is_alive = False

    def draw(self):
        pyxel.rect(self.x,self.y, 2,2,9)

    

        

class Mob:
    def __init__(self, life:int, damage:int, attack_speed:int, vitesse:int,player:object):
        """initialisation de la creation de mob
        Player est la l'instance du joueur """
        self.life = life
        self.damage = damage
        self.attack_speed = attack_speed
        self.vitesse = vitesse
        self.vitesse = 1
        self.taille = 5
        
        tmp = random.randint(1,4)
        if tmp == 1: #fait spawn les mobs en haut 
            self.x= random.randint(2,pyxel.width-7)
            self.y = 0

        elif tmp == 2: #fait spawn les mobs en gauche
            self.x = 0
            self.y = random.randint(2,pyxel.width-7)

        elif tmp == 3:#fait spawn les mobs en droite
            self.x = pyxel.width-7
            self.y = random.randint(2,pyxel.width-7)

        elif tmp == 4:
            self.x = random.randint(2,pyxel.width-7)
            self.y = pyxel.width-7


        self.cooldown_state = 3
        self.cooldown_max = random.randint(3,7)
        self.player = player
    

    def degat(self):
        """change la vie du mob"""
        self.life -= 1
    
    def is_alive(self):
        """donne de l'or au joueur et disparait si false"""
        if self.life > 0:
            return True
        elif self.life <= 0:
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
    

    def update(self, tableau_cible:list):
        """Prend en parametre tableau contenant les coordonnes cibles vers lesquels ils doivent se deplacer 
        tableau sous forme [x,y]
        la variable cooldown existe pour que les mobs se deplacent de facon plus saccadees"""


        if self.peut_bouger():
            """verifie si le mob peut jouer -> verifie son cooldown est ok;
            permet que le mob avance de maniere plus 'zombie' """
            player_x = tableau_cible[0]
            player_y = tableau_cible[1]
            mob_x = self.x
            mob_y = self.y
            
            if player_y-5 >= mob_y:
                self.y += self.vitesse

            elif player_y+5 <= mob_y:
                self.y -= self.vitesse

            if player_x+5 <= mob_x:
                self.x -= self.vitesse

            elif player_x-5 >= mob_x:
                self.x += self.vitesse

    def draw(self):
        """Dessine le Mob"""
        if self.player.is_alive():
            pyxel.rect(self.x,self.y,self.taille,self.taille,11)

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
