import numpy as np

def temperatura(x, TA, TB, L, k, q):
    """
    Calcula la temperatura usando la fórmula obtenida con Series de Taylor.
    """
    return ((TB - TA)/L + q /(2*k) * (L - x) ) * x + TA
    
# Datos físicos
k = 1000
L = 0.5
TA = 100
TB = 500
q = 0

# Datos numéricos
N = 21
x = np.linspace(0,L,N)

T = temperatura(x, TA, TB, L, k, q)

print('Valores de x:', x)
print('Valores de T: {}'.format(T))

