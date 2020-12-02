import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

file = 'data_new.csv'
df = pd.read_csv(file)

colors = df.groupby('color').size()
color_keys = [x for x in colors.keys()]
color_nums = [colors[key] for key in color_keys]
plt.bar(color_keys,colors)
plt.xlabel('color')
plt.ylabel('# of Cars')
plt.title('Color Observations')
plt.show()

bins = 30 
speeds = np.array(df['speed'])
plt.hist(speeds, bins = bins)
plt.xlabel('Speed MPS')
plt.ylabel('# of Cars')
plt.title('Speed Observations')
plt.show()