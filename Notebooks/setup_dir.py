import pandas as pd
import os 

puser = os.getcwd()

topics = []
with os.scandir(puser) as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_dir() and entry.name != 'data':
            topics.append(entry.name)

p_d = pd.DataFrame([puser], columns=['p'])
p_d.to_parquet('.__p', compression='gzip')

dummy = pd.read_parquet('.__p')

print('-'*5 + 'Ruta del repositorio local'+ '-'*5)
print(dummy,'\n'+'-'*36 + '\n')

print('Directorios a ser creados en "data/": ') 
[print('* ', i) for i in topics]
print()

for i in topics:
    directorio = puser +'/data/'+ i
    try:
        os.makedirs(directorio, mode=0o755, exist_ok=False)
        print(directorio)
    except OSError as error:
        print("El directorio {} ya existe".format(directorio))