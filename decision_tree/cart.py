"""
UCI iris data classification using Decision Tree
DecisionTree is imported from sklearn.tree

datasets are assumed to be located in same dir as script file
"""

print("*** Decision Tree Iris Starting ***\n")

import os
import random
import csv
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_val_score

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
train_X, test_X, train_y, test_y = train_test_split(all_X, all_y, 
                                    test_size=0.33)


# Model Building
cart = tree.DecisionTreeClassifier()
cart.fit(train_X, train_y)

# Prediction & Accuracy
prediction = cart.predict(test_X)
accuracy = metrics.accuracy_score(test_y, prediction)
print("Accuracy: " + repr(accuracy))
scores = cross_val_score(cart, train_X, train_y, cv=20)
cv_accuracy = scores.mean()
print("Scores: " + repr(scores))
print("CV Accuracy: " + repr(cv_accuracy * 100.0))




print("\n*** Decision Tree Iris Ending ***")