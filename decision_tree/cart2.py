"""
UCI iris data classification using Decision Tree
DecisionTree is written from scratch

datasets are assumed to be located in same dir as script file
website:
https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/
"""

print("*** Decision Tree Starting ***\n")

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
filename = 'iris.data'
#filename = 'data_banknote_authentication.csv'
with open(filename, 'r') as f:
    lines = csv.reader(f)
    dataset = list(lines)
print(dataset[:2])
# change list of list string to float
#dataset = [[float(i) for i in row] for row in dataset]
for row in dataset:
    row[:-1] = [float(i) for i in row[:-1]]
print(dataset[:2])


all_X = [d[:-1] for d in dataset]
all_y = [d[-1] for d in dataset]

# Training & Test Set



#### Functions Definition ####
# Calculate the Gini index for a split dataset
def gini_index(groups, classes):
    # count all samples at split point
    n_instances = float(sum([len(group) for group in groups]))
    # sum weighted Gini index for each group
    gini = 0.0
    for group in groups:
        size = float(len(group))
        # avoid divide by zero
        if size == 0:
            continue
        score = 0.0
        # score the group based on the score for each class
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p
        # weight the group score by its relative size
        gini += (1.0 - score) * (size / n_instances)
    return gini

# Split a dataset based on an attribute and an attribute value
def test_split(index, value, dataset):
    left, right = list(), list()
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right


# Select the best split point for a dataset
# 1. First loop through all features and split on each values of features
# 2. Calc Gini index for every feature & split and go with the lowest Gini
def get_split(dataset):
    print("*** Start --get_split-- function ***")
    class_values = list(set(row[-1] for row in dataset))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    for index in range(len(dataset[0])-1):
        for row in dataset:
            groups = test_split(index, row[index], dataset)
            gini = gini_index(groups, class_values)
            #print('X%d < %.3f Gini=%.3f' % ((index+1), row[index], gini))
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    print('Final Gini: ', b_score, '| SplitValue:', b_value)
    return {'index':b_index, 'value':b_value, 'groups':b_groups}

# Terminal Node
# I dont understand what this is for
def to_terminal(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)

# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):
    print("*** Starting --split-- function ***")
    left, right = node['groups']
    print('Depth:', depth, '| Max Depth:', max_depth)
    #print('LeftGroup:',left)
    #print('RightGroup:', right)
    del(node['groups'])
    # check for a no split
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        #print('Most common el in LeftNode:', node['left'])
        #print('Most common el in RightNode:', node['right'])
        return
    # check for max depth
    if depth >= max_depth:
        print('*** reached max depth ***')
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        print('Most common el in LeftNode:', node['left'])
        print('Most common el in RightNode:', node['right'])
        #print_tree(node)
        return
    # process left child
    #print('\n*** Grow Left NODE ***')
    #print('LeftNodeSize:', len(left), '| MinSize:', min_size)
    if len(left) <= min_size:
        print('*** Left Node reached min size ***')
        node['left'] = to_terminal(left)
        print('Most common el in LeftNode:', node['left'])
    else:
        node['left'] = get_split(left)
        #print('LeftNode after more split:', node['left'])
        split(node['left'], max_depth, min_size, depth+1)
    # process right child
    #print('\n*** Grow Right NODE ***')
    #print('RightNodeSize:', len(right), '| MinSize:', min_size)
    if len(right) <= min_size:
        print('*** Right Node reached min size ***')
        node['right'] = to_terminal(right)
        print('Most common el in RightNode:', node['left'])
    else:
        node['right'] = get_split(right)
        #print('RightNode after more split:', node['right'])
        split(node['right'], max_depth, min_size, depth+1)


# Build Tree
def build_tree(train, max_depth, min_size):
    print("\n*** Starting to grow TREE ***\n")
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root

# Print a decision tree
def print_tree(node, depth=0):
    if isinstance(node, dict):
        print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
        print_tree(node['left'], depth+1)
        print_tree(node['right'], depth+1)
    else:
        print('%s[%s]' % ((depth*' ', node)))

# Making predictions
def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']

# Classification and Regression Tree Algorithm
def decision_tree(train, test, max_depth, min_size):
    tree = build_tree(train, max_depth, min_size)
    predictions = list()
    for row in test:
        prediction = predict(tree, row)
        predictions.append(prediction)
    return(predictions)

# To check accuracy
def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0
 

d = [[2.771244718,1.784783929,0],
    [1.728571309,1.169761413,0],
    [3.678319846,2.81281357,0],
    [3.961043357,2.61995032,0],
    [2.999208922,2.209014212,0],
    [7.497545867,3.162953546,1],
    [9.00220326,3.339047188,1],
    [7.444542326,0.476683375,1],
    [10.12493903,3.234550982,1],
    [6.642287351,3.319983761,1]]

e = [[0.1,2,0],
     [0.2,3,0],
     [0.25,1,0],
     [0.44,3,0],
     [0.87,2,0],
     [1.1,2,1],
     [1.5,3,1],
     [1.4,5,1],
     [1.33,7,1],
     [0.12,2,1]]

# if lower than 5 -> left, higher than 5 -> right
f = [[0,0],
     [3,0],
     [1,1],
     [7,1]]

print('Data:', d)
#tree = build_tree(d, 3, 1)
#tree = build_tree(dataset, 10, 5)
#print_tree(tree)

random.shuffle(dataset)
n_split = int(0.7 * len(dataset))
train = dataset[:n_split]
test = dataset[n_split:]

#prediction = decision_tree(train, test, 5, 5)
#print(prediction)

test_y = [row[-1] for row in test]
#print(test_y)
#acc = accuracy_metric(test_y, prediction)
#print('Accuracy:', round(acc, 2))

print("\n*** Decision Tree Ending ***")