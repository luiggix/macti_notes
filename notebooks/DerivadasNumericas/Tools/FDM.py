import numpy as np

def buildMatrix2D(Nx, Ny, diag):
    """
    Construye la matriz para diferencias finitas en 2D.
    
    Parameters
    ----------
    Nx: int
    Número de puntos en la dirección x.
    
    Ny: int
    Número de puntos en la dirección y.
    
    diagonal: float
    Valor que se pone en la diagonal principal.
    
    Returns
    -------
    A: np.array
    Matriz del sistema para el caso 2D.
    """
    N = Nx * Ny
    A = np.zeros((N,N))

# Primero llena los bloques tridiagonales
    for j in range(0,Ny):
        ofs = Nx * j
        A[ofs, ofs] = diag 
        A[ofs, ofs + 1] = 1
        for i in range(1,Nx-1):
            A[ofs + i, ofs + i]     = diag
            A[ofs + i, ofs + i + 1] = 1
            A[ofs + i, ofs + i - 1] = 1
        A[ofs + Nx - 1, ofs + Nx - 2] = 1 
        A[ofs + Nx - 1, ofs + Nx - 1] = diag

# Despues llena las dos diagonales externas
    for k in range(0,N-Nx):
        A[k, Nx + k] = 1
        A[Nx + k, k] = 1

    return A

if __name__ == '__main__':

    Nx = 4
    Ny = 4

    A = buildMatrix2D(Nx, Ny, -4)
    print(A)
