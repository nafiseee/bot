import pandas as pd
df = pd.read_excel('df.xlsx',names = ['works','spares','time','type','sale','group'])
df_spares = df[['spares','type','group']]
