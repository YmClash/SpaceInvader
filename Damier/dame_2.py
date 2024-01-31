from tkinter import Tk, Canvas

# Initialisation des variables globales
pions_b = [(i, j) for i in range(3) for j in range(10) if (i + j) % 2 == 0]
pions_n = [(i, j) for i in range(7, 10) for j in range(10) if (i + j) % 2 == 0]
selected = None
joueur_actuel = 'rouge'  # Alternance entre 'rouge' et 'bleu'
case = 40  # Taille d'une case du damier

fenetre = Tk()
fenetre.title("Jeu de Dames")
can1 = Canvas(fenetre, width=case * 10, height=case * 10, bg='dark grey')
can1.pack(side="top")


def damier() :
    for i in range(10) :
        for j in range(10) :
            fill = 'black' if (i + j) % 2 == 0 else 'white'
            can1.create_rectangle(j * case, i * case, (j + 1) * case, (i + 1) * case, fill=fill)


def place_pions() :
    for i, j in pions_b :
        can1.create_oval(j * case + 5, i * case + 5, (j + 1) * case - 5, (i + 1) * case - 5, fill='red')
    for i, j in pions_n :
        can1.create_oval(j * case + 5, i * case + 5, (j + 1) * case - 5, (i + 1) * case - 5, fill='blue')


def select(event) :
    global selected, joueur_actuel
    col = event.x // case
    ligne = event.y // case
    pos = (ligne, col)

    # Détermine si le clic est sur un pion du joueur actuel
    is_pion_joueur = pos in pions_b if joueur_actuel == 'rouge' else pos in pions_n

    if selected and is_pion_joueur :
        # Si un pion était déjà sélectionné et l'utilisateur clique sur un autre pion du même joueur
        selected = pos  # Change la sélection
    elif selected :
        # Tente de déplacer le pion sélectionné
        effectuer_deplacement(selected, pos)
    elif is_pion_joueur :
        selected = pos  # Sélectionne le pion

def est_dame(pion, joueur):
    # Supposons que les dames sont stockées comme (ligne, colonne, 'dame')
    return len(pion) == 3 and pion[2] == 'dame'

def possibilites(pion, joueur):
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    resultats = []
    for dl, dc in directions:
        ligne, col = pion[0], pion[1]
        while 0 <= ligne + dl < 10 and 0 <= col + dc < 10:
            ligne += dl
            col += dc
            # Ajouter des vérifications pour les captures, etc.
            if ...:  # Vérifier si la case est libre ou si une capture est possible
                resultats.append((ligne, col))
            if not est_dame(pion, joueur):  # Les pions simples ne peuvent se déplacer que d'une case
                break
    return resultats


def effectuer_deplacement(origine, destination):
    global pions_b, pions_n, selected, joueur_actuel

    dx, dy = destination[0] - origine[0], destination[1] - origine[1]
    pions_adverses = pions_n if joueur_actuel == 'rouge' else pions_b

    # Vérifier le mouvement diagonal et la case libre (pour les pions simples)
    if abs(dx) == 1 and abs(dy) == 1 and destination not in pions_b + pions_n:
        deplacer_pion(origine, destination)
    # Gérer les captures
    elif abs(dx) == 2 and abs(dy) == 2:
        case_intermediaire = (origine[0] + dx // 2, origine[1] + dy // 2)
        if case_intermediaire in pions_adverses and destination not in pions_b + pions_n:
            pions_adverses.remove(case_intermediaire)
            deplacer_pion(origine, destination)

def deplacer_pion(origine, destination):
    global selected, joueur_actuel
    if joueur_actuel == 'rouge':
        pions_b.remove(origine)
        pions_b.append(destination)
    else:
        pions_n.remove(origine)
        pions_n.append(destination)
    selected = None  # Réinitialise la sélection après le déplacement
    joueur_actuel = 'bleu' if joueur_actuel == 'rouge' else 'rouge'  # Change de joueur
    dessiner_damier_et_pions()

def dessiner_damier_et_pions() :
    can1.delete("all")  # Efface tout le contenu du canvas
    damier()
    place_pions()


can1.bind("<Button-1>", select)
dessiner_damier_et_pions()

fenetre.mainloop()
