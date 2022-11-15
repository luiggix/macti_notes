import matplotlib.pyplot as plt
import numpy as np
import seaborn as snb; snb.set();

from ipywidgets import interact
import ipywidgets as widgets

def serie_6(N):
    return sum([((-1)**n)/(np.sqrt(n)) for n in range(1,N+1)])

def ejemplo6(N):
    plt.figure(figsize=(10,4))
    x_s = range(0,N,1)
    y_s = [serie_6(x) for x in x_s]
    for i in range(N):
        plt.plot(x_s[0:i],y_s[0:i],color="blue",marker="o",markersize=5,lw=1)
        
    
    
    plt.title(r'Serie $ \sum_{n=0}^{N} \frac{(-1)^n}{\sqrt{n} }$',fontsize=16,pad=20)
    plt.ylabel("Valor de la Serie")
    plt.xlabel("Valor de N")
    plt.show()
    print(f"Para N = {len(x_s)-1}\nValor de la serie: {np.around(y_s[-1],3)}")
    

w = interact(ejemplo6,
             N = widgets.Play(min=1, max=101, step=5,interval=1500))