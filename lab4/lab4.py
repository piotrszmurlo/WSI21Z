import pandas as pd
from pprint import pprint
df = pd.read_csv('whitewine.csv', delimiter=';')
df['count'] = 1
df_mean = df.groupby(['quality']).mean()
df_var = df.groupby(['quality']).var()
df_mean['count'] = 1
df_mean['count'] = df.groupby(['quality']).count()['count']
df_mean.rename(columns=lambda name: name + '(mean)', inplace=True)
df_var.rename(columns=lambda name: name + '(var)', inplace=True)
df_data = pd.concat([df_mean, df_var], axis=1)
all_count = df['count'].sum()
p_quality = {}
for i in range(11):
    try:
        p_quality[i] = df_mean.loc[i]['count(mean)']
    except KeyError:
        p_quality[i] = 0
df_data = df_data.drop(columns=['count(var)', 'count(mean)'])
print(p_quality)
p_attributes = {}

for col in df_data.columns:
    p_attributes[col] = 0
quality_dict = {}
pprint(p_attributes)
