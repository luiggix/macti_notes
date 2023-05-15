#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 12:05:57 2020

@author: luiggi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
from fdm_1D import Laplaciano1D_NS
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
N = 99                      # Número de incógnitas
dx = L / (N+1)              # Distancia entre nodos
z = np.linspace(0, L, N+2)  # Coordenada z de la profundidad
dt = 3600*24*365 # Paso de tiempo (seconds per year)
NT = 250000      # Número total de pasos de tiempo

print('\nDatos para la solución numérica usando FD')
print(' dx = {:10.1f} [m] \n L  = {:10.1f} [m] \n N  = {:8d}'.format(dx, L, N))
print(' dt = {:10.1f} [s] \n NT = {:8d}'.format(dt, NT))
#
# Aceleración para el método implícito
#
SP = 1000
dt *= SP
NT /= SP
print('\nUsamos un factor de aceleración debido al método implícito: ')
print(' SP = {:13d} (factor)\n dt = {:15.1f} [s] \n NT = {:13d} (pasos totales)'.format(SP, dt, int(NT)))
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
# Condición inicial: Profundidades
z_dat = [0, 100, 200, 400, 710, 803, 1100, 1200, 1400, 1500, 1600, 1700, 1800, 2000, 2500, 3000, 3500, 4000]
# Condición inicial: Temperaturas
T_dat = [15, 113, 145, 178, 155, 201, 215, 282, 223, 226, 252, 284, 310, 350, 450, 550, 650, 750]
# Interpolación a los lugares de la simulación
tck_1 = interpolate.splrep(z_dat, T_dat, s = 0)
T_ini = interpolate.splev(z, tck_1, der = 0)
#
# Temperaturas actuales
z_dat_now = [0, 96, 192, 389, 596, 798, 1000, 1197, 1408, 1495, 1586, 1649, 1702, 1750, 1803, 1851, 1904, 1942, 1967, 2000, 2500, 3000, 3500, 4000]
T_dat_now = [15, 69, 74, 95, 121, 159, 168, 192, 213, 213, 236, 251, 267, 272, 284, 288, 298, 293, 310, 325, 440, 550, 650, 750]
# Interpolación a los lugares de la simulación
tck_2 = interpolate.splrep(z_dat_now, T_dat_now, s = 0)
T_final = interpolate.splev(z, tck_2, der = 0)
#
# SOLUCIÓN USANDO DIFERENCIAS FINITAS
#
# Definicion del sistema lineal de N x N
#
dt_dx2 = dt / dx**2
gamma = Dth * dt_dx2
A = Laplaciano1D_NS(N, gamma) # Matriz del sistema

print('\nGamma shape = {}, A shape = {}'.format(gamma.shape, A.shape))
#
# Ciclo de solución temporal
#
T_new = T_ini.copy()
T_now = np.zeros(N+2)
for i in range(0, int(NT)+1):
    print(i)
    T_new[ 1] += gamma[0] * T_ini[0]
    T_new[-2] += gamma[-1] * T_ini[-1]    
    T_new[1:-1] = np.linalg.solve(A,T_new[1:-1])
    if (i == 7):
        T_now = T_new.copy() # Temperatura actual
#
# GRAFICACIÓN
#
ax1 = plt.subplot(121)
plt.plot([T_ini[0], T_ini[-1]], [z[0], z[-1]], '--', lw=0.75, c='k' )
plt.scatter(T_dat, z_dat, s=20, alpha=0.5)
plt.plot(T_ini, z, '.-', lw = 1.5, label='Cond. inicial')

plt.scatter(T_dat_now, z_dat_now, s=20, alpha=0.5, label='Datos de pozo')
plt.plot(T_now, z, label='Simulación Temp. actual')
plt.plot(T_final, z, label='Temp. actual interpolada')

plt.plot(T_new,z, label='Simulación Temp. final')
plt.ylim(4100,-100)
plt.xlim(-20,800)
plt.title('Solución Numérica')
plt.xlabel('$T$ [$^o$C]')
plt.ylabel('Depth [m]')
plt.grid()
plt.legend()

ax2 = plt.subplot(122, sharey=ax1)
plt.plot(Dth, z, 'k.--', lw=0.75)
plt.xlabel('$D_{th}$ [m$^2$/s]')
plt.xlim(0.65e-6,1.05e-6)
plt.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
plt.title('Coeficiente $D_{th}$')
plt.grid()

plt.subplots_adjust(hspace=1.0)

plt.show()
