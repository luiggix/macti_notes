# Herramientas para colorear texto y comparación de los resultados
from colorama import Fore
from nose.tools import assert_equal
import numpy as np

def verifica(x, y):
    """
    Permite comparar el contenido de x con el de y. Si se encuentra una diferencia entonces emite una alerta.
    """
    try:
        assert_equal(x, y)
    except AssertionError as info:
        print(Fore.RESET + 80*'-')
        print(Fore.RED + 'Cuidado: Ocurrió un error en tus cálculos: \n {}'.format(info))
        print(Fore.RESET + 80*'-')
    else:
        print(Fore.GREEN + '¡Tu resultado es correcto!')