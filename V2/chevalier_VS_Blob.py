# Importation des bibliothèques nécessaires
import pygame
import sqlite3
import sys
import random
import time
print("")
print("bienvenue sur chevalier VS blob !!")
print("")
print("pour vous déplacer : touche fléché")
print("pour poser des épées : espace")
print("pour poser des mégas épées : m")
print("")
print(" 1 ou 2 joueur ?")
choix = int(input(" entrez 1 ou 2 :"))
if choix == 2 :
    player2 = True
else :
    player2 = False

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600
couleur_fond = (0, 0, 0)

# Paramètres du joueur/ des joueurs
if player2 == True :
    vitesse_joueur2 = 7
    orientation_joueur2 = "haut"

vitesse_joueur = 7
orientation_joueur = "haut"

# Paramètres des gobelins
vitesse_gobelins = 2
if player2 == True :
    vitesse_gobelins = 4
vitesse_max = 1

# Paramètres de jeu
points_par_gobelin = 10
points_par_vie_perdue = 100
vies_initiales = 5
vie_mega_epee_initiale = 70
nb_coups_avant_vie = 50
nb_coups_avant_bombe = 30
capacite_coup = 5

# Tailles des sprites et des armes
taille_sprite = 35
taille_mega_epee = 55

# Limites de jeu
limite_coups = 5000
limite_mega_epee = 2

# Variables de suivi
if player2 == True:
    nb_2 = 0
    nb_coups_2 = 0
    nb_mega_epee_2 = 0
    nb_mort_2 = 0
    fin_nb_2 = 0

nb = 0
nb_coups = 0
nb_mega_epee = 0
nb_mort = 0
fin_nb = 0
# Variables de transition
supr = 0
couleur_fond_degat = (200, 0, 0)

# Initialisation de la fenêtre Pygame
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Jeu d'Épée contre les Gobelins")

# Initialisation des sons
pygame.mixer.init()
son_degat = pygame.mixer.Sound("degat.mp3")
son_fin = pygame.mixer.Sound("fin.mp3")
son_epee = pygame.mixer.Sound("epee.mp3")
son_vie = pygame.mixer.Sound("vie.mp3")

# Chargement des images
if player2 == True:
    image_joueur_2 = pygame.transform.scale(pygame.image.load("joueur2.png").convert_alpha(), (taille_sprite, taille_sprite))
image_joueur = pygame.transform.scale(pygame.image.load("joueur.png").convert_alpha(), (taille_sprite, taille_sprite))
image_gobelin = pygame.transform.scale(pygame.image.load("gobelin.png").convert_alpha(), (taille_sprite, taille_sprite))
image_epee = pygame.transform.scale(pygame.image.load("epee.png").convert_alpha(), (taille_sprite, taille_sprite))
image_mega_epee = pygame.transform.scale(pygame.image.load("mega_epee.png").convert_alpha(), (taille_mega_epee, taille_mega_epee))
image_fond = pygame.image.load("fond.png")
image_fond = pygame.transform.scale(image_fond, (largeur_fenetre, hauteur_fenetre))
image_vie = pygame.transform.scale(pygame.image.load("vie.png").convert_alpha(), (taille_sprite, taille_sprite))
image_bombe = pygame.transform.scale(pygame.image.load("bombe.png").convert_alpha(), (taille_sprite, taille_sprite))

# Initialisation des rectangles des personnages
joueur = pygame.Rect(largeur_fenetre // 2 - taille_sprite // 2, hauteur_fenetre - taille_sprite * 2, taille_sprite, taille_sprite)
if player2 == True:
    joueur2 = pygame.Rect(largeur_fenetre // 2 - taille_sprite // 2, hauteur_fenetre - taille_sprite * 2, taille_sprite, taille_sprite)
# Initialisation vie
vie = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)
# Initialisation bombe
bombe = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)

# liste bombe
bombe_list = []
# LISTE VIE
vie_list = []
# Liste des gobelins
gobelins = []

# Création d'un gobelin
gobelin = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)

# Variables du joueur/ des joueurs
if player2 == True:
    vies_2 = vies_initiales
points = 0
vies = vies_initiales

# Liste des coups du joueur
if player2 == True:
    joueur_coups_2 = []

joueur_coups = []

# Liste des méga-épées du joueur
if player2 == True:
    joueur_mega_epee_2 = []

joueur_mega_epee = []

# Liste des vies des méga-épées
if player2 == True:
    vie_mega_epees_2 = [vie_mega_epee_initiale] * limite_mega_epee
vie_mega_epees = [vie_mega_epee_initiale] * limite_mega_epee

# Connexion à la base de données SQLite
conn = sqlite3.connect("scores.db")
c = conn.cursor()

# Création de la table des scores si elle n'existe pas
c.execute('''CREATE TABLE IF NOT EXISTS scores
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              points INTEGER NOT NULL)''')

# Affichage des statistiques du joueur
def statistique():
    print(f"Votre score final : {points}")
    print("Nombre d'épées : ", nb_coups)
    print("Nombre de méga-épées : ", nb_mega_epee)
    print("Nombre de morts : ", nb_mort)
    print("Meilleur score : ", obtenir_meilleur_score())
    input("")

# Fonction pour ajouter un score à la base de données
def ajouter_score(points):
    c.execute("INSERT INTO scores (points) VALUES (?)", (points,))
    conn.commit()

# Fonction pour obtenir le meilleur score depuis la base de données
def obtenir_meilleur_score():
    c.execute("SELECT MAX(points) FROM scores")
    meilleur_score = c.fetchone()[0]
    return meilleur_score if meilleur_score is not None else 0

# Fonction pour afficher les informations du jeu (score et vies)
def afficher_infos():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {points}", True, (50, 70, 200))
    vies_text = font.render(f"Vies: {vies}", True, (50, 70, 200))
    if player2 == True:
        vies_text_2 = font.render(f"Vies: {vies_2}", True, (50, 70, 200))
        fenetre.blit(vies_text_2, (10, 30))
    fenetre.blit(score_text, (10, 10))
    fenetre.blit(vies_text, (10, 50))
    

# Horloge pour contrôler la vitesse du jeu
clock = pygame.time.Clock()
fenetre_rect = fenetre.get_rect()

# Fonction pour calculer la distance entre deux rectangles
def distance(rect1, rect2):
    return ((rect1.x - rect2.x)**2 + (rect1.y - rect2.y)**2)**0.5

def supprimer_pires_scores(limite_scores):
    # Récupérer tous les scores
    c.execute("SELECT id, points FROM scores ORDER BY points DESC")
    scores = c.fetchall()

    # Vérifier si le nombre total de scores dépasse la limite
    if len(scores) > limite_scores:
        # Supprimer les scores excédant la limite
        scores_a_supprimer = scores[limite_scores:]
        for score in scores_a_supprimer:
            c.execute("DELETE FROM scores WHERE id = ?", (score[0],))
        
        # Valider les modifications dans la base de données
        conn.commit()

# Boucle principale du jeu
while True:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Tir de coup de joueur avec la barre d'espace
        if vies_2 > 0:
            if player2 == True:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    if len(joueur_coups_2) < limite_coups:
                        coup_2 = pygame.Rect(joueur2.x, joueur2.y, taille_sprite, taille_sprite)
                        joueur_coups_2.append(coup_2)
                        nb_coups_2 += 1
                    if len(joueur_coups_2) > capacite_coup:
                        joueur_coups_2.pop(0)
                    # Tir de méga-épée avec la touche 'm'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    if len(joueur_mega_epee_2) < limite_mega_epee:
                        mega_epee_2 = pygame.Rect(joueur2.x, joueur2.y, taille_mega_epee, taille_mega_epee)
                        joueur_mega_epee_2.append(mega_epee_2)
                        supr = 1
                        vies_2 += 1
                        nb_mega_epee_2 += 1
                        for i in range(len(vie_mega_epees_2)):
                            if vie_mega_epees_2[i] <= 0:
                                vie_mega_epees_2[i] = vie_mega_epee_initiale
                                break
            
        if vies > 0:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if len(joueur_coups) < limite_coups:
                    coup = pygame.Rect(joueur.x, joueur.y, taille_sprite, taille_sprite)
                    joueur_coups.append(coup)
                    nb_coups += 1
                if len(joueur_coups) > capacite_coup:
                    joueur_coups.pop(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                vies +=10
            # Tir de méga-épée avec la touche 'm'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if len(joueur_mega_epee) < limite_mega_epee:
                    mega_epee = pygame.Rect(joueur.x, joueur.y, taille_mega_epee, taille_mega_epee)
                    joueur_mega_epee.append(mega_epee)
                    supr = 1
                    vies += 1
                    nb_mega_epee += 1
                    for i in range(len(vie_mega_epees)):
                        if vie_mega_epees[i] <= 0:
                            vie_mega_epees[i] = vie_mega_epee_initiale
                            break
    if vies_2 > 0:
        if player2 == True:
            # Gestion des mouvements du joueur
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q] and joueur2.left > 0:
                joueur2.x -= vitesse_joueur2
                orientation_joueur2 = "gauche"
            if keys[pygame.K_d] and joueur2.right < largeur_fenetre:
                joueur2.x += vitesse_joueur2
                orientation_joueur2 = "droite"
            if keys[pygame.K_z] and joueur2.top > 0:
                joueur2.y -= vitesse_joueur2
                orientation_joueur2 = "haut"
            if keys[pygame.K_s] and joueur2.bottom < hauteur_fenetre:
                joueur2.y += vitesse_joueur2
    
    if vies > 0 :
        # Gestion des mouvements du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and joueur.left > 0:
            joueur.x -= vitesse_joueur
            orientation_joueur = "gauche"
        if keys[pygame.K_RIGHT] and joueur.right < largeur_fenetre:
            joueur.x += vitesse_joueur
            orientation_joueur = "droite"
        if keys[pygame.K_UP] and joueur.top > 0:
            joueur.y -= vitesse_joueur
            orientation_joueur = "haut"
        if keys[pygame.K_DOWN] and joueur.bottom < hauteur_fenetre:
            joueur.y += vitesse_joueur

    if player2 == True :
        # Mouvements des gobelins
        for gobelin in gobelins:
        # Si deux joueurs
            if player2:
                distance_joueur1 = distance(gobelin, joueur)
                distance_joueur2 = distance(gobelin, joueur2)
                
                # Sélectionner le joueur le plus proche
                if distance_joueur1 < distance_joueur2:
                    joueur_cible = joueur
                else:
                    joueur_cible = joueur2
                if vies <= 0 :
                    joueur_cible = joueur2
                if vies_2 <= 0 :
                    joueur_cible = joueur
            # Calculer les composantes x et y du vecteur direction vers le joueur cible
            vecteur_x = joueur_cible.x - gobelin.x
            vecteur_y = joueur_cible.y - gobelin.y
            
            # Normaliser le vecteur (le rendre unitaire)
            norme = ((vecteur_x ** 2) + (vecteur_y ** 2)) ** 0.5
            if norme != 0:
                vecteur_x /= norme
                vecteur_y /= norme
            
            # Déplacer le gobelin dans la direction du joueur cible
            gobelin.x += int(vecteur_x * vitesse_gobelins)
            gobelin.y += int(vecteur_y * vitesse_gobelins)
    else:  
        #Mouvements des gobelins
        for gobelin in gobelins:
            if joueur.x < gobelin.x:
                gobelin.x -= vitesse_gobelins
            else:
                gobelin.x += vitesse_gobelins
            if joueur.y < gobelin.y:
                gobelin.y -= vitesse_gobelins
            else:
                gobelin.y += vitesse_gobelins

    # Gestion des collisions et des points
    if player2 == True:
        # collision joueur2 avec vie
        if joueur2.colliderect(vie) and vie in vie_list:
            son_vie.play()
            vies_2 += random.randint(1,3)
            vie_mega_epees_2 = [v + 50 for v in vie_mega_epees_2]
            nb_coups_avant_vie = 20
            vie_list.remove(vie)

        if joueur2.colliderect(bombe) and bombe in bombe_list :
            nb_coups_avant_bombe = 30
            supr = 1
            bombe_list.remove(bombe)
    # collision joueur avec vie
    if joueur.colliderect(vie) and vie in vie_list:
        son_vie.play()
        vies += random.randint(1,3)
        vie_mega_epees = [v + 50 for v in vie_mega_epees]
        nb_coups_avant_vie = 20
        vie_list.remove(vie)

    if joueur.colliderect(bombe) and bombe in bombe_list :
        nb_coups_avant_bombe = 30
        supr = 1
        bombe_list.remove(bombe)

            # collision gobelins
    for gobelin in gobelins[:]:
        try:
            if vies_2 > 0:
                if player2 == True:
                    if joueur2.colliderect(gobelin):
                        vies_2 -= 1
                        supr = 1
                        points -= points_par_vie_perdue
                        gobelins.remove(gobelin)
                        son_degat.play()
        
                    for coup_2 in joueur_coups_2[:]:
                        if gobelin.colliderect(coup_2):
                            points += points_par_gobelin
                            gobelins.remove(gobelin)
                            joueur_coups_2.remove(coup_2)
                            son_epee.play()
                            nb_coups_avant_vie -= 1
                            nb_coups_avant_bombe -= 1
                            nb_mort += 1
        
                    for mega_epee_2 in joueur_mega_epee_2[:]:
                        if gobelin.colliderect(mega_epee_2):
                            points += points_par_gobelin
                            gobelins.remove(gobelin)
                            nb_mort += 1
                            nb_coups_avant_bombe -=1
                            nb_coups_avant_vie -= 1
                            son_epee.play()
                            vie_mega_epees_2[joueur_mega_epee_2.index(mega_epee_2)] -= 1 
    
            if vies > 0:
                if joueur.colliderect(gobelin):
                    vies -= 1
                    supr = 1
                    points -= points_par_vie_perdue
                    gobelins.remove(gobelin)
                    son_degat.play()
    
                for coup in joueur_coups[:]:
                    if gobelin.colliderect(coup):
                        points += points_par_gobelin
                        gobelins.remove(gobelin)
                        joueur_coups.remove(coup)
                        son_epee.play()
                        nb_coups_avant_vie -= 1
                        nb_coups_avant_bombe -= 1
                        nb_mort += 1
    
                for mega_epee in joueur_mega_epee[:]:
                    if gobelin.colliderect(mega_epee):
                        points += points_par_gobelin
                        gobelins.remove(gobelin)
                        nb_mort += 1
                        nb_coups_avant_bombe -=1
                        nb_coups_avant_vie -= 1
                        son_epee.play()
                        vie_mega_epees[joueur_mega_epee.index(mega_epee)] -= 1
    
        except ValueError:
            pass
    
    if player2 == True:
        for i in range(len(joueur_mega_epee_2) - 1, -1, -1):
            if vie_mega_epees_2[i] == 0:
                joueur_mega_epee_2.pop(i)
                vie_mega_epees_2.pop(i)
                limite_mega_epee -= 1
                break

    # Suppression des méga-épées utilisées
    for i in range(len(joueur_mega_epee) - 1, -1, -1):
        if vie_mega_epees[i] == 0:
            joueur_mega_epee.pop(i)
            vie_mega_epees.pop(i)
            limite_mega_epee -= 1
            break


    # Effets visuels en cas de collision avec un gobelin
    if supr == 1:
        supr = 0
        nb = 1
        fenetre.fill(couleur_fond_degat)
        for gobelin in gobelins[:]:
            gobelins.remove(gobelin)

    # Suppression des coups et des méga-épées hors de l'écran
    if player2 == True:
        joueur_coups_2 = [coup_2 for coup_2 in joueur_coups_2 if coup_2.colliderect(fenetre_rect)]
        joueur_mega_epee_2 = [mega_epee_2 for mega_epee_2 in joueur_mega_epee_2 if mega_epee_2.colliderect(fenetre_rect)]
    
    joueur_coups = [coup for coup in joueur_coups if coup.colliderect(fenetre_rect)]
    joueur_mega_epee = [mega_epee for mega_epee in joueur_mega_epee if mega_epee.colliderect(fenetre_rect)]
    
    # spawn vie
    if nb_coups_avant_vie <= 0 and not vie_list:
        nb_coups_avant_vie = 37
        vie = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)
        vie_list.append(vie)
    # spawn bombe
    if nb_coups_avant_bombe <= 0 and not bombe_list:
        nb_coups_avant_bombe = 30
        bombe = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)
        bombe_list.append(bombe)
    # Réglage en fonction du score
    if points < 100:
        taux_spawn = 30
        capacite_coup = 10
    elif points > 500 : 
        capacite_coup = 100
        vie_mega_epee_initiale = 100
        points_par_gobelin = random.randint(10,30)
    elif points > 150 :
        capacite_coup = 70
    elif points > 100 :
        taux_spawn = 70
        capacite_coup = 30
    else:
        taux_spawn = 70
        
    # Spawn de gobelins en fonction du score
    if points < 100:
        if random.randint(0, 100) < 100 // taux_spawn:
            gobelin = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)
            if player2 == True:
                while distance(gobelin, joueur2) < 2 * taille_sprite:
                    gobelin = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)
            while distance(gobelin, joueur) < 2 * taille_sprite:
                gobelin = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)
            gobelins.append(gobelin)
    elif points >= 100:
        if random.randint(0, 300) < points // taux_spawn:
            gobelin = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)
            if player2 == True:
                while distance(gobelin, joueur2) < 2 * taille_sprite:
                    gobelin = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)
            while distance(gobelin, joueur) < 2 * taille_sprite:
                gobelin = pygame.Rect(random.randint(0, largeur_fenetre - taille_sprite), random.randint(0, hauteur_fenetre - taille_sprite), taille_sprite, taille_sprite)
            gobelins.append(gobelin)

    # Affichage des éléments du jeu
    fenetre.blit(image_fond, (0, 0))
    if nb == 1:
        fenetre.fill(couleur_fond_degat)
        nb -= 1
    
    if vies_2 > 0 :
        if player2 == True : 
            fenetre.blit(image_joueur_2, joueur2)
        else : 
            fenetre.blit(image_joueur, joueur)

    if vies > 0 :
        fenetre.blit(image_joueur, joueur)
    else :
        fenetre.blit(image_joueur_2, joueur2)

    for gobelin in gobelins:
        fenetre.blit(image_gobelin, gobelin)

    if vies_2 > 0:
        if player2 == True:
            for coup_2 in joueur_coups_2:
                fenetre.blit(image_epee, coup_2.topleft)
            for mega_epee_2 in joueur_mega_epee_2:
                fenetre.blit(image_mega_epee, mega_epee_2.topleft)
    if vies > 0 :
        for coup in joueur_coups:
            fenetre.blit(image_epee, coup.topleft)
        for mega_epee in joueur_mega_epee:
            fenetre.blit(image_mega_epee, mega_epee.topleft)
    # Affichage des vies
    for vie in vie_list:
        fenetre.blit(image_vie, vie.topleft)
    for bombe in bombe_list:
        fenetre.blit(image_bombe, bombe.topleft)
    # Affichage des informations du jeu
    afficher_infos()
    font = pygame.font.Font(None, 36)
    meilleur_score_text = font.render(f"Best: {obtenir_meilleur_score()}", True, (255, 255, 0))
    fenetre.blit(meilleur_score_text, (10, 90))
    pygame.display.flip()
    ajouter_score(points)
    limite_scores_a_garder = 10
    supprimer_pires_scores(limite_scores_a_garder)
    clock.tick(40)
    if vies <= 0:
        vies = 0
    if vies_2 <= 0 :
        vies_2 = 0
    if vies <= 0 and vies_2 <= 0:
        while fin_nb == 0:
            # Son de fin de jeu
            son_fin.play()
            # Son de fin de jeu
            son_fin.play()
            # Fermeture de la connexion à la base de données et de Pygame
            time.sleep(3)
            fenetre.fill(couleur_fond_degat)
            font = pygame.font.Font(None, 36)
    
            point_text = font.render(f"Score: {points}", True, (50, 70, 200))
            meilleur_score_text = font.render(f"Best: {obtenir_meilleur_score()}", True, (255, 255, 0))

            
            fenetre.blit(point_text, (350, 10))
            fenetre.blit(meilleur_score_text, (350, 170))
            pygame.display.flip()
            if keys[pygame.K_KP_ENTER] :
                fin_nb = 1
                conn.close()