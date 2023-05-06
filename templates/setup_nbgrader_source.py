import os, shutil, pkg_resources
import pandas as pd

# Nombre del curso
c_name = input('\n Nombre del curso : ')

# Lista de temas y tareas por cada tema
topic_list = pd.read_csv('topics_nbgrader.csv')

print('\n -- Inicializando el directorio para NBGRADER \n')

c_name_nbg = c_name + '_NBG'

nbgrader_qs = 'nbgrader quickstart ' + c_name_nbg

print(nbgrader_qs)

# Inicializamos el curso para NBGRADER
os.system(nbgrader_qs)

print('\n -- Copiando información al directorio {}'.format(c_name_nbg))

# Copiamos las notebooks de ejercicios al directorio
# correspondiente para NBGRADER
for topic in topic_list:
    p = c_name_nbg + '/source/' + topic
    if not os.path.exists(p):
        print('\n ---> Creando el directorio : {}'.format(p))
        os.makedirs(p , exist_ok=True)
    else:
        print('El directorio : {} ya existe'.format(p))
        
    for a in topic_list[topic]:
        if not isinstance(a, float):
            src = c_name + '/' + topic + '/' + a + '.ipynb'
            dst = c_name_nbg + '/' + 'source/' + topic        
            print('Copiando {} al directorio {}'.format(src, dst))
            shutil.copy2(src, dst)

# Agregamos la ruta del curso para NBGRADER en el archivo de 
# configuración nbgrader_config.py

print('\n -- Modificando : c.CourseDirectory.root')

with open(c_name_nbg + "/nbgrader_config.py","r") as f:
    all_file = f.readlines()
    
old_text = "# c.CourseDirectory.root = ''"
new_text = 'c.CourseDirectory.root = "' + os.getcwd() + '/' + c_name_nbg + '" \n' 

with open("nbgrader_config.py","w") as f:
    for line in all_file:        
        if old_text in line:
            f.writelines(new_text)
        else:
            f.writelines(line)
            
print('\n -- Fin del proceso \n')
