import socket
import pickle
import threading
import time
import queue



class ReseauJeu:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.est_serveur = False
        self.est_connecter = False
        self.adversaire = None
        self.port = 5555

        self.donnees_recues = queue.Queue()
        self.thread_reception = None
        # self.running = False
        self.running = True
        self.dernier_ping =  time.time()
        self.delai_timeout = 5.0  # Délai de timeout pour la connexion


    def creer_serveur(self):
        print("Création du serveur...")
        try:
            self.socket.bind(('', self.port))
            self.socket.listen(1)
            self.est_serveur = True
            self.socket.settimeout(1.0)  # Timeout pour éviter de bloquer indéfiniment
            print(f"Serveur créé sur le port {self.port}. En attente de connexion...")
            return True
        except Exception as e:
            print(f'Erreur lors de la création du serveur: {e}')
            return False

    def connecter_client(self,ip):
        print(f'Connexion du client au serveur à l\'adresse {ip}...')
        try:
            self.socket.settimeout(5.0)  # Timeout pour éviter de bloquer indéfiniment
            self.socket.connect((ip,self.port))
            self.est_connecter = True
            print("Client Connecté au serveur reussi.")
            self._demmarrer_thread_reception()
            return True
        except Exception as e:
            print(f'Erreur lors de la connexion au serveur: {e}')
            return False

    def accepter_connexion(self):
        print("Attente de connexion d'un client...")
        if self.est_serveur:
            try:
                self.adversaire, addr = self.socket.accept()
                self.adversaire.settimeout(1.0)  # Timeout pour éviter de bloquer indéfiniment            self.est_connecter = True
                print(f"Connexion acceptée de {addr}.")
                self._demmarrer_thread_reception()
                return True
            except socket.timeout:
                # print("Aucune connexion acceptée dans le délai imparti.")
                return False
            except Exception as e:
                print(f"Erreur lors de l'acceptation de la connexion: {e}")
                return False
        return False


    def _demmarrer_thread_reception(self):
        self.thread_reception = threading.Thread(target=self._thread_reception)
        self.thread_reception.daemon = True
        self.thread_reception.start()

    def _envoyer_ping(self):
        try:
            if self.est_serveur and self.adversaire:
                self.adversaire.send(b'ping')
            elif not self.est_serveur:
                self.socket.send(b'ping')
            return True
        except:
            return False

    def _verifier_connexion(self):
        if time.time() - self.dernier_ping > self.delai_timeout:
            print("Timeout de connexion detectö")
            self.est_connecter = False
            return False
        return True

    def _thread_reception(self):
        while self.running and self.est_connecter:
            try:
                # donnees = self._recevoir()
                # if donnees:
                #     self.donnees_recues.put(donnees)
                if self.est_serveur and self.adversaire:
                    socket_actif = self.adversaire
                else:
                    socket_actif = self.socket

                socket_actif.settimeout(1.0)
                try:
                    donnees = socket_actif.recv(4096)
                    if not donnees:
                        raise ConnectionError("Connexion perdue")

                    if donnees == b'ping':
                        self.dernier_ping = time.time()
                        if self._envoyer_ping():  # Répondre au ping
                            continue
                    else:
                        self.donnees_recues.put(pickle.loads(donnees))
                except socket.timeout:
                    # Envoyer un ping périodique
                    if not self._envoyer_ping():
                        raise ConnectionError("Échec d'envoi du ping")

                if not self._verifier_connexion():
                    break
            except Exception as e:
                # print(f"Erreur dans le thread de réception: {e}")
                print(f'Erreur Thread de réception: {e}')
                self.est_connecter = False
                break
            time.sleep(0.01)


    def _recevoir(self):
        try:
            if self.est_serveur and self.adversaire:
                donnees = self.adversaire.recv(4096)
            else:
                donnees = self.socket.recv(4096)
            if donnees:
                return pickle.loads(donnees)
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Erreur réception données: {e}")
            raise
        return None


    def envoyer_donnees(self, donnees):
        print("Envoi des données...")
        try:
            if not self.est_connecter:
                print("Erreur: Pas de connexion établie.")
                return False
            data = pickle.dumps(donnees)
            if self.est_serveur and self.adversaire:
                self.adversaire.send(data)
            elif not self.est_serveur:
                self.socket.send(data)
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi des données: {e}")
            self.est_connecter = False
            return False

    def recevoir_donnees(self):
        print("Reception des données...")
        try:
            return self.donnees_recues.get_nowait()
        except queue.Empty:
            return None


    def fermer(self):
        self.running = False
        if self.thread_reception:
            self.thread_reception.join(timeout=1)
        if self.est_serveur and self.adversaire:
            try:
                self.adversaire.close()
            except:
                pass
        try:
            self.socket.close()
        except:
            pass
        self.est_serveur = False



