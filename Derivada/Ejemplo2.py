from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
import seaborn as snb; snb.set();

def derivada(f,g,x0,h):
    xs =  np.linspace(0,10,100)
    
    plt.figure(figsize=(14,7))
    plt.grid(color="black",ls="--",alpha=0.3)
    plt.title("Derivada",fontsize=22)
    
    plt.plot(xs,f(xs),label='$f(x)$')
    plt.plot(xs,g(xs),label='$f^{\prime}(x)$')
    
    x_ticks_labels=['$x$','$x+h$']
    y_ticks_labels=['$f(x)$', '$f(x+h)$']
    
    plt.xticks((x0, x0 + h),x_ticks_labels,fontsize=15)
    plt.yticks((f(x0), f(x0 + h)),y_ticks_labels,fontsize=15)
    
    x1 = x0 + h
    plt.scatter(x0, f(x0), s=75, color='black', zorder=5)
    plt.scatter(x1, f(x1), s=75, color='black', zorder=5)
    
    plt.plot([x0,x1], [f(x0),f(x0)], lw=2, color='black', zorder=6)
    plt.plot([x1,x1], [f(x0),f(x1)], lw=2, color='black', zorder=6)
    plt.plot([x0,x1], [f(x0),f(x1)], lw=2, color='black', zorder=6)
    
    plt.scatter(x0, g(x0), s=75, fc='C1', ec='black', alpha=0.75, zorder=5)
    
    plt.legend(fontsize=18)
    plt.show()
    
f = lambda x: x**2 + 20 * np.sin(0.5*x)**2
g = lambda x: 2 * x - 20 * np.cos(0.5*x)

w = interact(derivada,
             f=fixed(f),
             g=fixed(g),
             x0 = widgets.FloatSlider(min=0, max=9, step=1, value=6),
             h = widgets.FloatSlider(min=0.1, max=1.5, step=0.1, value=1.0))