#-----------------------------------------------------------
# Ruta biblioteca macti
#
#import os, sys
#sys.path.insert(0, os.path.abspath('../../'))
#print(sys.path)
#-----------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import macti.visual as mvis

def solveFlujo(Nt, ht, rango, w, dTray=True):
    # Campo de velocidad
    u = lambda x,r: 0.298*(0.5**2 - r**2)/(4*3.0*1.05e-3)  # Flujo de Poiseuille
    v = lambda x,r: np.sin(x*w)                      # La velocidad en dirección y es cero.

    # Número de partículas
    Np = 7

    # Coordenadas iniciales de las partículas
    px = np.zeros(Np)
    py = np.linspace(rango[0], rango[1], Np) # Equiespaciadas en dirección y

    t = np.zeros((Np, Nt,2))

    for j in range(0, Np):
        t[j, 0, :] = (px[j], py[j]) 

    for j in range(0,Np):
        (xi, yi) = t[j, 0, :] # Posición inicial de la trayectoria j
        for n in range(1, Nt): # Ciclo para calcular las posiciones
            ### BEGIN SOLUTION
            xf = xi + ht * u(xi,yi)
            yf = yi + ht * v(xi,yi)
            t[j, n, :] = (xf, yf)   # Agregamos (xf, yf) a la lista de posiciones
            (xi, yi) = (xf, yf)     # Actualizamos (xi, yi)
            ### END SOLUTION
    
    vis = mvis.Plotter(1,1, [dict(aspect = 'equal')])

    if dTray:
        for j in range(Np):
            vis.scatter(1, [t[j,0,0], t[j,-1,0]], [t[j,0,1], t[j,-1,1]],  dict(ec='k', s=50, alpha=0.75, zorder=5))
            vis.plot(1, t[j,:,0], t[j,:,1], dict(ls='-', lw=2.0, zorder=5))
        vis.plot(1, t[:,:,0], t[:,:,1], dict(ls='--', c='gray', lw=.5))
    
    L = 3.0     # Longitud del tubo
    R = 0.5     # Radio del tubo
    x = np.linspace(0,L,20)
    r = np.linspace(-R,R,20)
    xg, yg = np.meshgrid(x, r, indexing='ij', sparse=False)
    
    if w == 0.0:
        # Graficación del flujo.
        vis.quiver(1, xg, yg, u(xg,yg), v(xg,yg), dict(color='silver'))
        vis.plot_frame(1, xg, yg, ticks=False)
        vis.axes(1).set_title('Campo vectorial', fontsize=10)
    else:
        # Graficación del flujo.
        vis.streamplot(1, xg, yg, u(xg,yg), v(xg,yg), dict(color='silver'))
        vis.plot_frame(1, xg, yg, ticks=False)
        vis.axes(1).set_title('Campo vectorial', fontsize=10)

if __name__ == '__main__':

    solveFlujo(50, 0.01, [-0.3,-0.2], 5.0, True)
    plt.show()
