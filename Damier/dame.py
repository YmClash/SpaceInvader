import pygame
from constants import *
from plateaux import Plateau
from ia import IA
import time

count_noir = 0
count_blanc = 0


class Jeu:
    def __init__(self, mode_jeu='1V1', reseau=None):
        self.plateau = Plateau()
        self.tour = NOIR
        self.piece_selectionnee = None
        self.mouvements_valides = []
        self.mode_jeu = mode_jeu
        self.reseau = reseau

        # Définition des couleurs pour le mode en ligne
        if mode_jeu == MODE_HOTE:
            self.couleur_joueur = NOIR
        elif mode_jeu == MODE_CLIENT:
            self.couleur_joueur = BLANC
        else:
            self.couleur_joueur = None

        # Initialisation de l'IA

        if mode_jeu == '1VCPU':
            self.ia = IA(self, BLANC)
            self.ia_noir = None
        elif mode_jeu == 'CPUVCPU':
            self.ia = IA(self, BLANC)
            self.ia_noir = IA(self, NOIR)
        else:
            self.ia = None
            self.ia_noir = None

        self.dernier_mouvement = time.time()
        self.delai_ia = 0.5  # Délai entre les mouvements de l'IA

        # Score et temps
        self.score_noir = 0
        self.score_blanc = 0

        self.temps_debut = time.time()
        self.temps_partie = 0

        self.partie_terminee = False
        self.gagnant = None
        self.erreur_reseau = False

        pygame.font.init()
        self.police = pygame.font.Font(None, TAILLE_POLICE)
        self.police_score = pygame.font.Font(None, TAILLE_POLICE_SCORE)

    def actualiser(self, fenetre):
        temps_actuel = time.time()
        # Gestion du réseau
        # if self.reseau and self.reseau.est_connecter:
        #     donnees = self.reseau.recevoir_donnees()
        #     if donnees:
        #         self._appliquer_mouvement_reseau(donnees)
        #     elif not self.reseau.est_connecter:
        #         self.erreur_reseau = True
        #         self.partie_terminee = True
        #         self.message_fin = MESSAGE_CONNEXION_PERDUE

        if self.reseau:
            if not self.reseau.est_connecte:
                if not self.partie_terminee:
                    print("Déconnexion détectée")
                    self.erreur_reseau = True
                    self.partie_terminee = True
                    self.message_fin = MESSAGE_CONNEXION_PERDUE
            else:
                try:
                    donnees = self.reseau.recevoir_donnees()
                    if donnees:
                        if not self._appliquer_mouvement_reseau(donnees):
                            print("Erreur lors de l'application du mouvement")
                except Exception as e:
                    print(f"Erreur réseau dans actualiser: {e}")
                    self.erreur_reseau = True
                    self.partie_terminee = True
                    self.message_fin = MESSAGE_CONNEXION_PERDUE



        # self.temps_partie = int(time.time() - self.temps_debut)
        self.plateau.dessiner(fenetre)
        self.dessiner_mouvements_valides(fenetre)
        self.dessiner_interface(fenetre)

        # pygame.display.update()

        # Mise à jour du chronomètre
        if not self.partie_terminee:
            self.temps_partie = int(time.time() - self.temps_debut)
            temps_actuel = time.time()

            # Gestion des tours des IAs
            if temps_actuel - self.dernier_mouvement > self.delai_ia:
                if self.mode_jeu == 'CPUVCPU':
                    if self.tour == NOIR and self.ia_noir:
                        self.jouer_tour_ia_noir()
                    elif self.tour == BLANC and self.ia:
                        self.jouer_tour_ia()
                    self.dernier_mouvement = temps_actuel
                elif self.mode_jeu == '1VCPU' and self.tour == BLANC and self.ia:
                    self.jouer_tour_ia()
                    self.dernier_mouvement = temps_actuel

        # Vérification de fin de partie
        self.verifier_fin_partie()

        pygame.display.update()

    def dessiner_interface(self, fenetre):
        # Afficher les scores
        score_noir = self.police_score.render(f"Noir: {self.score_noir}", True, NOIR)
        score_blanc = self.police_score.render(f"Blanc: {self.score_blanc}", True, BLANC)
        fenetre.blit(score_noir, (10, 10))
        fenetre.blit(score_blanc, (TAILLE_FENETRE - 120, 10))

        # Afficher le chrono
        minutes = self.temps_partie // 60
        secondes = self.temps_partie % 60
        temps = self.police_score.render(f"Temps: {minutes:02d}:{secondes:02d}", True, ROUGE)
        fenetre.blit(temps, (TAILLE_FENETRE // 2 - 50, 10))

        # Affichage du rôle en mode en ligne
        if self.mode_jeu in [MODE_HOTE, MODE_CLIENT]:
            role = "Noirs" if self.couleur_joueur == NOIR else "Blancs"
            tour = "Votre tour" if self.est_mon_tour() else "Tour de l'adversaire"
            info_role = self.police.render(f"Vous jouez les {role} - {tour}", True, VERT)
            fenetre.blit(info_role, (TAILLE_FENETRE // 2 - 150, TAILLE_FENETRE - 30))

        # Afficher le message de fin si la partie est terminée
        if self.partie_terminee and self.gagnant:
            self.afficher_message_fin(fenetre)

    def afficher_message_fin(self, fenetre):
        # Créer un fond semi-transparent
        # fond = pygame.Surface((TAILLE_FENETRE, TAILLE_FENETRE))
        fond = pygame.Surface((600, 200))
        fond.fill(BEIGE)
        # fond.set_alpha(128)
        fond.set_alpha(230)

        fenetre.blit(fond, (TAILLE_FENETRE // 2 - 300, TAILLE_FENETRE // 2 - 50))

        # Afficher le message du gagnant
        message = f"{'Noir' if self.gagnant == NOIR else 'Blanc'} a gagné!"
        texte = self.police.render(message, True, self.gagnant)
        # texte = self.police.render(message, True,VERT)
        rect_texte = texte.get_rect(center=(TAILLE_FENETRE // 2, TAILLE_FENETRE // 2))
        fenetre.blit(texte, rect_texte)

        # Afficher le score final
        score = f"Score final - Noir: {self.score_noir} Blanc: {self.score_blanc}"
        texte_score = self.police_score.render(score, True, VERT)
        rect_score = texte_score.get_rect(center=(TAILLE_FENETRE // 2, TAILLE_FENETRE // 2 + 50))
        fenetre.blit(texte_score, rect_score)

    def verifier_fin_partie(self):
        pieces_noir = pieces_blanc = 0
        for ligne in range(8):
            for colonne in range(8):
                piece = self.plateau.get_piece(ligne, colonne)
                if piece:
                    if piece.couleur == NOIR:
                        pieces_noir += 1
                    else:
                        pieces_blanc += 1

        if pieces_noir == 0:
            self.partie_terminee = True
            self.gagnant = BLANC
        elif pieces_blanc == 0:
            self.partie_terminee = True
            self.gagnant = NOIR

    def dessiner_mouvements_valides(self, fenetre):
        if self.piece_selectionnee:
            self.mouvements_valides = self.obtenir_mouvements_valides(self.piece_selectionnee)
            for mouvenent in self.mouvements_valides:
                ligne, colonne = mouvenent
                x = colonne * TAILLE_CASE + TAILLE_CASE // 2
                y = ligne * TAILLE_CASE + TAILLE_CASE // 2
                pygame.draw.circle(fenetre, ROUGE, (x, y), 15)

    def jouer_tour_ia(self):
        mouvement = self.ia.obtenir_mouvement()
        if mouvement:
            ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee = mouvement
            piece = self.plateau.get_piece(ligne_depart, colonne_depart)
            if piece:
                self.piece_selectionnee = piece
                self._deplacer(ligne_arrivee, colonne_arrivee)
                self.piece_selectionnee = None

    def jouer_tour_ia_noir(self):
        mouvement = self.ia_noir.obtenir_mouvement()
        if mouvement:
            ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee = mouvement
            piece = self.plateau.get_piece(ligne_depart, colonne_depart)
            if piece:
                self.piece_selectionnee = piece
                self._deplacer(ligne_arrivee, colonne_arrivee)
                self.piece_selectionnee = None

    def est_mon_tour(self):
        if self.mode_jeu in [MODE_HOTE, MODE_CLIENT]:
            return self.tour == self.couleur_joueur
        return True

    def obtenir_mouvements_valides(self, piece):
        mouvements = []

        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nouveau_ligne = piece.ligne + dy
            nouveau_colonne = piece.colonne + dx

            if 0 <= nouveau_ligne < 8 and 0 <= nouveau_colonne < 8:
                if not self.plateau.get_piece(nouveau_ligne, nouveau_colonne):
                    if (piece.couleur == NOIR and dy > 0) or (piece.couleur == BLANC and dy < 0) or piece.est_dame:
                        mouvements.append((nouveau_ligne, nouveau_colonne))

                elif self.plateau.get_piece(nouveau_ligne, nouveau_colonne).couleur != piece.couleur:
                    saut_ligne = nouveau_ligne + dy
                    saut_colonne = nouveau_colonne + dx
                    if 0 <= saut_ligne < 8 and 0 <= saut_colonne < 8:
                        if not self.plateau.get_piece(saut_ligne, saut_colonne):
                            mouvements.append((saut_ligne, saut_colonne))

        return mouvements

    def selectionner(self, ligne, colonne):
        if self.partie_terminee:
            return False
        if not self.est_mon_tour():
            return False
        if self.piece_selectionnee:
            resultat = self._deplacer(ligne, colonne)
            if not resultat:
                self.piece_selectionnee = None
                self.selectionner(ligne, colonne)

        piece = self.plateau.get_piece(ligne, colonne)
        if piece and piece.couleur == self.tour:
            self.piece_selectionnee = piece
            return True

        return False

    def _deplacer(self, ligne, colonne,envoyer_reseau=True):
        piece = self.plateau.get_piece(ligne, colonne)
        if not piece and (ligne + colonne) % 2 == 1:
            resultat_valide = False
            if abs(ligne - self.piece_selectionnee.ligne) == 2:
                ligne_milieu = (ligne + self.piece_selectionnee.ligne) // 2
                colonne_milieu = (colonne + self.piece_selectionnee.colonne) // 2
                piece_milieu = self.plateau.get_piece(ligne_milieu, colonne_milieu)
                if piece_milieu and piece_milieu.couleur != self.tour:
                    # Ajouter des points pour la capture
                    if self.tour == NOIR:
                        self.score_noir += POINTS_CAPTURE
                    else:
                        self.score_blanc += POINTS_CAPTURE

                    self.plateau.supprimer_piece(piece_milieu)
                    self.plateau.deplacer(self.piece_selectionnee, ligne, colonne)
                    resultat_valide = True

            elif abs(ligne - self.piece_selectionnee.ligne) == 1:
                self.plateau.deplacer(self.piece_selectionnee, ligne, colonne)
                resultat_valide = True

            if resultat_valide:
                # Ajouter des points si la pièce devient une dame
                if (ligne == 0 and self.tour == BLANC) or (ligne == 7 and self.tour == NOIR):
                    if self.tour == NOIR:
                        self.score_noir += POINTS_DAME
                    else:
                        self.score_blanc += POINTS_DAME

                if envoyer_reseau:
                    if not self._envoyer_mouvement_reseau(self.piece_selectionnee.ligne, self.piece_selectionnee.colonne, ligne, colonne):
                        return False



                # ENVOI DU MOUVEMENT AU RESEAU
                # if self.reseau and not self.erreur_reseau:
                #     if ((self.mode_jeu == MODE_HOTE and self.tour == NOIR) or
                #             (self.mode_jeu == MODE_CLIENT and self.tour == BLANC)):
                #         mouvement = (self.piece_selectionnee.ligne, self.piece_selectionnee.colonne,
                #                      ligne, colonne)
                #         if not self.reseau.envoyer_donnees(mouvement):
                #             self.erreur_reseau = True
                #             self.partie_terminee = True
                #             self.message_fin = MESSAGE_CONNEXION_PERDUE
                #             # self.afficher_message_fin(pygame.display.get_surface())

                self.changer_tour()
                return True
        return False

    # def _appliquer_mouvement_reseau(self, donnees):
    #     ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee = donnees
    #     piece = self.plateau.get_piece(ligne_depart, colonne_depart)
    #     if piece and piece.couleur != self.couleur_joueur:
    #         self.piece_selectionnee = piece
    #         self._deplacer(ligne_arrivee, colonne_arrivee)
    #         self.piece_selectionnee = None
    def _appliquer_mouvement_reseau(self, donnees):
        try:
            ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee = donnees
            piece = self.plateau.get_piece(ligne_depart, colonne_depart)
            if piece and piece.couleur != self.couleur_joueur:  # Vérification supplémentaire
                self.piece_selectionnee = piece
                ancien_tour = self.tour
                if self._deplacer(ligne_arrivee, colonne_arrivee, False):  # False = ne pas renvoyer le mouvement
                    return True
                self.tour = ancien_tour  # Restaurer le tour si le mouvement échoue
            return False
        except Exception as e:
            print(f"Erreur mouvement réseau: {e}")
            return False

    def _envoyer_mouvement_reseau(self, ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee):
        if self.reseau and not self.erreur_reseau:
            if ((self.mode_jeu == MODE_HOTE and self.tour == NOIR) or
                    (self.mode_jeu == MODE_CLIENT and self.tour == BLANC)):
                mouvement = (ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee)
                if not self.reseau.envoyer_donnees(mouvement):
                    self.erreur_reseau = True
                    self.partie_terminee = True
                    self.message_fin = MESSAGE_CONNEXION_PERDUE
                    return False
                return True
        return False



    def changer_tour(self):
        global count_noir, count_blanc
        if self.tour == NOIR:
            self.tour = BLANC or RANDOM_COLORS_1
            count_blanc += 1
            print(f"Nombre de tours des Blancs : {count_blanc}")
            print("Tour des Blancs :")
            # self.tour = RANDOM_COLORS_1 if self.mode_jeu == '1VCPU' else BLANC
            self.dernier_mouvement = time.time()
        else:
            self.tour = NOIR
            count_noir += 1
            print(f"Nombre de tours des Noirs : {count_noir}")
            print("Tour des Noirs")
