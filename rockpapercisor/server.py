#Importe le module Python permettant de gérer les connexions réseau via des sockets.
import socket
#Importe des fonctions pour permettre le multi-threading dans Python.
from _thread import *
#Importe le module Python pour la sérialisation et la désérialisation d'objets.
import pickle
#Importe la classe Game depuis un fichier appelé game.
from game import Game
#Initialise l'adresse IP du serveur et le port sur lequel le serveur écoute.
server = "127.0.0.1"
port = 5556
#Crée un objet socket pour la communication via IPv4 et TCP.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Tente de lier le socket à l'adresse et au port spécifiés
try:
    s.bind((server, port))
except socket.error as e:
    str(e)
#Met le socket en mode écoute
s.listen(2)
#Affiche un message indiquant que le serveur est en attente de connexions.
print("Waiting for a connection, Server Started")
#Initialise des variables pour suivre les connexions, les jeux en cours et compter les ID.
connected = set()
games = {}
idCount = 0

#Définit une fonction pour gérer chaque client dans un thread distinct.
def threaded_client(conn, p, gameId):
    global idCount
    #Envoie au client son numéro de joueur (0 ou 1) après connexion.
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        #Nettoie et ferme la connexion perdue
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    #accepte la connexion entrante et retourne un nouvel objet de connexion
    conn, addr = s.accept()
    print("Connected to:", addr)
    #Gère les ID des jeux et des joueurs en leur attribuant des valeurs
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    #Vérifie si le nombre actuel de connexions est impair pour créer un nouveau jeu.
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        #Démarre un nouveau thread pour gérer le client connecté.
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))