"""
Zero Rule algorithm
Zero Rule algorithm can be used to measure the baseline performance and
as a benchmark where all other ML algorithm will be compared with.
It is baseline for both classification & regression algorithm.

This script is for Classification version
"""

import csv

## Import data

filename = 'diabetes.csv'
with open(filename, 'r') as csvfile:
    l = csv.reader(csvfile)
    dataset = list(l)

colnames = dataset[0]
dataval = [[float(i) for i in lines] for lines in dataset[1:]]
outcomes = [el[8] for el in dataval]

# Classification
def predict_outcome(classlist):
    freqtable = [[el,classlist.count(el)] for el in set(classlist)]
    counts = [el[1] for el in freqtable]
    maxcount_idx = [i for i,j in enumerate(counts) if j == max(counts)]
    theoutcome_lbl = [freqtable[i][0] for i in maxcount_idx]
    theoutcome_val = [freqtable[i][1] for i in maxcount_idx]
    acc = round(theoutcome_val[0] / len(classlist), 5)
    outcome_acc = theoutcome_lbl.append(acc)
    return theoutcome_lbl

prediction = predict_outcome(outcomes)


print("** Zero Rule Algorithm: Classification **")
print('Prediction (based on most count):', prediction[0])
print('Accuracy (measured by count ratio):', prediction[1] * 100.0, '%' )
print("Any other Machine Learning Algorithm must give accuracy better than this accuracy")