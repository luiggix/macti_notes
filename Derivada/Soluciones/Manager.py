from IPython.display import display, Latex
from colorama import Fore
import numpy as np

class Actividad:
    def __init__(self,Funcion,S):
        self.Funcion=Funcion
        self.S=S
    
    def Respuesta(self):
        display(Latex(f'${self.Funcion}\'(x)$'))
        R1 = input("=")
        return R1
    
    def Ejercicio(self):
        R1 = self.Respuesta()
        R1 = R1.replace(" ","")
        R1 = R1.replace("*","")
        aux=False

        for i in self.S:            
            if R1 == i:
                aux=True
        if aux:
            print(Fore.RESET + 80*'-')
            print(Fore.GREEN + '¡Tu resultado es correcto!')
            print(Fore.RESET + 80*'-')
        else:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + '¡Tu respuesta es incorrecta!, verifica las reglas de la derivacion y vuelve a intentar')
            print(Fore.RESET + 80*'-')
            

            