import pandas as pd

# df = pd.read_csv('ids.csv')
#
# # df = df[df['id'] == 1234]
#
# df.at[0, 'fdr'] = 'teste'
# print(df)
#
# df.to_csv('ids.csv', index=False)
#
# # print(df[df['id'] == 1234].index.values[0])

df = pd.read_csv("ids.csv",
                 delimiter=';',
                 skipinitialspace=True)

print(df[df['oi'] == 'Vikram']['tudo'].values[0])
print(df.at[0, 'tudo'])

# df.at[0, 'uuid'] = 'oi'
#
# df.to_csv('data.csv', index=False, sep=';')
