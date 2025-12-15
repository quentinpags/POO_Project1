import pyxel
import webbrowser
from random import randint
# TODO:système de vague de + en + difficile, collision mob-player(degat) balle-sprite(degat au sprite et destruction balle)
#TODO: faire un mode pour voir les coordonnées a l'ecran grace à la sourie

        
class Game: #classe qui cree le jeu et qui possede la boucle de jeu
    def __init__(self,width,height,nom_jeu):
        self.width = width
        self.height = height
        self.nom = nom_jeu
        self.hitbox = False
        self.pos_cible = [0,0]#position vers lequel les mobs se dirigent
        
        
        self.liste_menu = ["Playing", "GameOver", "Start", "Pause", "Amelioration"]#liste des menus disponibles
        self.menu_actuel = "Start" 
        self.fps = 30

        pyxel.init(self.width, self.height, title= "Potato et Le Royaume Infesté",fps=self.fps)
        
        self.position_curseur = 0
        self.player = Player("JOUEUR1")
        self.liste_mob = []
        self.liste_arme = [Armes("Orbe tourbillonante", 10, 2,"epee"),Armes("Epee du debutant",1,2,"epee")]#liste des armes déblocables
        self.counter = self.fps*3 #decompte avant fin du jeu pour que l'explosion marche bien 30 est le nb de frame par seconde
        
        pyxel.run(self.update, self.draw)
        
        
    def reset_partie(self):
        """méthode qui permet de relancer une partie après une défaite, tt reset au niveau de départ"""
        
        self.changer_menu("Playing")
        self.position_curseur = 0
        self.player = Player("JOUEUR1")
        self.liste_mob = []
        
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
               
        if self.menu_actuel == "Playing":
            self.update_playing()


    def update_playing(self):
                
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


                    mob.update(self.pos_cible)
                    if not mob.is_alive():
                        self.liste_mob.remove(mob)
                        
                self.player.arme_active.update_attaque()
        else:
            
            self.counter-=1
            if len(self.player.liste_explosions) !=0 or (len(self.player.liste_explosions) ==1 and self.player.liste_explosions[0].taille_max == self.player.liste_explosions[0].etape-1):
                
                    self.player.update()
                    self.player.draw_explosions
                
            
            
            if  self.counter <=0 or (len(self.player.liste_explosions) ==1 and self.player.liste_explosions[0].taille_max == self.player.liste_explosions[0].etape+1):
                self.changer_menu("GameOver")
            
       
            

        


    def draw(self):
        if self.menu_actuel =="Playing":
            pyxel.cls(0)
            if self.hitbox:
                self.player.draw_hitbox()
    
            

            for mob in self.liste_mob:
                    if self.hitbox:
                        mob.draw_hitbox()
                    mob.draw()


            self.player.draw()
        
        if self.menu_actuel == "Start":
            self.draw_menu_start()
            
        elif self.menu_actuel == "GameOver":#si le joueur est mort
            self.draw_menu_fin()
               
            
            
    def draw_menu_fin(self):
        
        pyxel.cls(9)
        pyxel.text(pyxel.width//2 -18, pyxel.height//3 +9, "Game Over", 0)
        option = {0:"Try Again",
                  1:"Sortie"}
        
        
        for i in range(len(option)):#crée l'affichage du menu
            pyxel.text(pyxel.width//2 -18, pyxel.height//3 +30 +10*i, option[i], 8)
        
        
        
        #COPIE DE draw_menu_start:
        option_choisie = self.choix_option(option)
        pyxel.text(pyxel.width//2 -32, pyxel.height//3 +30 +10*self.position_curseur, "<X>", 0)#affiche le curseur lors du choix

        if  option_choisie != None:
            if option_choisie ==0:
                self.reset_partie()
             
                
            elif option_choisie ==1:
                webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
                pyxel.quit()



        
    def draw_menu_start(self):
        """dessine le menu de départ dans lequel on choisit de jouer on de quitter le jeu"""
        pyxel.cls(0)
        
        option = {0: "Playing",
                  1: "Sortie"}#tableau des options possible
        
        for i in range(len(option)):
            pyxel.text(pyxel.width//2 -18, pyxel.height//3 +9*i, option[i], 9)
        
        pyxel.text(8, self.height - self.height//4, "Mouvement : ZQSD", 8)
        pyxel.text(16, self.height - self.height//5, "Attaquer : [ Espace ]", 8)#affiche l'aide
        pyxel.text(pyxel.width//2 -pyxel.width //8 - 18, pyxel.height//3 +9*self.position_curseur, "<X>", 9)#affiche le curseur lors du choix
        
        
        option_choisie = self.choix_option(option)
        if  option_choisie != None:
            if option_choisie ==0:
                self.changer_menu("Playing")
            
            elif option_choisie ==1:
                webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
                pyxel.quit()
        

class Armes:
    def __init__(self, nom:str, degats:int, cooldown:int, type_arme:str):
        """cooldown: temps avant prochaine attaque
        critical_hit -> en %"""
        self.nom = nom
        self.degats = degats
        self.cooldown = cooldown #temps entre les attaques
        
        self.type_arme = type_arme
        self.liste_attaque_actives = []  
        self.vitesse_attaque = 1# vitesse qu'a la balle a avancer
        self.vitesse_progression = 2#vitesse de déplacement de l'attaque
        
    
    
    def creer_attaque(self, x,y,cote, vitesse):
        """cree une attaque en fonction du type d'arme utilisée"""        
        if self.type_arme == "arc" and pyxel.frame_count % self.cooldown == 0:
            self.liste_attaque_actives.append([x -vitesse, y+4, 2, 1, cote])#(on rajoute l'attaque à la liste d'attaque)
    
    
    def update_attaque(self):
        """gere la progression des attaques dans le temps"""
        for att in self.liste_attaque_actives:
            if att[4] == "g" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[0] -= self.vitesse_progression
                
            elif att[4] == "d" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[0] += self.vitesse_progression
                
            elif att[4] == "h" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[1] -= self.vitesse_progression
                
            elif att[4] == "b" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[1] += self.vitesse_progression
             
            
    
    def draw(self):
        """dessine l'attaque"""
        for lst in self.liste_attaque_actives:
            if lst[4] == "g" or lst[4] == "d":
                pyxel.rect(lst[0], lst[1], 2, 1, 2)
            else:
               pyxel.rect(lst[0], lst[1], 1, 2, 2) 
    
    

class Player: #classe qui cree le joueur
    def __init__(self,nom):
        self.nom = nom
        self.x = pyxel.width//2 -2 #faire spawn le perso au milieu de l'écran
        self.y = pyxel.height//2 -2
        self.defense = 0
        self.attaque = 1
        self.vie_max = 200 #vie initiale
        self.vie = 200
        
        self.vitesse = 1 #vitesse de deplacement
        
        self.regeneration = 1#% de vie par secondes
        self.liste_arme_joueur = [Armes("Arc du débutant", 1, 2, "arc")]#liste des armes possédées apr joueur
        self.arme_active = self.liste_arme_joueur[0]#arme utilisé par le joueur
        self.cote = "g"#va a gauche
        self.liste_explosions = []
        
        
    def ajouter_arme(self, num):
        """ajoute une arme aux armes possédées par le joueur"""
        self.liste_arme_joueur.append(jeu.liste_arme[num])
        print("ajout de l'arme", jeu.liste_arme[num])
    
                
    def ajouter_statistique(self, type_statistique):
        """ajoute des le type de statistique au joueur"""
        # TODO:rajouter un montant
        if type_statistique == "vitesse":
            self.vitesse += 0.01
        elif type_statistique == "attaque":
            self.attaque += 10
        
        elif type_statistique == "vie":
            self.vie_max += 10#on augment plus la vie que la vit et l'att car plus de dégats causés
        
        elif type_statistique == "regeneration":
            self.regeneration += 1 
        elif type_statistique == "defense":
            self.defense += 1
     
        
    
    def boutons(self):
        """Fonction qui permet de gérer la fonctions des touches"""
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.cote = "d"
            if (self.x < pyxel.width-5) :#eviter de sortir de l'écran
                self.x = self.x + self.vitesse

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
            self.cote = "g"
            if (self.x > 0) :
                self.x = self.x - self.vitesse
                

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.cote = 'b'
            if (self.y < pyxel.height-5) :
                self.y = self.y + self.vitesse
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
            self.cote = 'h'
            if (self.y > 0) : 
                self.y = self.y - self.vitesse
                
        if pyxel.btn(pyxel.KEY_SPACE):
            if pyxel.frame_count % self.arme_active.cooldown == 0:
                     self.arme_active.creer_attaque(self.x, self.y,self.cote, self.vitesse)        
            

        
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
        self.draw_explosions()
        if self.is_alive():
            pyxel.rect(self.x,self.y,5,5,6)
            self.draw_health()
            self.arme_active.draw()
        


    def draw_hitbox(self):
        """fonction de débug qui entoure le joueur"""
        pyxel.rect(self.x-1,self.y-1,7,7,9) #7= taille player + 2 pour que l'on voie un peu le rectangle

    
    def draw_explosions(self):
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
        




class Mob:
    def __init__(self, life:int, damage:int, attack_speed:int, vitesse:int,player:isinstance):
        """initialisation de la creation de mob
        Player est la l'instance du joueur """
        self.life = life
        self.damage = damage
        self.attack_speed = attack_speed
        self.vitesse = vitesse
        self.vitesse = 1
        self.x = randint(0,pyxel.width-7)
        self.y = 0
        self.cooldown_state = 3
        self.cooldown_max = randint(3,7)
        self.player = player
    

    def degat(self):
        """change la vie du mob"""
        self.life -= 1
    
    def is_alive(self):
        """donne de l'or au joueur et disparaitsi false"""
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
            #verifie si le mob peut jouer -> verifie son cooldown est ok
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
        if self.player.is_alive():
            pyxel.rect(self.x,self.y,5,5,11)

    def draw_hitbox(self):
            pyxel.rect(self.x-1,self.y-1,7,7,9) #7= taille mob + 2 pour que l'on voie un peu le rectangle
    
    
        



class Explosion:
    def __init__(self ,x:int,y:int,taille_max:int= 5):
        self.taille_max = taille_max
        self.x = x+2#pour que l'explosion ait pour centre a peu près le centre du player (vu que le player fait 5 par 5)
        self.y = y+2
        self.etape = 0
        self.alive = True
        
    
    def draw(self):
        
        
        self.etape += 1
        pyxel.circ(self.x,self.y,self.etape,9)

    def is_alive(self):
        if self.etape == self.taille_max:
            self.alive = False
        return self.alive
        
        
            

        



    


jeu = Game(128,128,"JEU")
