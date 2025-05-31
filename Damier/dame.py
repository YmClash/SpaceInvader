import pygame
from constants import *
from plateaux import Plateau
from ia import IA
import time


count_noir= 0
count_blanc = 0

class Jeu:
    def __init__(self,mode_jeu='1V1'):
        self.plateau = Plateau()
        self.tour = NOIR
        self.piece_selectionnee = None
        self.mouvements_valides = []
        self.mode_jeu = mode_jeu

        # Initialisation de l'IA

        if mode_jeu == '1VCPU':
            self.ia = IA(self, BLANC)
            self.ia_noir = None
        elif mode_jeu == 'CPUVCPU':
            self.ia = IA(self, BLANC)
            self.ia_noir = IA(self, NOIR)
        else:
            self.ia = None
            self.ia_2 = None


        self.dernier_mouvement = time.time()
        self.delai_ia = 0.5  # Délai entre les mouvements de l'IA

        # Score et temps
        self.score_noir = 0
        self.score_blanc = 0

        self.temps_debut = time.time()
        self.temps_partie = 0

        self.partie_terminee = False
        self.gagnant = None
        pygame.font.init()
        self.police = pygame.font.Font(None, TAILLE_POLICE)
        self.police_score = pygame.font.Font(None, TAILLE_POLICE_SCORE)


    def actualiser(self, fenetre):
        # self.temps_partie = int(time.time() - self.temps_debut)
        self.plateau.dessiner(fenetre)
        self.dessiner_mouvements_valides(fenetre)
        self.dessiner_interface(fenetre)

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

        # Afficher le message de fin si la partie est terminée
        if self.partie_terminee and self.gagnant:
            self.afficher_message_fin(fenetre)

    def afficher_message_fin(self, fenetre):
        # Créer un fond semi-transparent
        fond = pygame.Surface((TAILLE_FENETRE, TAILLE_FENETRE))
        fond.set_alpha(128)
        fond.fill(GRIS)
        fenetre.blit(fond, (0, 0))

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
                ligne,colonne = mouvenent
                x = colonne * TAILLE_CASE + TAILLE_CASE // 2
                y = ligne * TAILLE_CASE + TAILLE_CASE // 2
                pygame.draw.circle(fenetre,ROUGE,(x,y),15)



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
            ligne_depart,colonne_depart, ligne_arrivee, colonne_arrivee = mouvement
            piece = self.plateau.get_piece(ligne_depart, colonne_depart)
            if piece:
                self.piece_selectionnee = piece
                self._deplacer(ligne_arrivee, colonne_arrivee)
                self.piece_selectionnee = None


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

    def _deplacer(self, ligne, colonne):
        piece = self.plateau.get_piece(ligne, colonne)
        if not piece and (ligne + colonne) % 2 == 1:
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

                    # Ajouter des points si la pièce devient une dame
                    if (ligne == 0 and self.tour == BLANC) or (ligne == 7 and self.tour == NOIR):
                        if self.tour == NOIR:
                            self.score_noir += POINTS_DAME
                        else:
                            self.score_blanc += POINTS_DAME

                    self.changer_tour()
                    return True
            elif abs(ligne - self.piece_selectionnee.ligne) == 1:
                self.plateau.deplacer(self.piece_selectionnee, ligne, colonne)

                # Ajouter des points si la pièce devient une dame
                if (ligne == 0 and self.tour == BLANC) or (ligne == 7 and self.tour == NOIR):
                    if self.tour == NOIR:
                        self.score_noir += POINTS_DAME
                    else:
                        self.score_blanc += POINTS_DAME

                self.changer_tour()
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
