import numpy as np
import math
import ipywidgets as wd

#import macti.visual as mvis
import visual as mvis

def saxpy(α, x, y):
    αxpy = α * x + y

    print(' α = {} \t x = {} \t y = {}'.format(α, x, y))
    print(' α * x = {} '.format(α * x))
    print(' α * x + y = {} \n'.format(α * x + y))

    v = mvis.Plotter(fig_par = dict(figsize=(5,5)))
    v.set_coordsys()
    v.plot_vectors_sum(1, [α*x, y], ['α*x', 'y'])
    v.grid()
    v.show()

w_x1 = wd.FloatSlider(
    min=-2.0, max=2.0, step=0.5, value=0.5,
    description='x1',
    layout=wd.Layout(width='250px')
)

w_x2 = wd.FloatSlider(
    min=-2.0, max=2.0, step=0.5, value=1.0,
    description='x2',
    layout=wd.Layout(width='250px')
)

w_y1 = wd.FloatSlider(
    min=-2.0, max=2.0, step=0.5, value=1.5,
    description='y1',
    layout=wd.Layout(width='250px')
)

w_y2 = wd.FloatSlider(
    min=-2.0, max=2.0, step=0.5, value=0.5,
    description='y2',
    layout=wd.Layout(width='250px')
)

w_a = wd.FloatSlider(
    min=-2.0, max=2.0, step=0.5, value=1.0,
    description='α',
    layout=wd.Layout(width='250px')
)

button = wd.Button(
    description="", icon='play',
    layout=wd.Layout(width='50px')    
)

ui = wd.HBox([wd.VBox([w_a, button]),
              wd.VBox([w_x1, w_y1]),
              wd.VBox([w_x2, w_y2])])

ui.layout = wd.Layout(border='solid 1px black')
ui.layout.width = '900px'
            
output = wd.Output()

display(ui, output)

def on_button_clicked(b):
    output.clear_output(wait=True)
    with output:
        saxpy(w_a.value, np.array([w_x1.value, w_x2.value]), 
                         np.array([w_y1.value, w_y2.value]))

button.on_click(on_button_clicked)