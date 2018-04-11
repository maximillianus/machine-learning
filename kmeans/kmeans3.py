"""
implementation of KMeans from scratch without external packages
"""
import random
import statistics

# dataset
datapoint = [[1,3], [5, 8], [9,2], [7,10]]
x = [i[0] for i in datapoint]
y = [i[1] for i in datapoint]

print('x:',x)
print('y:',y)

# initial centroids
# random.seed(10)
k = 2
centroids = {
    i+1:[random.randint(0,10), random.randint(0,10)]
    for i in range(k)
}
colmap = {1: 'r', 2:'g', 3:'b'}
print(centroids)

# assign datapoints to a centroids

def euclidean_dist(data_x, data_y, centroid):
    centroid_x = centroid[0]
    centroid_y = centroid[1]
    dist_x = [xpoint - centroid_x for xpoint in data_x]
    dist_y = [ypoint - centroid_y for ypoint in data_y]
    totaldist = [(x**2 + y**2) ** 0.5 for x,y in zip(dist_x, dist_y)]
    totaldist = [round(d, 2) for d in totaldist]
    return totaldist

## calculate individual distance to each centroids
def calc_distance_to_centroids(x, y, centroids):
    totaldist_dict = {}
    for i in centroids.keys():
        print('Centroids',i)
        totaldist = euclidean_dist(x, y, centroids[i])
        totaldist_dict[i] = totaldist
        print(totaldist)
    print('Totaldist:',totaldist_dict)
    return totaldist_dict

totaldist_dict = calc_distance_to_centroids(x, y, centroids)

## compare which centroid has shortest distance and assign centroid
def assign_group(totaldist_dict):
    l1 = zip(*totaldist_dict.values())
    l2 = list(totaldist_dict.keys())
    assignment = [l2[i.index(min(i))] for i in l1]
    print('Assignment:',assignment)
    datagroup = {}
    for k,v in enumerate(assignment):
        if v in datagroup.keys():
            datagroup[v].append(datapoint[k])
        else:
            datagroup[v] = []
            datagroup[v].append(datapoint[k])
    print(datagroup)
    return datagroup

datagroup = assign_group(totaldist_dict)
print(datagroup)

## assign new centroid based on mean of the points in the cluster group

def update_centroids(datagroup, centroids):
    for key in datagroup.keys():
        print(key)
        # print(datagroup[key])
        x = [data[0] for data in datagroup[key]]
        y = [data[1] for data in datagroup[key]]
        new_x = round(statistics.mean(x), 2)
        new_y = round(statistics.mean(y), 2)
        centroids[key] = [new_x, new_y]
    return centroids
print('old centroids:', centroids)
centroids = update_centroids(datagroup, centroids)
print('new centroids:', centroids)

i=0
while True:
    print('Iteration:',i)
    i += 1
    old_centroids = centroids
    totaldist_dict = calc_distance_to_centroids(x, y ,centroids)
    datagroup = assign_group(totaldist_dict)
    centroids = update_centroids(datagroup, centroids)
    print('Centroids:', centroids)
    if centroids == old_centroids:
        print('Same centroids, clustering done')
        break







print('\n**end program**')


