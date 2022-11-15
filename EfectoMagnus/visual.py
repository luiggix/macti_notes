import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plotGrid(xm, ym, size, frame='grid'):
    Lx = xm[-1] - xm[0]
    Ly = ym[-1] - ym[0]
    plt.figure(figsize=(size, (Ly)/(Lx)*size))

    if frame == 'grid':
        for y in ym:
            plt.plot([xm[0],xm[-1]], [y,y], color = 'gray', ls = '-', lw = 0.5)
        for x in xm:
            plt.plot([x,x], [ym[0],ym[-1]], color = 'gray', ls = '-', lw = 0.5)
    elif frame == 'box':
        plt.plot([xm[0],xm[0]], [ym[0],ym[-1]], color = 'k', ls = '-', lw = 0.5)
        plt.plot([xm[-1],xm[-1]], [ym[0],ym[-1]], color = 'k', ls = '-', lw = 0.5)
        plt.plot([xm[0],xm[-1]], [ym[0],ym[0]], color = 'k', ls = '-', lw = 0.5)
        plt.plot([xm[0],xm[-1]], [ym[-1],ym[-1]], color = 'k', ls = '-', lw = 0.5)
    elif frame == 'topdown':
        plt.plot([xm[0],xm[-1]], [ym[0],ym[0]], color = 'k', ls = '-', lw = 0.5)
        plt.plot([xm[0],xm[-1]], [ym[-1],ym[-1]], color = 'k', ls = '-', lw = 0.5)
        
    axes = plt.gca()
    axes.set_aspect('equal')
    lmin = min(Lx, Ly)
    offx = lmin * 0.1
    offy = lmin * 0.1
    ax = xm[0]
    bx = xm[-1]
    ay = ym[0]
    by = ym[-1]
    axes.set_xlim(ax-offx, bx+offx)
    axes.set_ylim(ay-offy, by+offy)
    axes.set_xlabel('x', fontsize=20)
    axes.set_ylabel('y', fontsize=20)
    axes.spines.left.set_visible(True)
    axes.spines.right.set_visible(False)
    axes.spines.top.set_visible(False)
    axes.spines.bottom.set_visible(True)

    return axes

def plotContornos(xg, yg, u, levels = 50, lines=True, clabel=True, lcolor='k', title='', frame = 'box', cmap = "YlOrRd"):
    cf = plt.contourf(xg, yg, u, levels = levels, cmap = cmap)#, alpha=.75)
    if lines:
        cl = plt.contour(xg, yg, u, levels = 10, colors=lcolor, linewidths=0.5)
        if clabel:
            plt.clabel(cl, inline=True, fontsize=10.0)

    x = xg[:,0]
    y = yg[0,:]
    plt.xticks([x[0], x[-1]], labels=[x[0], x[-1]])
    plt.yticks([y[0], y[-1]], labels=[y[0], y[-1]])
    plt.xlabel(title)
    axes = plt.gca()
    
    Lx = xg[-1,0] - xg[0,0]
    Ly = yg[0,-1] - yg[0,0]
    lmin = min(Lx, Ly)
    offx = lmin * 0.1
    offy = lmin * 0.1
    ax = xg[0,0]
    bx = xg[-1,0]
    ay = yg[0,0]
    by = yg[0,-1]
    plt.xlim(ax-offx, bx+offx)
    plt.ylim(ay-offy, by+offy)
    plotGrid(x, y, frame)
    ax = plt.gca()
    ax.set_aspect('equal')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    cax.set_xticks([])
    cax.set_yticks([])
    fig = plt.gcf()
    fig.colorbar(cf, cax=cax, orientation='vertical')
    
    plt.tight_layout()

    return axes

def plotFlujo(xg, yg, u, v, kind='quiver', scale=10, color='', cmap='', title='', frame = 'box'):
    """
    """

    x = xg[:,0]
    y = yg[0,:]
    plt.xticks([x[0], x[-1]], labels=[x[0], x[-1]])
    plt.yticks([y[0], y[-1]], labels=[y[0], y[-1]])
    plt.xlabel(title)
    
    Lx = xg[-1,0] - xg[0,0]
    Ly = yg[0,-1] - yg[0,0]
    lmin = min(Lx, Ly)
    offx = lmin * 0.1
    offy = lmin * 0.1
    ax = xg[0,0]
    bx = xg[-1,0]
    ay = yg[0,0]
    by = yg[0,-1]
    plt.xlim(ax-offx, bx+offx)
    plt.ylim(ay-offy, by+offy)
    axes = plt.gca()
    
    if kind == 'quiver':
        if len(color) == 0:
            vf = plt.quiver(xg, yg, u, v, cmap='gray', scale=scale)
        else:
            vf = plt.quiver(xg, yg, u, v, color, cmap=cmap, scale=scale)
    elif kind == 'stream':
        if len(color) == 0:        
            vf = plt.streamplot(x, y, u, v, color='gray', linewidth=0.5)
        else:
            vf = plt.streamplot(x, y, u.T, v.T, color=color.T, cmap=cmap, linewidth=0.5)

    plotGrid(x, y, frame) 

    ax = plt.gca()
    ax.set_aspect('equal')
   
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    cax.set_xticks([])
    cax.set_yticks([])
    fig = plt.gcf()
    
    if len(color) != 0:
        if kind == 'quiver':
            fig.colorbar(vf, cax=cax, orientation='vertical')
        elif kind == 'stream':
            fig.colorbar(vf.lines, cax=cax, orientation='vertical')

    plt.tight_layout()         
    return axes
    
if __name__ == '__main__':
 
    Lx = 4.0
    Ly = 1.0
    Nx = 40
    Ny = 10

    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.set_aspect('equal')
    
    x = np.linspace(0,Lx,Nx+2)
    y = np.linspace(0,Ly,Ny+2)
    
#    plotGrid(x,y,'grid')
    
    xg, yg = np.meshgrid(x,y,indexing='ij', sparse=False)
    u = np.sin(xg) * np.cos(yg)
    v = np.cos(xg) * np.sin(yg)
    
    mag = np.sqrt(u**2 + v**2)
    
#    plotFlujo(xg, yg, u, v, kind='quiver')
#    plotFlujo(xg, yg, u, v, kind='quiver', color=mag, cmap='viridis', title='', frame = 'box')

#    plotFlujo(xg, yg, u, v, kind='stream')
    plotFlujo(xg, yg, u, v, kind='stream', color=mag, cmap='winter', title='', frame = 'box')

    
    plt.show()