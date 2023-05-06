import os, shutil, pkg_resources

paths = ['./Tema1/', 
         './utils/data/',
         './utils/src/',
         './utils/fig/']

for p in paths:
    if not os.path.exists(p):
        print('Creando el directorio : {}'.format(p))
        os.makedirs(p , exist_ok=True)
    else:
        print('El directorio : {} ya existe'.format(p))

for i in range(1,4):
    filename = '/data/Plantillas/plantilla0' + str(i) + '.ipynb'
    stream = pkg_resources.resource_stream('macti', filename)
    print('Copiando {} al directorio {}'.format(stream.name.split(sep='/')[-1], paths[0]))
    shutil.copy2(stream.name, paths[0])
