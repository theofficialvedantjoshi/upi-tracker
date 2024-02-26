import pandas as pd

df = pd.DataFrame(columns=['bank','money_prefix','id_prefix'])
b = ['HDFC','AXIS']
m = ['Rs.','INR ']
i = ['VPA','Info-']
df['bank'] = b
df['money_prefix'] = m
df['id_prefix'] = i
df.to_csv('banks.csv',index=False)