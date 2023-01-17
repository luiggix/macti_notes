import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact
import ipywidgets as widgets

R = lambda t, S: np.exp(-t/S)


def Ejemplo1(S,h,t):
    xs=np.linspace(0,10,100)
    ys=[olvido(x,S) for x in xs]
    
    m=[]
    td = np.arange(0,8,h)
    
    for i,x in enumerate(td):
        m.append((olvido(x + h, S) - olvido(x, S)) / h)
    
    ix = int(t * (len(m)-1) / 8)       
    recta = m[ix]*(xs-td[ix]) + olvido(td[ix], S) 
    
    plt.figure(figsize=(14,5))
    
    ax1 = plt.subplot(1,2,1)
    ax2 = plt.subplot(1,2,2)
    
    ax1.plot(xs,ys,color="orange",lw=3)
    
    ax1.plot(xs,recta,color="red")
    ax1.scatter(td[ix],olvido(td[ix],S),lw=5,color="red",zorder=6)
    
    ax1.plot(td,olvido(td,S),marker="o",color="black")
    
    ax2.plot(td,m,ls="--",marker="o")
    
    S_text = '$S$ = {}'.format(S)
    ax1.set_title('Función del olvido: $R(t) = e^{-t/s}$  ' + S_text, )
    ax1.set_xlabel("$t$ (días)")
    ax1.set_ylabel("$R$")
    ax1.set_ylim(-0.1,1.2)
    ax1.set_xlim(-0.5,8)
    
    ax2.set_title('Pendiente $m(t)$')
    ax2.set_xlabel("$t$ (días)")
    ax2.set_ylabel("m")
    ax2.set_ylim(-1,0.1)
    ax2.set_xlim(-0.5,8)
    
    
    plt.show()
    
    
w = interact(Ejemplo1,
             S = widgets.FloatSlider(min=0.1, max=1, step=0.1, value=0.5),
             h = widgets.FloatSlider(min=0.05, max=1, step=0.01, value=0.9),
             t = widgets.IntSlider(min=0, max=8, step=1, value=1))