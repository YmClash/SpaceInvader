import random
from icecream import ic

MAX_GENERATION = 100
mutation_count = 0

# Definition initial


popusize = 3
popu = [random.sample(range(10), 5) for i in range(popusize)]
print(popu)
print()
print()
print()

def initial():
    popusize = 10
    popu = [random.sample(range(10), 5) for i in range(popusize)]

#Fonction d'evaluation
def evalu(individual):
    return sum(individual)

def mutation(individual):
    global mutation_count
    gene_mutant = random.randint(0,len(individual)-1)    #on choisis  un gene aleatoire a muter chez un individu
    individual[gene_mutant]=random.randint(0,9)     # on  remplace le gene choix  par  une nouvelle choisi aussi aleatoirement
    mutation_count+=1
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
    # Choisir un point de croisement aléatoire
    index = random.randint(1, len(papa) - 1)
    # Effectuer le croisement en échangeant les parties des parents
    child1 = papa[:index] + mama[index:]
    child2 = mama[:index] + papa[index:]
    return child1, child2



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
        papa = selection_parent(popu,scores)
        mama = selection_parent(popu,scores)
        child1,child2 = crossover(papa,mama)

        if random.random() < 0.1:
            child1 = mutation(child1)
        if random.random() < 0.1:
            child2 = mutation(child2)

        offspring.extend([child1,child2])

    popu = elite + offspring

print(f'Population Final: {popu}')
print(f'Nombre de mutation: {mutation_count}')
