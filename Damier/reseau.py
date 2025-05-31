import socket
import pickle
import threading
import time



class ReseauJeu:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.est_serveur = False
        self.est_connecter = False
        self.adversaire = None
        self.port = 5555


    def creer_serveur(self):
        print("Création du serveur...")
        try:
            self.socket.bind(('', self.port))
            self.socket.listen(1)
            self.est_serveur = True
            return True
        except:
            print("Erreur lors de la création du serveur.")
            return False

    def connecter_client(self,ip):
        print("En Attente d'un client...")
        try:
            self.socket.connect((ip,self.port))
            self.est_connecter = True
            print("Client Connecté au serveur.")
        except:
            print("Erreur lors de la connexion du Client au serveur.")
            return False

    def accepter_connexion(self):
        if self.est_serveur:
            self.adversaire, _ = self.socket.accept()
            self.est_connecter = True
            print("Client connecté Accepter part lerserveur.")
            return True
        return False

    def envoyer_donnees(self, donnees):
        print("Envoi des données...")
        try:
            if self.est_serveur:
                print("Envoi des données au client...")
                self.adversaire.send(pickle.dumps(donnees))
            else:
                self.socket.send(pickle.dumps(donnees))
            return True
        except:
            print("Erreur lors de l'envoi des données.")
            return False

    def recevoir_donnees(self):
        print("Reception des données...")
        try:
            if self.est_serveur:
                donnees = self.adversaire.recv(4096)
            else:
                donnees = self.socket.recv(4096)
            return pickle.loads(donnees)
        except:
            print("Erreur lors de la réception des données.")
            return None


    def fermer(self):
        if self.est_serveur and self.adversaire:
            self.adversaire.close()
        self.socket.close()
        self.est_connecter = False


