import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
import imageio.v2 as imageio
from PIL import Image
import plotly.io as pio
import tempfile
import os

# Load the DataFrame
df = pd.read_csv('dot_data.csv')
# Assuming df is your DataFrame
fig = go.Figure()
# Assuming unique time values can be used to generate one surface per time step
time_values = df['time'].unique()
# Sort the time values to ensure correct animation order
time_values.sort()

#ONT color
colorscale = [[0, 'rgba(64,186,210,0)'],  # navy
             [0.1, 'rgba(32,65,139, .4)'],    #aqua
              [0.3, 'rgba(34,95,161, .6)'],
              [0.7, 'rgba(172,46,145,0.8)'],  #green
              [1, 'rgba(237,43,133,1)']] #red


#Corgan color
# colorscale = [[0, 'rgba(255, 209, 0, 0)'],  #
            #  [0.1, 'rgba(54, 181, 200, .13)'],    #
            #   [0.4, 'rgba(124, 195, 98, .35)'],  #
            #   [1, 'rgba(228, 86, 32, 1)']]


frames = []
for time in time_values:
   # Filter DataFrame for the current time step
   df_filtered = df[df['time'] == time]
   # Use the filtered DataFrame for KDE
   x = df_filtered['x_coor']
   y = df_filtered['y_coor']
   width = 792
   height = 612
   data = np.vstack([x, y])
   kde = gaussian_kde(data)
   x = np.linspace(0, width, 50)
   y = np.linspace(0, height, 50)
   xgrid, ygrid = np.meshgrid(x, y)
   z = kde(np.vstack([xgrid.flatten(), ygrid.flatten()]))
   zgrid = z.reshape(xgrid.shape)
   zgrid_transformed = (zgrid - zgrid.min()) / (zgrid.max() - zgrid.min())
   #zgrid_transformed = np.sqrt(zgrid_transformed)


   # Adding the initial trace or creating frames
   if time == time_values[0]:
       fig.add_trace(go.Surface(x=xgrid, y=ygrid, z=zgrid_transformed, name=f'Time {time}', colorscale=colorscale))
   else:
       frames.append(go.Frame(data=[go.Surface(x=xgrid, y=ygrid, z=zgrid_transformed, colorscale=colorscale)], name=str(time)))

fig.frames = frames
# Create the slider
sliders = [{
   'steps': [{
       'method': 'animate',
       'label': str(time),
       'args': [[str(time)], {'frame': {'duration': 500, 'redraw': True}, 'mode': 'immediate', "transition": {"duration": 3000}}]
   } for time in time_values],
   'transition': {'duration': 3000},
   'x': 0.1, 'y': 0, 'currentvalue': {'visible': True, 'prefix': 'Time: '}
}]


fig.update_layout(
   updatemenus=[{
       'type': 'buttons',
       'showactive': False,
       'buttons': [
           {
               'label': 'Play',
               'method': 'animate',
               'args': [None, {
                   'frame': {'duration': 2000, 'redraw': True},  # Increase duration to 1000 milliseconds (1 second) per frame
                   'fromcurrent': True,
                   'transition': {'duration': 300}
               }],
           },
           {
               'label': 'Pause',
               'method': 'animate',
               'args': [[None], {
                   'frame': {'duration': 0, 'redraw': False},
                   'mode': 'immediate',
                   'transition': {'duration': 0}
               }],
           }
       ]
   }],
   sliders=sliders,
   title="3D Surface Plot Animation",
)

#read image
img = imageio.imread('bg_image.png')
im = np.flipud(img)
im_x, im_y, _ = im.shape
eight_bit_img = Image.fromarray(im).convert('P', palette='WEB', dither=None)
eight_bit_array = np.array(eight_bit_img)


z = np.zeros(eight_bit_array.shape)

x = np.linspace(0, im_x, im_x)
y = np.linspace(0, im_y, im_y)
#z = np.zeros(im.shape[:2])

dum_img = Image.fromarray(np.ones((3,3,3), dtype='uint8')).convert('P', palette='WEB')
idx_to_color = np.array(dum_img.getpalette()).reshape((-1, 3))
#colorscale = [[i/255, "rgb({}, {}, {})".format(*rgb)] for i, rgb in enumerate(idx_to_color)]
cs = [[0, 'rgb(0, 0, 0)'], [1, 'rgb(255, 255, 255)']]

# Add the image as a surface plot
fig.add_trace(go.Surface(
  z=z,
   surfacecolor=eight_bit_img,  # Use the 2D array of indices here
   colorscale=cs,
   cmin=0,
   cmax=255,
   showscale=False,
))
# fig.update_traces(contours_z=dict(show=True, usecolormap=True,
#                                   highlightcolor="#444", project_z=True))



# Initial layout adjustments
fig.update_layout(
   autosize=False,
   scene_camera_eye=dict(x=-.4, y=-1, z=1.2), #angle
   width=1500,
   height=900,
   scene=dict(xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, visible=False, range=[0, width]),
                                                                    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, visible=False, range=[0, height]),
                                                                    zaxis=dict(showticklabels=False, showgrid=False, zeroline=False, visible=False, range=[0,1]),
                                                                    aspectmode='manual', aspectratio=dict(x=1, y=height/width, z=0.15),
                                                                    ),
   margin=dict(l=65, r=50, b=65, t=90)
)
fig.show()

#save output as HTML
import plotly.express as px

fig.write_html("3d_output.html")