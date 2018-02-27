"""
Predicting Kaggle's Titanic using KNN
"""

print("*** KNN Titanic Starting ***\n")

#### Library ####
import os
import random
import pandas as pd
import numpy as np
from sklearn import neighbors
from sklearn import tree
from sklearn import metrics
from sklearn import utils
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

#### Setting work dir ####
scriptloc = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptloc)

#### Import Data ####
traindf = pd.read_csv('train.csv')
testdf = pd.read_csv('test.csv')

#### Data Exploration ####
# Sex vs Survival
sex_survived = pd.crosstab(traindf.Survived, traindf.Sex)

# PClass vs Survival
pclass_survived = pd.crosstab(traindf.Survived, traindf.Pclass)

# Pclass & Sex vs Survival
sexclass_survived = pd.crosstab(traindf.Survived, 
                                [traindf['Sex'], traindf['Pclass']])


#### Data Processing ####

# Dealing with NaN values
## Based on traindf.Age.describe(), sum(traindf.Age.isnull()) is not 0
## there is some null values.
## Impute with 0
traindf.Age = traindf.Age.fillna(traindf.Age.median())
testdf.Age = testdf.Age.fillna(testdf.Age.median())


# Feature Engineering
## if sex is male then 0, if female then 1
## Use 'map' for string replacement
traindf['Sex'] = traindf['Sex'].map({'female':1, 'male':0})
testdf['Sex'] = testdf['Sex'].map({'female':1, 'male':0})

## Splitting Pclass into 3 individual class
Pclass_dummies = pd.get_dummies(traindf.Pclass, prefix='Pclass')
traindf = pd.concat([traindf, Pclass_dummies], axis=1)
Pclass_dummies = pd.get_dummies(testdf.Pclass, prefix='Pclass')
testdf = pd.concat([testdf, Pclass_dummies], axis=1)

## FamilySize
traindf['FamilySize'] = traindf.SibSp + traindf.Parch + 1
# Family ID: Alone, Small, Big
traindf['FamilyID'] = np.where((traindf.FamilySize == 1), 1, 0)
traindf['FamilyID'] = np.where((traindf.FamilySize > 1) & (traindf.FamilySize <= 4), 2, traindf.FamilySize)
traindf['FamilyID'] = np.where((traindf.FamilySize > 4), 3, traindf.FamilySize)

testdf['FamilySize'] = testdf.SibSp + testdf.Parch + 1
# Family ID: Alone, Small, Big
testdf['FamilyID'] = np.where((testdf.FamilySize == 1), 1, 0)
testdf['FamilyID'] = np.where((testdf.FamilySize > 1) & (testdf.FamilySize <= 4), 2, testdf.FamilySize)
testdf['FamilyID'] = np.where((testdf.FamilySize > 4), 3, testdf.FamilySize)

## Age group
traindf['AgeGroup'] = np.where((traindf.Age <= 5)&(traindf.Age>0), 1, 0)
testdf['AgeGroup'] = np.where((testdf.Age <= 5)&(testdf.Age>0), 1, 0)


## Splitting Fare into bins
traindf['Farelow'] = np.where(traindf.Fare <= 10, 1 ,0)
traindf['Faremid'] = np.where((traindf.Fare > 10) & (traindf.Fare < 70), 1 ,0)
traindf['Farehigh'] = np.where(traindf.Fare >= 70, 1 ,0)
testdf['Farelow'] = np.where(testdf.Fare <= 10, 1 ,0)
testdf['Faremid'] = np.where((testdf.Fare > 10) & (testdf.Fare < 70), 1 ,0)
testdf['Farehigh'] = np.where(testdf.Fare >= 70, 1 ,0)

#### Splitting data to train and test ####
split = 0.7
traindf = utils.shuffle(traindf)
idx = round(split * traindf.shape[0])
train = traindf.iloc[:idx]
test = traindf.iloc[idx:]

# using model_selection.train_test_split
# all_X = train.drop('Survived', axis=1)
# all_y = train['Survived']

# trainX, testX, trainY, testY = train_test_split(
#                                 all_X, all_y, test_size=0.3, random_state=None)

# print(trainX.head())


#### Feature Selection ####
# Feature
features = ['Sex', 'Pclass', 'AgeGroup', 'FamilyID']
#features.extend(['Farelow', 'Faremid', 'Farehigh'])
print("Features: " + repr(features))

## Converting columns in feature dataframe to list of list
all_X = traindf[features].values.tolist()
trainX = train[features].values.tolist()
testX = test[features].values.tolist()

# Target Var
all_y = traindf.Survived.tolist()
trainY = train.Survived.tolist()
testY = test.Survived.tolist()

# Using holdout/validation set
holdout_X = testdf[features].values.tolist()



#### Modelling ####
# Predict based on whether the passenger is female
knn = neighbors.KNeighborsClassifier(n_neighbors=6)
knn.fit(trainX, trainY)
prediction = knn.predict(testX)

dtree = tree.DecisionTreeClassifier()
dtree.fit(trainX, trainY)
prediction = dtree.predict(testX)

# Accuracy
accuracy = metrics.accuracy_score(testY, prediction)
print("Accuracy: " + repr(accuracy*100.0))

# Cross-Validation
scores = cross_val_score(knn, all_X, all_y, cv=10)
cv_accuracy = scores.mean()
print("Scores: " + repr(scores))
print("CV Accuracy: " + repr(cv_accuracy))


#### Modelling & Prediction using validation set ####
knn_real = neighbors.KNeighborsClassifier(n_neighbors=6)
knn_real.fit(all_X, all_y)
prediction = knn_real.predict(holdout_X)

# # Output result
# print("*** OUTPUT RESULT ***\n")
# myoutput = pd.DataFrame({"PassengerId": testdf.PassengerId,
#                          "Survived":prediction})
# print(myoutput.head(2))
myoutput = pd.DataFrame(data=prediction, index=testdf.PassengerId,
                       columns = ['Survived'])
#myoutput.to_csv('my_submission3.csv', header=True)

# # Write result to csv
# myoutput.to_csv('my_submission2.csv', index=False)

# Detailed result df
outputdf = testdf.assign(Survived = lambda x:prediction)
#print(outputdf.info())
#outputdf.to_csv('detail_result.csv', index=False)


## End
print("\n*** KNN Titanic Ending ***")