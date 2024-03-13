import numpy as np
import matplotlib.pyplot as plt
import macti.visual as mvis
from mpl_toolkits.axes_grid1 import make_axes_locatable

def set_axes(ax):
    """
    Configura la razón de aspecto, quita las marcas de los ejes y el marco.
    
    Parameters
    ----------
    ax: axis
    Ejes que se vana configurar.
    """
    ax.set_aspect('equal') 
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
def plot_mesh(ax, xg, yg):
    """
    Dibuja la malla del dominio.
    
    Paramters
    ---------
    ax: axis
    Son los ejes donde se dibujará la malla.
    
    xn: np.array
    Coordenadas en x de la malla.
    
    yn: np.array
    Coordenadas en y de la malla.
    """
    set_axes(ax)
    
    xn = xg[:,0]
    yn = yg[0,:]
    
    for xi in xn:
        ax.vlines(xi, ymin=yn[0], ymax=yn[-1], lw=0.5, color='darkgray')
        
    for yi in yn:
        ax.hlines(yi, xmin=xn[0], xmax=xn[-1], lw=0.5, color='darkgray')
        
    ax.scatter(xg,yg, marker='.', color='darkgray')
    
def plot_frame(ax, xn, yn, lw = 0.5, color = 'k'):
    """
    Dibuja el recuadro de la malla.
    
    Paramters
    ---------
    ax: axis
    Son los ejes donde se dibujará la malla.
    
    xn: np.array
    Coordenadas en x de la malla.
    
    yn: np.array
    Coordenadas en y de la malla.
    """
    set_axes(ax)
    
    # Dibujamos dos líneas verticales
    ax.vlines(xn[0], ymin=yn[0], ymax=yn[-1], lw = lw, color=color)
    ax.vlines(xn[-1], ymin=yn[0], ymax=yn[-1], lw = lw, color=color)

    # Dibujamos dos líneas horizontales
    ax.hlines(yn[0], xmin=xn[0], xmax=xn[-1], lw = lw, color=color)
    ax.hlines(yn[-1], xmin=xn[0], xmax=xn[-1], lw = lw, color=color)
    
def set_canvas(ax, Lx, Ly):
    """
    Configura un lienzo para hacer las gráficas más estéticas.
    
    Parameters
    ----------
    ax: axis
    Son los ejes que se van a configurar.
    
    Lx: float
    Tamaño del dominio en dirección x.
    
    Ly: float
    Tamaño del dominio en dirección y.
    
    Returns
    -------
    cax: axis
    Eje donde se dibuja el mapa de color.
    """
    set_axes(ax)

    lmax = max(Lx,Ly)
    offx = lmax * 0.01
    offy = lmax * 0.01
    ax.set_xlim(-offx, Lx+offx)
    ax.set_ylim(-offy, Ly+offy)
    ax.grid(False)
    
    ax.set_aspect('equal')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    cax.set_xticks([])
    cax.set_yticks([])
    cax.spines['bottom'].set_visible(False)
    cax.spines['left'].set_visible(False)
    
    return cax

def buildMatrix2D(Nx, Ny, a, b, c, orientacion='v'):
    """
    Construye la matriz para diferencias finitas en 2D.
    
    Parameters
    ----------
    Nx: int
    Número de puntos en la dirección x.
    
    Ny: int
    Número de puntos en la dirección y.
    
    a, b, c: float
    Coeficientes de diferencias finitas para las diagonales.
    
    Returns
    -------
    A: np.array
    Matriz del sistema para el caso 2D.
    """
    N = Nx * Ny
    A = np.zeros((N,N))
    RHS = np.zeros((Nx,Ny))

    coef = 2.0 if orientacion == 'v' else 1.0
            
# Primero llena los bloques tridiagonales
    for j in range(0,Ny):
        ofs = Nx * j
        A[ofs, ofs] = c
        A[ofs, ofs + 1] = -coef * a
        for i in range(1,Nx-1):
            A[ofs + i, ofs + i]     = c
            A[ofs + i, ofs + i + 1] = -a
            A[ofs + i, ofs + i - 1] = -a
        A[ofs + Nx - 1, ofs + Nx - 2] = -coef * a
        A[ofs + Nx - 1, ofs + Nx - 1] = c 

# Despues llena las dos diagonales externas
    for k in range(0,N-Nx):
        A[k, Nx + k] = -b
        A[Nx + k, k] = -b
        
    if orientacion == 'h':
        for k in range(N-2*Nx, N-Nx):
            A[Nx + k, k] = -2 * b
        for k in range(0,Nx):
            A[k, Nx + k] = -2 * b

    return A

def calc_coef_FDM(kx, ky, hx, hy):
    a = kx / hx**2 
    b = ky / hy**2
    c = 2 * (a + b)
    return a, b, c

def calc_grad_vertical(T, TH, TC, FL, FR, S, IS, JS, hx, a, b, c):
    NyT, NxT = T.shape
    Nx = NxT - 2 
    Ny = NyT - 2
    
    ### Gradiente vertical
    T[0,  :] = TH  
    T[-1, :] = TC 

    # Construccion de la matriz
    A = buildMatrix2D(Nx+2,Ny, a, b, c, 'v')

    # Definimos el vector del lado derecho RHS
    RHS = np.zeros((Ny,Nx+2))

    # Actualizamos las condiciones de frontera de tipo Dirichlet
    RHS[0,  :] += b * TH  
    RHS[-1, :] += b * TC

    # Actualizamos las condiciones de frontera de tipo Neumann
    RHS[:, 0] += 2 * a * hx * FL
    RHS[:,-1] -= 2 * a * hx * FR
    
    RHS[JS-1, IS] += S # El -1 se debe a que RHS es un vector que comienza en 0

    # Guardamos la temperatura inicial
    T0 = np.copy(T)
    
    # Calculamos la solución.
    T_temp = np.linalg.solve(A, RHS.flatten())

    # Actualizamos el campo escalar T con la solución calculada
    T[1:-1,:] = T_temp.reshape(Ny,Nx+2)
    
    return T0

def calc_grad_horizontal(T, TH, TC, FB, FT, S, IS, JS, hy, a, b, c):
    NyT, NxT = T.shape
    Nx = NxT - 2 
    Ny = NyT - 2
    
    ### Gradiente horizontal
    T[: , 0] = TH
    T[: ,-1] = TC 

    # Construccion de la matriz
    A = buildMatrix2D(Nx,Ny+2, a, b, c, 'h')

    # Definimos el vector del lado derecho RHS
    RHS = np.zeros((Ny+2,Nx))

    # Actualizamos las condiciones de frontera de tipo Dirichlet
    RHS[:, 0] += a * TH  
    RHS[:,-1] += a * TC

    # Actualizamos las condiciones de frontera de tipo Neumann
    RHS[ 0, :] += 2 * b * hy * FB
    RHS[-1, :] -= 2 * b * hy * FT

    RHS[JS, IS-1] += S # El -1 se debe a que RHS es un vector que comienza en 0

    # Guardamos la temperatura inicial
    T0 = np.copy(T)
    
    # Calculamos la solución.
    T_temp = np.linalg.solve(A, RHS.flatten())
    
    # Actualizamos el campo escalar T con la solución calculada
    T[:, 1:-1] = T_temp.reshape(Ny+2,Nx)   
    
    return T0

def plot_solution(T, T0, qx, qy, Lx, Ly, xg, yg, xn, yn):
    # Definimos dos subgráficas: 2 renglones y 1 columna
    fig, ax = plt.subplots(2,2, figsize=(12,5))

    # Primera subgráfica
    # ----------------------
    ## Definición del lienzo
    cax1 = set_canvas(ax[0,0], Lx, Ly)

    # Ejecutamos la función plot_mesh(...)
    plot_mesh(ax[0,0], xg, yg)

    # Segunda subgráfica
    # ----------------------
    ## Definición del lienzo
    cax2 = set_canvas(ax[0,1], Lx, Ly)

    ## Graficación de la componente x del campo escalar sobre la malla
    cb = ax[0,1].contourf(xg, yg, T0.T, levels=50, cmap='inferno')
    fig.colorbar(cb, cax=cax2, ticks=[T.min(), 0.0, T.max()])

    # Tercera gráfica
    # ----------------------
    ## Definición del lienzo
    cax2 = set_canvas(ax[1,0], Lx, Ly)

    ## Graficación de la componente x del campo escalar sobre la malla
    cb = ax[1,0].contourf(xg, yg, T.T, levels=50, cmap='inferno')
    ax[1,0].contour(xg, yg, T.T, levels=10, cmap='Greys')
    fig.colorbar(cb, cax=cax2, ticks=[T.min(), 0.0, T.max()])

    # Cuarta gráfica
    # ----------------------
    ## Definición del lienzo
    cax2 = set_canvas(ax[1,1], Lx, Ly)
    cu = ax[1,1].quiver(xg, yg, qx.T, qy.T)
    plot_frame(ax[1,1], xn, yn)

    plt.tight_layout()
    plt.show()