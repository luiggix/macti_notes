import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_mesh_lines(xm, ym):
    for y in ym:
        plt.plot([xm[0],xm[-1]], [y,y], color = 'gray', ls = '-', lw = 0.5)
    for x in xm:
        plt.plot([x,x], [ym[0],ym[-1]], color = 'gray', ls = '-', lw = 0.5)

def plot_mesh(Lx, Ly, xg, yg):
    plt.scatter(xg, yg, marker='.')
    xm = xg[:,0]
    ym = yg[0]
    plt.xticks(xm, labels=[])
    plt.yticks(ym, labels=[])
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    lmax = max(Lx,Ly)
    offx = lmax * 0.1
    offy = lmax * 0.1
    plt.xlim(-offx, Lx+offx)
    plt.ylim(-offy, Ly+offy)

    plot_mesh_lines(xm,ym)
        
    ax = plt.gca()
    ax.set_aspect('equal')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    cax.set_xticks([])
    cax.set_yticks([])

def plot_contour(Lx, Ly, xg, yg, T, ticks, mesh = False, lines = 0, colors = 'k',
                 cmap = 'inferno', yshared=False):
    c = plt.contourf(xg, yg, T, levels=50, cmap=cmap)
    
    if lines > 0:
        plt.contour(xg, yg, T, levels=lines, linewidths = 0.5, colors=colors)
        
    xm = xg[:,0]
    ym = yg[0]
    plt.xticks(xm, labels=[])
    plt.yticks(ym, labels=[])
    plt.xlabel('$x$')
    if not(yshared):
        plt.ylabel('$y$')
    lmax = max(Lx,Ly)
    offx = lmax * 0.1
    offy = lmax * 0.1
    plt.xlim(-offx, Lx+offx)
    plt.ylim(-offy, Ly+offy)
    if mesh:
        plot_mesh_lines(xm, ym)
    ax = plt.gca()
    ax.set_aspect('equal')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    cax.set_xticks([])
    cax.set_yticks([])
    plt.gcf().colorbar(c, cax=cax, ticks=ticks, orientation='vertical')

def plot_vector(Lx, Ly, xg, yg, v, mesh = False, yshared=False):    
    plt.quiver(xg, yg, v[0], v[1])
    
    xm = xg[:,0]
    ym = yg[0]
    
    plt.xticks(xm, labels=[])
    plt.yticks(ym, labels=[])
    plt.xlabel('$x$')
    if not(yshared):
        plt.ylabel('$y$')
    lmax = max(Lx,Ly)
    offx = lmax * 0.1
    offy = lmax * 0.1
    plt.xlim(-offx, Lx+offx)
    plt.ylim(-offy, Ly+offy)
    if mesh:
        plot_mesh_lines(xm, ym)
        
    ax = plt.gca()
    ax.set_aspect('equal')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    cax.set_xticks([])
    cax.set_yticks([])

def Laplaciano2D(Nx, Ny, diagonal):
    """ Esta funcion calcula los coeficientes del 
    sistema lineal producido por el operador de 
    Laplace en 2D. Estos coeficientes son almacenados 
    en la matriz pentadiagonal correspondiente."""
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

def RHS(Nx, Ny, T):
    f = np.zeros(Nx * Ny) # RHS
    
    # BOTTOM WALL
    for i in range(0,Nx):
        f[i] -= T[i+1, 0] 
    
    # TOP WALL
    idx = 1
    for i in range((Ny-1)*Nx, Ny * Nx):
        f[i] -= T[idx, -1] 
        idx += 1
    
    # LEFT WALL
    jdx = 1
    for j in range(0, Ny * Nx, Nx):
        f[j] -= T[0, jdx]
        jdx += 1
        
    # RIGHT WALL
    jdx = 1
    for j in range(Nx-1, Ny * Nx, Nx):
        f[j] -= T[-1, jdx]
        jdx += 1
        
    return f

def Laplaciano2D_NS(Nx, Ny, r):
    """ Esta funcion calcula los coeficientes del 
    sistema lineal producido por el operador de 
    Laplace en 2D. Estos coeficientes son almacenados 
    en la matriz pentadiagonal correspondiente."""
    N = Nx * Ny
    A = np.zeros((N,N))

# Primero llena los bloques tridiagonales
    for j in range(0,Ny):
        ofs = Nx * j
        A[ofs, ofs] = (1 + 4 * r)
        A[ofs, ofs + 1] = -r
        for i in range(1,Nx-1):
            A[ofs + i, ofs + i]     = (1 + 4 * r)
            A[ofs + i, ofs + i + 1] = -r
            A[ofs + i, ofs + i - 1] = -r
        A[ofs + Nx - 1, ofs + Nx - 2] = -r 
        A[ofs + Nx - 1, ofs + Nx - 1] = (1 + 4 * r) 

# Despues llena las dos diagonales externas
    for k in range(0,N-Nx):
        A[k, Nx + k] = -r
        A[Nx + k, k] = -r

    return A

def RHS_NS(Nx, Ny, T, r):
    f = np.zeros(Nx * Ny) # RHS
    
    # BOTTOM WALL
    for i in range(0,Nx):
        f[i] += r * T[i+1, 0] 
    
    # TOP WALL
    idx = 1
    for i in range((Ny-1)*Nx, Ny * Nx):
        f[i] += r * T[idx, -1] 
        idx += 1
    
    # LEFT WALL
    jdx = 1
    for j in range(0, Ny * Nx, Nx):
        f[j] += r * T[0, jdx]
        jdx += 1
        
    # RIGHT WALL
    jdx = 1
    for j in range(Nx-1, Ny * Nx, Nx):
        f[j] += r * T[-1, jdx]
        jdx += 1
    
    index = 0
    for j in range(1, Ny+1):
        for i in range(1, Nx+1):
            f[index] += T[i,j]
            index += 1
        
    return f

#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    Nx = 10
    Ny = 21
    Lx = 1.0
    Ly = 1.0

    xn = np.linspace(0,Lx,Nx)
    yn = np.linspace(0,Ly,Ny)
    xg, yg = np.meshgrid(xn, yn, indexing='ij', sparse=False)
    
    fig = plt.figure(figsize=(12,5))
    
    plt.subplot(1,2,1)
    plot_mesh(Lx, Ly, xg, yg)
    
    T = np.sin(xg * yg)
    plt.subplot(1,2,2)
    plot_contour(Lx, Ly, xg, yg, T, ticks = [0, 0.5, 1.0], lines = 10, colors='k', cmap = 'viridis', yshared=True)
    plt.show()
    
    A = Laplaciano2D(Nx-2, Ny-2, 20)
    print(A)
    
    f = RHS(Nx-2, Ny-2, T)
    print(f)
    
