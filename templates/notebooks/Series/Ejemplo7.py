import matplotlib.pyplot as plt
import numpy as np
import seaborn as snb; snb.set();

f = lambda t: 1/(2**(t))

def st(inicio, final):
    lista = []
    r = 0
    for n in range(inicio, final+1):
        r += 1/(2**(n))
        lista.append(r)
    return lista

t = np.arange(1, 21, 1) 
y = f(t)
y2 = st(0,19)

plt.figure(figsize=(8,4))
plt.scatter(x=t, y=y,ls='-',lw=1,color='blue', zorder=3,label=r'Sucesión:  $\frac{1}{2^n}$')
plt.scatter(x=t, y=y2, label=r'Serie:  $\sum_{n=0}^{\infty} \frac{1}{2^n}$',lw=1,color='red', zorder=1)
plt.legend()

plt.title(r'Lámpara')
plt.xlabel('$n$')
plt.ylabel('$S$')
plt.ylim(-0.1,2.2)


plt.show()