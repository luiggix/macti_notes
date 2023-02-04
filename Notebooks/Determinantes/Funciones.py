import numpy as np
from IPython.display import display, Latex
import matplotlib.pyplot as plt
import seaborn as snb; snb.set();

def MatrizCuadrada(filas):
    matriz1 = np.zeros((filas,filas))
    print ('Ingrese las entradas de la matriz: \n')
    for i in range(filas):
        for j in range(filas):
            matriz1[i][j] = float(input('Ingrese el valor del elemento ({},{}): '.format(i+1,j+1)))
    return matriz1

def Mostrar_Matriz(a):
    aux=""
    for i in range(len(a)):
        for j in range(len(a[i])):
            if j in range(len(a[i])-1):
                aux = aux + r"{} & ".format(a[i][j]) 
            else:
                aux = aux + r"{} ".format(a[i][j]) 
        aux =  aux + r'\\'
    aux = r'$$\left(\begin{array}{ccc}' + aux +  r'\end{array}\right)$$'
    display(Latex(aux))
    
def crear_matriz():
    filas = int(input("Ingrese el numero de filas, recuerde que se trata de una matriz Cuadrada: "))  
    print("La matriz es de la forma:")
    aux=[]
    aux2=[]
    for i in range(filas):
        for j in range(filas):
            aux2.append("a_" + str("{") + "{}{}".format(i+1,j+1) + str("}"))
        aux.append(aux2)
        aux2=[]
    Mostrar_Matriz(aux)
    m = MatrizCuadrada(filas)
    print("\nLa matriz ingresada es\n")
    Mostrar_Matriz(m)
    return m


def puntos_poligono(n):
    '''
        Función para para ingresar los vertices de un poligono.
        - n: Numero entero, numero de vertices del poligono
        
        Devuelve arreglo con los puntos ingresados
    '''
    puntos=[]

    for i in range(n):
        aux = []
        aux.append(float(input(f"Ingresa valor de X del punto {i+1}: ")))
        aux.append(float(input(f"Ingresa valor de Y del punto {i+1}: ")))
        if aux in puntos:
            print("\nError ya has ingresado este punto, vuelve a intentarlo")
            break
        else:
            puntos.append(aux)
    return puntos

def graficar_poligono(puntos):
    '''
        Funcion que nos permite graficar poligonos
        - Puntos: Arreglo de arreglos de dos elementos que representan los puntos de un poligono
    '''
    for i in range(len(puntos)):
        if i in range(len(puntos)-1):
            plt.plot((puntos[i][0],puntos[i+1][0]),(puntos[i][1],puntos[i+1][1]),color="blue")
            plt.scatter(puntos[i][0],puntos[i][1],color="red",zorder=5)
            plt.annotate(f"{i+1}", (puntos[i][0]+0.1,puntos[i][1]))
        else:
            plt.plot((puntos[0][0],puntos[-1][0]),(puntos[0][1],puntos[-1][1]),color="blue")
            plt.scatter(puntos[-1][0],puntos[-1][1],color="red",zorder=5)
            plt.annotate(f"{i+1}", (puntos[-1][0]+0.1,puntos[-1][1]))
    plt.show()

    
def calcular_area(puntos):
    area = 0
    for i in range(len(puntos)):
        if i in range(len(puntos)-1):
            area = area + np.linalg.det((puntos[i],puntos[i+1]))
        else:
            area = area + np.linalg.det((puntos[-1],puntos[0]))
    area = abs((1/2)*area)
    return area


def DiagonalMatriz():
    
    filas = int(input("Ingrese el numero de filas, recuerde que se trata de una matriz Cuadrada: "))  
    
    matriz1 = np.zeros((filas,filas))
    print ('Ingrese las entradas de la matriz: \n')
    for i in range(len(matriz1)):
        for j in range(i,len(matriz1)):
            matriz1[i][j] = float(input('Ingrese el valor del elemento ({},{}): '.format(i+1,j+1)))
    Mostrar_Matriz(matriz1)
    
    return matriz1
