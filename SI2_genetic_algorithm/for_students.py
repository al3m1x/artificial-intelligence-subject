from itertools import compress
import random
import time
import matplotlib.pyplot as plt

from data import *

def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]

def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))

def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness

# 2.1.2 Wybór rodziców - selekcja ruletkowa
def roulette_wheel_selection(population, knapsack_max_capacity, n_selection, items):
    fitness_scoreboard = []
    probability = []
    selected_individuals = []
    for individual in population:
        fitness_scoreboard.append(fitness(items, knapsack_max_capacity, individual))
    total_fitness = sum(fitness_scoreboard)
    for fitnesses in fitness_scoreboard:
        probability.append(fitnesses/total_fitness)
    for _ in range(n_selection):
        r = random.random()
        cumulative_probability = 0
        for i, p in enumerate(probability):
            cumulative_probability += p
            if r <= cumulative_probability:
                selected_individuals.append(population[i])
                break
    return selected_individuals

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def create_next_generation(selected_parents, population_size, elite_number, survivors_number):
    next_generation = []
    while len(next_generation) < (population_size-elite_number-survivors_number):
        parent1, parent2 = random.sample(selected_parents, 2)
        selected_parents.remove(parent1)
        selected_parents.remove(parent2)
        child1, child2 = crossover(parent1, parent2)
        next_generation.extend([child1, child2])
    return next_generation

def mutation(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = not individual[i]
    return individual


items, knapsack_max_capacity = get_big()
print(items)

population_size = 100
generations = 200
n_selection = 20
parent_number = 20
elite_number = 5
survivors_number = 100 - parent_number - elite_number

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
# 2.1.1 Tworzenie początkowej populacji rozwiązań
population = initial_population(len(items), population_size)
for _ in range(generations):
    population_history.append(population)
    # TODO: implement genetic algorithm
    # 2.1.2 Wybór rodziców - selekcja ruletkowa, oprócz tego wybieramy część populacji, która zostanie z poprzedniej generacji
    selected_parents = roulette_wheel_selection(population, knapsack_max_capacity, parent_number, items)
    selected_survivors = roulette_wheel_selection(population, knapsack_max_capacity, survivors_number, items)
    # 2.1.3 Tworzenie kolejnego pokolenia
    new_population = create_next_generation(selected_parents, population_size, elite_number, survivors_number)
    # 2.1.4 Mutacja
    for individuals in new_population:
        mutation(individuals, 0.10)

    # 2.1.5 Aktualizacja populacji rozwiązań
    sorted_population = sorted(population, key=lambda x: fitness(items, knapsack_max_capacity, x), reverse=True)
    elites = sorted_population[:elite_number]
    population = selected_survivors + new_population + elites

    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)

end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
