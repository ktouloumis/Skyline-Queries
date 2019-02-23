#program to plot times for KMFREQ and DBFREQ
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

kmean5= [6.19, 7.6, 11.673685550689697, 12.41, 19.58, 33.96, 52.18, 68.03, 73.6, 104.49, 136.51]

kmeans10= [7.63, 9.76, 12.46, 17.54, 23.94, 25.9, 39.72, 43.34, 60.97, 74.17, 90.3]

kmean15 = [9.03, 8.94, 11.53, 14.11, 17.87, 19.62, 30.40, 35.58, 46.74, 58.56, 68.99]

dbfreq5 = [8.36, 11.23, 16.72, 24.73, 26.53, 53.63, 63.66, 97.52, 98.67, 131.17, 226.51]

dbfreq10 = [17.02, 16.34, 25.55, 31.09, 55, 59.51, 132.85, 137, 169.22, 187.5, 293.49]

dbfreq15 = [9.56, 16.49, 19.75, 33.03, 69.08, 109.34, 105.52, 227.08, 209.54, 226.30, 265.8]



# Data
df = pd.DataFrame({'x': [5,6,7,8,9,10,11,12,13,14,15], '5 clusters': kmean5, '10 clusters': kmeans10,
                   '15 clusters': kmean15 })

# multiple line plot
plt.plot('x', '5 clusters', data=df, marker='o', markerfacecolor='blue', markersize=5, color='skyblue', linewidth=1)
plt.plot('x', '10 clusters', data=df, marker='x', color='olive', linewidth=1)
plt.plot('x', '15 clusters', data=df, marker='*', color='red', linewidth=1, linestyle='dashed')
plt.xlabel('Dimensions')
plt.ylabel('Time in seconds')
plt.title('KMFREQ')
plt.legend()
plt.show()

####DBFREQ
df = pd.DataFrame({'x': [5,6,7,8,9,10,11,12,13,14,15], '5 Minpts': dbfreq5, '10 Minpts': dbfreq10,
                   '15 Minpts': dbfreq15 })

# multiple line plot
plt.plot('x', '5 Minpts', data=df, marker='o', markerfacecolor='blue', markersize=5, color='skyblue', linewidth=1)
plt.plot('x', '10 Minpts', data=df, marker='x', color='olive', linewidth=1)
plt.plot('x', '15 Minpts', data=df, marker='*', color='red', linewidth=1, linestyle='dashed')
plt.xlabel('Dimensions')
plt.ylabel('Time in seconds')
plt.title('DBFREQ')
plt.legend()
plt.show()