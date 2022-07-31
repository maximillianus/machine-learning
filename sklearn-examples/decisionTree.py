from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.model_selection import train_test_split

iris = datasets.load_iris()

X = iris.data
y = iris.target

# Split dataset
train_X, test_X, train_y, test_y = train_test_split(X, y, train_size=0.5, random_state=0)

# Train dataset
dtree = DecisionTreeClassifier()
dtree.fit(train_X, train_y)

extratree = ExtraTreeClassifier()
extratree.fit(train_X, train_y)

# Validate
print("DecisionTree: Test fraction correct (Accuracy) = {:.2f}".format(dtree.score(test_X, test_y)))
print("ExtraTree: Test fraction correct (Accuracy) = {:.2f}".format(extratree.score(test_X, test_y)))