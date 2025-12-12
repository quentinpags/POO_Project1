import pyxel
import webbrowser
from random import randint


        
class Game: #classe qui cree le jeu et qui possede la boucle de jeu
    def __init__(self,width,height,nom_jeu):
        self.width = width
        self.height = height
        self.nom = nom_jeu
        self.hitbox = False
        self.pos_cible = [0,0]#position vers lequel les mobs se dirigent
        
        
        self.liste_menu = ["Playing", "GameOver", "Start", "Pause"]
        self.menu_actuel = "Start" 
        

        pyxel.init(self.width, self.height, title= "Potato et Le Royaume Infesté")
        
        self.position_curseur = 0
        self.player = Player("JOUEUR1")
        self.liste_mob = []
        self.liste_arme = [Armes("Orbe tourbillonante", 10, 2,0.5,"epee"),Armes("Epee du debutant",1,2, 0.20,"epee")]#liste des armes déblocables
        pyxel.run(self.update, self.draw)
        
        
    
        

    def update(self):
        
        
        if self.menu_actuel == "Playing":
            
            self.update_playing()

                    



            

        # if self.menu_actuel == "Start":
        #     if pyxel.btn(pyxel.KEY_RETURN) or pyxel.btn(pyxel.KEY_KP_ENTER):
        #         self.menu_actuel  = "Playing"
                
                
            
                

                
        
         
        if self.menu_actuel == "GameOver":
            webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
            pyxel.quit()
           

        
            
            
        


    def update_playing(self):
        
        if self.player.is_alive(): # boucle du jeu qui verifie si le joueur est mort
                #ici si le player est vivant
                #mettre la suite du jeu ici
                self.player.move()
                if pyxel.frame_count %90 ==0:
                    self.liste_mob.append(Mob(10,10,10,10))
                    # faire apparaitre les mobs dans une liste

                for mob in self.liste_mob:
                    if pyxel.frame_count % 15 ==0:
                        self.pos_cible = [self.player.x,self.player.y] #envoie cible des mobs pour ajouter un deplacement moins linéaire


                    mob.move(self.pos_cible)
                    if not mob.is_alive():
                        self.liste_mob.remove(mob)

        else:#si le joueur est mort
            print(self.player.nom, "est mort")

        self.player.arme_active.update_attaque()


    def draw(self):
        pyxel.cls(0)
        
        # self.menu()#debug    
            
        if self.menu_actuel =="Playing":
            if self.hitbox:
                self.player.draw_hitbox()
    
            

            for mob in self.liste_mob:
                    if self.hitbox:
                        mob.draw_hitbox()
                    mob.draw()
            self.player.draw()
        
        if self.menu_actuel == "Start":
            self.draw_menu_start()
            
            
    def draw_menu_start(self):
        
        pyxel.cls(10)
        
        
        #décor arrière plan qui défile (cascade?)
        # pyxel.bltm(0, 0, 0, 0, 0, self.width, self.height)A ESSAYER SUR CAPYTALE
        
        option = {0: "Playing",
                  1: "Sortie"}
        
        for i in range(len(option)):
            pyxel.text(pyxel.width//2 -18, pyxel.height//3 +9*i, option[i], 9)
        
        pyxel.text(8, self.height - self.height//4, "Mouvement : ZQSD", 8)
        pyxel.text(16, self.height - self.height//5, "Attaquer : [ Espace ]", 8)
        pyxel.text(pyxel.width//2 -pyxel.width //8 - 18, pyxel.height//3 +9*self.position_curseur, "<X>", 9)#affiche le curseur lors du choix
        option_choisie = self.choix_option(option)
        if  option_choisie != None:
            if option_choisie ==0:
                self.changer_menu("Playing")
            
            
            
            
            elif option_choisie ==1:
                webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
                pyxel.quit()
        
    
        
    
    def choix_option(self, liste_option):
        """gere l'appuie sur les touches haut bas et entree pour rendre le menu fonctionnel"""
        if pyxel.btnr(pyxel.KEY_UP):
            self.position_curseur -= 1
        
        elif pyxel.btnr(pyxel.KEY_DOWN):
            self.position_curseur += 1
            
        if self.position_curseur <0:
            self.position_curseur = len(liste_option)-1
        
        if self.position_curseur > len(liste_option)-1:
            self.position_curseur = 0
            
        if pyxel.btnp(pyxel.KEY_RETURN):
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
        


class Armes:
    def __init__(self, nom, degats, cooldown, critical_hit, type_arme):
        """cooldown: temps avant prochaine attaque
        critical_hit -> en %"""
        #pas encore appellée
        self.nom = nom
        self.degats = degats
        self.cooldown = cooldown
        self.critical_hit = critical_hit
        self.type_arme = type_arme
        self.liste_attaque_actives = []  
        self.vitesse_attaque = 1# vitesse qu'a la balle a avancer
        #plus bas mieux c
        self.vitesse_progression = 2
        self.delai_touche = 5#permet d'eviter de spam la barre espace
    
    
    def creer_attaque(self, x,y,cote, vitesse):
        if self.type_arme == "arc" and pyxel.frame_count % self.cooldown == 0:
            self.liste_attaque_actives.append([x -vitesse, y+4, 2, 1, cote])#x,y,w,h, cote
            
            
                
                
                
    def update_attaque(self):
        
        for att in self.liste_attaque_actives:
            if att[4] == "g" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[0] -= self.vitesse_progression
                
            elif att[4] == "d" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[0] += self.vitesse_progression
                
            elif att[4] == "h" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[1] -= self.vitesse_progression
                
            elif att[4] == "b" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[1] += self.vitesse_progression
                
            
                
            
            
    
    # def caracteristique(self):
    #     return[self.nom, self.degats, self.cooldown, self.critical_hit, self.type_arme]
    
    def draw(self):
        # pyxel.rect(self.x, self.y, 2, 4, 9)
        for lst in self.liste_attaque_actives:
            if lst[4] == "g" or lst[4] == "d":
                pyxel.rect(lst[0], lst[1], 2, 1, 2)
            else:
               pyxel.rect(lst[0], lst[1], 1, 2, 2) 
    
    
    
    def abilite(self):
        """l'arme a une proba d'avoir compétence spéciale"""
        pass

class Player: #classe qui cree le joueur
    def __init__(self,nom):
        self.nom = nom
        self.x = pyxel.width//2 -2 #faire spawn le perso au milieu de l'écran
        self.y = pyxel.height//2 -2
        self.defense = 0
        self.attaque = 1
        self.vie_max = 200 #vie initiale
        self.vie = 200
        
        self.vitesse = 0.75 #vitesse de deplacement
        
        self.regeneration = 1#% de vie par secondes
        self.liste_arme_joueur = [Armes("Arc du débutant", 1, 2, 0.1, "arc")]#liste des armes possédées apr joueur
        self.arme_active = self.liste_arme_joueur[0]#arme utilisé par le joueur
        self.cote = "g"#va a gauche
        
        
    def ajouter_arme(self, num):
        """ajoute une arme aux armes possédées par le joueur"""
        self.liste_arme_joueur.append(jeu.liste_arme[num])
        print("ajout de l'arme", jeu.liste_arme[num])
    
                
    def ajouter_statistique(self, type_statistique):
        
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
        
                
    
    
    
        
    def move(self):
        """déplacement avec les touches de direction"""
        # TODO: gerer l'orientation du perso
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
            
            if pyxel.frame_count % self.arme_active.delai_touche == 0:
                self.arme_active.creer_attaque(self.x, self.y,self.cote, self.vitesse)        
        
        if pyxel.btn(pyxel.KEY_U):
            #test enlever pv
            # print(self.vie)
            self.vie -= 5
            
        
            
    def orientation(self):
        """renvoie le cote que le personnage va: par exemple touche gauche -> gauche
        gère l'orientation du personnage"""
        
        if self.cote == 'g':
            #x -> -x
            pass
        elif self.cote == "d":
            #-x -> x
            pass
        
        

    

        
    def draw_hitbox(self):
        pyxel.rect(self.x-1,self.y-1,7,7,9) #7= taille player + 2 pour que l'on voie un peu le rectangle

    def degats(self,nb_degats):
        """
        Fonction qui prend en parametre le nb de degats a enlever au joueur
        et lui enlève
        """
        self.vie -= nb_degats
        


    def is_alive(self):
        """
        Fonction qui renvoie True si le joueur est vivant (vie>0)
        """
        if self.vie > 0:
            return True
        
        else:
            return False



    def draw(self):
        pyxel.rect(self.x,self.y,5,5,6)
        self.draw_health()
        self.arme_active.draw()
             

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
            # TODO: faire le noir dans la barre de vie
        
        else:
            print('The END')#MENU de FIN
            
        
         
            
            
            
            
            
        pyxel.rectb(0, 0, 32, 8, 6)#contour de la barre de vie
        # pyxel.rectb(0, 0, 3.2*(i+1), 8, 2)
        




class Mob:
    def __init__(self, life:int, damage:int, attack_speed:int, vitesse:int):
        """initialisation de la creation de mob"""
        self.life = life
        self.damage = damage
        self.attack_speed = attack_speed
        self.vitesse = vitesse
        self.vitesse = 1
        self.x = randint(0,pyxel.width-7)
        self.y = 0
        self.cooldown_state = 3
        self.cooldown_max = randint(3,7)
    

    
    def draw_hitbox(self):
            pyxel.rect(self.x-1,self.y-1,7,7,9) #7= taille mob + 2 pour que l'on voie un peu le rectangle

    def move(self, tableau_cible:list):
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
        pyxel.rect(self.x,self.y,5,5,11)
    
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
        



        
        
            

        



    


jeu = Game(128,128,"JEU")
