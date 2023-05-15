# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

np.set_printoptions(suppress=True)

def ejemplo(x):
    
    """
    Función para generar los valores de ejemplo
    
    Parameters
    ----------
    x: array
    Valores de x para generar el resultado de la función
    
    Returns
    -------
    f: array
    Valores generados para la función
    """
    
    f = 4 + 3*np.cos((2*np.pi/25)*x) + 1.5*np.sin((2*np.pi/60)*x)
    
    return f

def spline_lineal(x, y, faltantes = None):
    
    """
    Realiza la interpolación por splines lineales de un conjunto 
    de datos, además de la aproximación en caso de tener valores
    desconocidos.
    
    Parameters
    ----------
    x: array
    Valores de x
    y: array
    Valores de y
    faltantes: array, opcional
    Arreglo con los valores que se buscan aproximar
    
    Returns
    -------
    X_int: array
    Valores de x interpolados para todo el rango
    S_lin: array
    Valores del spline lineal para los valores de x interpolados
    f_int: array, opcional
    Valores aproximados de los datos ingresados
    """
    
    # INTERPOLACIÓN SPLINE LINEAL
    # Generamos un arreglo de tamaño k = N - 1 donde almacenaremos los valores de las pendientes
    k = np.size(x) - 1
    m = np.zeros(k)
    for i in range(k):
        m[i] = (y[i + 1] - y[i]) / (x[i + 1] - x[i]) 
        # Ecuación de la pendiente m_i
   
    # APROXIMACIÓN DE VALORES DESCONOCIDOS
    # Se verifica que se hayan pasado valores a aproximar
    # Si no, se ignora esta parte
    if faltantes is not None:
        # Se genera un arreglo del tamaño de los datos a aproximar
        f_int = np.zeros(np.size(faltantes))
        for idx, f in enumerate(faltantes):
            for i in range(k):
                if f >= x[i] and f <= x[i + 1]:
                    f_int[idx] = y[i] + m[i] * (f - x[i])

    # GENERACIÓN DE POLINOMIOS DEL SPLINE
    # Splines interpolantes para graficar
    X_int = np.linspace(x[0], x[-1], 1000)
    S_lin = np.piecewise(X_int, [(X_int >= x[i]) & (X_int <= x[i + 1]) for i in range(k)],
                                [lambda X_int, j = i: y[j] + m[j]*(X_int - x[j]) for i in range(k)])
                                
    if faltantes is None:
        return X_int, S_lin
    else:
        return X_int, S_lin, f_int

def spline_quad(x, y, faltantes = None):
    
    """
    Realiza la interpolación por splines cuadráticos de un conjunto 
    de datos, además de la aproximación en caso de tener valores
    desconocidos.
    
    Parameters
    ----------
    x: array
    Valores de x
    y: array
    Valores de y
    faltantes: array, opcional
    Arreglo con los valores que se buscan aproximar
    
    Returns
    -------
    X_int: array
    Valores de x interpolados para todo el rango
    S_lin: array
    Valores del spline cuadrático para los valores de x interpolados
    f_int: array, opcional
    Valores aproximados de los datos ingresados
    """
    
    # INTERPOLACIÓN SPLINE CUADRÁTICO
    # Generamos la matriz de tamaño N = 3*k donde almacenaremos los coeficientes del sistema de ecuaciones
    k = np.size(x) - 1
    N = 3*k
    A = np.zeros((N, N))
    
    # Asignamos los coeficientes de las ecuaciones para la condición de igualdad en puntos internos
    for i in range(k):
        A[2*(i + 1) - 2, 3*i] = x[i]**2
        A[2*(i + 1) - 1, 3*i] = x[i + 1]**2
        A[2*(i + 1) - 2, 3*i + 1] = x[i]
        A[2*(i + 1) - 2, 3*i + 2] = 1
        A[2*(i + 1) - 1, 3*i + 1] = x[i + 1]
        A[2*(i + 1) - 1, 3*i + 2] = 1
        
    # Asiganmos los coeficientes de las ecuaciones para la condición de continuidad de las derivadas en puntos internos
    for i in range(k - 1):
        A[2*k + i, 3*i + 1] = 1
        A[2*k + i, 3*i + 4] = -1 
        A[2*k + i, 3*i] = 2*x[i + 1]
        A[2*k + i, 3*i + 3] = -2*x[i + 1]
        A[3*k - 1, 0] = 1

    # Lado derecho del sistema
    b = np.zeros(N)
    
    # Asignamos los valores de f(x)
    b[0] = y[0]
    for i in range(1, 2*k - 1, 2):
        b[i] = y[(i + 1)//2]
        b[i + 1] = y[(i + 1)//2]
    b[2*k - 1] = y[k]
    
    # Resolvemos el sistema y almacenamos en otro arreglo
    sol = np.linalg.solve(A, b)
    
    # APROXIMACIÓN DE VALORES DESCONOCIDOS
    # Se verifica que se hayan pasado valores a aproximar
    # Si no, se ignora esta parte
    if faltantes is not None:
        # Se genera un arreglo del tamaño de los datos a aproximar
        f_int = np.zeros(np.size(faltantes))
        for idx, f in enumerate(faltantes):
            for i in range(k):
                if f >= x[i] and f <= x[i + 1]:
                    f_int[idx] = sol[3*i]*f**2 + sol[3*i + 1]*f + sol[3*i + 2]
    
    # Splines interpolantes para graficar
    X_int = np.linspace(x[0], x[-1], 1000)
    S_quad = np.piecewise(X_int, [(X_int >= x[i]) & (X_int <= x[i + 1]) for i in range(k)], 
                                [lambda X_int, j = i: sol[3*j]*X_int**2 + sol[3*j + 1]*X_int + sol[3*j + 2] for i in range(k)])
  
    if faltantes is None:
        return X_int, S_quad
    else:
        return X_int, S_quad, f_int
