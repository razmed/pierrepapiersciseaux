# Importe les modules nécessaires 
#pour la communication via des sockets 
#et pour la sérialisation/désérialisation des données
import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5556
        # Crée un tuple représentant l'adresse du serveur avec l'IP et le port.
        self.addr = (self.server, self.port)
        #Appelle la méthode connect() pour établir la connexion avec le serveur
        self.p = self.connect()
    #Méthode pour obtenir le numéro du joueur
    def getP(self):
        return self.p
    #Méthode pour établir la connexion avec le serveur
    def connect(self):
        # reçoit et retourne les données du serveur à travers le socket
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    #envoyer des données au serveur
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)



