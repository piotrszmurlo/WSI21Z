import bnlearn as bn
from pgmpy.factors.discrete import TabularCPD
edges_input = {
    'studies' : 'overeating',
    'loneliness' : 'overeating',
    'overeating' : 'depression'
}

edges = [(edge, edges_input[edge]) for edge in edges_input]
# rain = TabularCPD(variable='rain', variable_card=2, values=[[0.7], [0.3]])
# sprinkler = TabularCPD(variable='sprinkler', variable_card=2,
#                        values=[[0.2, 0.9],
#                                [0.8, 0.1]],
#                        evidence=['rain'], evidence_card=[2])
# wet = TabularCPD(variable='wet', variable_card=2,
#                  values=[[0.99, 0.1, 0.3, 0.05],
#                          [0.01, 0.9, 0.7, 0.95]],
#                  evidence=['rain', 'sprinkler'],
#                  evidence_card=[2, 2])

# edges = [('rain', 'sprinkler'),
#          ('rain', 'wet'),
#          ('sprinkler', 'wet')]

# DAG = bn.make_DAG(edges)
# DAG = bn.make_DAG(DAG, CPD=[rain, sprinkler, wet])

# bn.print_CPD(DAG)

# Probability of wet when no rain
# q = bn.inference.fit(DAG, variables=['wet'], evidence={'rain': 0})
# print(q.df)
# Probability of wet when no rain and no sprinkler
# bn.inference.fit(DAG, variables=['wet'], evidence={'rain': 0, 'sprinkler': 0})
# # Probability of rain when wet
# bn.inference.fit(DAG, variables=['rain'], evidence={'wet': 1})
# # Probability of rain and/or sprinkler when wet
# table = bn.inference.fit(DAG, variables=['rain', 'sprinkler'], evidence={'wet': 1})
# print(table.df['p'])

loneliness = TabularCPD(variable='loneliness', variable_card=2, values=[[0.15], [0.85]])
studies = TabularCPD(variable='studies', variable_card=2, values=[[0.64], [0.36]])

overeating = TabularCPD(variable='overeating', variable_card=2,
                 values=[[0.85, 0.35, 0.7, 0.15],
                         [0.15, 0.65, 0.3, 0.85]],
                 evidence=['studies', 'loneliness'],
                 evidence_card=[2, 2])

depression = TabularCPD(variable='depression', variable_card=2, values=[[0.8, 0.3], [0.2, 0.7]], evidence=['overeating'], evidence_card=[2])


DAG = bn.make_DAG(edges)
DAG = bn.make_DAG(DAG, CPD=[loneliness, studies, overeating, depression])

bn.print_CPD(DAG)