"""
UCI iris data classification using KNN
KNN is imported from sklearn.neighbors

datasets are assumed to be located in same dir as script file
"""

print("*** KNN Iris Starting ***")
# #Library
import os
import csv
import random
import pandas as pd
from sklearn import neighbors
from sklearn import datasets
from sklearn import metrics
import numpy as np

#pd.set_option('display.max_colwidth', -1)

#### Setting work dir ####
scriptloc = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptloc)

# Load sklearn data
#iris = datasets.load_iris()
#print((iris.data))

# Read in Data
with open('iris.data', 'r') as f:
    lines = csv.reader(f)
    dataset = list(lines)
    
print(dataset[0:2])

# Training & Test set
testSet = []
trainingSet = []

for x in range(len(dataset) - 1):
    for y in range(4):
        # changing data type to float
        dataset[x][y] = float(dataset[x][y])
    if random.random() < 0.66:
        trainingSet.append(dataset[x])
    else:
        testSet.append(dataset[x])

# Separating data & target for both Training and Test
trainingSetdata = [x[:-1] for x in trainingSet]
trainingSettarget = [x[-1] for x in trainingSet]
testSetdata = [x[:-1] for x in testSet]
testSettarget = [x[-1] for x in testSet]

neigh = neighbors.KNeighborsClassifier(n_neighbors=5)
neigh.fit(trainingSetdata,trainingSettarget)
predictions = neigh.predict(testSetdata)

# Measuring accuracy
accuracy = metrics.accuracy_score(testSettarget, predictions)

print("Predictions: ", predictions)
print("Test Set: ", testSettarget)
print("Model Accuracy:", round(accuracy*100, 2), '%')