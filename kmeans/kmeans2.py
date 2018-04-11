"""
Script to K-means using 
"""

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans

# np.random.seed(100)
k = 3
centroids = {
    i+1: [np.random.randint(0, 50), np.random.randint(0, 70)]
    for i in range(k)
}
print('Initial centroids:', centroids)
df = pd.DataFrame({
    'x': [12, 20, 28, 18, 29, 33, 24, 45, 45],
    'y': [39, 36, 30, 52, 54, 46, 55, 59, 63]
    })
colmap = {1: 'r', 2:'g', 3:'b'}

# fig = plt.figure(figsize=(5,5))
# plt.scatter(df['x'], df['y'], color='k')
# for i in centroids.keys():
#     plt.scatter(*centroids[i], color=colmap[i])
# plt.xlim(0, 80)
# plt.ylim(0, 80)
# plt.show()

def assignment(df, centroids):
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2)
        df['distance_from_{}'.format(i)] = (
            np.sqrt(
                (df['x'] - centroids[i][0]) ** 2
                + (df['y'] - centroids[i][1]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
    df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
    df['color'] = df['closest'].map(lambda x: colmap[x])
    return df

def update(centroids):
    for i in centroids.keys():
        centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
        centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
    return centroids

df = assignment(df, centroids)
centroids = update(centroids)
df = assignment(df, centroids)

while True:
    closest_centroids = df['closest'].copy(deep=True)
    centroids = update(centroids)
    df = assignment(df, centroids)
    if closest_centroids.equals(df['closest']):
        break

print(df)
print('end')
