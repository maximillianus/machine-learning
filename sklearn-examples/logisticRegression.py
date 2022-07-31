from sklearn import datasets
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import train_test_split

iris = datasets.load_iris()

X = iris.data
y = iris.target

# Split dataset
train_X, test_X, train_y, test_y = train_test_split(X, y, train_size=0.5, random_state=0)

# Train dataset
lr = LogisticRegression()
lr.fit(train_X, train_y)

lrcv = LogisticRegressionCV(cv=5, random_state=0, max_iter=5)
lrcv.fit(train_X, train_y)

# Validate
print("Logistic Regression: Test fraction correct (Accuracy) = {:.2f}".format(lr.score(test_X, test_y)))
print("Logistic RegressionCV: Test fraction correct (Accuracy) = {:.2f}".format(lrcv.score(test_X, test_y)))