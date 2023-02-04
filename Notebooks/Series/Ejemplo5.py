import matplotlib.pyplot as plt
import numpy as np
import seaborn as snb; snb.set();


from ipywidgets import interact
import ipywidgets as widgets

def serie_5(K):
    return sum([(k**k)/(np.math.factorial(k)) for k in range(0,K+1)])



def ejemplo5(k):
    plt.figure(figsize=(8,4))
    x_s = range(1,k+1,1)
    y_s = [serie_5(x) for x in x_s]
        
    plt.scatter(x_s,y_s,lw=0.1,label=r"Serie $\sum_{k=0}^{N} \frac{k^k}{k!}$")
    plt.plot(x_s,np.ones(len(x_s))*y_s[-1],linestyle="--",color="green",zorder=4,label=f"Recta \nconstante: {np.around(y_s[-1],4)}")
    
    plt.title('Serie Ejemplo 5',fontsize=16,pad=20)
    plt.ylabel("Valor de la Serie")
    plt.xlabel("Valor de N")
    plt.legend(loc='center left')
    plt.show()
    
w = interact(ejemplo5,
             k = widgets.Play(min=1,max=20,step=1,description=r"Valor de $N$",interval=1000))