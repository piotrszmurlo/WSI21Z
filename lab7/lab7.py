import bnlearn as bn
from pgmpy.factors.discrete import TabularCPD
import csv
import numpy as np
import sys
N = 10
# uncond1_input = {'name' : 'studies', 'p' : 0.64}
# uncond2_input = {'name' : 'loneliness', 'p' : 0.15}
# cond1_input = {}
# cond2_input = {}

p_input = {
    'studies' : [[0.64], [0.36]],
    'loneliness' : [[0.15], [0.85]],
    'overeating' : [[0.85, 0.35, 0.7, 0.15],
                    [0.15, 0.65, 0.3, 0.85]],
    'depression' : [[0.8, 0.3], [0.2, 0.7]]
}

edges_input = {
    'studies' : 'overeating',
    'loneliness' : 'overeating',
    'overeating' : 'depression'
}

edges = [(edge, edges_input[edge]) for edge in edges_input]
unconditional_nodes = [node for node in edges_input if node not in edges_input.values()]
print(unconditional_nodes)
studies = TabularCPD(variable='studies', variable_card=2, values=[[0.64], [0.36]])
unconditional_cpd = []
for node in unconditional_nodes:
    unconditional_cpd.append(TabularCPD(variable=node, variable_card=2, values=p_input[node]))
# loneliness = TabularCPD(variable='loneliness', variable_card=2, values=[[0.15], [0.85]])

# overeating = TabularCPD(variable='overeating', variable_card=2,
#                  values=[[0.85, 0.35, 0.7, 0.15],
#                          [0.15, 0.65, 0.3, 0.85]],
#                  evidence=['studies', 'loneliness'],
#                  evidence_card=[2, 2])

# depression = TabularCPD(variable='depression', variable_card=2, values=[[0.8, 0.3], [0.2, 0.7]], evidence=['overeating'], evidence_card=[2])



# DAG = bn.make_DAG(edges)
# DAG = bn.make_DAG(DAG, CPD=[studies, loneliness, overeating, depression])

# bn.print_CPD(DAG)


# with open('out.csv', 'w', newline = '' ) as outFile:
#     writer = csv.writer(outFile)
#     writer.writerow([uncond1_input['name'], uncond2_input['name'], 'overeating', 'depression'])
#     for n in range(N):
#         uncond1_rand = np.random.binomial(1, uncond1_input['p'])
#         uncond2_rand = np.random.binomial(1, uncond2_input['p'])
#         cond1_p = bn.inference.fit(DAG, variables=['overeating'], evidence={'studies': uncond1_rand, 'loneliness' : uncond2_rand})
#         cond1_rand = np.random.binomial(1, cond1_p.df['p'][1])
#         cond2_p = bn.inference.fit(DAG, variables=['depression'], evidence={'overeating': cond1_rand})
#         cond2_rand = np.random.binomial(1, cond2_p.df['p'][1])

#         writer.writerow([uncond1_rand, uncond2_rand, cond1_rand, cond2_rand])