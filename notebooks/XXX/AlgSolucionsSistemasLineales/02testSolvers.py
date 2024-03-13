#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:58:12 2018

@author: luiggi
"""

import numpy as np
import StationarySolvers as sol
import KrylovSolvers as kry
import time

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.titlesize'] = 24
mpl.rcParams['axes.titlesize'] = 20
mpl.rcParams['axes.titlecolor'] = 'blue'
mpl.rcParams['axes.labelsize'] = 20
mpl.rcParams['legend.fontsize'] = 12
mpl.rcParams['lines.linewidth'] = 2.0
mpl.rcParams['scatter.edgecolors'] = 'black'
mpl.rcParams['legend.fancybox'] = True
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.edgecolor'] = 'black'

boundA = 100
boundB = -25
boundC = 34
boundD = 7
    
def plotSolution(ut,Nx,Ny,title,xlabel):
    # contador es un un atributo estatico que cuenta las llamadas a esta funcion
    plotSolution.contador = getattr(plotSolution, 'contador', 0) + 1

    u = np.zeros((Ny+2, Nx+2))

    u[Ny+1,:   ] = boundB 
    u[:   ,0   ] = boundC 
    u[:   ,Nx+1] = boundD
    u[0   ,:   ] = boundA

    ut.shape = (Ny, Nx) # Regresamos el arreglo a formato bidimensional
    u[1:Ny+1,1:Nx+1] = ut

    x = np.linspace(0,1,Nx+2)
    y = np.linspace(0,1,Ny+2)
    xg, yg = np.meshgrid(x,y)

    plt.subplot(2,3,plotSolution.contador)    
    plt.contourf(xg, yg, u, 10, alpha=.75, cmap=plt.cm.inferno)
    C = plt.contour(xg, yg, u, 10, colors='black')
    plt.clabel(C, inline=1, fontsize=7.5)
    plt.title(title)
    plt.xlabel(xlabel)    
    
def generateSystem(Nx, Ny, diagonal):
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

    f = np.zeros((Ny,Nx)) # RHS
# Aplicacion de las condiciones de frontera Dirichlet
    f[0   ,:] -= boundA # Bottom wall    
    f[Ny-1,:] -= boundB # Upper wall
    f[:,0   ] -= boundC # Left wall 
    f[:,Nx-1] -= boundD # Right wall
    f.shape = f.size     # Cambiamos los arreglos a formato unidimensional

    return A, f

Nx = 11
Ny = 11
A, b = generateSystem(Nx, Ny,-4) # Matriz del sistema

tol = 1e-6
max_iter = 200
w = 1.5

plt.figure(figsize=(20,10))

t1 = time.perf_counter()
ut = np.linalg.solve(A,b)
t2 = time.perf_counter()
te = t2 - t1
print("\n linalg.solve() \n Elapsed time to solve Ax = b : %g" % te)
plotSolution(ut,Nx,Ny,'linalg.solve({:>5.4e})'.format(0),'Tiempo[s] : {:5.4f}'.format(te))

t1 = time.perf_counter()
ut,error,it, eaJ = sol.jacobi(A,b,tol,max_iter)
t2 = time.perf_counter()
te = t2 - t1
print("\n Jacobi \n Elapsed time to solve Ax = b : %g" % te)
print(" error : %g, iteraciones : %d" % (error, it))
plotSolution(ut,Nx,Ny,'Jacobi ({:>5.4e} - {})'.format(error, it),'Tiempo[s] : {:5.4f}'.format(te))

t1 = time.perf_counter()
ut,error,it, eaGS = sol.gauss_seidel(A,b,tol,max_iter)
t2 = time.perf_counter()
te = t2 - t1
print("\n Gauss Seidel \n Elapsed time to solve Ax = b : %g" % te)
print(" error : %g, iteraciones : %d" % (error, it))
plotSolution(ut,Nx,Ny,'Gauss Seidel ({:>5.4e} - {})'.format(error, it),'Tiempo[s] : {:5.4f}'.format(te))


t1 = time.perf_counter()
ut,error,it, eaSOR = sol.sor(A,b,tol,max_iter,w)
t2 = time.perf_counter()
te = t2 - t1
print("\n SOR \n Elapsed time to solve Ax = b : %g" % te)
print(" error : %g, iteraciones : %d" % (error, it))
plotSolution(ut,Nx,Ny,'SOR ({:>5.4e} - {})'.format(error, it),'Tiempo[s] : {:5.4f}'.format(te))


b = np.matrix(b)
x0 = b.copy()

t1 = time.perf_counter()
ut,residual,it, raSD = kry.steepestDescent(A,b.T,x0.T,tol,max_iter)
t2 = time.perf_counter()
te = t2 - t1
print("\n Steepest Descent \n Elapsed time to solve Ax = b : %g" % te)
print(" residual : %g, iteraciones : %d" % (residual, it))
plotSolution(ut,Nx,Ny,'SD ({:>5.5e} - {})'.format(residual, it),'Tiempo : {:5.4f}'.format(te))

t1 = time.perf_counter()
ut,residual,it, raCG = kry.conjugateGradient(A,b.T,x0.T,tol,max_iter)
t2 = time.perf_counter()
te = t2 - t1
print("\n Conjugate Gradient \n Elapsed time to solve Ax = b : %g" % te)
print(" residual : %g, iteraciones : %d" % (residual, it))
plotSolution(ut,Nx,Ny,'CG ({:>8.5e} - {})'.format(residual, it),'Tiempo : {:5.4f}'.format(te))

plt.subplots_adjust(bottom=0.1, right=0.9, top=0.9, wspace=0.5, hspace=0.5)
plt.savefig('LaplaceComparaKrylov_{}.pdf'.format(Nx))
plt.show()

plt.figure()
plt.plot(eaJ, label='Jacobi')
plt.plot(eaGS, label='G-S')
plt.plot(eaSOR, label='SOR')
plt.plot(raSD, label='SD')
plt.plot(raCG, label='CGM')
plt.semilogy()
plt.legend(bbox_to_anchor=(1.26, 1.0), loc='upper right', ncol=1)
plt.title('Malla: {} X {}'.format(Nx,Ny))
plt.xlabel('Iteraciones')
plt.ylabel('Error')
plt.grid()
plt.savefig('LaplaceComparaErrorKrylov_{}.pdf'.format(Nx))
plt.show()