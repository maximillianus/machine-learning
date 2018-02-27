######## Titanic Kaggle ########

## Initialize
rm(list=ls())
setwd("C:/NotBackedUp/datafiles/kaggle")


## Read Data
train_df <- read.csv("titanic/train.csv", stringsAsFactors = F)
test_df <- read.csv("titanic/test.csv", stringsAsFactors = F)


## Edit Data
train_df$Child <- 0
train_df$Child[train_df$Age < 18] <- 1
train_df$Title <- sapply(train_df$Name, FUN=function(x) {strsplit(x, split='[,.]')[[1]][2]})
train_df$Title <- trimws(train_df$Title)


# combine df into 1
train_df$Child <- NULL
test_df$Survived <- NA
combi <- rbind(train_df, test_df)


# Feature engineering & filling up NA variables
combi$Title <- sapply(combi$Name, FUN=function(x) {strsplit(x, split='[,.]')[[1]][2]})
combi$Title <- trimws(combi$Title)
combi$FamilySize <- combi$SibSp + combi$Parch + 1

combi$Surname <- sapply(combi$Name, FUN=function(x) {strsplit(x, split='[,.]')[[1]][1]})
combi$FamilyID <- paste(as.character(combi$FamilySize), combi$Surname, sep="")
combi$FamilyID[combi$FamilySize <= 2] <- 'Small'
famIDs <- data.frame(table(combi$FamilyID))
famIDs <- famIDs[famIDs$Freq <= 2,]
combi$FamilyID[combi$FamilyID %in% famIDs$Var1] <- 'Small'
combi$FamilyID <- factor(combi$FamilyID)

combi$FamilyID2 <- combi$FamilyID
combi$FamilyID2 <- as.character(combi$FamilyID2)
combi$FamilyID2[combi$FamilySize <= 3] <- 'Small'
combi$FamilyID2 <- factor(combi$FamilyID2)

combi$Embarked[combi$Embarked==""] <- "S"
combi$Embarked <- factor(combi$Embarked)

combi$Fare[which(is.na(combi$Fare))] <- median(combi$Fare, na.rm=TRUE)

combi$Title <- factor(combi$Title)
combi$Sex <- factor(combi$Sex)

# Split data into train and test
train <- combi[1:891,]
test <- combi[892:1309,]

## Machine Learning
library(rpart)

## Finetuning model
# fit <- rpart(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked,
#              data=train_df,
#              method="class")

# Unleash more control over fitting
fit <- rpart(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked,
             data=train_df,
             method="class",
             control=rpart.control(minsplit=2, cp=0))


# Trying to find good model fit for Age
AgeFit <- rpart(Age ~ Pclass + Sex + SibSp + Parch + Fare + Embarked + Title + FamilySize,
                data=combi[!is.na(combi$Age),], 
                method="anova")
combi$Age[is.na(combi$Age)] <- predict(AgeFit, combi[is.na(combi$Age),])



## plotting model
library(rattle)
library(rpart.plot)
library(RColorBrewer)
fancyRpartPlot(fit)

Prediction <- predict(fit, test_df, type = 'class')

## using Random Forest
library(randomForest)
set.seed(415)
fit <- randomForest(as.factor(Survived) ~ Pclass + Sex + Age + SibSp + Parch + 
                      Fare + Embarked + Title + FamilySize + FamilyID2,
                    data=train, 
                    importance=TRUE, 
                    ntree=2000)


Prediction <- predict(fit, test)

## Using conditional forest
library(party)
set.seed(415)
fit <- cforest(as.factor(Survived) ~ Pclass + Sex + Age + SibSp + Parch + 
                      Fare + Embarked + Title + FamilySize + FamilyID,
               data=train,
               controls = cforest_unbiased(ntree=2000, mtry=3))

Prediction <- predict(fit, test, OOB=TRUE, type = "response")

## Write Result
# Initial prediction
test_df$Survived <- 0
test_df[test_df$Sex == 'female'] <- 1 

# Using logical decision
#my_submit <- data.frame(PassengerId = test_df$PassengerId, Survived = test_df$Survived)
# Using decision tree
my_submit <- data.frame(PassengerId = test_df$PassengerId, Survived = Prediction)
# Using random forest
my_submit <- data.frame(PassengerId = test$PassengerId, Survived = Prediction)

#Write into file
write.csv(x = my_submit, file = "titanic/my_submission.csv", row.names = FALSE)