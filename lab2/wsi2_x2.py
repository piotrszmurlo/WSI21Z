from random import gauss, randint, random
import numpy as np
from numpy.core.numeric import cross
import matplotlib.pyplot as plt
import math



def find_minimum(iterations, population_size, func, dim, tournament_size=2, elite_size=1, alfa=0.1, sigma=0.1, mutation_p=0.5, cross_p=0.5):
    upp_bound = 10
    low_bound = 8
    # population = np.random.uniform(low_bound, upp_bound, (population_size, dim))
    # best_point = min(population, key=func)
    population = np.random.uniform(low_bound, upp_bound, population_size)
    best_point = min(population, key=func)
    i = 0
    R_population = np.array([])
    pts = population.copy()
    while i < iterations:
        R_population = tournament_select(population, func, dim, tournament_size)
        M_population = cross_and_mutate(R_population, mutation_p, cross_p, alfa, sigma)
        new_best_point = min(M_population, key=func)
        if func(new_best_point) < func(best_point):
            best_point = new_best_point
        population = np.array(sorted(population, key=func))
        # population = np.concatenate((population[:elite_size], np.array([e for e in M_population if e not in population[:elite_size]])))[:-elite_size]
        # population = np.unique(np.concatenate((population[:elite_size], M_population)))[:-elite_size]
        # population = np.concatenate((population[:elite_size], np.array([e for e in M_population if e not in population[:elite_size]])))[:population.size]
        population = np.concatenate((population[:elite_size], M_population))
        population = np.array(sorted(population, key=func))
        population = population[:population_size]
        pts = np.concatenate((pts, population))
        i += 1
    pts = np.unique(pts)
    ys = pts**2
    plt.scatter(pts, ys)
    
    return best_point


def tournament_select(population, func, dim, tournament_size=2) -> np.ndarray:
    sorted_population = np.array(sorted(population, key=func))
    new_population = np.zeros_like(population)
    for i in range(population.size):
        winner_index = randint(0, population.size - 1)
        for _123 in range(tournament_size - 1):
            new_index = randint(0, population.size - 1)
            if new_index < winner_index:
                winner_index = new_index
        new_population[i] = sorted_population[winner_index]
    return new_population


def cross_and_mutate(population, mutation_p, cross_p, alfa, sigma) -> np.ndarray:
    population_size = len(population)
    M_population = np.empty_like(population)
    indexes = np.array((range(M_population.size)))
    i = 0
    while i < population_size:
        parents = np.random.choice(indexes, size=2, replace=False)
        if random() < cross_p:
            M_population[i] = alfa * population[parents[0]] + (1 - alfa) * population[parents[1]]
            if i + 1 < population.size:
                M_population[i + 1] = alfa * population[parents[1]] + (1 - alfa) * population[parents[0]]
        else:
            M_population[i] = population[parents[0]]
            if i + 1 < population.size:
                M_population[i + 1] = population[parents[1]]
        i += 2
    for j in range(M_population.size):
        if random() < mutation_p:
            M_population[j] += gauss(0, 1)*sigma
    return M_population


def main():
    iterations = 300
    population_size = 200
    tournament_size=2
    elite_size=1
    alfa=0.1
    sigma=0.1
    mutation_p=0.1
    cross_p=0.5
    # f = lambda w: math.cos(w[0]) + w[1]**2 - w[2]**1.5 
    func = lambda x: x**2
    dim = 1
    # population = np.random.uniform(-10, 10, population_size)
    # population = np.array(sorted(population, key=lambda x: x**2))
    # M_population = cross_and_mutate(population, mutation_p, cross_p, alfa, sigma)
    # print(population)
    # population = np.concatenate((population[:elite_size], M_population))
    # population = np.array(sorted(population, key=lambda x: x**2))
    # population = population[:population_size]
    # print(len(population) == population_size)

    x = np.linspace(-10,10,200)
    y= x**2
    plt.plot(x, y)
    print(find_minimum(iterations, population_size, func, dim, tournament_size, elite_size, alfa, sigma, mutation_p, cross_p))
    plt.show()


if __name__ == "__main__":
    main()