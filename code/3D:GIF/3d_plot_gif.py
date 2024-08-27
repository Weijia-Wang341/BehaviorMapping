#pip install fitz
#pip install PyMuPDF


import matplotlib.pyplot as plt

import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
import imageio.v2 as imageio
import plotly.io as pio
import tempfile
import os
from plotly.io import write_image
from PIL import Image
import fitz  # PyMuPDF
import glob



################### Convert PDF to PNG #####################
pdf = fitz.open('plan_flat.pdf')  # Load the PDF file
page = pdf[0]

dpi = 200  # This can be adjusted as needed for higher or lower resolution
zoom = dpi / 72  # PDFs are typically 72 DPI, so calculate the zoom factor

pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))

pix.save('bg_image.png')  

image = Image.open('bg_image.png') 

width, height = image.size



################### Plot #####################
# Load the DataFrame
df = pd.read_csv('dot_data.csv')
width_scale_factor = width / 792
height_scale_factor = height / 612
df['x_coor'] = df['x_coor'] * width_scale_factor
df['y_coor'] = df['y_coor'] * height_scale_factor
# Assuming df is your DataFrame
fig = go.Figure()
# Assuming unique time values can be used to generate one surface per time step
time_values = df['time'].unique()
# Sort the time values to ensure correct animation order
time_values.sort()

#color
colorscale = [[0, 'rgba(64,186,210,0)'],  # navy
             [0.1, 'rgba(32,65,139, .4)'],    #aqua
              [0.3, 'rgba(34,95,161, .6)'],
              [0.7, 'rgba(172,46,145,0.8)'],  #green
              [1, 'rgba(237,43,133,1)']] #red

img = imageio.imread('bg_image.png')
im = np.flipud(img)
im_x, im_y, _ = im.shape
eight_bit_img = Image.fromarray(im).convert('P', palette='WEB', dither=None)
eight_bit_array = np.array(eight_bit_img)

save_dir_3d = '3dplots/'
#frames = []
for time in time_values:
   fig = go.Figure()
   # Filter DataFrame for the current time step
   df_filtered = df[df['time'] == time]
   # Use the filtered DataFrame for KDE
   x = df_filtered['x_coor']
   y = df_filtered['y_coor']

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
   fig.add_trace(go.Surface(x=xgrid, y=ygrid, z=zgrid_transformed, name=f'Time {time}', colorscale=colorscale))


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
      scene_camera_eye=dict(x=-.3, y=-0.6, z=0.9), #angle
      width=1500,
      height=900,
      title = dict(x=0.5,text=f"Time: {time}"),
      title_font_size=30,
      scene=dict(xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, visible=False, range=[0, width]),
                                                                    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, visible=False, range=[0, height]),
                                                                    zaxis=dict(showticklabels=False, showgrid=False, zeroline=False, visible=False, range=[0,1]),
                                                                    aspectmode='manual', aspectratio=dict(x=1, y=height/width, z=0.15),
                                                                    ),
      margin=dict(l=65, r=50, b=65, t=90)
   )


   plot_name_3d = f"{time}.png"  # Generate a unique name for the plot
   fig_path = os.path.join(save_dir_3d, plot_name_3d)
   fig.write_image( fig_path)


############ GIF ##########

def make_gif(frame_folder):
    frames = []  
    images_path = os.path.join(frame_folder, "*")  
    image_files = sorted(glob.glob(images_path))  
    frames = [Image.open(image) for image in image_files]  
    frame_one = frames[-1]
    frame_one.save("download.gif", format="GIF", append_images=frames,
                   save_all=True, duration=1000, loop=0)  # Set loop to 0 for indefinite looping

if __name__ == "__main__":
    make_gif("3dplots")

##### export as HTML file#####

#import plotly.express as px
#fig.write_html("3d_output.html")