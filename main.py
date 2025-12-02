
import pyxel
import webbrowser
from random import randint


        
class Game: #classe qui cree le jeu et qui possede la boucle de jeu
    def __init__(self,width,height,nom_jeu):
        self.width = width
        self.height = height
        self.nom = nom_jeu
        self.hitbox = True
        self.pos_cible = [0,0]
        
        self.menu_actuel = "None" #None, GameOver, Start, Pause
        

        pyxel.init(self.width, self.height)
        
        
        self.player = Player("JOUEUR1")
        self.liste_mob = []
        self.liste_arme = [Armes("Orbe tourbillonante", 10, 2,0.5,"epee"),Armes("Epee du debutant",1,2, 0.20,"epee")]#liste des armes déblocables
        pyxel.run(self.update, self.draw)
        

    def update(self):
        if pyxel.frame_count %90 ==0:
            self.liste_mob.append(Mob(10,10,10,10))
            # faire apparaitre les mobs dans une liste

            
            



        if  self.menu_principal.is_showed:
            if pyxel.btn(pyxel.KEY_RETURN) or pyxel.btn(pyxel.KEY_KP_ENTER):
                self.menu_principal.is_showed = False

        
        
        if self.menu_actuel == "None":
            


        for mob in self.liste_mob:
            if pyxel.frame_count % 15 ==0:
                self.pos_cible = [self.player.x,self.player.y] #envoie cible des mobs pour ajouter un deplacement moins linéaire

            
            mob.move(self.pos_cible)
            if not mob.is_alive():
                self.liste_mob.remove(mob)
            if self.player.is_alive(): # boucle du jeu qui verifie si le joueur est mort
                #ici si le player est vivant
                #mettre la suite du jeu ici
                self.player.move()
                
                
            else:#si le joueur est mort
                print(self.player.nom, "est mort")
                
            #test de la mort des Mobs
            for mobs in self.liste_mob:
                if mobs.is_alive() == True:
                    self.liste_mob.remove(mobs)
                    
            # update des balles de l'arc:
                #...
                
            self.player.arme_active.update_attaque()
         
        if self.menu_actuel == "GameOver":
              webbrowser.open_new("https://www.youtube.com/watch?v=xvFZjo5PgG0")
              pyxel.quit()
        
            
            
        



    def draw(self):
        pyxel.cls(0)
        
        self.menu()    
            
        if self.menu_actuel =="None":
            if self.hitbox:
                self.player.draw_hitbox()
            
            for v in self.liste_mob:
                    if self.hitbox:
                        v.draw_hitbox()
                    v.draw()
                    


            self.player.draw()
            
    def menu(self):
        if self.menu_actuel == "GameOver":
            print('This is the end...')
        
        elif self.menu_actuel == "Pause":
            print('pause activée')
            
        elif self.menu_actuel == "Start":
            print('Menu de départ')
            
        elif self.menu_actuel =="None":
            print('rien à faire')
    
    def changer_menu(self, menu_remplacement):
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
        self.vitesse_attaque = 1#plus bas mieux c
    
    
    def creer_attaque(self, x,y,cote, vitesse):
        if self.type_arme == "arc":
            self.liste_attaque_actives.append([x -vitesse, y+4, 2, 1, cote])#x,y,w,h, cote
            
            
                
                
                
    def update_attaque(self):
        
        for att in self.liste_attaque_actives:
            if att[4] == "g" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[0] -= 2
                
            elif att[4] == "d" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[0] += 2
                
            elif att[4] == "h" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[1] -= 2
                
            elif att[4] == "b" and pyxel.frame_count % self.vitesse_attaque == 0:
                att[1] += 2
                
            
                
            
    def update(self):
        pass
            
    
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
        
        self.vitesse = 1 #vitesse de deplacement
        
        self.regeneration = 1#% de vie par secondes
        self.liste_arme_joueur = [Armes("Arc du débutant", 1, 2, 0.1, "arc")]#liste des armes possédées apr joueur
        self.arme_active = self.liste_arme_joueur[0]#arme utilisé par le joueur
        self.cote = "g"#va a gauche
        
        
    def ajouter_arme(self, num):
        """ajoute une arme aux armes possédées par le joueur"""
        self.liste_arme_joueur.append(Game.liste_arme[num])
        print("ajout de l'arme", Game.liste_arme[num])
    
                
    
        
                
    
    
    
        
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
            self.arme_active.creer_attaque(self.x, self.y,self.cote, self.vitesse)                 
        
            
    def orientation(self):
        """renvoie le cote que le personnage va: par exemple touche gauche -> gauche
        gère l'orientation du personnage"""
        
        if self.cote == 'g':
            #x -> -x
            pass
        elif self.cote == "d":
            #-x -> x
            pass
        
        

    

        

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

    def draw_hitbox(self):
            pyxel.rect(self.x-1,self.y-1,7,7,9) #7= taille player + 2 pour que l'on voie un peu le rectangle

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
        else:
            print('The END')#MENU de FIN
            Game.changer_menu("GameOver")
        
         
            
            
            
            
            
        pyxel.rectb(0, 0, 32, 8, 6)#contour de la barre de vie
        # pyxel.rectb(0, 0, 3.2*(i+1), 8, 2)
        




class Mob:
    def __init__(self, life:int, damage:int, attack_speed:int, vitesse:int):
        """initialisation de la creation de mob"""
        self.life = life
        self.damage = damage
        self.attack_speed = attack_speed
        self.vitesse = 1
        self.x = randint(0,pyxel.width-7)
        self.y = 0
        self.cooldown_state = 3
        self.cooldown_max = randint(3,7)
    
    def update(self):
        pass
    
    def draw_hitbox(self):
            pyxel.rect(self.x-1,self.y-1,7,7,9) #7= taille mob + 2 pour que l'on voie un peu le rectangle

    def move(self, tableau_cible:list):
        """Prend en parametre tableau ontenatn les coordonnes cibles vers lesquels ils doivent se deplacer 
        tableau sous forme [x,y]
        la variable cooldown existe pour que les mobs se deplacent de faconc plus saccadees"""
        
        
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
        pass
    
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
        



        
        
            

        



    


Game(128,128,"JEU")
