import matplotlib.pyplot as plt
import numpy as np
import seaborn as snb; snb.set();


from ipywidgets import interact
import ipywidgets as widgets

def serie_telescopica(K):
    return sum([(1/k)-(1/(k+1)) for k in range(1,K+1)])



def ejemplo3(k):
    plt.figure(figsize=(8,4))
        
    if 0<k and k<50:
        x_s = range(1,k+1,1)
        y_s = [serie_telescopica(x) for x in x_s]
        plt.xticks(range(0, k+1, 5))
        
    
    elif k>=50 and k<=200:
        x_s = range(1,k+1,5)
        y_s = [serie_telescopica(x) for x in x_s]
        plt.xticks(range(0, k+1, 10))
        
    elif k>=200 and k<400:
        x_s = range(1,k+1,20)
        y_s = [serie_telescopica(x) for x in x_s]
        plt.xticks(range(0, k+1, 20))
        
    elif k>=400 and k<800:
        x_s = range(1,k+1,40)
        y_s = [serie_telescopica(x) for x in x_s]
        plt.xticks(range(0, k+1, 100))
    
    else:
        x_s = range(1,k+1,80)
        y_s = [serie_telescopica(x) for x in x_s]
        plt.xticks(range(0, k+1, 400))
    
    plt.scatter(x_s,y_s,lw=0.1,label=r"Serie $\sum_{k=1}^{N} \left( \frac{1}{k}-\frac{1}{k+1}\right)$")
    plt.plot(x_s,np.ones(len(x_s))*y_s[-1],linestyle="--",color="green",zorder=4,label=f"Recta \nconstante: {np.around(y_s[-1],4)}")
    
    plt.title(r'Serie Telescopica',fontsize=16,pad=20)
    plt.ylabel("Valor de la Serie")
    plt.xlabel("Valor de N")
    plt.legend()
    plt.show()
    
w = interact(ejemplo3,
             k = widgets.IntText(value=8,description=r"Valor de $N$"))