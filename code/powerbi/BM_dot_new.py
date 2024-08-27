# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(x_coor, y_coor)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

bin_size = 8  # can change the bin size
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
max_count = dataset.groupby(['Contents', pd.cut(dataset['x_coor'], bins=x_bin_edges, labels=False, right=False), pd.cut(dataset['y_coor'], bins=y_bin_edges, labels=False, right=False)]).size().max()
fig = plt.figure(figsize=(17, 11), facecolor='none', edgecolor='none')   # (width, height)
ax = fig.add_subplot(111)
ax.axis('off')
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
 #['PolyLine', 'Ellipse']  # keys
#unique keys
types = dataset['Contents'].unique()
colors = sns.color_palette("tab20", len(types))
color_map = {subject: color for subject, color in zip(types, colors)}

#colors = {'PolyLine': 'red', 'Ellipse': 'green'}  # Map types to colors
added_labels = set()
colors = {'Eating': 'paleturquoise', 'Getting water': 'royalblue', 'Having a meeting': 'violet', 'Mentoring': 'gold', 'Standing': 'lawngreen', 'Talking': 'navy', 'Using a phone': 'mediumpurple', 'Walking': 'blueviolet', 'Working': 'darkorange'} 



for type_name in types:
    non_zero_bins, circle_sizes, type_name = process_data_for_type(dataset, type_name, x_bin_edges, y_bin_edges, max_count)
    color = colors[type_name]  # Extract color for the current type_name
    for index, row in non_zero_bins.iterrows():
        x_center = (row['x_bin'] * bin_size) + bin_size / 2
        y_center = (row['y_bin'] * bin_size) - bin_size / 2
        if type_name not in added_labels:
            plt.scatter(x_center, y_center, s=circle_sizes.iloc[index], alpha=1, color=color, label=type_name)
            added_labels.add(type_name)
        else:
            plt.scatter(x_center, y_center, s=circle_sizes.iloc[index], alpha=1, color=color)

time = dataset['time'] 
ax.set_xlim(0, width) #width = 792
ax.set_ylim(0, height) #height = 612
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1), ncol=7)

#plt.savefig('occupancy_bin.png', dpi=600, bbox_inches='tight', pad_inches=0, transparent=True)
plt.show()