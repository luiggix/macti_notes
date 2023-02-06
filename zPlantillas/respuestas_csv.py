import numpy as np
import pandas as pd

file = pd.read_csv('ejemplo_res.csv')
                        
print(file)

for i in range(len(file)):
    if file.iloc[i]['Tipo'] == 'str':
        dummy = file.iloc[i]['Respuesta'].split(',')
        file.iloc[i]['Respuesta'] = dummy
    if file.iloc[i]['Tipo'] == 'float':
        file.iloc[i]['Respuesta'] = np.array([float(file.iloc[i]['Respuesta'])])
    if file.iloc[i]['Tipo'] == 'array':
        dummy = eval(file.iloc[i]['Respuesta'],{"__builtins__": {}}, {"np":np})
        file.iloc[i]['Respuesta']=dummy

print(file)
    
"""
# Numero de quiz
q = '1'
# Numeración de los ejercicios
ejercicios = list(file.N)

# Lista vacía para las respuestas
respuestas = list(file.Respuesta)

# Agregar las respuestas a cada ejercicio
respuestas.append(np.array([0.1450]))   # 1
respuestas.append(np.array([0.0196]))   # 2
respuestas.append(['C', 'c'])           # 3
respuestas.append(np.array([2.369007])) # 4A
respuestas.append(np.array([0.498646])) # 4a
respuestas.append(np.array([4.9e-09]))  # 4b
respuestas.append(np.array([1.1e-09]))  # 4c
respuestas.append(['3x^2-3xh+h^2', '3x^2-3hx+h^2'])     # 5

# Convertimos a un DataFrame
ans_df = pd.DataFrame([respuestas], columns=ejercicios)

# Escribimos las respuestas en un archivo tipo parquet, binario y comprimido
ans_df.to_parquet('.__ans_' + q, compression='gzip')

# Mostramos el contenido del DataFrame
print(ans_df)

# Se puede leer el contenido del archivo tipo parquet, binario y comprimido como sigue
ans_df2 = pd.read_parquet('.__ans_' + q) # Se lee en un DataFrame
print(ans_df2)
"""