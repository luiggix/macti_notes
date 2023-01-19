# Herramientas para colorear texto y comparación de los resultados
from colorama import Fore
from nose.tools import assert_equal
import numpy as np
import pkg_resources
from IPython.display import display, Latex


class Evalua():
    def __init__(self, topic, local=False):
        self.topic = topic
        self.local = local 

    def verifica(self, x, i):
        """
        Permite comparar el contenido de x con el de y. Si se encuentra una diferencia entonces emite una alerta.
        """

        if self.local:
            stream = self.topic + '/sol{:02d}.npy'.format(i)
        else:
            filename = 'data/' + self.topic + '/sol{:02d}.npy'.format(i)
            stream = pkg_resources.resource_stream('macti', filename)
        y = np.load(stream)
    
        try:
            assert_equal(list(x.flatten()), list(y.flatten()))
        except AssertionError as info:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Cuidado: Ocurrió un error en tus cálculos: \n {}'.format(info))
            print(Fore.RESET + 80*'-')
        else:
            print(Fore.GREEN + '¡Tu resultado es correcto!')

            
class EvaluaEjercicio():
    def __init__(self, topic, local=False):
        self.topic = topic
        self.local = local 

    def ejercicio(self, f, i):
        """
        Permite comparar el contenido de x con el de y. Si se encuentra una diferencia entonces emite una alerta.
        """

        if self.local:
            stream = self.topic + './sol{:02d}.npy'.format(i)
        else:
            filename = 'data/' + self.topic + '/sol{:02d}.npy'.format(i)
            stream = pkg_resources.resource_stream('macti', filename)
        y = np.load(stream)

        display(Latex(f'$f(x) = {f}$,\n $f\'(x) = ¿?$ '))
        respuesta = input("=")
        respuesta = respuesta.replace(" ","")
        correcta = respuesta in y
        if correcta:
            print(Fore.GREEN + '¡Tu resultado es correcto!')
        else:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + '¡Tu respuesta es incorrecta!, verifica las reglas de la derivacion y vuelve a intentar')
            print(Fore.RESET + 80*'-')            
            
#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':
    x = np.linspace(0,1500,10)
    PA = 0.10 * x + 200
    PB = 0.35 * x + 20

    print('\n Global data')
    d = Evalua('SistemasLineales')     
    d.verifica(PA, 1)
    d.verifica(PB, 2)
    
    print('Test')
    np.save('sol01.npy', np.array(['4x^3','b',343.34]))
    e = EvaluaEjercicio('',local=True)
    e.ejercicio(1)
    
"""
    print('\n Local data')
    f = Evalua('./data/SistemasLineales/', local=True)
    f.verifica(PA, 1)
    f.verifica(PB, 2)
"""

