import random


def generateur_nom(nombre:int):

    noms_fictif = []
    liste_noms = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller",
                  "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White",
                  "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson","Toure"]

    liste_prenoms = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Isabella", "Sophia", "Mia",
                     "Charlotte", "Amelia", "Harper", "Evelyn", "Abigail", "Emily", "Elizabeth",
                     "Mila", "Ella", "Avery", "Sofia", "Camila"]


    for _ in range(nombre):
        nom = random.choice(liste_noms)
        prenom = ''.join(random.choices(liste_prenoms))
        noms_fictif.append(f"{prenom} {nom}")

    print(noms_fictif)

def generator_infini():
    i = 0
    while True:
        yield i
        i += 2


generateur_nom(5)
#
# for i in generator_infini():
#     print(i)
#     if i > 30 :
#         break

# for l in b'Ymc':
#     print(l)