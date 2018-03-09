"""
Implementation of linear regression from scratch in Python
No library is used for the implementation

"""

print(" ** Start Linear Regression **\n")

## Library
import matplotlib.pyplot as plt
import csv

## Dummy Data
#x = [1, 2, 4, 3, 5]
#y = [1, 3, 3, 2, 5]

## Import data
filename = 'swedish_insurance.csv'
with open(filename, 'r', ) as csvfile:
    l = csv.reader(csvfile)
    dataset = list(l)
print('Dataset:')
print(dataset[:5])
x = [float(i[0]) for i in dataset[1:]]
y = [float(i[1]) for i in dataset[1:]]

print('X:', x)
print('Y:', y)

#plt.plot(x, y, 'bx')
#plt.show()

## Helper Functions Definition

def mean(values):
    return sum(values)/len(values)

def variance(values):
    # find mean
    values_mean = mean(values)
    # find sample size
    N = len(values)
    # calc variance
    result = sum([(i - values_mean) ** 2 for i in values]) / N
    return result

def covariance(valX, valY):
    # find mean X & Y
    meanX = mean(valX)
    meanY = mean(valY)
    # check sample size X & Y. X & Y must be same length
    if len(valX) == len(valY):
        N = len(valX)
    else:
        return '** Error X and Y are not the same!! **'
    # calc covariance
    result = sum([(x - meanX) * (y - meanY) for x,y in zip(valX,valY)]) / N
    return result

def coefficients(valX, valY):
    # Find Coefficients B1 (slope)
    # * b1 = covariance(X,Y) / variance(x)
    b1 = covariance(valX, valY) / variance(valX)
    #print('Coef B1:', b1)
    # Find Coefficients B0 (slope)
    # * Formula: b0 = meanY - b1 * meanX
    b0 = mean(valY) - b1 * mean(valX)
    #print('Coef B0:', b0)
    return [b0, b1]

def predictio(novlalX, valY):
    b0, b1 = coefficients(valX,valY)
    y_hat = [round(b0 + b1 * y, 3) for y in valX]
    return y_hat

# Evaluating error using root mean square error
# RMSE formula: sqrt(sum(pi-yi)^2/n)
# basically: find diff -> square it -> average it -> sqrt it

def eval_rmse(predict, actual):
    res = [(i-j) ** 2 for i,j in zip(predict, actual)]
    rmse = mean(res) ** 0.5
    return rmse

def rsquared(valX, valY):
    y_hat = predictions(valX, valY)
    meanY = mean(valY)
    total_sum_squares = sum([(y - meanY) ** 2 for y in valY])
    total_sum_squares_res = sum([(y - y_h) ** 2 for y, y_h in zip(y, y_hat)])
    return 1 - (total_sum_squares / total_sum_squares_res)

print('rsquared:', rsquared(x,y))

def simple_linear_regr(train, test):
    print("\n ** Simple Linear Regression ** ")
    trainX = [x[0] for x in train]
    trainY = [x[1] for x in train]
    coef = coefficients(trainX, trainY)
    b0 = coef[0]
    b1 = coef[1]
    print('Coef B0:', b0, '| Coef B1:', b1)
    # Accuracy of RMSE
    trainY_hat = [round(b0 + b1 * x, 3) for x in trainX]
    rmse = eval_rmse(trainY_hat, trainY)
    print('RMSE:', rmse)
    # Prediction
    testY_hat = [round(b0 + b1 * x, 3) for x in test]
    print('Prediction test_Y_hat:', testY_hat)
    return testY_hat


# Main function
train = list(zip(x,y))
testX = [100, 200, 300, 400, 500]

print(simple_linear_regr(train, testX))

print("\n ** End Linear Regression ** ")


