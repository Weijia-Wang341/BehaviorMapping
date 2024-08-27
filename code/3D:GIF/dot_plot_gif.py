
import pandas as pd
from scipy.stats import gaussian_kde
import imageio.v2 as imageio
from PIL import Image
import plotly.io as pio
import tempfile
from plotly.io import write_image
import fitz  # PyMuPDF
import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


################### Convert PDF to PNG #####################
pdf = fitz.open('plan_flat.pdf')  # Load the PDF file
page = pdf[0]

dpi = 900  # This can be adjusted as needed for higher or lower resolution
zoom = dpi / 72  # PDFs are typically 72 DPI, so calculate the zoom factor

pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))

pix.save('bg_image.png')  

image = Image.open('bg_image.png') 

width, height = image.size

################### Plot #####################
# Convert RGBA values from 0-255 range to 0-1 range
def convert_color(rgba):
    return tuple([c / 255.0 for c in rgba[:-1]] + [rgba[-1] / 255.0])

colors = {
    'Walking Alone': (172,46,145,255), 'Socialization': (202,222,244,255), 'Sitting': (225,211,238,255), 'Manual Phone Use': (98,158,222,255), 'Eating/Drinking': (230,162,215,255), 'Large Electronic Use': (16,47,80,255), 'Bag Shuffling': (32,65,139,255), 'Standing': (108,59,150,255), 'Talking on Phone': (144,170,229,255),
    'Walking in Groups': (89,128,216,255), 'Interacting with Passengers': (23,48,104,255), 'Interacting with Staff': (15,32,69,255), 'Staff Standing': (199,212,242,255), 'Staff Sitting': (150,190,233,255), 'Staff Manual Phone Use': (196,168,221,255), 'Buying Food or Goods': (167,125,204,255),
    'Staff Socialization': (81,44,112,255), 'Additional Bags': (54,29,75,255), 'Staff Large Electronic Use': (34,95,161,255), 'Taking Photos or Video': (242,208,235,255), 'Staff Eating/Drinking': (25,71,120,255)
}

# Convert colors to Matplotlib-friendly format
converted_colors = {k: convert_color(v) for k, v in colors.items()}

### legend image ###


# Load your data
df = pd.read_csv('dot_data.csv')
bin_size = 10  # can change the bin size
width = 792  # Assuming width is defined
height = 612  # Assuming height is defined
x_bin_edges = np.arange(0, width + 1, bin_size)
y_bin_edges = np.arange(0, height + 1, bin_size)

def process_data_for_type(df, type_name, x_bin_edges, y_bin_edges, max_count):
    type_df = df[df['Contents'] == type_name].copy()
    type_df['x_bin'] = pd.cut(type_df['x_coor'], bins=x_bin_edges, labels=False, right=False)
    type_df['y_bin'] = pd.cut(type_df['y_coor'], bins=y_bin_edges, labels=False, right=False)
    bin_counts = type_df.groupby(['x_bin', 'y_bin']).size().reset_index(name='count')
    circle_sizes = (bin_counts['count'] / max_count) * 150  # Adjust size relative to max count
    return bin_counts[bin_counts['count'] > 0], circle_sizes, type_name

# Determine the overall max count to scale circle sizes consistently
max_count = df.groupby(['Contents', pd.cut(df['x_coor'], bins=x_bin_edges, labels=False, right=False), pd.cut(df['y_coor'], bins=y_bin_edges, labels=False, right=False)]).size().max()

# Create a separate figure just for the legend
legend_fig, legend_ax = plt.subplots()

# ['PolyLine', 'Ellipse']  # keys
# unique keys
types = df['Contents'].unique()



# Loop through each type_name to add legends for each type
for type_name in types:
    color = converted_colors[type_name]
    # Get processed data for the type
    non_zero_bins, circle_sizes, _ = process_data_for_type(df, type_name, x_bin_edges, y_bin_edges, max_count)

    # Add a scatter plot to the legend figure with label=type_name and color corresponding to the type
    legend_ax.scatter([], [], label=type_name, color=color)

# Place the legend in the figure
legend_ax.legend(ncol=7)

# Hide the axes
legend_ax.axis('off')

# Save the legend as a single image
legend_fig.savefig('legend.png',bbox_inches='tight',  transparent=True)

# Close the legend figure
plt.close(legend_fig)


########### By Hours ###################

background = Image.open('bg_image.png') #path to blank floor plan
background = background.convert("RGBA")
# Get image size
width, height = background.size

legend = Image.open('legend.png')
legend = legend.convert("RGBA")

#resize the legend and put it on top of background
legend_width, legend_height = legend.size
new_legend_width = int(legend_width * 0.6)  # Resize the legend to 50% of its original width
new_legend_height = int(legend_height * 0.6)  # Resize the legend to 50% of its original height
legend = legend.resize((new_legend_width, new_legend_height), Image.LANCZOS)

x_offset = (background.width - legend.width) // 2  # Center the legend horizontally
y_offset = background.height - legend.height // 2
background.paste(legend, (x_offset, y_offset), legend)
background.save('bg.png')
bg = Image.open('bg.png')


def process_data_for_type(df, type_name, x_bin_edges, y_bin_edges, max_count):
   type_df = df[df['Contents'] == type_name].copy()
   type_df['x_bin'] = pd.cut(type_df['x_coor'], bins=x_bin_edges, labels=False, right=False)
   type_df['y_bin'] = pd.cut(type_df['y_coor'], bins=y_bin_edges, labels=False, right=False)
   bin_counts = type_df.groupby(['x_bin', 'y_bin']).size().reset_index(name='count')
   circle_sizes = (bin_counts['count'] / max_count) * 100

   return bin_counts[bin_counts['count'] > 0], circle_sizes, type_name



df = pd.read_csv('dot_data.csv')
width_scale_factor = 9900 / 792
height_scale_factor = 7650 / 612
df['x_coor'] = df['x_coor'] * width_scale_factor
df['y_coor'] = df['y_coor'] * height_scale_factor
for time in df['time'].unique():
  hours = df[df['time'] == time]
  bin_size = 125  # can change the bin size
  #width = 792  # Assuming width is defined
  #height = 612  # Assuming height is defined
  x_bin_edges = np.arange(0, width + 1, bin_size)
  y_bin_edges = np.arange(0, height + 1, bin_size)

  # Determine the overall max count to scale circle sizes consistently
  max_count = hours.groupby(['Contents', pd.cut(hours['x_coor'], bins=x_bin_edges, labels=False, right=False), pd.cut(hours['y_coor'], bins=y_bin_edges, labels=False, right=False)]).size().max()
  fig = plt.figure(figsize=(17, 11), facecolor='none', edgecolor='none')  # (width, height)
  ax = fig.add_subplot(111)
  ax.axis('off')
  plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
  #['PolyLine', 'Ellipse']  # keys
  #unique keys
  types = hours['Contents'].unique()
  #colors = sns.color_palette("tab20", len(types))
  #color_map = {subject: color for subject, color in zip(types, colors)}

  save_dir = "plots/"
  #colors = {'PolyLine': 'red', 'Ellipse': 'green'}  # Map types to colors
  added_labels = set()
  #colors = {'Walking Alone': 'papayawhip', 'Socialization': 'royalblue', 'Sitting': 'violet', 'Manual Phone Use': 'gold', 'Eating/Drinking': 'lawngreen', 'Large Electronic Use': 'coral', 'Bag Shuffling': 'mediumpurple', 'Standing': 'blueviolet', 'Talking on Phone': 'darkorange', 'Walking in Groups': 'silver', 'Interacting with Passengers': 'paleturquoise', 'Interacting with Staff': 'lightskyblue', 'Staff Standing': 'hotpink', 'Staff Sitting': 'indigo', 'Staff Manual Phone Use': 'yellow', 'Buying Food or Goods': 'green', 'Staff Socialization': 'navy', 'Additional Bags': 'darkred', 'Staff Large Electronic Use': 'darkorange', 'Taking Photos or Video': 'moccasin', 'Staff Eating/Drinking': 'palegreen'}

  for type_name in types:
    non_zero_bins, circle_sizes, type_name = process_data_for_type(hours, type_name, x_bin_edges, y_bin_edges, max_count)
    color = converted_colors[type_name]  # Extract color for the current type_name
    for index, row in non_zero_bins.iterrows():
        x_center = (row['x_bin'] * bin_size) + bin_size / 2
        y_center = (row['y_bin'] * bin_size) + bin_size /2
        if type_name not in added_labels:
            plt.scatter(x_center, y_center, s=circle_sizes.iloc[index], alpha=1, color=color, label=type_name)
            added_labels.add(type_name)
        else:
            plt.scatter(x_center, y_center, s=circle_sizes.iloc[index], alpha=1, color=color)


  ax.set_xlim(0, width) #width = 792
  ax.set_ylim(0, height) #height = 612
  #plt.legend()
  plt.title(f"Time: {time}", fontsize=26, fontweight='bold', y=0.9)


  plot_name = f"{time}.png"  # Generate a unique name for the plot
  plt.savefig(os.path.join(save_dir, plot_name),dpi=900, bbox_inches='tight', pad_inches=0, transparent=True)


  img = Image.open(os.path.join(save_dir, plot_name))
  img = img.convert("RGBA")
  img = img.resize((width, height), Image.ANTIALIAS)
  combined_img = Image.alpha_composite(bg, img)
  combined_name = f"combined_{time}.png"
  combined_img.save(os.path.join(save_dir, plot_name))

  # plt.savefig(f"{time}.png", dpi=600, bbox_inches='tight', pad_inches=0, transparent=True)
  plt.close(fig)


################### GIF #####################
import os
import glob
from PIL import Image

def make_gif(frame_folder):
    frames = []  
    images_path = os.path.join(frame_folder, "*")  
    image_files = sorted(glob.glob(images_path))  
    frames = [Image.open(image) for image in image_files]  
    frame_one = frames[-1]
    frame_one.save("download.gif", format="GIF", append_images=frames,
                   save_all=True, duration=1000, loop=0)  # Set loop to 0 for indefinite looping

if __name__ == "__main__":
    make_gif("plots")
