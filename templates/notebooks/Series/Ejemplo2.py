import matplotlib.pyplot as plt
import numpy as np
import seaborn as snb; snb.set();


from ipywidgets import interact
import ipywidgets as widgets

def serie_geometrica(a,r,K):
    return sum([a*((r)**k) for k in range(K+1)])

def ejemplo2(a,r,k):
    x_s = range(0,k+1,1)
    y_s = [serie_geometrica(a,r,x) for x in x_s]
    
    plt.figure(figsize=(8,4))
    plt.scatter(x_s,y_s)
    plt.scatter(x_s[-1],y_s[-1],color="red")
    
    if 0<k and k<50:
        plt.xticks(range(0, k+1, 5))
    
    elif k>=50 and k<=200:
        plt.xticks(range(0, k+1, 10))
        
    elif k>=200 and k<400:
        plt.xticks(range(0, k+1, 20))
        
    elif k>=400 and k<1000:
        plt.xticks(range(0, k+1, 100))
    
    else:
        plt.xticks(range(0, k+1, 500))
    
    plt.title(r'Serie Geometrica $\sum_{n=0}^{k} ar^{k}$',fontsize=16,pad=20)
    plt.ylabel("Valor de la Serie")
    plt.xlabel("Valor de K")
    plt.show()
    
    if -1<r and r<1:
        print(f"La serie converge a: {a}/(1-({r})) = {np.around(a/(1-r),3):^10}")
        
    elif r>=1:
        print("Valor de r mayor o igual que 1, la serie diverge")
     
    elif r<=1:
        print("Valor de r menor o igual que -1, la serie diverge")

w = interact(ejemplo2,
             a = widgets.IntText(value=3,description=r"$a$"),
             r = widgets.FloatText(value=0.16,description=r"$r$"),
             k = widgets.IntText(value=20,description=r"$k$"))