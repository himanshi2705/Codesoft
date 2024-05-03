# -*- coding: utf-8 -*-
"""movie rating prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Urk-OHwGq1zkd0uukbjklRE_YI6Hu3uk

**Task 2:-MOVIE RATING PREDDICTIO**N


*   Author -Himanshi Gupta
*   Batch-April
*   Domian-Data Science
*   Aim-Buid a model that predict the rating of a movie based on the features like genre,director,rating,and many more....

#i am using kaggle Api for downloading the datasets for fast execution of the program uploading the download data set take lots of time . for that i am using the kaggle API

#installing the kaggle
"""

!pip install -q kaggle

"""# make the directory to upload the dataset"""

!mkdir ~/.kaggle

"""#uploading the file from downloaded files"""

from google.colab import files
import os

# Uploading  the kaggle (1).json file
uploaded = files.upload()

# Geting  the name of the uploaded file
filename = next(iter(uploaded))

# Moving  the uploaded file to ~/.kaggle directory
os.makedirs('/root/.kaggle', exist_ok=True)
os.rename(filename, '/root/.kaggle/kaggle.json')

# providing the  appropriate permissions
os.chmod('/root/.kaggle/kaggle.json', 0o600)

"""#listing the kaggle datasets"""

!kaggle datasets list

!kaggle datasets download -d adrianmcmahon/imdb-india-movies

!unzip imdb-india-movies.zip

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

"""#this dataset involve character encoding or this files contain  bytes so to resolve this issue i am using "latin1" encoding that can read this csv file

"""

df = pd.read_csv("/content/IMDb Movies India.csv",encoding='latin1')

df.head()

"""#general detail about dataset"""

df.describe()

df.info()

missing_values=df.isnull().sum()

"""total nummber of missing value in each row"""

print(missing_values[missing_values > 0])

"""## Removes rows with missing values from the DataFrame


"""

df.dropna(inplace=True)
df.head()

"""#Calculates the sum of NaN values for each columns


"""

df.isnull().sum()

df.shape

# Extract numeric part of the string
df['Year'] = df['Year'].str.extract('(\d+)')
# Convert to numeric
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

df['Duration'] = df['Duration'].str.extract('(\d+)')
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')

df["Year"].head()

genre=df['Genre']
genre.head(5)

"""#Spliting the 'Genre' column in the DataFrame df into multiple columns based on the delimiter ','"""

genres=df['Genre'].str.split(',', expand=True)
genres.head(5)

"""Computing the count of each genre present in the genres"""

genre_counts = {}
for genre in genres.values.flatten():
    if genre is not None:
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

genereCounts = {genre: count for genre, count in sorted(genre_counts.items())}
for genre, count in genereCounts.items():
    print(f"{genre}: {count}")

"""Computes the count of each unique value in the 'Genre' column"""

genrespie=df['Genre'].value_counts()
genrespie.head()

genrePie = pd.DataFrame(list(genrespie.items()))
genrePie = genrePie.rename(columns={0: 'Genre', 1: 'Count'})
genrePie.head(5)

# Convert the 'Votes' column to string type
df['Votes'] = df['Votes'].astype(str)

# Replace commas with empty strings
df['Votes'] = df['Votes'].str.replace(',', '')

# Convert the 'Votes' column to float type and round the values
df['Votes'] = df['Votes'].astype(float).round()

# Convert the rounded values to integer type
df['Votes'] = df['Votes'].astype(int)

# Print the first five rows of the 'Votes' column
print(df['Votes'].head(5))

"""Returns the number of unique directors present in the 'Director' column"""

df['Director'].nunique()

"""Calculates the count of occurrences for each unique director in the 'Director' column"""

directors=df['Director'].value_counts()
directors.head()

"""Concatenates three columns ('Actor 1', 'Actor 2', and 'Actor 3') from the DataFrame df, then drops any missing values (NaNs), and finally calculates the count of occurrences for each unique actor"""

actors = pd.concat([df['Actor 1'], df['Actor 2'], df['Actor 3']]).dropna().value_counts()
actors.head(5)

"""Importing the library"""

import plotly.express as px
from wordcloud import WordCloud

# Convert the 'Year' column to float type
df['Year'] = df['Year'].astype(float)

# Replace any non-numeric values with NaN
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Convert the 'Year' column to integer type, while handling NaN values
df['Year'] = df['Year'].fillna(0).astype(int)

# Print the first five rows of the 'Year' column
print(df['Year'].head(5))

# Set font family to a known font
plt.rcParams['font.family'] = 'sans-serif'
# Plotting
ax = sns.lineplot(data=df['Year'].value_counts().sort_index())
tick_positions = range(min(df['Year']), max(df['Year']) + 1, 5)
ax.set_title("Annual Movie Release Counts Over Time")
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_positions, rotation=90)
ax.set_xlabel("Years")
ax.set_ylabel("Count")
plt.show()

"""Creates a box plot of the 'Year' column"""

ax=sns.boxplot(data=df, y='Year')
ax.set_ylabel('Year')
ax.set_title("Box plot of year")
plt.show()

"""Creating a line plot showing the average movie duration trends over the years"""

ax=sns.lineplot(data=df.groupby('Year')['Duration'].mean().reset_index(), x='Year',y ='Duration')
tick_positions=range(min(df['Year']),max(df['Year']) +1,5)
ax.set_title("Average  Movie Duration Trends over the Years")
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_positions,rotation =90)
ax.set_xlabel("Years")
ax.set_ylabel('Average Duration (in minutes)')
plt.show()

"""Generates a box plot showing the distribution of average movie durations in minute"""

ax= sns.boxplot(data=df ,y='Duration')
ax.set_title(" Boxplot of Average Movie duration")
ax.set_ylabel("Average Duration (in minutes)")
plt.show()

"""#Performs outlier removal based on the IQR method for the 'Duration' column"""

Q1 = df['Duration'].quantile(0.25)
Q3 = df['Duration'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['Duration'] >= lower_bound) & (df['Duration'] <= upper_bound)]
df.head(5)

"""#Creates a visual representation of the genre distribution in the 'Genre' column"""

genre_counts = df['Genre'].str.split(', ', expand=True).stack().value_counts()

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(genre_counts)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Genre Word Cloud')
plt.show()

""" #Generates a bar plot showing the frequency of each genre in the dataset"""

genreLabels =  sorted(genereCounts.keys())
genreCounts = sorted(genereCounts.values())
ax=sns.barplot(x=genreLabels,y=genreCounts)
ax.set_xticklabels(labels=genreLabels,rotation =90)
plt.show()

"""#Generates a pie chart showing the distribution of movie genres"""

genrePie.loc[genrePie['Count']<50, 'Genre']='other'
ax= px.pie(genrePie,values ='Count',names ='Genre',title ='More than on genre of movies in indian Cinemas')
ax.show()

"""#Generates a histogram showing the distribution of movie ratings"""

ax=sns.histplot(data=df ,x="Rating",bins =20,kde =True)
ax.set_xlabel('Rating')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Movie Rating')
plt.show()

"""
#Generates a box plot showing the distribution of movie ratings"""

ax=sns.boxplot(data=df,y="Rating")
ax.set_ylabel('Rating')
ax.set_title("Box plot of movie rating")
plt.show()

Q1 = df['Rating'].quantile(0.25)
Q3 = df['Rating'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['Rating'] >= lower_bound) & (df['Rating'] <= upper_bound)]
df.head(5)

"""#Clean the dataset by removing outliers from the 'Rating' column based on the IQR method"""

rating_votes = df.groupby('Rating')['Votes'].sum().reset_index()
plt.figure(figsize=(10, 6))
ax_line_seaborn = sns.lineplot(data=rating_votes, x='Rating', y='Votes', marker='o')
ax_line_seaborn.set_xlabel('Rating')
ax_line_seaborn.set_ylabel('Total Votes')
ax_line_seaborn.set_title('Total Votes per Rating')
plt.show()

"""#Generates a bar plot showing the top 20 directors by the frequency of movies"""

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=directors.head(20).index, y=directors.head(20).values, hue=directors.head(20).index, palette='viridis', legend=False)
ax.set_xlabel('Directors')
ax.set_ylabel('Frequency of Movies')
ax.set_title('Top 20 Directors by Frequency of Movies')

# Set the tick positions and labels
ax.set_xticks(range(len(directors.head(20).index)))
ax.set_xticklabels(directors.head(20).index, rotation=90)

plt.show()

"""#Creates a bar plot to visualize the top 20 actors"""

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=actors.head(20).index, y=actors.head(20).values, hue=actors.head(20).index, palette='viridis', legend=False)
ax.set_xlabel('Actors')
ax.set_ylabel('Total Number of Movies')
ax.set_title('Top 20 Actors with Total Number of Movies')

# Set the tick positions and labels
ax.set_xticks(range(len(actors.head(20).index)))
ax.set_xticklabels(actors.head(20).index, rotation=90)

plt.show()

"""#Concatenates actor names, encodes director, genre, and actor columns as numerical codes"""

df["Actor"] = df['Actor 1'] + ', ' + df['Actor 2'] + ', ' + df['Actor 3']
df["Directors"] = df['Director'].astype('category').cat.codes
df["Genres"] = df['Genre'].astype('category').cat.codes
df["Actors"] = df['Actor'].astype('category').cat.codes
df.head(5)

"""#Create a count plot showing the distribution of genres along the y-axis."""

ax=sns.boxplot(data=df ,y='Genres')
ax.set_ylabel('Genres')
ax.set_title("Box plot of Geners")
plt.show()

"""#Calculates the lower and upper bounds using the IQR method and then filters the DataFrame"""

Q1=df['Genres'].quantile(0.25)
Q3 =df['Genres'].quantile(0.75)
IQR =Q3-Q1
lower_bound= Q1-1.5 *IQR
upper_bound=Q3+1.5*IQR
df =df[(df['Genres']>= lower_bound) & (df['Genres']<= upper_bound)]
df.head(5)

"""#Creates a horizontal bar plot where each bar represents the number of movies directed by a particular director."""

ax = sns.boxplot(data=df, y='Directors')
ax.set_ylabel('Directors')
ax.set_title('Box Plot of Directors')
plt.show()

"""#Helps to remove potential outliers from the "Directors" column"""

Q1 = df['Directors'].quantile(0.25)
Q3 = df['Directors'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['Directors'] >= lower_bound) & (df['Directors'] <= upper_bound)]
df.head(5)

"""#Generates a box plot for the "Actors" column in the DataFrame"""

ax = sns.boxplot(data=df, y='Actors')
ax.set_ylabel('Actors')
ax.set_title('Box Plot of Actors')
plt.show()

"""# Calculates the lower and upper bounds for outliers in the "Actors" column of the DataFrame"""

Q1 = df['Actors'].quantile(0.25)
Q3 = df['Actors'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['Actors'] >= lower_bound) & (df['Actors'] <= upper_bound)]
df.head(5)

"""#preparing the input and output data for a machine learning model"""

Input = df.drop(['Name', 'Genre', 'Rating', 'Director', 'Actor 1', 'Actor 2', 'Actor 3', 'Actor'], axis=1)
Output = df['Rating']
Input.head(5)

"""Aop five output valuetA

"""

Output.head(5)

"""#Splitting the input and output data into training and testing sets for machine learning model training and evaluation"""

x_train, x_test, y_train, y_test = train_test_split(Input, Output, test_size = 0.2, random_state = 1)

!pip install catboost

"""#importing some remaing libraries"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score as score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from catboost import CatBoostRegressor

"""#Performs outlier detection and removal for the 'Genres' column"""

Q1 = df['Genres'].quantile(0.25)
Q3 = df['Genres'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['Genres'] >= lower_bound) & (df['Genres'] <= upper_bound)]
df.head(5)

"""#Provides a concise summary of the model's performance metrics, including accuracy and mean squared error"""

def evaluate_model(y_true, y_pred, model_name):
    print("Model: ", model_name)
    print("Accuracy = {:0.2f}%".format(score(y_true, y_pred)*100))
    print("Mean Squared Error = {:0.2f}\n".format(mean_squared_error(y_true, y_pred, squared=False)))
    return round(score(y_true, y_pred)*100, 2)

# Instantiate and fit the models
LR = LinearRegression()
LR.fit(x_train, y_train)
lr_preds = LR.predict(x_test)

RFR = RandomForestRegressor(n_estimators=100, random_state=1)
RFR.fit(x_train, y_train)
rf_preds = RFR.predict(x_test)

DTR = DecisionTreeRegressor(random_state=1)
DTR.fit(x_train, y_train)
dt_preds = DTR.predict(x_test)

XGBR = XGBRegressor(n_estimators=100, random_state=1)
XGBR.fit(x_train, y_train)
xgb_preds = XGBR.predict(x_test)

GBR = GradientBoostingRegressor(n_estimators=100, random_state=60)
GBR.fit(x_train, y_train)
gb_preds = GBR.predict(x_test)

LGBMR = LGBMRegressor(n_estimators=100, random_state=60)
LGBMR.fit(x_train, y_train)
lgbm_preds = LGBMR.predict(x_test)

CBR = CatBoostRegressor(n_estimators=100, random_state=1, verbose=False)
CBR.fit(x_train, y_train)
catboost_preds = CBR.predict(x_test)

KNR = KNeighborsRegressor(n_neighbors=5)
KNR.fit(x_train, y_train)
knn_preds = KNR.predict(x_test)

"""#Provides a comprehensive evaluation of multiple machine learning models and their respective accuracy scores"""

LRScore = evaluate_model(y_test, lr_preds, "LINEAR REGRESSION")
RFScore = evaluate_model(y_test, rf_preds, "RANDOM FOREST")
DTScore = evaluate_model(y_test, dt_preds, "DECEISION TREE")
XGBScore = evaluate_model(y_test, xgb_preds, "EXTENDED GRADIENT BOOSTING")
GBScore = evaluate_model(y_test, gb_preds, "GRADIENT BOOSTING")
LGBScore = evaluate_model(y_test, lgbm_preds, "LIGHT GRADIENT BOOSTING")
CBRScore = evaluate_model(y_test, catboost_preds, "CAT BOOST")
KNNScore = evaluate_model(y_test, knn_preds, "K NEAREST NEIGHBORS")

models = pd.DataFrame(
    {
        "MODELS": ["Linear Regression", "Random Forest", "Decision Tree", "Gradient Boosting", "Extended Gradient Boosting", "Light Gradient Boosting", "Cat Boosting", "K Nearest Neighbors"],
        "SCORES": [LRScore, RFScore, DTScore, GBScore, XGBScore, LGBScore, CBRScore, KNNScore]
    }
)
models.sort_values(by='SCORES', ascending=False)