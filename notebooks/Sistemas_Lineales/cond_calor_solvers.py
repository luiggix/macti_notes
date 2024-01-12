#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:58:12 2018
Updated on Fri Jan 12 08:32:59 PM UTC 2024
@author: luiggi
"""

import numpy as np
import macti.fdm.solvers as sol
import macti.visual as mvis

import time
from colorama import Fore, Style
import matplotlib.pyplot as plt

def buildMatrix(Nx, Ny, diagonal):
    N = Nx * Ny
    A = np.zeros((N,N))

# Primero llena los bloques tridiagonales
    for j in range(0,Ny):
        ofs = Nx * j
        A[ofs, ofs] = diagonal; 
        A[ofs, ofs + 1] = 1
        for i in range(1,Nx-1):
            A[ofs + i, ofs + i]     = diagonal
            A[ofs + i, ofs + i + 1] = 1
            A[ofs + i, ofs + i - 1] = 1
        A[ofs + Nx - 1, ofs + Nx - 2] = 1; 
        A[ofs + Nx - 1, ofs + Nx - 1] = diagonal 

# Despues llena las dos diagonales externas
    for k in range(0,N-Nx):
        A[k, Nx + k] = 1
        A[Nx + k, k] = 1

    return A

def RHS(Nx, Ny, boundaries):
    f = np.zeros((Ny,Nx)) # RHS
# Aplicacion de las condiciones de frontera Dirichlet
    f[Ny-1,:] -= boundaries['RIGHT'] 
    f[0   ,:] -= boundaries['LEFT']    
    f[:,Nx-1] -= boundaries['TOP'] 
    f[:,0   ] -= boundaries['BOT']  
    f.shape = f.size     # Cambiamos los arreglos a formato unidimensional

    return f

def solucion(B, T, L, R, metodo, N):
    Lx = 1.0
    Ly = 1.0
    Nx = N
    Ny = N

    boundaries = {'BOT':B, 'TOP':T, 'LEFT':L, 'RIGHT':R}

    A = buildMatrix(Nx, Ny,-4) # Matriz del sistema
    b = RHS(Nx, Ny, boundaries)
    
    tol = 1e-6
    max_iter = 200
    w = 1.09 # 1.09

    # Arreglo para la solución
    u = np.zeros((Ny+2, Nx+2))
    
    # Condiciones de frontera
    u[Ny+1,:   ] = boundaries['RIGHT']
    u[0   ,:   ] = boundaries['LEFT']
    u[:   ,Nx+1] = boundaries['TOP']
    u[:   ,0   ] = boundaries['BOT'] 
    x0 = u[1:-1,1:-1].flatten()
    
    t1 = time.perf_counter()
    
    if metodo == 'LU (linalg)':
        ut = np.linalg.solve(A,b)
        error = 0.0
        it = 1
    elif metodo == 'Jacobi':
        ut,error,it, ea = sol.jacobi(A, b, x0, tol, max_iter)
    elif metodo == 'Gauss-Seidel':
        ut,error,it, ea = sol.gauss_seidel(A, b, x0, tol, max_iter)
    elif metodo == 'SOR':
        ut,error,it, ea = sol.sor(A, b, x0, tol, max_iter,w)
    elif metodo == 'Steepest':
        ut,error, it, ea = sol.steepest(A, b, x0, tol, max_iter)
    elif metodo == 'CGM':
        ut,error, it, ea = sol.conjugateGradient(A, b, x0, tol, max_iter)

    t2 = time.perf_counter()
    te = t2 - t1
    print(Fore.BLUE + "Método: {}\n".format(metodo) +
          Fore.RESET + " CPU: {:5.4f} [s] ".format(te) +
          Fore.MAGENTA + " Sistema : {}x{} = {}\n".format(N*N, N*N, (N * N)**2) +
          Fore.RED   + " Error : {:5.4e} ".format(error) + 
          Fore.GREEN + " Iter : {} ".format(it) + Style.RESET_ALL)

    ut.shape = (Ny, Nx) # Regresamos el arreglo a formato bidimensional
    u[1:Ny+1,1:Nx+1] = ut
    
    titulo = 'Método: {} ][ Error = {:5.4f} | Iter = {} | CPU = {:5.4f} [s] ][ Sistema : {}]'.format(metodo, error, it, te, N * N)
#    plotSolution(u,Lx, Ly, Nx,Ny,titulo)

    x = np.linspace(0,Lx,Nx+2)
    y = np.linspace(0,Ly,Ny+2)
    xg, yg = np.meshgrid(x, y, indexing='ij', sparse=False)
    

    vis = mvis.Plotter(1,2, [dict(aspect = 'equal') for i in range(2)], dict(figsize=(10,4)))
    
    vis.set_canvas(1, Lx, Ly)
    vis.plot_mesh2D(1, xg, yg, nodeson=True)
    vis.plot_frame(2, xg, yg, ticks=False)
    vis.axes(1).set_title('Malla (incógnitas:{}x{})'.format(N,N))

    cax = vis.set_canvas(2, Lx, Ly)
    c = vis.contourf(2, xg, yg, u, levels=50, cmap='OrRd')
    vis.contour(2, xg, yg, u, levels=10, cmap='gray', linewidths=0.5)
    vis.fig.colorbar(c, cax=cax, ticks = [u.min(), u.max()], shrink=0.5, orientation='vertical')
    vis.plot_frame(2, xg, yg, ticks=False)
    vis.axes(2).set_title('Temperatura', fontsize=14)
    
    plt.show()
    
if __name__ == '__main__':

    R = 7   # Derecha 
    L = 34  # Izquierda
    T = 0   # Arriba
    B = 100 # Abajo
    
    N = 3 
    metodos = {'1':'Jacobi', '2':'Gauss-Seidel', '3':'SOR', '4':'Steepest', '5':'CGM'}
    print('Métodos disponibles')
    _ = [print('{}) {}'.format(k, v)) for k,v in metodos.items()]
    m = input('Método : ')
    solucion(B,T,L,R,metodos[m],N)
