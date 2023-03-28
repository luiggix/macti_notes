import matplotlib.pyplot as plt
import numpy as np
import seaborn as snb; snb.set();


from ipywidgets import interact
import ipywidgets as widgets

def serie_P(a,p):
    return sum([1/(n**p) for n in range(1,a+1)])

def ejemplo4(a,p):
    plt.figure(figsize=(8,4))
    
    if 0<a and a<50:
        x_s = range(1,a+1,1)
        y_s = [serie_P(x,p) for x in x_s]
        plt.xticks(range(0, a+1, 5))
        
    elif a>=50 and a<=200:
        x_s = range(1,a+1,10)
        y_s = [serie_P(x,p) for x in x_s]
        plt.xticks(range(0, a+1, 10))
        
    elif a>=200 and a<400:
        x_s = range(1,a+1,20)
        y_s = [serie_P(x,p) for x in x_s]
        plt.xticks(range(0, a+1, 20))
        
    elif a>=400 and a<800:
        x_s = range(1,a+1,40)
        y_s = [serie_P(x,p) for x in x_s]
        plt.xticks(range(0, a+1, 100))
    
    elif a>=800 and a<1600:
        x_s = range(1,a+1,80)
        y_s = [serie_P(x,p) for x in x_s]
        plt.xticks(range(0, a+1, 200))
    
    elif a>=1600 and a<5000:
        x_s = range(1,a+1,160)
        y_s = [serie_P(x,p) for x in x_s]
        plt.xticks(range(0, a+1, 400))
        
    else:
        x_s = range(1,a+1,500)
        y_s = [serie_P(x,p) for x in x_s]
        
    
    plt.title(r'Serie P ',fontsize=16,pad=20)
    plt.ylabel("Valor de la Serie")
    plt.xlabel("Valor de K")
    
    plt.scatter(x_s,y_s,lw=0.1,label=r"Serie $\sum_{n=1}^{a} \frac{1}{n^p}$")
    plt.plot(x_s,np.ones(len(x_s))*y_s[-1],linestyle="--",color="green",zorder=10,label=f"Recta \nconstante: {np.around(y_s[-1],4)}")
    
    plt.legend()
    plt.show()
    

w = interact(ejemplo4,
             a = widgets.IntText(value=100,description=r"Valor de $a$"),
             p = widgets.FloatText(value=1,description=r"Valor de $p$"))