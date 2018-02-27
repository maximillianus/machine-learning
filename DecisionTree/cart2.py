"""
UCI iris data classification using Decision Tree
DecisionTree is written from scratch

datasets are assumed to be located in same dir as script file
website:
https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/
"""

print("*** Decision Tree Iris Starting ***\n")

import os
import random
import csv


### Setting work dir ####
scriptloc = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptloc)

# Load sklearn data
#iris = datasets.load_iris()
#print((iris.data))

# Read in Data
#filename = 'iris.data'
filename = 'data_banknote_authentication.csv'
with open(filename, 'r') as f:
    lines = csv.reader(f)
    dataset = list(lines)
    
print(dataset[0:2])

all_X = [d[:-1] for d in dataset]
all_y = [d[-1] for d in dataset]

# Training & Test Set



# Model Building





print("\n*** Decision Tree Iris Ending ***")