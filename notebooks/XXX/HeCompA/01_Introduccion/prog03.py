import numpy as np
import matplotlib.pyplot as plt

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

# Definimos algunos parámetros para la gráfica
plt.figure(figsize=(6,3))
plt.title('Transferencia de calor')
plt.xlabel('$x$ [m]')
plt.ylabel('$T$ [$^oC$]')

# Realizamos la gráfica con una línea 
plt.plot(x, T, color='k', lw =1.0)

# Graficamos puntos con un color dependiendo de su temperatura
s = plt.scatter(x, T, c=T, cmap='jet', s=80, alpha=0.5)

# Se muestra una barra de color 
plt.colorbar(s) 

plt.savefig('temperatura.pdf')
plt.show()