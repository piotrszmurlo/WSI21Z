from random import gauss, randint, uniform

def find_minimum(iterations, population_size, tournament_size, elite_size, sigma, mutation_p):
    population = []
    upp_bound = 10
    low_bound = -10
    for i in range(0, population_size):
        r = uniform(low_bound, upp_bound)
        population.append((r, r**2)) 
    i = 0
    while i < iterations:
        population = sorted(population, key=lambda x: x[1])

        rep = []
        for j in range(0, population_size):
            winner = randint(0, population_size - 1)
            for k in range(0, tournament_size - 1):
                new_index = randint(0, population_size - 1)
                if new_index < winner:
                    winner = new_index
            rep.append(population[winner])
        for r in rep:
            r[0] += gauss(0,1)*sigma
            r[1] = r[0]**2



if __name__ == "__main__":
    population = []
    population_size = 10
    for i in range(0, population_size):
        r = uniform(-2, 2)
        population.append((r, r**2))
    population = sorted(population, key=lambda x: x[1])
    rep = []
    for j in range(0, population_size):
        winner = randint(0, population_size - 1)
        for k in range(0, 1):
            new_index = randint(0, population_size - 1)
            if new_index < winner:
                winner = new_index
        rep.append(population[winner])
    print(rep)
    # for r in rep:
    #     r
