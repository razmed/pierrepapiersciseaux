#Importe la bibliothèque Pygame pour la création de l'interface graphique
import pygame
#Importe une classe ou une fonction nommée Network depuis le fichier  network.
from network import Network
#Importe le module pickle pour la sérialisation et la désérialisation d'objets Python.
import pickle
#Initialise le module de polices de caractères pour Pygame.
pygame.font.init()
#Définit la largeur et la hauteur de la fenêtre du jeu.
width = 700
height = 700
# Crée une fenêtre de jeu de la taille spécifiée.
win = pygame.display.set_mode((width, height))
#Définit le titre de la fenêtre du jeu.
pygame.display.set_caption("Client")


class Button:
    #Initialise les attributs d'un bouton : texte, position (x, y) et couleur.
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
    #Méthode pour dessiner le bouton sur la fenêtre.
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("silkscreen", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))
    #Méthode pour détecter si un bouton est cliqué en fonction de la position de la souris.
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

#Fonction pour redessiner la fenêtre du jeu en fonction de son état actuel.
def redrawWindow(win, game, p):
    win.fill((0,0,0))

    if not(game.connected()):
        font = pygame.font.SysFont("rubik", 70)
        text =font.render("Attente de joueur...", 1, (255,255,255), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("Silkscreen", 50)
        text = font.render("Votre Choix", 1, (255, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Adversaire", 1, (255, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (255,255,255))
            text2 = font.render(move2, 1, (255, 255, 255))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (255,255,255))
            elif game.p1Went:
                text1 = font.render("Choix Effectués", 1, (255, 255, 255))
            else:
                text1 = font.render("En Attente...", 1, (255, 255, 255))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (255,255,255))
            elif game.p2Went:
                text2 = font.render("Choix Effectués", 1, (255, 255, 255))
            else:
                text2 = font.render("En Attente...", 1, (255, 255, 255))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

#Crée trois boutons pour les choix de pierre-feuille-ciseaux. 
btns = [Button("Pierre", 50, 500, (50,35,35)), Button("Sciseaux", 250, 500, (50,35,35)), Button("Papier", 450, 500, (50,35,35))]
#Définit la fonction principale du jeu.
def main():
    #Initialise des variables pour contrôler la boucle principale du jeu et le temps
    run = True
    clock = pygame.time.Clock()
    #Initialise un objet de la classe Network pour gérer la communication réseau.
    n = Network()
    #Obtient le numéro du joueur en se connectant au réseau.
    player = int(n.getP())
    print("You are player", player)
    #contrôle le déroulement du jeu
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("silkscreen", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (0,255,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (0,0,255))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        #Redessine la fenêtre du jeu avec les mises à jour
        redrawWindow(win, game, player)
#Définit une fonction pour l'écran de menu
def menu_screen():
    run = True
    clock = pygame.time.Clock()
   #affiche un écran de menu et attend un clic pour commencer le jeu.
    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("silkscreen", 60)
        text = font.render("Click pour jouer!", 1, (255,255,255))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()