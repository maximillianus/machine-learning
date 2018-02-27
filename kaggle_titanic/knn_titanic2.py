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

# Combine data so no duplicate job for both train & test dataset
# Do this after research on traindf done
combined = pd.concat([traindf])
#combined = pd.concat([traindf, testdf])

#print(combined.info())


#### Data Exploration ####

# This is where we do exploratory data analysis to determine which features
# can be used, dropped, or engineered

#### Data Cleaning ####

# Drop unnecessary columns ie. Cabin & Ticket
combined = combined.drop(['Cabin', 'Ticket'], axis=1)

# Imputing Embarked column
### Check Embarked value counts
combined.Embarked.value_counts()
combined.Embarked = combined.Embarked.fillna('S')


# Extracting Title from Name
passengerTitle = combined.Name.str.extract('([A-Za-z]+)\.', expand=False)
combined['Title'] = passengerTitle

### Replacing title string
combined['Title'] = combined['Title'].replace(['Mlle', 'Ms'], 'Miss')
combined['Title'] = combined['Title'].replace('Mme', 'Mrs')

combined['Title'] = combined['Title'].replace(['Don', 'Capt', 'Col', 'Rev',
                                               'Dr', 'Jonkheer', 'Major'], 'Sir')
combined['Title'] = combined['Title'].replace(['Countess', 'Dona'], 'Lady')

### Converting Title string to numeric
title_map = {'Mr':1, 'Miss':2, 'Mrs':3, 'Master':4, 'Sir':5, 'Lady':6}
combined['Title'] = combined['Title'].map(title_map)

### Drop Name since it's not needed anymore after Title extracted
combined = combined.drop('Name', axis=1)

# Sex
### Nothing much to change. Convert to numeric
sex_map = {'female': 1, 'male': 0}
combined['Sex'] = combined['Sex'].map(sex_map)



# Age
#### Imputing Age
#print(combined[combined.Age.isnull()].Title.value_counts())
#print(combined.groupby('Title', axis=0).mean())
#print(combined.groupby('Title', axis=0).Age.median())
### Try to impute age based on title using median Age
title_age = (combined.groupby('Title', axis=0).Age.median())

combined = combined.set_index(['Title'])
combined['Age'] = combined['Age'].fillna(title_age)
combined.reset_index()


# Family Size ie. Parch & SibSp
combined['FamilySize'] = combined.Parch + combined.SibSp + 1
print(pd.crosstab(combined.FamilySize, combined.Survived, normalize='index'))

#print(combined.info())



#### Data Processing ####



## End
print("\n*** KNN Titanic Ending ***")