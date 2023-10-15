import random
from icecream import ic

MAX_GENERATION = 100

# Definition initial


popusize = 10
people = [random.sample(range(10), 5) for i in range(popusize)]

print(people)


def inialise():
    popusize = 10
    people = [random.sample(range(10), 5) for i in range(popusize)]

#Fonction d'evaluation
def evalu(individual):
    return sum(individual)


def mutation(individual):
    gene_mutant = random.randint(0,len(individual)-1)    #on choisis  un gene aleatoire a muter chez un individu
    individual[gene_mutant]=random.randint(0,9)     # on  remplace le gene choix  par  une nouvelle choisi aussi aleatoirement
    return individual                                         # return la nouvelle valeur muter
def selection_parent() :
    pass


def crossover(papa,mama):
    cross = random.randint(1,len(papa)-1)       # on choisis un point de croisement aleatoire
    child1 = papa[:cross] + mama[cross:]        # on cree un enfant 1 avec le gene de papa jusqua  la croisement et le gene de maman apres le croisement
    child2 = papa[:cross] + mama[cross:]        # on cree un enfant 2 avec le gene de papa jusqua  la croisement et le gene de maman apres le croisement
    return child1,child2


def ancestre_evalue(ancester ):
    return sum(ancester)


def remplacement() :
    pass
