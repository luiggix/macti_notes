#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 12:05:57 2020.

@author: luiggi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fdm_1D import harmonicMean, arithmeticMean, Laplaciano1D
#
# Datos físicos del problema
#
Ttop = 15   # Temperatura en la superficie
Tbot = 750  # Temperatura a 4000 m
L = 4000.0  # Profundidad máxima
data = pd.read_csv('phys_dat.csv') # Lectura de datos: k, cp, rho
Dth_data = data['k'] / (data['rho']*data['cp']) # Cálculo del coeficiente Dth

print('\nDatos del problema \n{}'.format(data))
print('\n Dth : \n{}'.format(Dth_data))
#input('Presiona <enter>')
#
# Datos para la solución numérica por diferencias finitas
#
N = 79                      # Número de incógnitas
dx = L / (N+1)              # Distancia entre nodos
z = np.linspace(0, L, N+2)  # Coordenada z de la profundidad

print('\nDatos para la solución numérica usando FD')
print(' dx = {:10.1f} [m] \n L  = {:10.1f} [m] \n N  = {:8d}'.format(dx, L, N))
print('\nz shape = {} \n{}'.format(z.shape,z))
#input('Presiona <enter>')
#
# Vector con el valor del coeficiente dependiendo de la profundidad 
#
Dth = np.zeros((N+2))
for k in range(0, N+2):
    if (z[k] <= 50.0):
        Dth[k] = Dth_data[0]
    elif ((z[k] > 50.0) and (z[k] <= 250.0)):
        Dth[k] = Dth_data[1]
    elif ((z[k] > 250.0) and (z[k] <= 400.0)):
        Dth[k] = Dth_data[2]
    elif ((z[k] > 400.0) and (z[k] <= 600.0)):
        Dth[k] = Dth_data[3]
    elif ((z[k] > 600.0) and (z[k] <= 800.0)):
        Dth[k] = Dth_data[4]
    elif ((z[k] > 800.0) and (z[k] <= 1000.0)):
        Dth[k] = Dth_data[5]
    elif ((z[k] > 1000.0) and (z[k] <= 1500.0)):
        Dth[k] = Dth_data[6]
    elif ((z[k] > 1500.0) and (z[k] <= 1900.0)):
        Dth[k] = Dth_data[7]
    else:
        Dth[k] = Dth_data[8]
        
print('\nCoeficiente en los puntos de la simulación: \n D_th shape = {} \n{}'.format(Dth.shape, Dth))
#
# SOLUCIÓN USANDO DIFERENCIAS FINITAS
#
# Definición del sistema lineal de N x N
#
gamma = Dth / dx**2
f = np.zeros(N)            # RHS
A = Laplaciano1D(N, gamma) # Matriz del sistema
#A = Laplaciano1D(N, gamma, harmonicMean) # Matriz del sistema
#A = Laplaciano1D(N, gamma, arithmeticMean) # Matriz del sistema

print('\nGamma shape = {} \nf shape = {}, A shape = {}'.format(gamma.shape, f.shape, A.shape))
#
# Arreglo para la solución
#
T = np.zeros(N+2)
#
# Aplicación de las condiciones de frontera tipo Dirichlet.
#
T[0] = Ttop
T[N+1] = Tbot 
f[0] -= Ttop * gamma[0]
f[N-1] -= Tbot * gamma[N+1]
#
# Solución del sistema lineal
#
T[1:N+1] = np.linalg.solve(A,f)

print('\nSolución T shape = {} \n{}'.format(T.shape, T))
#
# GRAFICACIÓN
#
ax1 = plt.subplot(121)
plt.plot(T,z, 'r-', lw=2.0, label='FDM', zorder=10)
plt.plot([T[0], T[-1]], [z[0], z[-1]], '--', lw=0.75, c='k' )
plt.ylim(4100,-100)
plt.xlim(-10,800)
plt.title('Solución Numérica')
plt.xlabel('$T$ [$^o$C]')
plt.ylabel('Depth [m]')
plt.minorticks_on()
plt.legend()
plt.grid()

ax2 = plt.subplot(122, sharey=ax1)
plt.plot(Dth, z, '.--', lw=0.75, c='k')
plt.xlabel('$D_{th}$ [m$^2$/s]')
plt.xlim(0.65e-6,1.05e-6)
plt.minorticks_on()
plt.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
plt.title('Coeficiente $D_{th}$')
plt.grid()

plt.subplots_adjust(hspace=1.0)

plt.show()