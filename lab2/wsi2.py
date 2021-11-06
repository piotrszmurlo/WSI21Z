from random import gauss, randint, random
import numpy as np
import matplotlib.pyplot as plt

def main():
    iterations = 50
    population_size = 20
    tournament_size=2
    elite_size=1
    alfa=0.5
    sigma=0.5
    mutation_p=1
    cross_p=0
    clones_start = False
    upp_bound = 5
    low_bound = -5
    # func = lambda x: x**2
    # func = lambda w: w[0]**2 + w[1]**2
    # func = lambda w: np.sin(w[0])*(np.exp(1-np.cos(w[1]))**2)+np.cos(w[1])*(np.exp(1-np.sin(w[0]))**2)+(w[0]-w[1])**2
    # func = lambda w: w[0]**2 + w[1]**2 + w[2]**2 + w[3]**2
    # func = lambda w: w[0]**2 + w[1]**3
    def func(w):
      sum1 = sum2 = 0
      for i in range(1,6):
          sum1 = sum1 + (i* np.cos(((i+1)*w[0]) +i))
          sum2 = sum2 + (i* np.cos(((i+1)*w[1]) +i))
      return sum1 * sum2
    dim = 2
    result = find_minimum(iterations, population_size, func, dim, tournament_size, elite_size, alfa, sigma, mutation_p, cross_p, clones_start, upp_bound, low_bound)
    if dim < 3:
        x = np.linspace(-20,20,100)
        y = np.linspace(-20,20,100)
        X, Y = np.meshgrid(x, y)
        Z = func(np.array([X, Y]))
        plt.contourf(X, Y, Z, alpha=0.5, levels=15)
        plt.colorbar()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.scatter(result[1][:, 0], result[1][:, 1], np.ones((len(result[1]), 1)), c='#FF0000')
        plt.show()
    print(f'value: {func(result[0])}')
    print(f'point: {result[0]}')


def find_minimum(iterations, population_size, func, dim, tournament_size=2, elite_size=1, alfa=0.1, sigma=0.1, mutation_p=0.5, cross_p=0.5, clones_start=False, upp_bound = 5, low_bound = -5):
    population = np.random.uniform(low_bound, upp_bound, (population_size, dim))
    best_point = min(population, key=func)
    i = 0
    R_population = np.array([])
    pts = population.copy()
    while i < iterations:
        R_population = tournament_select(population, func, dim, population_size, tournament_size)
        M_population = cross_and_mutate(R_population, mutation_p, cross_p, alfa, sigma, population_size)
        new_best_point = min(M_population, key=func)
        if func(new_best_point) < func(best_point):
            best_point = new_best_point
        population = np.array(sorted(population, key=func))
        # population = np.concatenate((population[:elite_size], np.array([e for e in M_population if e not in population[:elite_size]])))[:-elite_size]
        population = np.concatenate((population[:elite_size], M_population))
        population = np.array(sorted(population, key=func))
        population = population[:population_size]
        pts = np.concatenate((pts, population))
        i += 1
    return (best_point, pts)


def tournament_select(population, func, dim, population_size, tournament_size=2) -> np.ndarray:
    sorted_population = np.array(sorted(population, key=func))
    new_population = np.zeros_like(population)
    for i in range(population_size):
        winner_index = randint(0, population_size - 1)
        for _123 in range(tournament_size - 1):
            new_index = randint(0, population_size - 1)
            if new_index < winner_index:
                winner_index = new_index
        new_population[i] = sorted_population[winner_index]
    return new_population


def cross_and_mutate(population, mutation_p, cross_p, alfa, sigma, population_size) -> np.ndarray:
    M_population = np.empty_like(population)
    indexes = np.array((range(population_size)))
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
    for j in range(population_size):
        if random() < mutation_p:
            M_population[j] += gauss(0, 1)*sigma
    return M_population


if __name__ == "__main__":
    main()