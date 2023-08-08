import sympy
import numpy as np
import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt
import macti.visual as mvis

def algoritmo_1(y, n, r):
    return round(1.0 / n - 5 * y[n-1], r)
                 
def calc_error(sol_exa, sol_num):
    error = []
    for e, n in zip(sol_exa, sol_num):
        error.append(np.abs(e - n))
    return error
                 
def calc_exac_num(N,r):
    iexa = []
    x = sympy.symbols('x')

    for n in range(N):
        f = x**n / (x+5)
        g = sympy.integrate(f, (x, 0.0, 1.0))
        iexa.append(g)
        
    inum = [round(np.log(6) - np.log(5), r)]
    for n in range(1,N):
        inum.append(algoritmo_1(inum, n, r))
        
    ierr = calc_error(iexa, inum)

    vis = mvis.Plotter(1,2,[dict(title = "Valor de la integral", xlabel='$n$'), 
                            dict(title="Error", xlabel='$n$')], dict(figsize=(10,4)))
    xn = [i for i in range(N)]
    vis.plot(1, xn, iexa, marker='o', label='Exacta')
    vis.plot(1, xn, inum, marker='s', label='Numérica')
    vis.plot(2, xn, ierr, marker='o', color='C2',label='Error absoluto')
    vis.axes(2).set_ylim(-0.1, 0.21)
    vis.figtitle('N={}, Redondeo: {}'.format(N,r))
    vis.grid()
    vis.legend()
    vis.show()
        
w = widgets.interact(calc_exac_num,         
             N = widgets.IntSlider(min=5, max=10, step=1, value=5),
             r = widgets.IntSlider(min=3, max=10, step=1, value=3))

display(w)