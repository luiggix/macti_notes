import numpy as np
import matplotlib.pyplot as plt
import macti.visual
import time

def plot_initial_status(ax, x, u):
    ax.plot(x,[0 for i in x], '-', c='gray', lw=5)#, label='Malla')
    ax.plot(x,u,'r-',lw=2, label='Cond. inicial')
    ax.plot([0,0],[0,-1], 'k--', lw=1.0)
    ax.plot([1,1],[0,1], 'k--', lw=1.0)
    ax.scatter([0,1],[u[0], u[-1]], fc='blue', ec='k', alpha=0.75, label='Cond. de frontera')
    ax.grid()
    
def plot_results(fig, ax1, ax2, metodo,x,u,e,n,ht,suma_tiempos,error):
    # Gráficación de resultados
    titulo = metodo + ': Error = {:5.4e}, Pasos = {:4d}, CPU = {:5.4} [s]'.format(e, n, suma_tiempos)
    fig.suptitle(titulo, fontsize=12)

    ax1.plot(x,u,'-k',lw=3,alpha=0.75,label='Sol. Final ($t=${:3.2f})'.format(n*ht))
    ax1.set_xlabel('$x$')
    ax1.set_ylabel('$u(x)$')
    ax1.grid(True)
    ax1.set_title('Solución numérica', color='blue')
    ax1.legend(fontsize=9)

    ax2.plot(error)
    ax2.set_yscale('log')
    ax2.set_xlabel('$n$')
    ax2.set_ylabel('$Error$')
    ax2.set_title('Error numérico', color='blue')
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(metodo + '.pdf')
    plt.show()

    
def plot_method(ax,metodo,x,u,e,n,ht,suma_tiempos,error):
    titulo = metodo + ': Error = {:5.4e}, Pasos = {:4d}, \n CPU = {:5.4} [s]'.format(e, n, suma_tiempos)
    ax.plot(x,u,'-k',lw=3,alpha=0.75,label='Sol. Final ($t=${:3.2f})'.format(n*ht))
    ax.set_xlabel('$x$')
    ax.set_ylabel('$u(x)$')
    ax.grid(True)
    ax.set_title(titulo, color='blue', fontsize=8)
    ax.legend(fontsize=9)

    
def buildMatrix(N, r):
    '''
    Parameters:
    N: int Tamaño de la matriz.
    r: float r = h_t * alpha / h**2.
    '''
    # Matriz de ceros
    A = np.zeros((N,N))
    
    # Primer renglón
    A[0,0] = 1 + 2 * r
    A[0,1] = -r
    
    # Renglones interiores
    for i in range(1,N-1):
        A[i,i] = 1 + 2 * r
        A[i,i+1] = -r
        A[i,i-1] = -r
    
    # Último renglón
    A[N-1,N-2] = -r
    A[N-1,N-1] = 1 + 2 * r
    
    return A

def FEuler(L,N,alpha,bA,bB,Nt,ht,tol,compara=False,ax=None):
    h = L / (N+1) # Tamaño de la malla
    r = ht * alpha / h**2 
    tolerancia = tol

    print('h = {:6.5f}, ht = {:6.5f}'.format(h, ht))
    x = np.linspace(0,L,N+2) # Puntos de la malla
    u = np.zeros(N+2)        # Arreglo para la solución

    # Condiciones de frontera
    u[0] = bA
    u[N+1] = bB

    suma_tiempos = 0.0 # Tiempo total
    error = []  # Errores

    if not compara:
        # Inicialización de la figura.
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,4))
    else:
        ax1 = ax
        
    plot_initial_status(ax1, x,u)

    # Ciclo en el tiempo, desde 1 hasta Nt-1
    for n in range(1, Nt):
        e = 0.0  
        # Ciclo para resolver en el espacio
        t_start = time.perf_counter()  

        for i in range(1,N+1):
            # Método de Euler hacia adelante
            unew = u[i] + r * (u[i-1] - 2 * u[i] + u[i+1])
            e += (unew - u[i])**2 
            u[i] = unew # Actualización

        t_stop = time.perf_counter()
        suma_tiempos += (t_stop - t_start) 
        e = np.sqrt(h*e)
        error.append(e)

        # Graficación cada 25 pasos
        if n % 25 == 0:
            ax1.plot(x,u,'-', lw = 1.0, alpha = 0.75, zorder=1)

        # Terminación anticipada si se cumple la tolerancia
        if e < tolerancia: 
            break

    if not compara:
        plot_results(fig, ax1, ax2, 'ForwardEuler',x,u,e,n,ht,suma_tiempos,error)
    else:
        return x,u,e,n,ht,suma_tiempos,error

def BEuler(L,N,alpha,bA,bB,Nt,ht,tol,compara=False,ax=None):
    h = L / (N+1) # Tamaño de la malla
    r = ht * alpha / h**2 
    tolerancia = tol

    print('h = {:6.5f}, ht = {:6.5f}'.format(h, ht))
    x = np.linspace(0,L,N+2) # Puntos de la malla
    u = np.zeros(N+2)        # Arreglo para la solución

    # Condiciones de frontera
    u[0] = bA
    u[N+1] = bB

    # Lado derecho del sistema, contiene la condicion inicial u
    f = np.copy(u[1:N+1])
    # Copia de la solución para mantener el resultado en el paso previo.
    uold = np.copy(u)

    # Construcción de la matriz
    A = buildMatrix(N,r)

    suma_tiempos = 0.0 # Tiempo total
    error = []  # Errores

    if not compara:
        # Inicialización de la figura.
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,4))
    else:
        ax1 = ax
    
    plot_initial_status(ax1, x,u)

    # Ciclo en el tiempo, desde 1 hasta Nt-1
    for n in range(1, Nt):

        t_start = time.perf_counter()    

        # Actualización de las condiciones de frontera
        f[0] += r * bA
        f[N-1] += r * bB

        # Solución del sistema lineal
        u[1:N+1] = np.linalg.solve(A,f) 

        t_stop = time.perf_counter()
        suma_tiempos += (t_stop - t_start) 

        # Cálculo del error
        e = np.sqrt(h) * np.linalg.norm(uold-u)
        error.append(e)

        # Graficación cada 25 pasos
        if n % 25 == 0:
            ax1.plot(x,u,'-', lw = 1.0, alpha = 0.75, zorder=1)

        # Actualizacion de la solucion para dar el siguiente paso
        t_start = time.perf_counter()

        f = np.copy(u[1:N+1])
        uold = np.copy(u)

        t_stop = time.perf_counter()
        suma_tiempos += (t_stop - t_start)

        # Terminación anticipada si se cumple la tolerancia
        if e < tolerancia:
            break

    if not compara:
        plot_results(fig, ax1, ax2, 'BackwardEuler',x,u,e,n,ht,suma_tiempos,error)
    else:
        return x,u,e,n,ht,suma_tiempos,error
    
def FE_vs_BE(L,N,alpha,bA,bB,Nt,ht,tol):
    tolerancia = tol

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,4))
    fig.suptitle('Compación de los métodos de Euler', fontsize=12)

    x,u,e,n,ht,suma_tiempos,error = FEuler(L,N,alpha,bA,bB,Nt,ht,tolerancia,True,ax1)
    plot_method(ax1,'Forward',x,u,e,n,ht,suma_tiempos,error)
    
    x,u,e,n,ht,suma_tiempos,error = BEuler(L,N,alpha,bA,bB,Nt,ht,tolerancia,True,ax2)
    plot_method(ax2,'Backward',x,u,e,n,ht,suma_tiempos,error)

    plt.tight_layout()
    plt.savefig('Comparacion.pdf')
    plt.show()
    
if __name__ == "__main__":
    # Parámetros físicos
    L = 1.0   # Longitud del dominio
    bA = -1   # Dirichlet en A
    bB = 1    # Dirichlet en B
    alpha = 1 # Parámetro físico

    # Parámetros numéricos
    N = 49        # Número de incógnitas
    ht = 0.0001   # Paso del tiempo
    Tmax = 1.0    # Tiempo total de simulación
    Nt = int(Tmax / ht) # Número total de pasos

    tolerancia = 1e-6 # Criterio de término anticipado

    FEuler(L,N,alpha,bA,bB,Nt,ht,tolerancia)
    BEuler(L,N,alpha,bA,bB,Nt,ht,tolerancia)

    comparaEuler(L,N,alpha,bA,bB,Nt,ht,tolerancia)
