import bnlearn as bn
from pgmpy.factors.discrete import TabularCPD
import csv
import numpy as np
import sys
import os

N = 10

p_input = {
    'studies' : [[0.36], [0.64]],
    'loneliness' : [[0.85], [0.15]],
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
cpds = []
for node in unconditional_nodes:
    cpds.append(TabularCPD(variable=node, variable_card=2, values=p_input[node]))
for node in p_input:
    if node not in unconditional_nodes:
        evidence = [edge[0] for edge in edges if edge[1] == node]
        cpds.append(TabularCPD(variable=node, variable_card=2, values=p_input[node], evidence=evidence, evidence_card=[2]*len(evidence)))

DAG = bn.make_DAG(edges)
DAG = bn.make_DAG(DAG, CPD=cpds)

bn.print_CPD(DAG)


with open('out.csv', 'w', newline = '') as outFile:
    writer = csv.DictWriter(outFile, fieldnames=p_input.keys())
    writer.writeheader()
    real_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")
    for n in range(1000):
        row = {}
        for node in unconditional_nodes:
            row[node] = np.random.binomial(1, p_input[node][1][0])
        for node in p_input:
            if node not in unconditional_nodes:
                evidence = {}
                for edge in edges:
                    if edge[1] == node:
                        evidence[edge[0]] = row[edge[0]]
                cond_p = bn.inference.fit(DAG, variables=[node], evidence=evidence).df['p'][1]
                row[node] = np.random.binomial(1, cond_p)
        writer.writerow(row)
    sys.stdout = real_stdout

From data:
{'studies': 0.6299, 'loneliness': 0.1477, 'overeating': 0.3269, 'depression': 0.3644}
From distribition:
{'studies': 0.64, 'loneliness': 0.15, 'overeating': 0.32580000000000003, 'depression': 0.3629}
Difference:
{'studies': 0.010099999999999998, 'loneliness': 0.0022999999999999965, 'overeating': 0.0010999999999999899, 'depression': 0.0015000000000000013}

P(depression|overeating) from data:
0.6267837541163557
P(depression|overeating) from distribution:
0.6284375861118766
P(depression|overeating) difference
0.001653831995520938

