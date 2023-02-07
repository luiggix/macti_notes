import matplotlib.pyplot as plt
import numpy as np
import seaborn as snb; snb.set();

from ipywidgets import interact
import ipywidgets as widgets

def S1(N):
    aux = range(1,N+1)
    return sum([abs(np.sin(n))/(n**2) for n in aux])

def ejemplo1(N):
    plt.figure(figsize=(10,4))
    x_s = range(0,151,5)
    y_s = [S1(x) for x in x_s]
    plt.scatter(x_s,y_s)
    plt.scatter(N,S1(N),color="red",label=f'S = {np.around(S1(N),3)}\nN = {N}')
    
    plt.title(r'Serie $\sum_{n=1}^{\infty} \frac{|Sin(n)|}{n^2}$',fontsize=16,pad=20)
    plt.ylabel("Valor de la Serie")
    plt.xlabel("Valor de N")
    plt.legend(fontsize=12,loc="lower center")
    
    plt.show()

w = interact(ejemplo1,
             N = widgets.IntSlider(min=0, max=150, step=5, value=0,interval=1000))

