import numpy as np
from Soluciones.Manager import Actividad

class Ejercicios:
    def __init__(self,Num,Let):
        self.Num=Num
        self.Let=Let
        
    def Solucion(self):
        cadena=str("./Soluciones/sol0"+str(self.Num)+self.Let+".npy")
        S=np.load(cadena)
        if self.Let == "a":
            Actividad("F",S).Ejercicio()
        if self.Let == "b":
            Actividad("G",S).Ejercicio()
        if self.Let == "c":
            Actividad("H",S).Ejercicio()

Ejercicio_1a=Ejercicios(1,"a").Solucion
Ejercicio_1b=Ejercicios(1,"b").Solucion
Ejercicio_2a=Ejercicios(2,"a").Solucion
Ejercicio_2b=Ejercicios(2,"b").Solucion
Ejercicio_3a=Ejercicios(3,"a").Solucion
Ejercicio_3b=Ejercicios(3,"b").Solucion
Ejercicio_4a=Ejercicios(4,"a").Solucion
Ejercicio_4b=Ejercicios(4,"b").Solucion
Ejercicio_4c=Ejercicios(4,"c").Solucion
Ejercicio_5a=Ejercicios(5,"a").Solucion
Ejercicio_5b=Ejercicios(5,"b").Solucion
Ejercicio_6a=Ejercicios(6,"a").Solucion
Ejercicio_6b=Ejercicios(6,"b").Solucion
Ejercicio_7a=Ejercicios(7,"a").Solucion
Ejercicio_7b=Ejercicios(7,"b").Solucion
