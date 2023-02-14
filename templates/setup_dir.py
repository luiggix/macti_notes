import os 

puser = os.getcwd()

directorios = ['student', 'teacher', 'utils/data', 'utils/fig', 'utils/src']

for d in directorios:
    os.makedirs(d, exist_ok=True)
