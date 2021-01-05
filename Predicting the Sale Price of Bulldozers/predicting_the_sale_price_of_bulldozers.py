# -*- coding: utf-8 -*-
"""Predicting the Sale Price of Bulldozers

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dIAOVqLKGmf3aZK6D8iK5T5tQPqatWnI

# ***Predicting the Sale Price of Bulldozers using Machine Learning***

*In this notebook, we're going to go through an example machine learning project with the goal of predicting the sale price of bulldozers.*

# ***1. Problem defition***

> How well can we predict the future sale price of a bulldozer, given its characteristics and previous examples of how much similar bulldozers have been sold for?

# ***2. Data***
*The data is downloaded from the Kaggle Bluebook for Bulldozers competition: https://www.kaggle.com/c/bluebook-for-bulldozers/data*

*There are 3 main datasets:*

1.   Train.csv is the training set, which contains data through the end of 2011.
1.   Valid.csv is the validation set, which contains data from January 1, 2012 - April 30, 2012 You make predictions on this set throughout the majority of the competition. Your score on this set is used to create the public leaderboard.
3.   Test.csv is the test set, which won't be released until the last week of the competition. It contains data from May 1, 2012 - November 2012. Your score on the test set determines your final rank for the competition.

# ***3. Evaluation***

*The evaluation metric for this competition is the RMSLE (root mean squared log error) between the actual and predicted auction prices.*

*For more on the evaluation of this project check: https://www.kaggle.com/c/bluebook-for-bulldozers/overview/evaluation*

***Note:*** *The goal for most regression evaluation metrics is to minimize the error. For example, our goal for this project will be to build a machine learning model which minimises RMSLE.*

# ***4. Features***

*Kaggle provides a data dictionary detailing all of the features of the dataset. You can view this data dictionary on Google Sheets:* [Bulldozers Data Dictionary](https://docs.google.com/spreadsheets/d/1PfF_tXQuZcF2PBeOziys6Y5SvlG3bT7NEv90VanDHLY/edit?usp=sharing)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn

# Import training and validation sets
df = pd.read_csv("/content/TrainAndValid.csv",
                 low_memory=False)

df.info();

df.isna().sum()

fig, ax = plt.subplots()
ax.scatter(df["saledate"][:1000], df["SalePrice"][:1000]);

df.SalePrice.plot.hist();

"""## ***Parsing Dates***
*When we work with time series data, we want to enrich the time & date component as much as possible.*

*We can do that by telling pandas which of our columns has dates in it using the `parse_dates` parameter.*
"""

df = pd.read_csv("/content/TrainAndValid.csv", low_memory=False,parse_dates=["saledate"])

df.saledate[:1000]

fix, ax = plt.subplots()
ax.scatter(df["saledate"][:1000], df["SalePrice"][:1000]);

df.head()

df.head().T

df.saledate.head(20)

"""## ***Sort DataFrame by saledate***

*When working with time series data, it's a good idea to sort it by date.*

"""

#Sort DataFrame with date order
df.sort_values(by=["saledate"], inplace=True, ascending=True)
df.saledate.head(20)

df.head()

"""## ***Make a copy of the original DataFrame***

*We make a copy of the original dataframe so when we  manipulate the copy, we've still got out original data.*
"""

#Make a copy
df_tmp = df.copy()

"""## ***Add datatime parameters for `saledate` column***"""

df_tmp["saleYear"] = df_tmp.saledate.dt.year
df_tmp["saleMonth"] = df_tmp.saledate.dt.month
df_tmp["saleDay"] = df_tmp.saledate.dt.day
df_tmp["saleDayOfWeek"] = df_tmp.saledate.dt.dayofweek
df_tmp["saleDayOfYear"] = df_tmp.saledate.dt.dayofyear

df_tmp.head().T

#Now we've enriched our DataFrame with date time features, we can remove 'saledate'
df_tmp.drop("saledate", axis=1,inplace=True)

df_tmp.state.value_counts()

"""# ***5. Modelling***

*We've done enough EDA(We could always do more) but let's start to do some model driven-EDA*

## ***Convert string to categories***

*One way we can turn all of our data into numbers is by converting them into pandas categories.*

*We can check the different datatypes compatible with pandas here:* 

https://pandas.pydata.org/pandas-docs/stable/reference/general_utility_functions.html#data-types-related-functionality*
"""

df_tmp.head().T

pd.api.types.is_string_dtype(df_tmp["UsageBand"])

# Find the columns which contain string
for label, content in df_tmp.items():
  if pd.api.types.is_string_dtype(content):
    print(label)

# This will turn all of the string values into category values
for label, content in df_tmp.items():
  if pd.api.types.is_string_dtype(content):
    df_tmp[label] = content.astype("category").cat.as_ordered()

df_tmp.info()

df_tmp.state.cat.categories

df_tmp.state.cat.codes

"""*Thanks to Pandas Categories we now have a way to access all of our data in the form of numbers*

*But we still have a bunch of missing data...*

"""

#check missing data
df_tmp.isnull().sum()/len(df_tmp)

"""## ***Save preprocessed data***"""

# Export current tmp dataframe
df_tmp.to_csv("/content/train_tmp.csv",index=False)

# Import preprocessed data
df_tmp = pd.read_csv("/content/train_tmp.csv", low_memory=False)

df_tmp.head()

"""## ***Fill missing values***

###   ***Fill numerical missing values***
"""

for label, content in df_tmp.items():
  if pd.api.types.is_numeric_dtype(content):
    print(label)

# Check for which numeric columns have null values
for label, content in df_tmp.items():
  if pd.api.types.is_numeric_dtype(content):
    if pd.isnull(content).sum():
      print(label)

# Fill numeric rows with the median 
for label, content in df_tmp.items():
  if pd.api.types.is_numeric_dtype(content):
    if pd.isnull(content).sum():
      # Add a binary column which tells us if the data was missing or not
      df_tmp[label + "_is_missing"] = pd.isnull(content)
      # Fill missing numeric values with median
      df_tmp[label] = content.fillna(content.median())

# Check if there is any null numeric values
for labels, content in df_tmp.items():
  if pd.api.types.is_numeric_dtype(content):
    if pd.isnull(content).sum():
      print(label)

# Check to see how many examples were missing
df_tmp.auctioneerID_is_missing.value_counts()

df_tmp.isna().sum()

"""### ***Fill and turning categorical variables into numbers***"""

# Check for columns which aren't numeric
for label, content in df_tmp.items():
  if not pd.api.types.is_numeric_dtype(content):
    print(label)

# Turn categorical variables into numbers 
for label, content in df_tmp.items():
  if not pd.api.types.is_numeric_dtype(content):
    #Add a binary column to indicate whether sample had missing value
    df_tmp[label + "_is_missing"] = pd.isnull(content)
    #Turn categories into numbers and add +1
    df_tmp[label] = pd.Categorical(content).codes + 1

df_tmp.head()

df_tmp.isna().sum()

"""## ***Instantiate model***
Now that all of our data is numeric as well as our dataframe has no missing values, we should be able to build a machine learning model.

### ***Splitting data into train/validation sets***
"""

df_tmp.saleYear

# Split data into training/validation

df_val = df_tmp[df_tmp.saleYear == 2012]
df_train = df_tmp[df_tmp.saleYear !=2012]

len(df_val), len(df_train)

# Split data into X & y 
X_train, y_train = df_train.drop("SalePrice", axis=1), df_train.SalePrice
X_valid, y_valid = df_val.drop("SalePrice", axis=1), df_val.SalePrice

X_train.shape, y_train.shape, X_valid.shape, y_valid.shape

"""## **Building an evaluation function**"""

# Create evaluation function(The competition uses RMSLE)
from sklearn.metrics import mean_squared_log_error, mean_absolute_error, r2_score

def rmsle(y_test,y_preds):
  return np.sqrt(mean_squared_log_error(y_test,y_preds))

# Create function to evaluate model on a few different levels
def show_scores(model):
  train_preds = model.predict(X_train)
  val_preds = model.predict(X_valid)
  scores = {"Training MAE": mean_absolute_error(y_train,train_preds),
            "Valid MAE": mean_absolute_error(y_valid,val_preds),
            "Training RMSLE": rmsle(y_train, train_preds),
            "Valid RMSLE": rmsle(y_valid, val_preds),
            "Training R^2": r2_score(y_train, train_preds),
            "Valid R^2": r2_score(y_valid, val_preds)}
  return scores

"""## **Testing our model on a subset (To tune the hyperparameters)**


"""

len(X_train)

# Change max_samples value
model = RandomForestRegressor(n_jobs=-1,
                              random_state=42,
                              max_samples=10000)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # Cutting down on the max number of samples each estimator can see imporves training time
# model.fit(X_train,y_train)

show_scores(model)

"""## **Hyperparameter tuning with RandomizedSearchCV**


"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# from sklearn.model_selection import RandomizedSearchCV
# 
# # Different RandomForestRegressor hyperparameters
# rf_grid = {"n_estimators": np.arange(10,100,10),
#            "max_depth": [None, 3,5,10],
#            "min_samples_split": np.arange(2,20,2),
#            "min_samples_leaf": np.arange(1,20,2),
#            "max_features": [0.5,1,"sqrt","auto"],
#            "max_samples": [10000]}
# 
# # Instantiate RandomizedSearchCV model
# rs_model = RandomizedSearchCV(RandomForestRegressor(n_jobs=-1, random_state=42),
#                               param_distributions=rf_grid,
#                               n_iter=2,
#                               cv=5,
#                               verbose=True)
# 
# # Fit the RandomizedSearchCV model
# rs_model.fit(X_train,y_train)

# Find the best model hyperparameters
rs_model.best_params_

# Evaluate the RandomizedSearchCV model
show_scores(rs_model)

"""## **Train a model with the best hyperparameters**

***Note:*** These were found after 100 iterations of `RandomizedSearchCV`
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # Most ideal hyperparameters
# 
# ideal_model = RandomForestRegressor(n_estimators=40,
#                                     min_samples_leaf=1,
#                                     min_samples_split=14,
#                                     max_features=0.5,
#                                     n_jobs=-1,
#                                     max_samples=None,
#                                     random_state=42)
# 
# # Fit the ideal model
# ideal_model.fit(X_train,y_train)

# Scores for ideal_model (Trained on all the data)
show_scores(ideal_model)

# Scores on rs_model (Only trained on ~10,000 examples)
show_scores(rs_model)

"""## ***Make predictions on test data***

"""

# Import the test set
df_test = pd.read_csv("/content/Test.csv",
                      low_memory=False,
                      parse_dates=["saledate"])
df_test.head()

"""### **Preprocessing the data (Getting the test dataset in the same format as our training dateset)**"""

def preprocess_data(df):
  df["saleYear"] = df.saledate.dt.year
  df["saleMonth"] = df.saledate.dt.month
  df["saleDay"] = df.saledate.dt.day
  df["saleDayOfWeek"] = df.saledate.dt.dayofweek
  df["saleDayOfYear"] = df.saledate.dt.dayofyear
  df.drop("saledate", axis=1,inplace=True)

  # Fill the numeric rows with median
  for label, content in df.items():
    if pd.api.types.is_numeric_dtype(content):
      if pd.isnull(content).sum():
        # Add a binary column which tells us if the data was missing or not
        df[label + "_is_missing"] = pd.isnull(content)
        # Fill missing numeric values with median
        df[label] = content.fillna(content.median())

      # Filled categorical missing data turn categories into numbers
    if not pd.api.types.is_numeric_dtype(content):
      #Add a binary column to indicate whether sample had missing value
      df[label + "_is_missing"] = pd.isnull(content)
      #Turn categories into numbers and add +1
      df[label] = pd.Categorical(content).codes + 1

  return df

#Process the test data
df_test = preprocess_data(df_test)
df_test.head()

X_train.head()

# We can find how the columns differ using sets
set(X_train.columns) - set(df_test.columns)

# Manually adjust df_test to have auctioneerID_is_missing column
df_test["auctioneerID_is_missing"] = False
df_test.head()

"""*Finally now our test dataframe has the same features as our training dataframe, we can make predictions!*"""

test_preds = ideal_model.predict(df_test)

test_preds

"""*We've made some predictions but they're not in the same format Kaggle is asking for:*

https://www.kaggle.com/c/bluebook-for-bulldozers/overview/evaluation
"""

# Format predictions into the same format Kaggle is after
df_preds = pd.DataFrame()
df_preds["SalesID"] = df_test["SalesID"]
df_preds["SalePrice"] = test_preds
df_preds

# Export prediction data
df_preds.to_csv("/content/test_predictions.csv", index=False)

"""## ***Features Importance***

*Feature importance seeks to figure out which different attributes of the data were most importance when it comes to predicting the **target variable**(SalePrice).*
"""

# Find features importance of our best model
ideal_model.feature_importances_

X_train

# Helper function for plotting feature importance 
def plot_features(columns, importances, n=20):
  df = (pd.DataFrame({"features": columns,
                      "feature_importances": importances})
        .sort_values("feature_importances", ascending=False)
        .reset_index(drop=True))
  
  # Plot the dataframe
  fig, ax = plt.subplots()
  ax.barh(df["features"][:n], df["feature_importances"][:n])
  ax.set_ylabel("Features")
  ax.set_xlabel("Feature Importance")
  ax.invert_yaxis()

plot_features(X_train.columns, ideal_model.feature_importances_)

df["ProductSize"].value_counts()

df["Enclosure"].value_counts()