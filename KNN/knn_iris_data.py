"""
UCI iris data classification using KNN
KNN is written from ground up

datasets are assumed to be located in same dir as script file
"""

# #Library
import os
import csv
import pandas as pd
import random
import math
#pd.set_option('display.max_colwidth', -1)

#### Setting work dir ####
scriptloc = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptloc)


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

import operator
def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    print(len(distances))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1

    return (correct / float(len(testSet))) * 100.0

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
    if random.random() < 0.70:
        trainingSet.append(dataset[x])
    else:
        testSet.append(dataset[x])

print(len(trainingSet))
print(len(testSet))
predictions = []
k = 3
for x in range(len(testSet)):
    neighbors = getNeighbors(trainingSet, testSet[x], k)

    result = getResponse(neighbors)
    predictions.append(result)
    print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
accuracy = getAccuracy(testSet, predictions)
print('Accuracy: ' + repr(accuracy) + '%')


#print(predictions)