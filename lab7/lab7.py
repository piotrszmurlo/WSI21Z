import bnlearn as bn
from pgmpy.factors.discrete import TabularCPD

edges = [('rain', 'spray'), ('rain', 'wet'), ('spray', 'wet')]

rain = TabularCPD(values=[[]])