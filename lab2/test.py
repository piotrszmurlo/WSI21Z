import numpy as np

population_size = 10
dim = 2
low_bound = 5
upp_bound = 10
population = np.full((population_size, dim), np.random.uniform(low_bound, upp_bound, (1, dim))[0])
# population = np.random.uniform(low_bound, upp_bound, (1, dim))[0]
# print(population)
# best_point = np.empty(10)
# print(best_point)

s = np.random.normal(0, 1, dim)
print(s)