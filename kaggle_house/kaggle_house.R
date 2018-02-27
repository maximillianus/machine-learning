#### Kaggle House Price ####

## Initialize
rm(list=ls())
setwd("C:/NotBackedUp/datafiles/kaggle")

## Read Data
train <- read.csv("house/train.csv", stringsAsFactors = F)
test <- read.csv("house/test.csv", stringsAsFactors = F)

#### Data Cleaning ####

## Dealing with NAs/missing value
# Check which column has NA:
colSums(is.na(train))
# 4 variables with a lot of NAs: PoolQC, Fence, MiscFeature, Alley
# let's just exclude these 4 variables since too many NAs
drops <- c("PoolQC", "Fence", "MiscFeature", "Alley")
train <- train[ , !(names(train) %in% drops)]
rm(drops)

#######################


#### Feature Engineering ####

## correlation plot
#plot(train$OverallQual, train$SalePrice)
#plot(train$GrLivArea, train$SalePrice)

# create dummy train_df
train_ <- train
# Converting character variable to numeric
# MSZoning
train_$zone[train_$MSZoning %in% c("C (all)")] <- 1
train_$zone[train_$MSZoning %in% c("FV")] <- 2
train_$zone[train_$MSZoning %in% c("RH", "RM")] <- 3
train_$zone[train_$MSZoning %in% c("RL")] <- 4

# Street
train_$paved[train_$Street == "Pave"] <- 1
train_$paved[train_$Street != "Pave"] <- 0

# LotShape
# 1 is regular, 0 is irregular
train_$lot_shape[train_$LotShape %in% c("Reg")] <- 1
train_$lot_shape[train_$LotShape %in% c("IR1", "IR2", "IR3")] <- 0

# LandContour
# 1 is Level, 0 is non-level
train_$isflat[train_$LandContour %in% c("Lvl")] <- 1
train_$isflat[train_$LandContour %in% c("Bnk", "HLS", "Low")] <- 0

# Utilities
# 1 is all pub utilies, 0 not all
train_$pubutil[train_$Utilities %in% c("AllPub")] <- 1
train_$pubutil[train_$Utilities %in% c("NoSewr", "NoSeWa", "ELO")] <- 0

# Lot Config
# 1 is all pub utilies, 0 not all
train_$lot_config[train_$LotConfig %in% c("Inside")] <- 1
train_$lot_config[train_$LotConfig %in% c("Corner")] <- 2
train_$lot_config[train_$LotConfig %in% c("CulDSac")] <- 3
train_$lot_config[train_$LotConfig %in% c("FR2", "FR3")] <- 4

# Land Slope
# 1 is all pub utilies, 0 not all
train_$slope[train_$LandSlope %in% c("Gtl")] <- 1
train_$slope[train_$LandSlope %in% c("Mod", "Sev")] <- 0

# Neighborhood
price <- summarize(group_by(train_, Neighborhood), mean(SalePrice, na.rm=T))
# based on price, divide into house with neighborhood pricing >150k or <150k
nbhd_lo <- price$Neighborhood[price$`mean(SalePrice, na.rm = T)` < 150000]
nbhd_hi <- price$Neighborhood[price$`mean(SalePrice, na.rm = T)` >= 150000]
train_$nbhd_price_hi[train_$Neighborhood %in% nbhd_hi] <- 1
train_$nbhd_price_hi[!train_$Neighborhood %in% nbhd_hi] <- 0

# Condition1
price <- summarize(group_by(train_, Condition1), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$Condition1, exclude = NULL)

train_$normalcond1[train_$Condition1 == 'Norm'] <- 1
train_$normalcond1[train_$Condition1 != 'Norm'] <- 0

# Condition2
price <- summarize(group_by(train_, Condition2), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$Condition2, exclude = NULL)

train_$normalcond2[train_$Condition2 == 'Norm'] <- 1
train_$normalcond2[train_$Condition2 != 'Norm'] <- 0


# BldgType
price <- summarize(group_by(train_, BldgType), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$BldgType, exclude = NULL)

train_$buildingtype[train_$BldgType %in% c("1Fam", "TwnhsE")] <- 1
train_$buildingtype[!train_$BldgType %in% c("1Fam", "TwnhsE")] <- 0

# HouseStyle
price <- summarize(group_by(train_, HouseStyle), value=median(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$HouseStyle, exclude = NULL)

train_$hse_style[train_$HouseStyle %in% c("1.5Unf")] <- 1
train_$hse_style[train_$HouseStyle %in% c("SFoyer", "1.5Fin")] <- 2
train_$hse_style[train_$HouseStyle %in% c("2.5Unf", "SLvl", "1Story")] <- 3
train_$hse_style[train_$HouseStyle %in% c("2.5Fin", "2Story")] <- 4

# RoofStyle
price <- summarize(group_by(train_, RoofStyle), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$RoofStyle, exclude = NULL)
train_$roof_style[train_$RoofStyle == "Gambrel"] <- 1
train_$roof_style[train_$RoofStyle == "Gable"] <- 2
train_$roof_style[train_$RoofStyle == "Mansard"] <- 3
train_$roof_style[train_$RoofStyle == "Flat"] <- 4
train_$roof_style[train_$RoofStyle == "Hip"] <- 5
train_$roof_style[train_$RoofStyle == "Shed"] <- 6


# RoofMatl
price <- summarize(group_by(train_, RoofMatl), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$RoofMatl, exclude = NULL)

train_$stdroofmatl[train_$RoofMatl == "CompShg"] <- 1
train_$stdroofmatl[train_$RoofMatl != "CompShg"] <- 0

# Exterior1st
price <- summarize(group_by(train_, Exterior1st), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$Exterior1st, exclude = NULL)

extgrade1_lo <- price$Exterior1st[price$value < 150000]
extgrade1_med <- price$Exterior1st[price$value >= 150000 & price$value < 200000]
extgrade1_hi <- price$Exterior1st[price$value >= 200000]

train_$ext_grade_1[train_$Exterior1st %in% extgrade1_lo] <- 1
train_$ext_grade_1[train_$Exterior1st %in% extgrade1_med] <- 2
train_$ext_grade_1[train_$Exterior1st %in% extgrade1_hi] <- 3

rm(extgrade1_lo, extgrade1_med, extgrade1_hi)

# Exterior2nd
price <- summarize(group_by(train_, Exterior2nd), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$Exterior2nd, exclude = NULL)

extgrade2_lo <- price$Exterior2nd[price$value < 150000]
extgrade2_med <- price$Exterior2nd[price$value >= 150000 & price$value < 200000]
extgrade2_hi <- price$Exterior2nd[price$value >= 200000]

train_$ext_grade_2[train_$Exterior2nd %in% extgrade2_lo] <- 1
train_$ext_grade_2[train_$Exterior2nd %in% extgrade2_med] <- 2
train_$ext_grade_2[train_$Exterior2nd %in% extgrade2_hi] <- 3

rm(extgrade2_lo, extgrade2_med, extgrade2_hi)

# MasVnrType
price <- summarize(group_by(train_, MasVnrType), median(SalePrice, na.rm=T))
price
train_$msn_vnrtype[train_$MasVnrType == "None" | is.na(train_$MasVnrType)] <- 2
train_$msn_vnrtype[train_$MasVnrType == "BrkCmn"] <- 1
train_$msn_vnrtype[train_$MasVnrType == "BrkFace"] <- 3
train_$msn_vnrtype[train_$MasVnrType == "Stone"] <- 4

# ExterQual
train_$extern_qual[train_$ExterQual == "Po" | is.na(train_$ExterQual)] <- 1
train_$extern_qual[train_$ExterQual == "Fa"] <- 2
train_$extern_qual[train_$ExterQual == "TA"] <- 3
train_$extern_qual[train_$ExterQual == "Gd"] <- 4
train_$extern_qual[train_$ExterQual == "Ex"] <- 5

# ExterCond
train_$extern_cond[train_$ExterCond == "Po" | is.na(train_$ExterCond)] <- 1
train_$extern_cond[train_$ExterCond == "Fa"] <- 2
train_$extern_cond[train_$ExterCond == "TA"] <- 3
train_$extern_cond[train_$ExterCond == "Gd"] <- 4
train_$extern_cond[train_$ExterCond == "Ex"] <- 5

# Foundation
price <- summarize(group_by(train_, Foundation), mean(SalePrice, na.rm=T))
table(train_$Foundation, exclude = NULL)
train_$bsmt_qual[train_$BsmtQual == "Slab"] <- 1
train_$bsmt_qual[train_$BsmtQual == "BrkTil"] <- 2
train_$bsmt_qual[train_$BsmtQual == "Cblock"] <- 3
train_$bsmt_qual[train_$BsmtQual == "Stone"] <- 4
train_$bsmt_qual[train_$BsmtQual == "Wood"] <- 5
train_$bsmt_qual[train_$BsmtQual == "PConc"] <- 6

# BsmtQual
train_$bsmt_qual[train_$BsmtQual == "Po" | is.na(train_$BsmtQual)] <- 1
train_$bsmt_qual[train_$BsmtQual == "Fa"] <- 2
train_$bsmt_qual[train_$BsmtQual == "TA"] <- 3
train_$bsmt_qual[train_$BsmtQual == "Gd"] <- 4
train_$bsmt_qual[train_$BsmtQual == "Ex"] <- 5

# BsmtCond
train_$bsmt_cond[train_$BsmtCond == "Po" | is.na(train_$BsmtCond)] <- 1
train_$bsmt_cond[train_$BsmtCond == "Fa"] <- 2
train_$bsmt_cond[train_$BsmtCond == "TA"] <- 3
train_$bsmt_cond[train_$BsmtCond == "Gd"] <- 4
train_$bsmt_cond[train_$BsmtCond == "Ex"] <- 5

# BsmtExposure
price <- summarize(group_by(train_, BsmtExposure), mean(SalePrice, na.rm=T))
train_$bsmt_expose[is.na(train_$BsmtExposure)] <- 1
train_$bsmt_expose[train_$BsmtExposure == "No"] <- 2
train_$bsmt_expose[train_$BsmtExposure == "Mn"] <- 3
train_$bsmt_expose[train_$BsmtExposure == "Av"] <- 4
train_$bsmt_expose[train_$BsmtExposure == "Gd"] <- 5

# BsmtFinType1
price <- summarize(group_by(train_, BsmtFinType1), mean(SalePrice, na.rm=T))
train_$bsmt_fin1[train_$BsmtFinType1 == "GLQ"] <- 5
train_$bsmt_fin1[train_$BsmtFinType1 == "Unf"] <- 4
train_$bsmt_fin1[train_$BsmtFinType1 == "ALQ"] <- 3
train_$bsmt_fin1[train_$BsmtFinType1 %in% c("BLQ","LwQ","Rec")] <- 2
train_$bsmt_fin1[is.na(train_$BsmtFinType1)] <- 1

# BsmtFinType2
price <- summarize(group_by(train_, BsmtFinType1), mean(SalePrice, na.rm=T))
train_$bsmt_fin2[train_$BsmtFinType2 == "ALQ"] <- 5
train_$bsmt_fin2[train_$BsmtFinType2 == "Unf"] <- 4
train_$bsmt_fin2[train_$BsmtFinType2 == "GLQ"] <- 3
train_$bsmt_fin2[train_$BsmtFinType2 %in% c("BLQ","LwQ","Rec")] <- 2
train_$bsmt_fin2[is.na(train_$BsmtFinType2)] <- 1


# Heating
# check pricing of heating using groupingby & summarize
price <- summarize(group_by(train_, Heating), mean(SalePrice, na.rm=T))
# Based on pricing, gas heating is significantly more expensive
train_$gasheat[train_$Heating %in% c("GasA", "GasW")] <- 1
train_$gasheat[!train_$Heating %in% c("GasA", "GasW")] <- 0

# HeatingQC
train_$heatqc[train_$HeatingQC == "Po"] <- 1
train_$heatqc[train_$HeatingQC == "Fa"] <- 2
train_$heatqc[train_$HeatingQC == "TA"] <- 3
train_$heatqc[train_$HeatingQC == "Gd"] <- 4
train_$heatqc[train_$HeatingQC == "Ex"] <- 5

# CentralAir
train_$aircon[train_$CentralAir == "Y"] <- 1
train_$aircon[train_$CentralAir == "N"] <- 0

# Electrical
#price <- summarize(group_by(train_, Electrical), mean(SalePrice, na.rm=T))
train_$electric[train_$Electrical == "SBrkr" | is.na(train$Electrical) ] <- 1
train_$electric[train_$Electrical != "SBrkr"] <- 0

# KitchenQual
train_$kitchen_qual[train_$KitchenQual == "Po"] <- 1
train_$kitchen_qual[train_$KitchenQual == "Fa"] <- 2
train_$kitchen_qual[train_$KitchenQual == "TA"] <- 3
train_$kitchen_qual[train_$KitchenQual == "Gd"] <- 4
train_$kitchen_qual[train_$KitchenQual == "Ex"] <- 5

# Functional
train_$functions[train_$Functional == "Typ"] <- 1
train_$functions[train_$Functional != "Typ"] <- 0

# FireplaceQu
train_$fireplace_qual[train_$FireplaceQu == "Po" | is.na(train_$FireplaceQu)] <- 1
train_$fireplace_qual[train_$FireplaceQu == "Fa"] <- 2
train_$fireplace_qual[train_$FireplaceQu == "TA"] <- 3
train_$fireplace_qual[train_$FireplaceQu == "Gd"] <- 4
train_$fireplace_qual[train_$FireplaceQu == "Ex"] <- 5

# GarageType
price <- summarize(group_by(train_, GarageType), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$GarageType, exclude = NULL)
train_$grgtype[train_$GarageType %in% c("CarPort") | is.na(train_$GarageType)] <- 1
train_$grgtype[train_$GarageType %in% c("Detchd")] <- 2
train_$grgtype[train_$GarageType %in% c("2Types", "Basment")] <- 3
train_$grgtype[train_$GarageType %in% c("Attchd")] <- 4
train_$grgtype[train_$GarageType %in% c("BuiltIn")] <- 5

# GarageFinish
price <- summarize(group_by(train_, GarageFinish), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$GarageFinish, exclude = NULL)
train_$grgfinish[is.na(train_$GarageFinish)] <- 1
train_$grgfinish[train_$GarageFinish %in% c("Unf")] <- 2
train_$grgfinish[train_$GarageFinish %in% c("RFn")] <- 3
train_$grgfinish[train_$GarageFinish %in% c("Fin")] <- 4


# GarageQual
train_$garage_qual[train_$GarageQual == "Po" | is.na(train_$GarageQual)] <- 1
train_$garage_qual[train_$GarageQual == "Fa"] <- 2
train_$garage_qual[train_$GarageQual == "TA"] <- 3
train_$garage_qual[train_$GarageQual == "Gd"] <- 4
train_$garage_qual[train_$GarageQual == "Ex"] <- 5

# GarageCond
train_$garage_cond[train_$GarageCond == "Po" | is.na(train_$GarageCond)] <- 1
train_$garage_cond[train_$GarageCond == "Fa"] <- 2
train_$garage_cond[train_$GarageCond == "TA"] <- 3
train_$garage_cond[train_$GarageCond == "Gd"] <- 4
train_$garage_cond[train_$GarageCond == "Ex"] <- 5

# PaveDrive
train_$paved_driveway[train_$PavedDrive == 'Y'] <- 1
train_$paved_driveway[train_$PavedDrive != 'Y'] <- 0

# SaleType
price <- summarize(group_by(train_, SaleType), mean(SalePrice, na.rm=T))
price
train_$sale_type[train_$SaleType %in% c("Oth")] <- 1
train_$sale_type[train_$SaleType %in% c("ConLD", "ConLW", "COD")] <- 2
train_$sale_type[train_$SaleType %in% c("WD")] <- 3
train_$sale_type[train_$SaleType %in% c("ConLI","CWD")] <- 4
train_$sale_type[train_$SaleType %in% c("Con", "New")] <- 5


# SaleCondition
price <- summarize(group_by(train_, SaleCondition), value=mean(SalePrice, na.rm=T))
price[order(price$value),]
table(train_$SaleCondition, exclude = NULL)
train_$sale_cond[train_$SaleCondition %in% c("AdjLand")] <- 1
train_$sale_cond[train_$SaleCondition %in% c("Abdnorml", "Family", "COD")] <- 2
train_$sale_cond[train_$SaleCondition %in% c("Alloca")] <- 3
train_$sale_cond[train_$SaleCondition %in% c("Normal")] <- 4
train_$sale_cond[train_$SaleCondition %in% c("partial")] <- 5

## Nulling char variable
train_$MSZoning <- NULL
train_$Street <- NULL
train_$LotShape <- NULL
train_$LandContour <- NULL
train_$Utilities <- NULL
train_$LotConfig <- NULL
train_$LandSlope <- NULL
train_$Neighborhood <- NULL
train_$Condition1 <- NULL
train_$Condition2 <- NULL
train_$BldgType <- NULL
train_$HouseStyle <- NULL
train_$RoofStyle <- NULL
train_$RoofMatl <- NULL
train_$Exterior1st <- NULL
train_$Exterior2nd <- NULL
train_$MasVnrType <- NULL
train_$ExterQual <- NULL
train_$ExterCond <- NULL
train_$Foundation <- NULL
train_$BsmtQual <- NULL
train_$BsmtCond <- NULL
train_$BsmtExposure <- NULL
train_$BsmtFinType1 <- NULL
train_$BsmtFinType2 <- NULL
train_$Heating <- NULL
train_$HeatingQC <- NULL
train_$CentralAir <- NULL
train_$Electrical <- NULL
train_$KitchenQual <- NULL
train_$Functional <- NULL
train_$FireplaceQu <- NULL
train_$GarageType <- NULL
train_$GarageFinish <- NULL
train_$GarageQual <- NULL
train_$GarageCond <- NULL
train_$PavedDrive <- NULL
train_$SaleType <- NULL
train_$SaleCondition <- NULL

#############################

#### Abstract Analysis ####

## Drawing correlation plot
library(corrplot)
correlations <- cor(train_[,c(3:37, 38)], use="everything")
corrplot(correlations, method='circle', type='lower', sig.level=0.01, insig='blank')

###########################


#### Create model ####
library(rpart)
fit <- rpart(SalePrice ~ GrLivArea + OverallQual + TotalBsmtSF + X1stFlrSF + FullBath + GarageCars + GarageArea,
             data = train_,
             method="anova")

fit2 <- rpart(SalePrice ~ .,
              data = train_,
              method = 'anova')

######################


#### Test model ####
SalePricePrediction <- predict(fit, test)
SalePricePrediction2 <- predict(fit2, test)


####################

#### Output Result ####

my_submission <- data.frame(Id = test$Id, SalePrice = SalePricePrediction)

write.csv(x = my_submission, file = "house/my_submission.csv", row.names = FALSE)

#######################


#### my submission ####
## Goal: top 1% of 2786 = 277


## first submission: 12 Dec 2017
# predict only using greater living area & overall qual
# score 0.23534 RMS of error. rank 2463/2786
