import bnlearn as bn
from pgmpy.factors.discrete import TabularCPD
import csv
import numpy as np
import os, contextlib

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


<<<<<<< HEAD
with open(os.devnull, 'w') as devnull:
    with contextlib.redirect_stdout(devnull):
        with open('out.csv', 'w', newline = '') as outFile:
            writer = csv.DictWriter(outFile, fieldnames=p_input.keys())
            writer.writeheader()
            for n in range(N):
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

def check_output(out_filename):
    with open(out_filename, newline ='') as outFile:
        output = csv.DictReader(outFile)
        fieldnames = output.fieldnames
        p = {}
        dist_p = {}
        diff_p = {}
        for field_name in fieldnames:
            p[field_name] = 0
            dist_p[field_name] = bn.inference.fit(DAG, variables=[field_name], evidence={}).df['p'][1]
        for line in output:
            for field_name in fieldnames:
                p[field_name] += int(line[field_name])
        for key in p:
            p[key] = p[key] / N
        print('From data:')
        print(p)
        print('From distribition:')
        print(dist_p)
        for field_name in fieldnames:
            diff_p[field_name] = abs(p[field_name] - dist_p[field_name])
        print('Difference:')
        print(diff_p)
        return p

p = check_output('out.csv')

dist_p_depression_overeating = bn.inference.fit(DAG, variables=['overeating'], evidence={'depression' : 1}).df['p'][1]

p_depression_overeating = 0
with open('out.csv', newline ='') as outFile:
    output = csv.DictReader(outFile)
    for line in output:
        if int(line['depression']) == 1:
            p_depression_overeating += int(line['overeating'])
p_depression_overeating = p_depression_overeating/N/p['depression']


print("P(depression|overeating) from data:")
print(p_depression_overeating)
print("P(depression|overeating) from distribution:")
print(dist_p_depression_overeating)
print("P(depression|overeating) difference")
print(abs(p_depression_overeating - dist_p_depression_overeating))
=======
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

>>>>>>> 1af646792f5d73910458228c9cb54f5b3712da15
