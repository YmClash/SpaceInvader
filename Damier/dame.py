from tkinter import Tk, Canvas, Label, Button, messagebox, simpledialog

def damier():
    """Dessine le damier."""
    for i in range(10):
        for j in range(10):
            fill = 'black' if (i + j) % 2 == 0 else 'white'
            can1.create_rectangle(j*case, i*case, (j+1)*case, (i+1)*case, fill=fill)

def place_pions():
    """Place les pions sur le damier."""
    # Exemple de placement de pions, à adapter selon votre logique de jeu
    for i in range(3):  # Lignes de pions rouges
        for j in range(10):
            if (i + j) % 2 == 0:
                can1.create_oval(j*case+5, i*case+5, (j+1)*case-5, (i+1)*case-5, fill='red')
    for i in range(7, 10):  # Lignes de pions bleus
        for j in range(10):
            if (i + j) % 2 == 0:
                can1.create_oval(j*case+5, i*case+5, (j+1)*case-5, (i+1)*case-5, fill='blue')

# def select(event):
#     """Gère les événements de clic sur le damier."""
#     # Exemple de gestion de clic, à compléter avec votre logique de sélection et de mouvement
#     ligne = event.y // case
#     colonne = event.x // case
#     print(f"Case sélectionnée : ({ligne}, {colonne})")
#     # Ajoutez ici votre logique pour sélectionner ou déplacer un pion

def on_canvas_click(event):
    global selected, pos, pions_b, pions_n
    colonne, ligne = event.x // case, event.y // case
    dest = ligne * 10 + colonne
    if selected is not None and dest in pos:
        if deplacement(dest):
            # Rafraîchir l'affichage
            dessiner_damier()
            dessiner_pions()
            # Réinitialiser la sélection
            selected = None
        else:
            messagebox.showerror("Mouvement invalide", "Ce mouvement n'est pas autorisé.")
    else:
        # Logique pour sélectionner un pion
        # ...

def select(event) :
    global selected
    col = event.x // case
    ligne = event.y // case
    dest = ligne * 10 + col  # Conversion en format attendu par votre logique de déplacement

    if selected == -1 :
        selected = dest
    else :
        if deplacement(dest) :
            print("Déplacement réussi")
            # Mettre à jour l'affichage ici
        else :
            print("Déplacement invalide")
        selected = -1  # Réinitialiser la sélection

def interface():
    """Initialise et affiche l'interface graphique du jeu."""
    global fenetre, can1, case
    fenetre = Tk()
    fenetre.title("Jeu de Dames")

    case = 40  # Taille d'une case du damier
    can1 = Canvas(fenetre, width=case*10, height=case*10, bg='dark grey')
    can1.bind("<Button-1>", select)
    can1.pack(side="top")

    damier()  # Dessine le damier
    place_pions()  # Place les pions sur le damier

    fenetre.mainloop()

if __name__ == "__main__":
    interface()
