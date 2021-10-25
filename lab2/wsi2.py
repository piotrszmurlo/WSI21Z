from random import gauss, randint, random
import numpy as np

def find_minimum(iterations, population_size, tournament_size, elite_size, sigma, mutation_p):
    f = lambda x: x**2
    upp_bound = 10
    low_bound = -10
    population = np.random.uniform(low_bound, upp_bound, population_size)
    best_point = min(population, key=lambda x: x**2)
    i = 0
    while i < iterations:
        temp_population = tournament_select(population, tournament_size)
        for point in temp_population:
            if random() < mutation_p:
                point += gauss(0, 1)*sigma
        new_best_point = min(population, key=lambda x: x**2)
        if f(new_best_point) < f(best_point):
            best_point = new_best_point

def tournament_select(population, tournament_size=2) -> np.ndarray:
    sorted_population = np.array(sorted(population, key=lambda x: x**2))
    new_population = np.zeros_like(population)
    population_size = population.size
    for i in range(population_size):
        winner_index = randint(0, population_size - 1)
        for _123 in range(tournament_size - 1):
            new_index = randint(0, population_size - 1)
            if new_index < winner_index:
                winner_index = new_index
        new_population[i] = sorted_population[winner_index]
    return new_population



if __name__ == "__main__":
    population_size = 10
    population = np.random.uniform(-5, 5, population_size)
