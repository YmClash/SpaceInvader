import pygame
from constants import *
from dame import Jeu
from reseau import ReseauJeu
import tkinter as tk
from tkinter import simpledialog
import socket




pygame.init()
FENETRE = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption('Jeu de Dames by YmC')
mode = []

def afficher_ip():
    print("Affichage de l'IP Hôte...")
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(f"Adresse IP locale: {ip}")
    return ip




def demander_ip():
    print("Demander l'IP du serveur...")
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    ip = simpledialog.askstring("Connexion", "Entrez l'IP du hote :")
    print("IP demandée :", ip)
    return ip


def obtenir_position_souris():
    x, y = pygame.mouse.get_pos()
    ligne = y // TAILLE_CASE
    colonne = x // TAILLE_CASE
    return ligne, colonne


def dessiner_message_attente():
    FENETRE.fill(BEIGE)
    police = pygame.font.Font(None, 50)
    message = police.render(MESSAGE_ATTENTE, True, NOIR)
    message_rect = message.get_rect(center=(TAILLE_FENETRE // 2, TAILLE_FENETRE // 2))
    FENETRE.blit(message, message_rect)
    pygame.display.update()



def dessiner_menu():
    FENETRE.fill(BEIGE)
    police = pygame.font.Font(None, 74)

    # Titre
    titre = police.render("Jeu de Dames by YmC", True, RANDOM_COLORS_2)
    titre_rect = titre.get_rect(center=(TAILLE_FENETRE // 2, TAILLE_FENETRE // 4))
    FENETRE.blit(titre, titre_rect)

    # Boutons
    police_bouton = pygame.font.Font(None, 50)

    bouton_1v1 = police_bouton.render("1 VS 1", True, NOIR)
    bouton_1v1_rect = bouton_1v1.get_rect(center=(TAILLE_FENETRE // 2, TAILLE_FENETRE // 2 -100))
    pygame.draw.rect(FENETRE, MARRON, bouton_1v1_rect.inflate(60, 30))  # 20,10
    FENETRE.blit(bouton_1v1, bouton_1v1_rect)

    bouton_1vcpu = police_bouton.render("1 VS CPU", True, NOIR)
    bouton_1vcpu_rect = bouton_1vcpu.get_rect(center=(TAILLE_FENETRE // 2, TAILLE_FENETRE // 2 ))
    pygame.draw.rect(FENETRE, MARRON, bouton_1vcpu_rect.inflate(60, 30))
    FENETRE.blit(bouton_1vcpu, bouton_1vcpu_rect)

    bouton_cpuvcpu = police_bouton.render("CPU VS CPU", True, NOIR)
    bouton_cpuvcpu_rect = bouton_cpuvcpu.get_rect(center=(TAILLE_FENETRE // 2, TAILLE_FENETRE // 2 + 100))
    pygame.draw.rect(FENETRE, MARRON, bouton_cpuvcpu_rect.inflate(60, 30))
    FENETRE.blit(bouton_cpuvcpu, bouton_cpuvcpu_rect)

    bouton_heberger = police_bouton.render("Héberger partie en ligne", True, NOIR)
    bouton_heberger_rect = bouton_heberger.get_rect(center=(TAILLE_FENETRE // 2, TAILLE_FENETRE // 2 + 200))
    pygame.draw.rect(FENETRE, MARRON, bouton_heberger_rect.inflate(60, 30))
    FENETRE.blit(bouton_heberger, bouton_heberger_rect)

    bouton_rejoindre = police_bouton.render("Rejoindre partie en ligne", True, NOIR)
    bouton_rejoindre_rect = bouton_rejoindre.get_rect(center=(TAILLE_FENETRE // 2, TAILLE_FENETRE // 2 + 300))
    pygame.draw.rect(FENETRE, MARRON, bouton_rejoindre_rect.inflate(60, 30))
    FENETRE.blit(bouton_rejoindre, bouton_rejoindre_rect)

    pygame.display.update()
    return bouton_1v1_rect, bouton_1vcpu_rect, bouton_cpuvcpu_rect, bouton_heberger_rect, bouton_rejoindre_rect


def main():
    # Menu principal
    # bouton_1v1_rect, bouton_1vcpu_rect ,bouton_cpuvcpu_rect = dessiner_menu()
    bouton = dessiner_menu()
    bouton_1v1_rect, bouton_1vcpu_rect, bouton_cpuvcpu_rect, bouton_heberger_rect, bouton_rejoindre_rect = bouton
    mode_jeu = None
    reseau = None
    afficher_ip()

    # Boucle du menu
    while mode_jeu is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if bouton_1v1_rect.collidepoint(x, y):
                    mode_jeu = '1V1'
                    mode.append('1_VS_1')
                elif bouton_1vcpu_rect.collidepoint(x, y):
                    mode_jeu = '1VCPU'
                    mode.append('1_VS_CPU')
                elif bouton_cpuvcpu_rect.collidepoint(x, y):
                    mode_jeu = 'CPUVCPU'
                    mode.append('CPU_VS_CPU')
                elif bouton_heberger_rect.collidepoint(x, y):
                    mode_jeu = 'HEBERGER'
                    mode.append('HEBERGER')
                    # ip = demander_ip()
                    reseau = ReseauJeu()
                    if reseau.creer_serveur():
                        mode_jeu = 'MODE_HOTE'
                        dessiner_message_attente()
                        reseau.accepter_connexion()
                elif bouton_rejoindre_rect.collidepoint(x, y):
                    mode_jeu = 'REJOINDRE'
                    mode.append('REJOINDRE')
                    ip = demander_ip()
                    if ip:
                        reseau = ReseauJeu()
                        if reseau.connecter_client(ip):
                            mode_jeu = 'MODE_CLIENT'



    # Démarrage du jeu
    jeu = Jeu(mode_jeu, reseau)
    running = True
    print("Mode de jeu sélectionné :", mode_jeu)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if reseau:
                    reseau.fermer()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode_jeu in ['1V1', MODE_HOTE, MODE_CLIENT]:
                    if (mode_jeu == '1V1') or \
                            (mode_jeu == MODE_HOTE and jeu.tour == NOIR) or \
                            (mode_jeu == MODE_CLIENT and jeu.tour == BLANC):
                        ligne, colonne = obtenir_position_souris()
                        jeu.selectionner(ligne, colonne)
                elif mode_jeu == '1VCPU' and jeu.tour == NOIR:
                    ligne, colonne = obtenir_position_souris()
                    jeu.selectionner(ligne, colonne)

        jeu.actualiser(FENETRE)

    pygame.quit()




def print_game_info():

    print("Bienvenue dans le jeu de dames !")
    print("Utilisez la souris pour sélectionner une pièce et la déplacer.")
    print("Les pièces noires sont en bas, les blanches en haut.")
    print("Pour gagner, capturez toutes les pièces de l'adversaire.")
    print("Appuyez sur la croix pour quitter le jeu.")


    print("Taile de la fenêtre :", TAILLE_FENETRE)
    print("Taille de la case :", TAILLE_CASE)
    print(f'Mode de jeu sélectionné : {mode}')





if __name__ == '__main__':
    main()

#
# pygame.init()
#
# FENETRE = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
# pygame.display.set_caption("Jeu de Dame by YmC")
#
# def obtenir_posion_souris():
#     x,y = pygame.mouse.get_pos()
#     ligne = y // TAILLE_CASE
#     colonne = x // TAILLE_CASE
#     return ligne, colonne
#
#
#
# def main():
#     jeu = Jeu()
#     running = True
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 ligne, colonne = obtenir_posion_souris()
#                 jeu.selectionner(ligne, colonne)
#
#         jeu.actualiser(FENETRE)
#
#     pygame.quit()
#
# if __name__ == "__main__":
#     main()