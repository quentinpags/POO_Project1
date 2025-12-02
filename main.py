import pyxel
import webbrowser


        
class Game: #classe qui cree le jeu et qui possede la boucle de jeu
    def __init__(self,width,height,nom_jeu):
        self.width = width
        self.height = height
        self.nom = nom_jeu
        self.hitbox = True
        
        self.menu_actuel = "None" #None, GameOver, Start, Pause
        

        pyxel.init(self.width, self.height)
        
        
        self.player = Player("JOUEUR1")
        self.liste_mob = []
        self.liste_arme = [Armes("Orbe tourbillonante", 10, 2,0.5,"epee"),Armes("Epee du debutant",1,2, 0.20,"epee")]#liste des armes déblocables
        pyxel.run(self.update, self.draw)
        

    def update(self):
        
        
        if self.menu_actuel == "None":
            
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
    
    
    def creer_attaque(self, x,y,cote, vitesse):
        if self.type_arme == "arc":
            if cote == "g":
                self.liste_attaque_actives.append([x -vitesse, y+4, 2, 1, cote])#x,y,w,h, cote
                
    def update_attaque(self):
        for att in self.liste_attaque_actives:
            if att[4] == "g" and pyxel.frame_count % 4 == 0:
                att[0] -= 2
                
            
    def update(self):
        pass
            
    
    # def caracteristique(self):
    #     return[self.nom, self.degats, self.cooldown, self.critical_hit, self.type_arme]
    
    def draw(self):
        # pyxel.rect(self.x, self.y, 2, 4, 9)
        for lst in self.liste_attaque_actives:
            pyxel.rect(lst[0], lst[1], 2, 1, 2)
    
    
    
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
            
            if (self.x < pyxel.width-5) :#eviter de sortir de l'écran
                self.x = self.x + self.vitesse

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
            
            if (self.x > 0) :
                self.x = self.x - self.vitesse
                

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            if (self.y < pyxel.height-5) :
                self.y = self.y + self.vitesse
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
            if (self.y > 0) : 
                self.y = self.y - self.vitesse
                
        if pyxel.btn(pyxel.KEY_SPACE):
            self.arme_active.creer_attaque(self.x, self.y,self.cote, self.vitesse)        
        
        if pyxel.btn(pyxel.KEY_U):
            # test enlever pv
            # print(self.vie)
            # self.vie -= 5
            pass
        
            
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
        else:
            print('The END')#MENU de FIN
            Game.changer_menu("GameOver")
        
         
            
            
            
            
            
        pyxel.rectb(0, 0, 32, 8, 6)#contour de la barre de vie
        # pyxel.rectb(0, 0, 3.2*(i+1), 8, 2)
        




class Mob:
    def __init__(self, life, damage, attack_speed, speed):
        """initialisation de la creation de mob"""
        self.life = life
        self.damage = damage
        self.attack_speed = attack_speed
        self.speed = speed
    
    def update(self):
        pass
    
    def draw(self):
        pass
    
    def degat(self):
        """change la vie du mob"""
        pass
    
    def is_alive(self):
        """donne de l'or au joueur et disparaitsi false"""
        if self.life > 0:
            return True
        elif self.life <= 0:
            return False
        



        
        
            

        



    


Game(128,128,"JEU")