import pandas as pd
import os 

os.chdir('../')
puser = os.getcwd()

topic  = input('Tópico (directorio) : ')
topic  = '/' + topic
name   = input('Directorio para datos (<enter> .data) : ')
plocal = '/.data' if len(name)==0 else '/' + name

path = puser + topic + plocal
print(puser + topic)
print(path)

os.chdir(puser + topic)

p_d = pd.DataFrame([puser, topic, plocal], columns=['p'])
p_d.to_parquet('.__p', compression='gzip')

dummy = pd.read_parquet('.__p')
print('-'*20+'\n', dummy,'\n'+'-'*20)