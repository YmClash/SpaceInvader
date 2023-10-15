import random
from icecream import ic

MAX_GENERATION = 100

# Definition initial


popusize = 2
popu = [random.sample(range(10), 5) for i in range(popusize)]



def inialise():
    popusize = 10
    popu = [random.sample(range(10), 5) for i in range(popusize)]

#Fonction d'evaluation
def evalu(individual):
    return sum(individual)

def mutation(individual):
    gene_mutant = random.randint(0,len(individual)-1)    #on choisis  un gene aleatoire a muter chez un individu
    individual[gene_mutant]=random.randint(0,9)     # on  remplace le gene choix  par  une nouvelle choisi aussi aleatoirement
    return individual                                         # return la nouvelle valeur muter
def selection_parent(popu,scores):
    total_fitness = sum(scores)
    pick = random.uniform(0,total_fitness)
    current = 0
    for individual,score in zip(popu,scores):
        current += score
        if current > pick: return  individual
    return popu[-1]
    pass

def crossover(papa,mama):
    nombre_enfant = random.randint(1,3)
    for kid in range(0,nombre_enfant):
        cross = random.randint(1, len(papa) - 1)  # on choisis un point de croisement aleatoire


    return child1,child2
def ancestre_evalue(ancester):
    return sum(ancester)

def remplacement():
    pass


# boucle principale

for generation in range(MAX_GENERATION):
    scores = [evalu(individual)for individual in popu]
    print(f'Generation: {generation}  Scores: {scores}')
    #selection
    elite = [popu[i] for i in sorted(range(popusize),key=lambda x:scores[x])[:2]]

    offspring = []
    for o in range(popusize-2):
        papa =
        mama = random.choice(elite)
        child1,child2 = crossover(papa,mama)

        if random.random() < 0.1:
            cil
        offspring.append(mutation(child1))