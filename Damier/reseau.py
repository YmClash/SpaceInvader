import socket
import pickle
import threading
import time
import queue
import json



class ReseauJeu:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.est_serveur = False
        self.est_connecte = False
        self.adversaire = None
        self.port = 5555
        self.donnees_recues = queue.Queue()
        self.thread_reception = None
        self.thread_ping = None
        self.running = True
        self.dernier_ping = time.time()
        self.delai_timeout = 10.0  # 10 secondes sans réponse = déconnexion
        self.derniere_verification_ping = time.time()
        self.intervalle_ping = 2.0  # Envoyer un ping toutes les 2 secondes
        self.messages_recus = []
        self.message_lock = threading.Lock()


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
            self.dernier_ping = time.time()  # Réinitialiser le dernier ping
            print("Client Connecté au serveur reussi.")
            # self._demmarrer_thread_reception()
            self._demarrer_thread()
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
                try:
                    self._demarrer_threads()
                    print("Threads démarrés avec succès")
                except Exception as e:
                    print(f"Erreur lors du démarrage des threads: {e}")
                    self.est_connecte = False
                    self.adversaire.close()
                    return False
                return True
            except socket.timeout:
                # print("Aucune connexion acceptée dans le délai imparti.")
                return False
            except Exception as e:
                print(f"Erreur lors de l'acceptation de la connexion: {e}")
                return False
        return False

    def _thread_ping(self):
        while self.running and self.est_connecter:
            try:
                self._envoyer_ping()
                time.sleep(2.0)  # Envoi d'un ping toutes les 2 secondes
            except:
                pass

    def verifier_connection(self):
        if not self.est_connecter:
            return False

        maintenant = time.time()

        # Envoyer un ping régulièrement
        if maintenant - self.derniere_verification_ping >= self.intervalle_ping:
            self.envoyer_ping()
            self.derniere_verification_ping = maintenant

        # Vérifier le timeout
        if maintenant - self.dernier_ping > self.delai_timeout:
            print("Timeout - Aucune réponse du pair")
            self.deconnecter()
            return False

        return True

    def envoyer_ping(self):
        try:
            self.envoyer_donnees({'type': 'ping'})
        except:
            print("Erreur envoi ping")

    def recevoir_ping(self):
        self.dernier_ping = time.time()
        try:
            self.envoyer_donnees({'type': 'pong'})
        except:
            print("Erreur envoi pong")

    def recevoir_pong(self):
        self.dernier_ping = time.time()


    def _demarrer_thread(self):
        self.thread_reception = threading.Thread(target=self._thread_reception)
        self.thread_reception.daemon = True
        self.thread_reception.start()

        self.thread_ping = threading.Thread(target=self._thread_ping)
        self.thread_ping.daemon = True
        self.thread_ping.start()

    def _envoyer_ping(self):
        try:
            message = pickle.dumps("ping")
            if self.est_serveur and self.adversaire:
                self.adversaire.send(message)
            elif not self.est_serveur:
                self.socket.send(message)
            return True
        except:
            return False

    def _verifier_connexion(self):
        if time.time() - self.dernier_ping > self.delai_timeout:
            print(f"Timeout de connexion détecté - Dernier ping il y a {time.time() - self.dernier_ping} secondes")
            self.est_connecter = False
            return False
        return True

    def _thread_reception(self):
        while self.running and self.est_connecte:
            try:
                if self.est_serveur and self.adversaire:
                    socket_actif = self.adversaire
                else:
                    socket_actif = self.socket

                socket_actif.settimeout(1.0)
                try:
                    donnees = socket_actif.recv(4096)
                    if not donnees:
                        raise ConnectionError("Connexion perdue - Aucune donnée reçue")

                    try:
                        message = json.loads(donnees.decode())
                        # Traiter les messages de ping/pong
                        if message.get('type') == 'ping':
                            self.recevoir_ping()
                            continue
                        elif message.get('type') == 'pong':
                            self.recevoir_pong()
                            continue
                        # Autres messages
                        with self.message_lock:
                            self.messages_recus.append(message)
                    except json.JSONDecodeError:
                        # Essayer le format pickle pour la rétrocompatibilité
                        donnees_dechiffrees = pickle.loads(donnees)
                        if donnees_dechiffrees == "ping":
                            self.dernier_ping = time.time()
                            continue
                        else:
                            self.donnees_recues.put(donnees_dechiffrees)

                except socket.timeout:
                    # Une timeout est normale, on continue
                    pass
                except Exception as e:
                    print(f"Erreur lors de la réception : {e}")
                    raise

                # Vérification de la connexion
                if not self._verifier_connexion():
                    print("Connexion perdue - Timeout de ping")
                    break

            except Exception as e:
                print(f"Erreur thread réception: {e}")
                self.est_connecte = False
                break

            time.sleep(0.01)

    # def _thread_reception(self):
    #     while self.running and self.est_connecter:
    #         try:
    #             # donnees = self._recevoir()
    #             # if donnees:
    #             #     self.donnees_recues.put(donnees)
    #             if self.est_serveur and self.adversaire:
    #                 socket_actif = self.adversaire
    #             else:
    #                 socket_actif = self.socket
    #
    #             socket_actif.settimeout(1.0)
    #             try:
    #                 donnees = socket_actif.recv(4096)
    #                 if not donnees:
    #                     raise ConnectionError("Connexion perdue")
    #
    #                 if donnees == b'ping':
    #                     self.dernier_ping = time.time()
    #                     if self._envoyer_ping():  # Répondre au ping
    #                         continue
    #                 else:
    #                     self.donnees_recues.put(pickle.loads(donnees))
    #             except socket.timeout:
    #                 # Envoyer un ping périodique
    #                 if not self._envoyer_ping():
    #                     raise ConnectionError("Échec d'envoi du ping")
    #
    #             if not self._verifier_connexion():
    #                 break
    #         except Exception as e:
    #             # print(f"Erreur dans le thread de réception: {e}")
    #             print(f'Erreur Thread de réception: {e}')
    #             self.est_connecter = False
    #             break
    #         time.sleep(0.01)


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

    # def recevoir_donnees_thread(self):
    #     while self.est_connecter:
    #         try:
    #             donnees = self.socket.recv(4096)
    #             if not donnees:
    #                 print("Connexion perdue - aucune donnée reçue")
    #                 self.deconnecter()
    #                 break
    #
    #             message = json.loads(donnees.decode())
    #
    #             # Traiter les messages de ping/pong
    #             if message.get('type') == 'ping':
    #                 self.recevoir_ping()
    #                 continue
    #             elif message.get('type') == 'pong':
    #                 self.recevoir_pong()
    #                 continue
    #
    #             # Traiter les autres types de messages
    #             with self.message_lock:
    #                 self.messages_recus.append(message)
    #
    #         except socket.timeout:
    #             continue
    #         except json.JSONDecodeError:
    #             print("Erreur décodage JSON")
    #             continue
    #         except Exception as e:
    #             print(f"Erreur réception : {e}")
    #             self.deconnecter()
    #             break

    def recevoir_donnees(self):
        print("Reception des données...")
        try:
            return self.donnees_recues.get_nowait()
        except queue.Empty:
            return None

    def fermer(self):
        print("Fermeture de la connexion")
        self.running = False
        self.est_connecte = False

        if self.thread_reception:
            self.thread_reception.join(timeout=1.0)
        if self.thread_ping:
            self.thread_ping.join(timeout=1.0)

        if self.est_serveur and self.adversaire:
            try:
                self.adversaire.close()
            except:
                pass
        try:
            self.socket.close()
        except:
            pass

    def deconnecter(self):
        print("Déconnexion...")
        self.est_connecte = False
        self.running = False
        if self.thread_reception:
            self.thread_reception.join(timeout=1.0)
        if self.thread_ping:
            self.thread_ping.join(timeout=1.0)
        if self.est_serveur and self.adversaire:
            try:
                self.adversaire.close()
            except:
                pass
        self.adversaire = None



