class Game:
    def __init__(self, id):
        #Initialise les attributs pour indiquer si 
        #chaque joueur a fait son mouvement et si le jeu est prêt à commencer
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        #Crée une liste pour stocker les mouvements des joueurs
        self.moves = [None, None]
        #Initialise les compteurs de victoires pour chaque joueur et de parties nulles.
        self.wins = [0,0]
        self.ties = 0
#btenir le mouvement d'un joueur spécifique 
    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
    #vérifier si les deux joueurs sont connectés
    def connected(self):
        return self.ready
    # vérifier si les deux joueurs ont effectué leur mouvement
    def bothWent(self):
        return self.p1Went and self.p2Went
    # déterminer le gagnant
    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False