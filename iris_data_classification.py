# -*- coding: utf-8 -*-
"""iris data classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ne-wrutW2UmNdAuF39R_G6KdahxPvJF4

**TASK 3:IRIS DATA CLASSIFICATION**
*  AUTHOR -HIMANSHI GUPTA
*  BATCH-April
*  DOMAIN- Data Science
*  AIM-Buid a model that can classify Iris flower species

#importing library
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

"""#read the file"""

df = pd.read_csv('IRIS.csv')
df.head()

"""#some stastical information of data"""

df.describe()

"""#info of data"""

df.info()

"""#shape of data"""

df.shape

"""#counting total number of species"""

df['species'].value_counts()

"""#counting total number of null values"""

df.isnull().sum()

"""#histogram of sepal_length"""

df['sepal_length'].hist()

"""#histogram of sepal_width"""

df['sepal_width'].hist()

"""#histogram of petal_length"""

df['petal_length'].hist()

"""#histogram of petal_width"""

df['petal_width'].hist()

Colors = ['red', 'orange', 'blue']
Species = ['Iris-virginica','Iris-versicolor','Iris-setosa']

"""#creates a scatter plot with sepal length on the x-axis and sepal width on the y-axis"""

for i in range(3):
    x = df[df['species'] == Species[i]]
    plt.scatter(x['sepal_length'], x['sepal_width'], c = Colors[i], label=Species[i])
plt.xlabel("Sepal Length")
plt.ylabel("Sepal Width")
plt.legend()

"""#creates a scatter plot with petal length on the x-axis and petal width on y axis"""

for i in range(3):
    x = df[df['species'] == Species[i]]
    plt.scatter(x['petal_length'], x['petal_width'], c = Colors[i], label=Species[i])
plt.xlabel("petal length")
plt.ylabel("petal Width")
plt.legend()

"""#creates a scatter plot with sepal length on the x-axis and sepal width on the y-axis"""

for i in range(3):
    x = df[df['species'] == Species[i]]
    plt.scatter(x['petal_length'], x['sepal_width'], c = Colors[i], label=Species[i])
plt.xlabel("sepal length")
plt.ylabel("petal length")
plt.legend()

"""#scatter  plot between sepal width and petal width"""

for i in range(3):
    x = df[df['species'] == Species[i]]
    plt.scatter(x['sepal_length'], x['petal_width'], c = Colors[i], label=Species[i])
plt.xlabel("sepal width")
plt.ylabel("Petal width")
plt.legend()

"""#counting total number of species"""

valuecount = df['species'].value_counts().reset_index()

"""#printing the count of species

"""

valuecount

"""#creating a pie chart of different species woth their respective percentages"""

plt.figure(figsize=(8,8))
plt.pie(valuecount['count'],labels=['Iris-setosa','Iris-versicolor','Iris-virginica'],autopct='%1.3f%%',explode=[0,0,0])
plt.legend(loc='upper left')
plt.show()

"""#printing the data set again"""

df

"""#generates a scatter plot with a linear regression line fit to the data, showing the relationship between sepal length and sepal width"""

sns.lmplot(
    x="sepal_length",
    y="sepal_width",
    hue="species",
    palette="bright",
    data=df
)

plt.title("Sepal Length VS Sepal Width")
plt.show()

df

"""#generates a scatter plot with a linear regression line fit to the data, showing the relationship between petal length and petal width"""

sns.lmplot(
    x="petal_length",
    y="petal_width",
    hue="species",
    palette="bright",
    data=df
)

plt.title("Petal Length VS Petal Width")
plt.show()

""" #to encode the categorical variable "species" into numerical labels."""

label_encoder = LabelEncoder()
df['species'] = label_encoder.fit_transform(df['species'])

"""#droping the species column"""

X = df.drop(columns='species')
Y = df['species']

"""#printing x vlaues"""

X

"""#printing the y values"""

Y

"""#importing some remaining library"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

"""#splits the dataset into training and testing sets using the train_test_split function"""

X_train, x_test, Y_train, y_test = train_test_split(X,Y,test_size=0.2,random_state=43)

"""#printing x_train data"""

X_train

"""#printing x_test data"""

x_test

"""#printing Y_train data"""

Y_train

"""#printing y_test data"""

y_test

"""#creates a new DataFrame dfcorr by dropping the column 'species' from the original DataFrame"""

dfcorr = df.drop(columns = 'species', axis=1)

"""#printing the new data frame"""

dfcorr

"""#calculates the correlation matrix"""

dfcorr.corr()

"""#creates a heatmap to visualize the correlation matrix of the DataFrame"""

plt.figure(figsize=(10, 8))  # Set the size of the heatmap
sns.heatmap(dfcorr.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

"""#initializing a logistic regression mode"""

logmodel = LogisticRegression()

logmodel.fit(X_train,Y_train)

"""#printing the score"""

logmodel.score(x_test,y_test)

logmodel.score(X_train, Y_train)

logmodel.predict([[5.1,3.5,1.4,0.2]])

df.iloc[0]

"""#printing the species"""

predicted_label = logmodel.predict([[5.1, 3.5, 1.4, 0.2]])  # Make a prediction
predicted_class = label_encoder.inverse_transform(predicted_label)  # Convert numerical label to original class name
print(predicted_class)