"""
Stochastic Gradient Descent from scratch and its application
in Linear Regression

Linear Regression Rule:
yhat = b0 + b1 * x
"""

# Creating simple linear regression

def predict(row, coef):
    yhat = coef[0]
    pred = 0
    for i in range(len(row)-1):
        pred += yhat + coef[i + 1] * row[i]
    return pred


dataset = [[1, 1], [2, 3], [4, 3],
           [3, 2], [5, 5]]
coef = [0.4, 0.8]

for row in dataset:
    yhat = predict(row, coef)
    print('yhat: %.2f | y_true: %d' % (yhat, row[1]))

# estimating coefficients
"""
We need:
1. Learning Rate: to see how much the coefficient is corrected each time. ie.
it's the amount of step to descend in each iteration.
2. Epoch: number of iterations to run through the data while updating coef.

We need to update for each coefficients, each row, and each epoch
"""

def coefficients_sgd(train, learning_rate, n_epoch):
    coef = [1.0 for i in range(len(train[0]))]
    # coef will be [0.0] * len(train[0]) = [0.0, 0.0, ...]
    for epoch in range(n_epoch):
        sum_error = 0
        for row in train:
            yhat = predict(row, coef)
            error = yhat - row[-1]
            sum_error += error ** 2
            coef[0] = coef[0] - learning_rate * error
            for i in range(len(row)-1):
                coef[i + 1] = coef[i+1] - learning_rate * error * row[i]
        print('>epoch=%d, error=%.2f' % (epoch, sum_error), '|', coef)
    return coef

learning_rate = 0.01
n_epoch = 100
new_coef = coefficients_sgd(dataset, learning_rate, n_epoch)

# New yhat after using stochastic gradient descent to get coefficient
for row in dataset:
    yhat = predict(row, new_coef)
    print('yhat: %.2f | y_true: %d' % (yhat, row[1]))
