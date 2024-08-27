# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(undefined, undefined.1, undefined.2, undefined.3)
# dataset = dataset.drop_duplicates()
df = dataset
# Paste or type your script code here:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from scipy.ndimage.filters import gaussian_filter
# Assuming df is already loaded
# df = pd.read_csv('dot_data.csv')
# Your existing setup
grid_size = 10
x_bins = np.arange(0, max(df['x_coor']) + grid_size, grid_size)
y_bins = np.arange(0, max(df['y_coor']) + grid_size, grid_size)
fig = plt.figure(figsize=(17, 11), facecolor='none', edgecolor='none') 
ax = fig.add_subplot(111)
ax.axis('off')
# Calculate the 2D histogram
hist, x_edges, y_edges = np.histogram2d(df['x_coor'], df['y_coor'], bins=[x_bins, y_bins])
hist = gaussian_filter(hist, .15)
# Masking zero values
hist_masked = np.ma.masked_where(hist == 0, hist)
# Generate the heatmap
cmap = clr.LinearSegmentedColormap.from_list('custom blue', ['#0733f5', '#07f5c9', '#f5f107', '#ed1607'], N=256)
# Ensure the colormap alpha is set to 0 for the lowest value
cmap.set_bad(color='none') # This makes the zero-count areas fully transparent
plt.imshow(hist_masked.T, origin='lower', cmap=cmap, extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]], aspect='auto')
ax.set_xlim(0, 792) # Assuming width is defined elsewhere as 792
ax.set_ylim(0, 612) # Assuming height is defined elsewhere as 612
plt.tight_layout()  # Adjust the layout to remove extra space

plt.show()