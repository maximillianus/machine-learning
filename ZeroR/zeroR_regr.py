"""
Zero Rule algorithm
Zero Rule algorithm can be used to measure the baseline performance and
as a benchmark where all other ML algorithm will be compared with.
It is baseline for both classification & regression algorithm.

This script is for Regression version
"""

## Import data

filename = 'housing.data'
with open(filename, 'r') as f:
    l = f.readlines()
dataset = [i.split() for i in l]
dataset = [[float(i) for i in lines] for lines in dataset]

medv = [el[13] for el in dataset]
# print(medv)

# Regression
# ZeroR for regression is predicting the mean value
def mean(numlist):
    return sum(numlist)/len(numlist)

# Accuracy is measured by RMSE
def rmse(numlist):
    numlist_mean = sum(numlist)/len(numlist)
    res = [(actual - numlist_mean) ** 2 for actual in numlist]
    return mean(res) ** 0.5

print("** Zero Rule Algorithm: Regression **")
print('Prediction (based on mean):', round(mean(medv),2))
print('Accuracy (measured by RMSE):', round(rmse(medv),2) )
print("Any other Machine Learning Algorithm must give accuracy better than this RMSE")